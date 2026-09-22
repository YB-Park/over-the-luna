#!/usr/bin/env python3
"""Zero-AI runtime trace summarizer for the Premium v2.1 experiment.

The reporter consumes raw hook JSONL, controller state/final records, and
optional Copilot CLI JSONL. It does not invoke a model and it does not infer
facts that are absent from the captured runtime evidence.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any, Iterable

EXPECTED_EVENTS = (
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "SubagentStart",
    "SubagentStop",
    "Stop",
)
BUILDER_NAME = "Premium v2.1 Luna Builder"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            rows.append({"_parse_error": True, "_line": lineno})
            continue
        if isinstance(value, dict):
            rows.append(value)
        else:
            rows.append({"_parse_error": True, "_line": lineno, "_non_object": True})
    return rows


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def first_value(value: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in value and value.get(name) is not None:
            return value.get(name)
    return None


def event_name(event: dict[str, Any]) -> str:
    explicit = first_value(event, "hook_event_name", "hookEventName", "event_name", "eventName")
    if isinstance(explicit, str):
        aliases = {
            "sessionStart": "SessionStart",
            "userPromptSubmitted": "UserPromptSubmit",
            "userPromptSubmit": "UserPromptSubmit",
            "preToolUse": "PreToolUse",
            "postToolUse": "PostToolUse",
            "subagentStart": "SubagentStart",
            "subagentStop": "SubagentStop",
            "agentStop": "Stop",
            "stop": "Stop",
        }
        return aliases.get(explicit, explicit)
    return ""


def agent_names(event: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for key in ("agent_type", "agent_name", "agentName", "agent_display_name", "agentDisplayName"):
        value = event.get(key)
        if isinstance(value, str) and value and value not in out:
            out.append(value)
    return out


def session_id(event: dict[str, Any]) -> str | None:
    value = first_value(event, "session_id", "sessionId")
    return value if isinstance(value, str) and value else None


def flatten_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from flatten_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from flatten_dicts(child)


def span_attributes(row: dict[str, Any]) -> dict[str, Any]:
    for key in ("attributes", "attrs"):
        value = row.get(key)
        if isinstance(value, dict):
            return value
    data = row.get("data")
    if isinstance(data, dict):
        for key in ("attributes", "attrs"):
            value = data.get(key)
            if isinstance(value, dict):
                return value
    return {}


def span_id(row: dict[str, Any]) -> str | None:
    value = first_value(row, "spanId", "span_id")
    if isinstance(value, str) and value:
        return value
    return None


def parent_span_id(row: dict[str, Any]) -> str | None:
    value = first_value(row, "parentSpanId", "parent_span_id")
    if isinstance(value, str) and value:
        return value
    return None


def _builder_agent_name(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    return normalized in {
        BUILDER_NAME.lower(),
        "premium-v2-1-luna-builder",
        "luna-builder-v2-1",
    } or ("premium" in normalized and "luna" in normalized and "builder" in normalized)


def parse_otel_jsonl(path: Path | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "present": bool(path and path.exists()),
        "parse_errors": 0,
        "span_count": 0,
        "root_invoke_count": 0,
        "builder_invoke_count": 0,
        "root_requested_models": [],
        "root_resolved_models": [],
        "builder_requested_models": [],
        "builder_resolved_models": [],
        "root_usage_credits": None,
    }
    if path is None:
        return result

    rows = read_jsonl(path)
    result["parse_errors"] = sum(1 for row in rows if row.get("_parse_error") is True)
    spans = [row for row in rows if span_attributes(row)]
    result["span_count"] = len(spans)

    by_id = {
        sid: row
        for row in spans
        if (sid := span_id(row)) is not None
    }

    invoke_spans: list[dict[str, Any]] = []
    chat_spans: list[dict[str, Any]] = []
    for row in spans:
        attrs = span_attributes(row)
        operation = attrs.get("gen_ai.operation.name")
        if operation == "invoke_agent":
            invoke_spans.append(row)
        elif operation == "chat":
            chat_spans.append(row)

    root_invokes = [
        row
        for row in invoke_spans
        if "server.address" in span_attributes(row)
        or "server.port" in span_attributes(row)
    ]
    builder_invokes = [
        row
        for row in invoke_spans
        if _builder_agent_name(span_attributes(row).get("gen_ai.agent.name"))
        or _builder_agent_name(span_attributes(row).get("gen_ai.agent.id"))
    ]
    result["root_invoke_count"] = len(root_invokes)
    result["builder_invoke_count"] = len(builder_invokes)

    root_ids = {sid for row in root_invokes if (sid := span_id(row))}
    builder_ids = {sid for row in builder_invokes if (sid := span_id(row))}

    def nearest_invoke_id(row: dict[str, Any]) -> str | None:
        current = parent_span_id(row)
        seen: set[str] = set()
        while current and current not in seen:
            seen.add(current)
            parent = by_id.get(current)
            if parent is None:
                return None
            attrs = span_attributes(parent)
            if attrs.get("gen_ai.operation.name") == "invoke_agent":
                return current
            current = parent_span_id(parent)
        return None

    def append_unique(target: list[str], value: Any) -> None:
        if isinstance(value, str) and value and value not in target:
            target.append(value)

    root_requested: list[str] = []
    builder_requested: list[str] = []
    for row in root_invokes:
        append_unique(root_requested, span_attributes(row).get("gen_ai.request.model"))
    for row in builder_invokes:
        append_unique(builder_requested, span_attributes(row).get("gen_ai.request.model"))

    root_resolved: list[str] = []
    builder_resolved: list[str] = []
    for row in chat_spans:
        attrs = span_attributes(row)
        owner = nearest_invoke_id(row)
        model = attrs.get("gen_ai.response.model")
        if owner in root_ids:
            append_unique(root_resolved, model)
        elif owner in builder_ids:
            append_unique(builder_resolved, model)

    credits: list[float] = []
    for row in root_invokes:
        value = span_attributes(row).get("github.copilot.nano_aiu")
        if isinstance(value, (int, float)):
            credits.append(float(value) / 1_000_000_000)

    result["root_requested_models"] = root_requested
    result["root_resolved_models"] = root_resolved
    result["builder_requested_models"] = builder_requested
    result["builder_resolved_models"] = builder_resolved
    result["root_usage_credits"] = sum(credits) if credits else None
    return result


def parse_cli_jsonl(path: Path | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "present": bool(path and path.exists()),
        "parse_errors": 0,
        "model_call_models": [],
        "subagents": [],
        "usage_credits": None,
    }
    if path is None:
        return result

    rows = read_jsonl(path)
    result["parse_errors"] = sum(1 for row in rows if row.get("_parse_error") is True)
    models: list[str] = []
    subagents: list[dict[str, Any]] = []
    usage: float | None = None

    for row in rows:
        typ = row.get("type")
        data = row.get("data")
        if not isinstance(data, dict):
            data = {}

        if typ == "model.call_start":
            model = data.get("model")
            if isinstance(model, str) and model and model not in models:
                models.append(model)
        elif typ == "subagent.completed":
            subagents.append(
                {
                    "agent": first_value(data, "agentDisplayName", "agentName", "agent_type"),
                    "model": data.get("model"),
                    "tool_calls": first_value(data, "totalToolCalls", "tool_calls"),
                    "tokens": first_value(data, "totalTokens", "tokens"),
                    "duration_ms": first_value(data, "durationMs", "duration_ms"),
                }
            )
        elif typ == "session.usage_checkpoint":
            nano = data.get("totalNanoAiu")
            if isinstance(nano, (int, float)):
                usage = nano / 1_000_000_000

    result["model_call_models"] = models
    result["subagents"] = subagents
    result["usage_credits"] = usage
    return result


def _family_status(models: list[str], family: str) -> str:
    if not models:
        return "NOT_OBSERVED"
    lowered = [model.lower() for model in models]
    if all(family in model for model in lowered):
        return "OBSERVED"
    return "CONFLICT"


def classify_model_identity(cli: dict[str, Any], otel: dict[str, Any]) -> dict[str, Any]:
    # Root backend identity is accepted only from resolved chat spans attributed
    # to a top-level invoke_agent span. Unscoped legacy model.call_start events
    # are retained for diagnostics but cannot prove root identity.
    root_resolved = [
        model for model in otel.get("root_resolved_models", [])
        if isinstance(model, str)
    ]

    builder_models: list[str] = []
    for model in otel.get("builder_resolved_models", []):
        if isinstance(model, str) and model not in builder_models:
            builder_models.append(model)
    for subagent in cli.get("subagents", []):
        if not isinstance(subagent, dict):
            continue
        name = str(subagent.get("agent") or "")
        model = subagent.get("model")
        if name == BUILDER_NAME and isinstance(model, str) and model not in builder_models:
            builder_models.append(model)

    return {
        "root_terra": _family_status(root_resolved, "terra"),
        "builder_luna": _family_status(builder_models, "luna"),
        "root_resolved_models": root_resolved,
        "builder_models": builder_models,
        "root_requested_models": otel.get("root_requested_models", []),
        "builder_requested_models": otel.get("builder_requested_models", []),
        "legacy_unscoped_model_call_models": cli.get("model_call_models", []),
        "evidence_rule": (
            "root requires resolved chat-span model under top-level invoke_agent; "
            "builder may use builder invoke-agent chat spans or subagent.completed model"
        ),
    }


def summarize(
    state_dir: Path,
    workspace: Path | None = None,
    cli_output: Path | None = None,
    otel_output: Path | None = None,
) -> dict[str, Any]:
    event_files = sorted(state_dir.glob("*.events.jsonl")) if state_dir.exists() else []
    state_files = sorted(
        p for p in state_dir.glob("*.json")
        if not p.name.endswith(".events.jsonl")
    ) if state_dir.exists() else []

    events: list[dict[str, Any]] = []
    for path in event_files:
        events.extend(read_jsonl(path))

    event_names = [event_name(event) for event in events if event_name(event)]
    counts = collections.Counter(event_names)
    field_shapes: dict[str, list[list[str]]] = {}
    for event in events:
        name = event_name(event) or "UNKNOWN"
        shape = sorted(str(key) for key in event)
        known = field_shapes.setdefault(name, [])
        if shape not in known:
            known.append(shape)

    builder_starts = sum(
        1 for event in events
        if event_name(event) == "SubagentStart" and BUILDER_NAME in agent_names(event)
    )
    builder_stops = sum(
        1 for event in events
        if event_name(event) == "SubagentStop" and BUILDER_NAME in agent_names(event)
    )

    session_ids = sorted({sid for event in events if (sid := session_id(event))})

    controller_states = [value for path in state_files if (value := read_json(path)) is not None]
    receipt_count = 0
    collected_pass_receipts = 0
    for state in controller_states:
        receipts = state.get("receipts")
        if not isinstance(receipts, dict):
            continue
        receipt_count += len(receipts)
        collected_pass_receipts += sum(
            1
            for receipt in receipts.values()
            if isinstance(receipt, dict)
            and receipt.get("collection_status") == "COLLECTED"
            and receipt.get("result_class") == "PASS"
        )

    final_records: list[dict[str, Any]] = []
    if workspace is not None:
        final = read_json(workspace / ".otl-v2-1" / "final-record.json")
        if final is not None:
            final_records.append(final)
    for state in controller_states:
        final = state.get("final_record")
        if isinstance(final, dict) and final not in final_records:
            final_records.append(final)

    cli = parse_cli_jsonl(cli_output)
    otel = parse_otel_jsonl(otel_output)
    model_identity = classify_model_identity(cli, otel)

    missing_events = [name for name in EXPECTED_EVENTS if counts.get(name, 0) == 0]
    hook_firing = "OBSERVED" if events else "NOT_OBSERVED"
    delegation = (
        "OBSERVED"
        if builder_starts == 1 and builder_stops == 1
        else "NOT_OBSERVED"
    )
    controller_final = "OBSERVED" if final_records else "NOT_OBSERVED"

    calibration_ready = (
        not missing_events
        and builder_starts == 1
        and builder_stops == 1
        and controller_final == "OBSERVED"
        and model_identity["root_terra"] == "OBSERVED"
        and model_identity["builder_luna"] == "OBSERVED"
        and not any(event.get("_parse_error") is True for event in events)
    )

    return {
        "schema": "premium-v2.1-runtime-trace-v1",
        "zero_ai": True,
        "state_dir": str(state_dir),
        "workspace": str(workspace) if workspace else None,
        "hook_trace": {
            "status": hook_firing,
            "event_files": [str(path) for path in event_files],
            "event_count": len(events),
            "event_counts": dict(sorted(counts.items())),
            "missing_expected_events": missing_events,
            "session_ids": session_ids,
            "field_shapes": field_shapes,
            "parse_errors": sum(1 for event in events if event.get("_parse_error") is True),
        },
        "delegation": {
            "status": delegation,
            "builder_name": BUILDER_NAME,
            "builder_start_count": builder_starts,
            "builder_stop_count": builder_stops,
            "exactly_one_complete_builder_lifecycle": builder_starts == 1 and builder_stops == 1,
        },
        "controller": {
            "state_files": [str(path) for path in state_files],
            "receipt_count": receipt_count,
            "collected_pass_receipts": collected_pass_receipts,
            "final_record_status": controller_final,
            "final_records": final_records,
        },
        "cli": cli,
        "otel": otel,
        "backend_identity": model_identity,
        "calibration": {
            "ready_for_enforce_mode_candidate": calibration_ready,
            "note": (
                "True means the minimum runtime evidence needed to consider a separate "
                "enforce-mode change was observed. It is not a security or correctness proof."
            ),
        },
        "not_proven_by_this_report": [
            "semantic completeness of the criterion register",
            "semantic relevance of a passing receipt",
            "tamper resistance against same-user shell access",
            "product quality or cost advantage",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--cli-output", type=Path)
    parser.add_argument("--otel-output", type=Path)
    parser.add_argument("--require-calibration-ready", action="store_true")
    args = parser.parse_args(argv)

    report = summarize(
        args.state_dir.expanduser().resolve(),
        args.workspace.expanduser().resolve() if args.workspace else None,
        args.cli_output.expanduser().resolve() if args.cli_output else None,
        args.otel_output.expanduser().resolve() if args.otel_output else None,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.require_calibration_ready and not report["calibration"]["ready_for_enforce_mode_candidate"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
