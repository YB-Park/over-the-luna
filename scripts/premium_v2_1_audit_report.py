#!/usr/bin/env python3
"""Summarize a Premium v2.1 audit-mode hook trace without invoking AI."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BUILDER_NAME = "Premium v2.1 Luna Builder"
EXPECTED_EVENTS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "SubagentStart",
    "SubagentStop",
    "Stop",
}


def first_value(event: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in event and event.get(name) is not None:
            return event.get(name)
    return None


def agent_name(event: dict[str, Any]) -> str:
    return str(
        first_value(
            event,
            "agent_type",
            "agent_name",
            "agentName",
            "agent_display_name",
            "agentDisplayName",
        )
        or ""
    )


def read_events(path: Path) -> tuple[list[dict[str, Any]], int]:
    events: list[dict[str, Any]] = []
    invalid = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            invalid += 1
            continue
        if isinstance(value, dict):
            events.append(value)
        else:
            invalid += 1
    return events, invalid


def summarize(events: list[dict[str, Any]], invalid_lines: int = 0, state: Any = None) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    field_sets: dict[str, set[tuple[str, ...]]] = defaultdict(set)
    session_ids: set[str] = set()
    builder_starts = 0
    builder_stops = 0
    order: list[str] = []

    for event in events:
        name = str(first_value(event, "hook_event_name", "hookEventName") or "UNKNOWN")
        counts[name] += 1
        order.append(name)
        field_sets[name].add(tuple(sorted(event)))
        sid = first_value(event, "session_id", "sessionId")
        if isinstance(sid, str) and sid:
            session_ids.add(sid)
        tool = first_value(event, "tool_name", "toolName")
        if isinstance(tool, str) and tool:
            tool_names[tool] += 1
        if name == "SubagentStart" and agent_name(event) == BUILDER_NAME:
            builder_starts += 1
        if name == "SubagentStop" and agent_name(event) == BUILDER_NAME:
            builder_stops += 1

    state_obj = state if isinstance(state, dict) else {}
    state_builder_count = state_obj.get("builder_count")
    observed = set(counts)
    lifecycle_core = {"SessionStart", "UserPromptSubmit", "Stop"}.issubset(observed)
    delegation = builder_starts >= 1 and builder_stops >= 1
    single_builder = (
        builder_starts == 1
        and builder_stops == 1
        and (state_builder_count in (None, 1))
    )
    report = {
        "schema": "premium-v2.1-audit-report-v1",
        "zero_ai": True,
        "event_count": len(events),
        "invalid_jsonl_lines": invalid_lines,
        "event_counts": dict(sorted(counts.items())),
        "event_order": order,
        "missing_expected_events": sorted(EXPECTED_EVENTS - observed),
        "tool_names": dict(sorted(tool_names.items())),
        "session_ids": sorted(session_ids),
        "field_sets": {
            name: [list(fields) for fields in sorted(sets)]
            for name, sets in sorted(field_sets.items())
        },
        "builder": {
            "name": BUILDER_NAME,
            "starts": builder_starts,
            "stops": builder_stops,
            "state_builder_count": state_builder_count,
        },
        "controller_state": {
            "phase": state_obj.get("phase"),
            "builder_count": state_builder_count,
            "takeover": state_obj.get("takeover"),
            "correction_count": state_obj.get("correction_count"),
            "receipt_count": len(state_obj.get("receipts", {}))
            if isinstance(state_obj.get("receipts"), dict)
            else None,
            "final_record": state_obj.get("final_record"),
        },
        "observations": {
            "core_hook_lifecycle_observed": lifecycle_core,
            "builder_delegation_observed": delegation,
            "single_builder_trajectory_observed": single_builder,
            "schema_trace_parse_clean": invalid_lines == 0,
        },
        "not_observable_from_hook_trace_alone": [
            "actual root backend model identity",
            "actual Luna child backend model identity",
            "AI credit usage",
            "tamper resistance of same-user controller state",
        ],
    }
    report["calibration_status"] = (
        "TRACE_READY_FOR_SCHEMA_REVIEW"
        if lifecycle_core and delegation and invalid_lines == 0
        else "TRACE_INCOMPLETE"
    )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--state", type=Path)
    args = parser.parse_args(argv)

    events, invalid = read_events(args.events)
    state: Any = None
    if args.state and args.state.exists():
        try:
            state = json.loads(args.state.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            state = {"state_parse_error": True}

    print(json.dumps(summarize(events, invalid, state), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
