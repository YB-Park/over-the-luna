from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def events(path: Path) -> list[dict]:
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            out.append(value)
    return out


def requests(event: dict) -> list[dict]:
    return [x for x in ((event.get("data") or {}).get("toolRequests") or []) if isinstance(x, dict)]


def route(rows: list[dict]) -> tuple[str | None, str | None]:
    pattern = re.compile(r"Mode:\s*(SIMPLE|STANDARD|DEEP).*?Assurance:\s*(NONE|REVIEW|RISK)", re.S)
    for row in rows:
        if row.get("type") != "assistant.message" or row.get("agentId"):
            continue
        match = pattern.search(str((row.get("data") or {}).get("content") or ""))
        if match:
            return match.group(1), match.group(2)
    return None, None


def patch_supplied(prompt: str) -> bool:
    low = prompt.lower()
    return "@@" in prompt and ("diff --git" in prompt or "changed files" in low or "current diff" in low or "patch" in low)


def sealed_paths(content: str) -> set[str]:
    if "Boundary sealed" not in content:
        return set()
    # Main reports paths in backticks in the canonical transition.
    values = set(re.findall(r"`([^`]+\.[A-Za-z0-9_]+)`", content))
    return {value.lstrip("./") for value in values}


def normalize(path: str) -> str:
    marker = "/fixture/"
    if marker in path:
        return path.split(marker, 1)[1].lstrip("./")
    return path.lstrip("./")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--case", choices=("tiny", "local", "broad", "risk"), required=True)
    p.add_argument("--events", type=Path, required=True)
    p.add_argument("--ownership", type=Path, required=True)
    a = p.parse_args()

    rows = events(a.events)
    ownership = json.loads(a.ownership.read_text(encoding="utf-8"))
    failures: list[str] = []
    mode, assurance = route(rows)

    expected_mode, expected_assurance = {
        "tiny": ("SIMPLE", "NONE"),
        "local": ("SIMPLE", "REVIEW"),
        "broad": ("STANDARD", "REVIEW"),
        "risk": (None, "RISK"),
    }[a.case]
    if expected_mode and mode != expected_mode:
        failures.append(f"route mode expected {expected_mode}, got {mode}")
    if assurance != expected_assurance:
        failures.append(f"assurance expected {expected_assurance}, got {assurance}")

    names = [str((r.get("data") or {}).get("agentName") or "") for r in rows if r.get("type") == "subagent.started"]
    reviewer_count = sum(n.endswith("luna-reviewer") for n in names)
    architect_count = sum(n.endswith("luna-architect") for n in names)
    premium_count = sum("sonnet" in n.lower() or "opus" in n.lower() for n in names)

    expected_reviewers = {"tiny": 0, "local": 1, "broad": 1}.get(a.case)
    if expected_reviewers is not None and reviewer_count != expected_reviewers:
        failures.append(f"Reviewer count expected {expected_reviewers}, got {reviewer_count}")
    if a.case == "risk" and not (1 <= reviewer_count <= 2):
        failures.append(f"RISK Reviewer count expected 1..2, got {reviewer_count}")
    expected_architect = {"tiny": 0, "local": 0, "broad": 1}.get(a.case)
    if expected_architect is not None and architect_count != expected_architect:
        failures.append(f"Architect count expected {expected_architect}, got {architect_count}")
    if premium_count:
        failures.append(f"automatic premium count must be 0, got {premium_count}")

    by_agent = ownership.get("by_agent") or {}
    for agent, tools in by_agent.items():
        if agent.endswith("luna-reviewer"):
            read_calls = sum(int(tools.get(k, 0)) for k in ("view", "rg", "glob", "read", "search"))
            if read_calls > 8:
                failures.append(f"Reviewer read/search budget exceeded: {read_calls}")
        if agent != "over-the-luna:over-the-luna":
            for mutation in ("apply_patch", "edit", "create", "delete"):
                if int(tools.get(mutation, 0)):
                    failures.append(f"leaf {agent} mutated via {mutation}")

    architect_done: int | None = None
    seal_index: int | None = None
    work_set: set[str] = set()
    first_mutation: int | None = None

    for idx, row in enumerate(rows):
        if row.get("type") == "subagent.completed" and str((row.get("data") or {}).get("agentName") or "").endswith("luna-architect"):
            architect_done = idx
        if row.get("type") != "assistant.message" or row.get("agentId"):
            continue
        content = str((row.get("data") or {}).get("content") or "")
        paths = sealed_paths(content)
        if paths and seal_index is None:
            seal_index = idx
            work_set = paths
        for req in requests(row):
            name = str(req.get("name") or "")
            vals = req.get("arguments") or {}
            if name == "apply_patch" and first_mutation is None:
                first_mutation = idx
            if name == "task" and str(vals.get("agent_type") or "").endswith("luna-reviewer"):
                prompt = str(vals.get("prompt") or "")
                if not patch_supplied(prompt):
                    failures.append("Reviewer prompt missing concrete diff/hunk artifact")

    # VCS internals are never legitimate evidence for these read-only leaf tasks.
    for row in rows:
        if row.get("type") != "assistant.message" or not row.get("agentId"):
            continue
        for req in requests(row):
            if req.get("name") == "view":
                path = str((req.get("arguments") or {}).get("path") or "")
                if "/.git" in path or path.endswith("/.git"):
                    failures.append(f"leaf attempted VCS metadata inspection: {path}")

    if a.case == "broad":
        if architect_done is None:
            failures.append("broad case has no Architect")
        if seal_index is None:
            failures.append("Main did not emit Boundary sealed work set")
        if not work_set:
            failures.append("sealed work set had no concrete paths")
        if architect_done is not None and seal_index is not None and seal_index < architect_done:
            failures.append("Boundary sealed appeared before Architect completed")

        broad_shell = re.compile(r"(^|[;&|]\s*)(find\s+\.|ls\s+-R|tree(?:\s|$)|git\s+(?:grep|ls-files)|grep\s+-R|rg(?:\s|$))")
        first_repo_action = True
        start = architect_done + 1 if architect_done is not None else 0
        stop = first_mutation if first_mutation is not None else len(rows)
        for idx, row in enumerate(rows[start:stop], start=start):
            if row.get("type") != "assistant.message" or row.get("agentId"):
                continue
            for req in requests(row):
                name = str(req.get("name") or "")
                vals = req.get("arguments") or {}
                if name in {"task", "list_agents", "read_agent"}:
                    continue
                if first_repo_action:
                    first_repo_action = False
                    if name != "view" or normalize(str(vals.get("path") or "")) not in work_set:
                        failures.append(f"first repository action after Architect must read sealed work-set file, got {name}")
                if name in {"rg", "glob"}:
                    failures.append(f"Main replayed discovery after Architect via {name}")
                elif name == "view":
                    path = normalize(str(vals.get("path") or ""))
                    if path not in work_set:
                        failures.append(f"Main read outside sealed work set before mutation: {path}")
                elif name == "bash":
                    command = str(vals.get("command") or "")
                    if broad_shell.search(command):
                        failures.append(f"Main used shell discovery after Architect: {command[:180]}")

    print("POLICY_GATE:", "PASS" if not failures else "FAIL")
    print(f"- route={mode}+{assurance}")
    print(f"- architect={architect_count}")
    print(f"- reviewer={reviewer_count}")
    print(f"- premium={premium_count}")
    if work_set:
        print(f"- work_set={sorted(work_set)}")
    for failure in failures:
        print("FAIL:", failure)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
