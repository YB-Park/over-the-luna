from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_events(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def tool_requests(event: dict) -> list[dict]:
    return [value for value in ((event.get("data") or {}).get("toolRequests") or []) if isinstance(value, dict)]


def parse_route(rows: list[dict]) -> tuple[str | None, str | None]:
    pattern = re.compile(r"Mode:\s*(SIMPLE|STANDARD|DEEP).*?Assurance:\s*(NONE|REVIEW|RISK)", re.S)
    for row in rows:
        if row.get("type") != "assistant.message" or row.get("agentId"):
            continue
        match = pattern.search(str((row.get("data") or {}).get("content") or ""))
        if match:
            return match.group(1), match.group(2)
    return None, None


def sealed_paths(content: str) -> set[str]:
    match = re.search(r"Boundary sealed\s*[—-]\s*work set:\s*([^\n]+)", content, re.I)
    if not match:
        return set()
    body = match.group(1).strip().strip("*_")
    backticked = re.findall(r"`([^`]+)`", body)
    raw = backticked if backticked else body.split(",")
    paths: set[str] = set()
    for item in raw:
        value = item.strip().strip("`*_ ").lstrip("./")
        if value and Path(value).suffix:
            paths.add(value)
    return paths


def normalize(path: str) -> str:
    marker = "/fixture/"
    if marker in path:
        return path.split(marker, 1)[1].lstrip("./")
    return path.lstrip("./")


def verbatim_patch(prompt: str) -> bool:
    return all(
        token in prompt
        for token in (
            "BEGIN_UNIFIED_DIFF",
            "END_UNIFIED_DIFF",
            "diff --git",
            "@@",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("tiny", "local", "broad", "risk"), required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--ownership", type=Path, required=True)
    args = parser.parse_args()

    rows = load_events(args.events)
    ownership = json.loads(args.ownership.read_text(encoding="utf-8"))
    failures: list[str] = []
    mode, assurance = parse_route(rows)

    expected_mode, expected_assurance = {
        "tiny": ("SIMPLE", "NONE"),
        "local": ("SIMPLE", "REVIEW"),
        "broad": ("STANDARD", "REVIEW"),
        "risk": (None, "RISK"),
    }[args.case]
    if expected_mode is not None and mode != expected_mode:
        failures.append(f"route mode expected {expected_mode}, got {mode}")
    if assurance != expected_assurance:
        failures.append(f"assurance expected {expected_assurance}, got {assurance}")

    subagents = [
        str((row.get("data") or {}).get("agentName") or "")
        for row in rows
        if row.get("type") == "subagent.started"
    ]
    architect_count = sum(name.endswith("luna-architect") for name in subagents)
    reviewer_count = sum(name.endswith("luna-reviewer") for name in subagents)
    premium_count = sum("sonnet" in name.lower() or "opus" in name.lower() for name in subagents)

    expected_architect = {"tiny": 0, "local": 0, "broad": 1}.get(args.case)
    if expected_architect is not None and architect_count != expected_architect:
        failures.append(f"Architect count expected {expected_architect}, got {architect_count}")
    expected_reviewer = {"tiny": 0, "local": 1, "broad": 1}.get(args.case)
    if expected_reviewer is not None and reviewer_count != expected_reviewer:
        failures.append(f"Reviewer count expected {expected_reviewer}, got {reviewer_count}")
    if args.case == "risk" and not (1 <= reviewer_count <= 2):
        failures.append(f"RISK Reviewer count expected 1..2, got {reviewer_count}")
    if premium_count:
        failures.append(f"automatic premium count must be 0, got {premium_count}")

    by_agent = ownership.get("by_agent") or {}
    for agent, tools in by_agent.items():
        if agent.endswith("luna-reviewer"):
            reads = sum(int(tools.get(name, 0)) for name in ("view", "rg", "glob", "read", "search"))
            if reads > 8:
                failures.append(f"Reviewer read/search budget exceeded: {reads}")
        if agent != "over-the-luna:over-the-luna":
            for mutation_tool in ("apply_patch", "edit", "create", "delete"):
                if int(tools.get(mutation_tool, 0)):
                    failures.append(f"leaf {agent} mutated via {mutation_tool}")

    architect_done: int | None = None
    first_mutation: int | None = None
    seal_index: int | None = None
    work_set: set[str] = set()
    reviewer_prompts: list[str] = []

    for index, row in enumerate(rows):
        if row.get("type") == "subagent.completed" and str((row.get("data") or {}).get("agentName") or "").endswith("luna-architect"):
            architect_done = index
        if row.get("type") != "assistant.message" or row.get("agentId"):
            continue
        content = str((row.get("data") or {}).get("content") or "")
        paths = sealed_paths(content)
        if paths and seal_index is None:
            seal_index = index
            work_set = paths
        for request in tool_requests(row):
            name = str(request.get("name") or "")
            values = request.get("arguments") or {}
            if name == "apply_patch" and first_mutation is None:
                first_mutation = index
            if name == "task" and str(values.get("agent_type") or "").endswith("luna-reviewer"):
                reviewer_prompts.append(str(values.get("prompt") or ""))

    for prompt in reviewer_prompts:
        if not verbatim_patch(prompt):
            failures.append("Reviewer prompt missing verbatim marked unified diff")

    for row in rows:
        if row.get("type") != "assistant.message" or not row.get("agentId"):
            continue
        for request in tool_requests(row):
            if request.get("name") == "view":
                path = str((request.get("arguments") or {}).get("path") or "")
                if "/.git" in path or path.endswith("/.git"):
                    failures.append(f"leaf attempted VCS metadata inspection: {path}")

    broad_shell = re.compile(
        r"(^|[;&|]\s*)(find\s+\.|ls\s+-R|tree(?:\s|$)|git\s+(?:grep|ls-files)|grep\s+-R|rg(?:\s|$))"
    )

    if args.case in {"tiny", "local"}:
        stop = first_mutation if first_mutation is not None else len(rows)
        locator_count = 0
        concrete_reads: set[str] = set()
        for row in rows[:stop]:
            if row.get("type") != "assistant.message" or row.get("agentId"):
                continue
            for request in tool_requests(row):
                name = str(request.get("name") or "")
                values = request.get("arguments") or {}
                if name in {"rg", "glob"}:
                    locator_count += 1
                elif name == "view":
                    path = normalize(str(values.get("path") or ""))
                    if not Path(path).suffix:
                        failures.append(f"local orientation viewed directory: {path}")
                    else:
                        concrete_reads.add(path)
                elif name == "bash" and broad_shell.search(str(values.get("command") or "")):
                    failures.append(f"local orientation used broad shell discovery: {values.get('command')}")
        if locator_count > 2:
            failures.append(f"bounded locator budget exceeded: {locator_count} > 2")
        if len(concrete_reads) > 3:
            failures.append(f"bounded local read set exceeded: {len(concrete_reads)} > 3 ({sorted(concrete_reads)})")

    if args.case == "broad":
        if architect_done is None:
            failures.append("broad case has no Architect")
        if seal_index is None or not work_set:
            failures.append("Main did not emit a concrete Boundary sealed work set")
        if architect_done is not None and seal_index is not None and seal_index < architect_done:
            failures.append("Boundary sealed appeared before Architect completed")

        start = architect_done + 1 if architect_done is not None else 0
        stop = first_mutation if first_mutation is not None else len(rows)
        first_repo_action = True
        for row in rows[start:stop]:
            if row.get("type") != "assistant.message" or row.get("agentId"):
                continue
            for request in tool_requests(row):
                name = str(request.get("name") or "")
                values = request.get("arguments") or {}
                if name in {"task", "list_agents", "read_agent"}:
                    continue
                if first_repo_action:
                    first_repo_action = False
                    if name != "view" or normalize(str(values.get("path") or "")) not in work_set:
                        failures.append(f"first repository action after Architect must read sealed work-set file, got {name}")
                if name in {"rg", "glob"}:
                    failures.append(f"Main replayed discovery after Architect via {name}")
                elif name == "view":
                    path = normalize(str(values.get("path") or ""))
                    if path not in work_set:
                        failures.append(f"Main read outside sealed work set before mutation: {path}")
                elif name == "bash" and broad_shell.search(str(values.get("command") or "")):
                    failures.append(f"Main used shell discovery after Architect: {values.get('command')}")

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
