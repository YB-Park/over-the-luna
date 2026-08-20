from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


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


def tool_requests(event: dict) -> list[dict]:
    data = event.get("data") or {}
    values = data.get("toolRequests") or []
    return [value for value in values if isinstance(value, dict)]


def route(events: list[dict]) -> tuple[str | None, str | None]:
    pattern = re.compile(r"Mode:\s*(SIMPLE|STANDARD|DEEP).*?Assurance:\s*(NONE|REVIEW|RISK)", re.S)
    for event in events:
        if event.get("type") != "assistant.message" or event.get("agentId"):
            continue
        content = str((event.get("data") or {}).get("content") or "")
        match = pattern.search(content)
        if match:
            return match.group(1), match.group(2)
    return None, None


def concrete_patch(prompt: str) -> bool:
    lowered = prompt.lower()
    if "diff --git" in prompt and "@@" in prompt:
        return True
    # A compact caller-supplied hunk is still a concrete artifact even if file headers were omitted.
    if "@@" in prompt and ("changed files" in lowered or "current diff" in lowered or "patch" in lowered):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("tiny", "local", "broad", "risk"), required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--ownership", type=Path, required=True)
    args = parser.parse_args()

    events = load_events(args.events)
    ownership = json.loads(args.ownership.read_text(encoding="utf-8"))
    failures: list[str] = []

    mode, assurance = route(events)
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

    subagent_names = [
        str((event.get("data") or {}).get("agentName") or "")
        for event in events
        if event.get("type") == "subagent.started"
    ]
    reviewer_count = sum(name.endswith("luna-reviewer") for name in subagent_names)
    architect_count = sum(name.endswith("luna-architect") for name in subagent_names)
    premium_count = sum("sonnet" in name.lower() or "opus" in name.lower() for name in subagent_names)

    expected_reviewer = {"tiny": 0, "local": 1, "broad": 1}.get(args.case)
    if expected_reviewer is not None and reviewer_count != expected_reviewer:
        failures.append(f"Reviewer count expected {expected_reviewer}, got {reviewer_count}")
    if args.case == "risk" and not (1 <= reviewer_count <= 2):
        failures.append(f"RISK Reviewer count expected 1..2, got {reviewer_count}")

    expected_architect = {"tiny": 0, "local": 0, "broad": 1}.get(args.case)
    if expected_architect is not None and architect_count != expected_architect:
        failures.append(f"Architect count expected {expected_architect}, got {architect_count}")
    if premium_count:
        failures.append(f"automatic premium subagent count must be 0, got {premium_count}")

    by_agent = ownership.get("by_agent") or {}
    for agent, tools in by_agent.items():
        if agent.endswith("luna-reviewer"):
            reads = sum(int(tools.get(name, 0)) for name in ("view", "rg", "glob", "search", "read"))
            if reads > 8:
                failures.append(f"Reviewer read/search budget exceeded: {reads} > 8")
        if agent != "over-the-luna:over-the-luna":
            for mutation_tool in ("apply_patch", "edit", "create", "delete"):
                if int(tools.get(mutation_tool, 0)):
                    failures.append(f"leaf agent {agent} used mutation tool {mutation_tool}")

    reviewer_prompts: list[str] = []
    architect_done: int | None = None
    boundary_sealed_index: int | None = None

    for index, event in enumerate(events):
        if event.get("type") == "subagent.completed":
            name = str((event.get("data") or {}).get("agentName") or "")
            if name.endswith("luna-architect"):
                architect_done = index

        if event.get("type") != "assistant.message" or event.get("agentId"):
            continue

        content = str((event.get("data") or {}).get("content") or "")
        if "Boundary sealed" in content and boundary_sealed_index is None:
            boundary_sealed_index = index

        for request in tool_requests(event):
            if request.get("name") != "task":
                continue
            values = request.get("arguments") or {}
            if str(values.get("agent_type") or "").endswith("luna-reviewer"):
                reviewer_prompts.append(str(values.get("prompt") or ""))

    if args.case == "broad":
        if architect_done is None:
            failures.append("broad case has no completed Architect handback")
        if boundary_sealed_index is None:
            failures.append("Main did not emit Boundary sealed work-set transition")
        elif architect_done is not None and boundary_sealed_index < architect_done:
            failures.append("Boundary sealed transition appeared before Architect completed")

    for prompt in reviewer_prompts:
        if not concrete_patch(prompt):
            failures.append("Reviewer prompt missing concrete diff/hunk artifact")

    # No read-only leaf needs VCS internals for these product tasks.
    for event in events:
        if event.get("type") != "assistant.message" or not event.get("agentId"):
            continue
        for request in tool_requests(event):
            if request.get("name") == "view":
                path = str((request.get("arguments") or {}).get("path") or "")
                if "/.git" in path or path.endswith("/.git"):
                    failures.append(f"leaf attempted VCS metadata inspection: {path}")

    if args.case == "broad" and architect_done is not None:
        broad_shell = re.compile(
            r"(^|[;&|]\s*)(find\s+\.|ls\s+-R|tree(?:\s|$)|git\s+(?:grep|ls-files)|grep\s+-R|rg(?:\s|$))"
        )
        first_repo_action_checked = False
        allowed_first_view = False

        for event in events[architect_done + 1 :]:
            if event.get("type") != "assistant.message" or event.get("agentId"):
                continue
            for request in tool_requests(event):
                name = str(request.get("name") or "")
                values = request.get("arguments") or {}

                if name in {"task", "list_agents", "read_agent"}:
                    continue

                if not first_repo_action_checked:
                    first_repo_action_checked = True
                    # After sealing, the first repository action should be a concrete file read,
                    # not a discovery or shell command. File paths have a suffix in these fixtures.
                    if name == "view":
                        path = str(values.get("path") or "")
                        allowed_first_view = bool(Path(path).suffix)
                    if not allowed_first_view:
                        failures.append(f"first repository action after Architect was {name}, expected concrete file view")

                if name in {"rg", "glob"}:
                    failures.append(f"Main replayed broad discovery after Architect via {name}")
                elif name == "view":
                    path = str(values.get("path") or "")
                    if path and not Path(path).suffix:
                        failures.append(f"Main viewed directory after Architect handback: {path}")
                elif name == "bash":
                    command = str(values.get("command") or "")
                    if broad_shell.search(command):
                        failures.append(f"Main used shell broad discovery after Architect: {command[:180]}")

    print("POLICY_GATE:", "PASS" if not failures else "FAIL")
    print(f"- route={mode}+{assurance}")
    print(f"- architect={architect_count}")
    print(f"- reviewer={reviewer_count}")
    print(f"- premium={premium_count}")
    for failure in failures:
        print("FAIL:", failure)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
