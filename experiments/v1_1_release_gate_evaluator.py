from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CASES = ("tiny", "local", "broad", "risk")


def load_events(path: Path) -> list[dict]:
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def task_requests(message: dict) -> list[dict]:
    data = message.get("data") or {}
    requests = data.get("toolRequests") or []
    return [request for request in requests if isinstance(request, dict)]


def parse_route(events: list[dict]) -> tuple[str | None, str | None]:
    route_re = re.compile(
        r"Mode:\s*(SIMPLE|STANDARD|DEEP).*?Assurance:\s*(NONE|REVIEW|RISK)",
        re.S,
    )
    for event in events:
        if event.get("type") != "assistant.message" or event.get("agentId"):
            continue
        content = str((event.get("data") or {}).get("content") or "")
        match = route_re.search(content)
        if match:
            return match.group(1), match.group(2)
    return None, None


def has_concrete_patch(prompt: str) -> bool:
    if "diff --git" in prompt or "```diff" in prompt:
        return True
    # Accept a compact hand-assembled patch packet. Do not couple the gate to a
    # specific heading or to full `git diff` headers.
    has_hunk = bool(re.search(r"(?m)^@@(?:\s|$)", prompt))
    has_add = bool(re.search(r"(?m)^\+(?!\+)", prompt))
    has_del = bool(re.search(r"(?m)^-(?!--)", prompt))
    return has_hunk and (has_add or has_del)


def evaluate(case: str, events_path: Path, ownership_path: Path) -> int:
    events = load_events(events_path)
    ownership = json.loads(ownership_path.read_text(encoding="utf-8"))
    failures: list[str] = []

    mode, assurance = parse_route(events)
    expected_mode, expected_assurance = {
        "tiny": ("SIMPLE", "NONE"),
        "local": ("SIMPLE", "REVIEW"),
        "broad": ("STANDARD", "REVIEW"),
        "risk": (None, "RISK"),
    }[case]
    if expected_mode is not None and mode != expected_mode:
        failures.append(f"route mode expected {expected_mode}, got {mode}")
    if assurance != expected_assurance:
        failures.append(f"assurance expected {expected_assurance}, got {assurance}")

    subagent_names = [
        str((event.get("data") or {}).get("agentName") or "")
        for event in events
        if event.get("type") == "subagent.started"
    ]
    reviewer_count = sum(name.endswith("luna-reviewer") for name in subagent_names)
    architect_count = sum(name.endswith("luna-architect") for name in subagent_names)
    premium_count = sum(
        "sonnet" in name.lower() or "opus" in name.lower() for name in subagent_names
    )

    expected_reviewer = {"tiny": 0, "local": 1, "broad": 1}.get(case)
    if expected_reviewer is not None and reviewer_count != expected_reviewer:
        failures.append(f"Reviewer count expected {expected_reviewer}, got {reviewer_count}")
    if case == "risk" and not (1 <= reviewer_count <= 2):
        failures.append(f"RISK Reviewer count expected 1..2, got {reviewer_count}")

    expected_architect = {"tiny": 0, "local": 0, "broad": 1}.get(case)
    if expected_architect is not None and architect_count != expected_architect:
        failures.append(f"Architect count expected {expected_architect}, got {architect_count}")
    if premium_count:
        failures.append(f"automatic premium subagent count must be 0, got {premium_count}")

    by_agent = ownership.get("by_agent") or {}
    for agent, tools in by_agent.items():
        if agent.endswith("luna-reviewer"):
            reads = sum(
                int(tools.get(name, 0))
                for name in ("view", "rg", "glob", "search", "read")
            )
            if reads > 8:
                failures.append(f"Reviewer read/search budget exceeded: {reads} > 8")
        if agent != "over-the-luna:over-the-luna":
            for mutation_tool in ("apply_patch", "edit", "create", "delete"):
                if int(tools.get(mutation_tool, 0)):
                    failures.append(f"leaf agent {agent} used mutation tool {mutation_tool}")

    reviewer_task_prompts: list[str] = []
    architect_completed_index: int | None = None
    for index, event in enumerate(events):
        if event.get("type") == "subagent.completed":
            name = str((event.get("data") or {}).get("agentName") or "")
            if name.endswith("luna-architect"):
                architect_completed_index = index
        if event.get("type") == "assistant.message" and not event.get("agentId"):
            for request in task_requests(event):
                if request.get("name") != "task":
                    continue
                args = request.get("arguments") or {}
                if str(args.get("agent_type") or "").endswith("luna-reviewer"):
                    reviewer_task_prompts.append(str(args.get("prompt") or ""))

    for prompt in reviewer_task_prompts:
        if not has_concrete_patch(prompt):
            failures.append("Reviewer prompt missing concrete diff/hunk artifact")

    # A root directory listing may display `.git`; that is not a metadata read.
    # Flag only explicit tool arguments that target VCS metadata itself.
    for event in events:
        if event.get("type") != "assistant.message" or not event.get("agentId"):
            continue
        for request in task_requests(event):
            args = request.get("arguments") or {}
            if request.get("name") == "view":
                path = str(args.get("path") or "")
                if ".git" in Path(path).parts:
                    failures.append(f"leaf attempted .git inspection: {path}")
            elif request.get("name") in {"rg", "glob", "search", "read"}:
                serialized = json.dumps(args, sort_keys=True)
                if re.search(r"(?:^|[/\\])\.git(?:[/\\]|\b)", serialized):
                    failures.append(
                        f"leaf attempted .git inspection via {request.get('name')}: {serialized[:180]}"
                    )

    if case == "broad" and architect_completed_index is not None:
        shell_broad = re.compile(
            r"(^|(?:&&|\|\||[;|])\s*)(?:find\s+\.|ls\s+-R|tree(?:\s|$)|"
            r"git\s+(?:grep|ls-files)|grep\s+-R|rg(?:\s|$))"
        )
        for event in events[architect_completed_index + 1 :]:
            if event.get("type") != "assistant.message" or event.get("agentId"):
                continue
            for request in task_requests(event):
                name = str(request.get("name") or "")
                args = request.get("arguments") or {}
                if name in {"rg", "glob"}:
                    failures.append(f"Main replayed broad discovery after Architect via {name}")
                elif name == "view":
                    path = str(args.get("path") or "")
                    if path and not Path(path).suffix and not path.endswith(".agent.md"):
                        failures.append(f"Main viewed directory after Architect handback: {path}")
                elif name == "bash":
                    command = str(args.get("command") or "")
                    if shell_broad.search(command):
                        failures.append(
                            f"Main used shell broad discovery after Architect: {command[:160]}"
                        )

    print("POLICY_GATE:", "PASS" if not failures else "FAIL")
    print(f"- route={mode}+{assurance}")
    print(f"- architect={architect_count}")
    print(f"- reviewer={reviewer_count}")
    print(f"- premium={premium_count}")
    for failure in failures:
        print("FAIL:", failure)
    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--ownership", type=Path, required=True)
    args = parser.parse_args()
    return evaluate(args.case, args.events, args.ownership)


if __name__ == "__main__":
    raise SystemExit(main())
