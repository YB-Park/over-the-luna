#!/usr/bin/env python3
"""Zero-AI runtime trace summarizer for the Premium v2.1 experiment.

The reporter consumes raw hook JSONL, controller state/final records, and
optional Copilot CLI JSONL. It does not invoke a model and it does not infer
facts that are absent from the captured runtime evidence.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import stat
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
ROOT_AGENT_NAME = "Premium Cascade v2.1 (Experimental)"
BUILDER_NAME = "Premium v2.1 Luna Builder"
TERMINAL_OUTCOMES = {
    "COMPLETE",
    "BLOCKED",
    "FAILED",
    "PARTIAL_WITH_USER_WAIVER",
    "NO_VERIFIED_COMPLETION",
}


def workspace_digest(
    root: Path,
    exclude_names: Iterable[str] = (".git", ".otl-v2-1"),
) -> str:
    """Recompute the plugin-compatible worktree digest for trace validation."""
    root = root.resolve()
    excluded = set(exclude_names)
    hasher = hashlib.sha256()
    entries: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in excluded for part in relative.parts):
            continue
        entries.append(path)

    for path in sorted(entries, key=lambda p: p.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        executable = bool(info.st_mode & stat.S_IXUSR)
        if path.is_symlink():
            kind = "L"
            payload = os.readlink(path).encode("utf-8", "surrogateescape")
        elif path.is_file():
            kind = "F"
            payload = path.read_bytes()
        elif path.is_dir():
            kind = "D"
            payload = b""
        else:
            kind = "O"
            payload = b""
        hasher.update(kind.encode("ascii"))
        hasher.update(b"\0")
        hasher.update(relative.encode("utf-8", "surrogateescape"))
        hasher.update(b"\0")
        hasher.update(b"x" if executable else b"-")
        hasher.update(b"\0")
        hasher.update(hashlib.sha256(payload).digest())
    return hasher.hexdigest()


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


def _root_agent_name(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    return normalized in {
        ROOT_AGENT_NAME.lower(),
        "premium-cascade-v2-1",
        "premium-v2-1-cascade",
    } or ("premium" in normalized and "cascade" in normalized and "v2.1" in normalized)


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
        "root_invoke_selection": "none",
        "builder_invoke_count": 0,
        "builder_invoke_candidate_count": 0,
        "disconnected_builder_invoke_count": 0,
        "hook_span_count": 0,
        "hook_span_under_root_count": 0,
        "hook_span_counts": {},
        "hook_result_kinds": {},
        "hook_decisions": {},
        "missing_expected_hook_spans": list(EXPECTED_EVENTS),
        "hook_span_failures": [],
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

    named_root_invokes = [
        row
        for row in invoke_spans
        if _root_agent_name(span_attributes(row).get("gen_ai.agent.name"))
        or _root_agent_name(span_attributes(row).get("gen_ai.agent.id"))
    ]

    def has_invoke_ancestor(row: dict[str, Any]) -> bool:
        current = parent_span_id(row)
        seen: set[str] = set()
        while current and current not in seen:
            seen.add(current)
            parent = by_id.get(current)
            if parent is None:
                return False
            if span_attributes(parent).get("gen_ai.operation.name") == "invoke_agent":
                return True
            current = parent_span_id(parent)
        return False

    top_level_invokes = [
        row
        for row in invoke_spans
        if not has_invoke_ancestor(row)
        and not _builder_agent_name(span_attributes(row).get("gen_ai.agent.name"))
        and not _builder_agent_name(span_attributes(row).get("gen_ai.agent.id"))
    ]
    legacy_server_root_invokes = [
        row
        for row in invoke_spans
        if (
            "server.address" in span_attributes(row)
            or "server.port" in span_attributes(row)
        )
        and not _builder_agent_name(span_attributes(row).get("gen_ai.agent.name"))
        and not _builder_agent_name(span_attributes(row).get("gen_ai.agent.id"))
    ]
    if named_root_invokes:
        root_invokes = named_root_invokes
        result["root_invoke_selection"] = "named_root_agent"
    elif len(top_level_invokes) == 1:
        root_invokes = top_level_invokes
        result["root_invoke_selection"] = "single_top_level_invoke"
    elif legacy_server_root_invokes:
        root_invokes = legacy_server_root_invokes
        result["root_invoke_selection"] = "legacy_server_heuristic"
    else:
        root_invokes = []
    builder_candidates = [
        row
        for row in invoke_spans
        if _builder_agent_name(span_attributes(row).get("gen_ai.agent.name"))
        or _builder_agent_name(span_attributes(row).get("gen_ai.agent.id"))
    ]
    result["root_invoke_count"] = len(root_invokes)
    result["builder_invoke_candidate_count"] = len(builder_candidates)

    root_ids = {sid for row in root_invokes if (sid := span_id(row))}

    def has_ancestor_id(row: dict[str, Any], ancestor_ids: set[str]) -> bool:
        current = parent_span_id(row)
        seen: set[str] = set()
        while current and current not in seen:
            if current in ancestor_ids:
                return True
            seen.add(current)
            parent = by_id.get(current)
            if parent is None:
                return False
            current = parent_span_id(parent)
        return False

    builder_invokes = [
        row for row in builder_candidates if has_ancestor_id(row, root_ids)
    ]
    result["builder_invoke_count"] = len(builder_invokes)
    result["disconnected_builder_invoke_count"] = (
        len(builder_candidates) - len(builder_invokes)
    )
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
    root_resolved: list[str] = []
    builder_resolved: list[str] = []
    for row in root_invokes:
        attrs = span_attributes(row)
        append_unique(root_requested, attrs.get("gen_ai.request.model"))
        append_unique(root_resolved, attrs.get("gen_ai.response.model"))
    for row in builder_invokes:
        attrs = span_attributes(row)
        append_unique(builder_requested, attrs.get("gen_ai.request.model"))
        append_unique(builder_resolved, attrs.get("gen_ai.response.model"))

    for row in chat_spans:
        attrs = span_attributes(row)
        owner = nearest_invoke_id(row)
        model = attrs.get("gen_ai.response.model")
        if owner in root_ids:
            append_unique(root_resolved, model)
        elif owner in builder_ids:
            append_unique(builder_resolved, model)

    all_hook_spans = [
        row
        for row in spans
        if span_attributes(row).get("gen_ai.operation.name") == "execute_hook"
    ]
    hook_spans = [
        row for row in all_hook_spans if has_ancestor_id(row, root_ids)
    ]
    hook_counts: collections.Counter[str] = collections.Counter()
    hook_result_kinds: dict[str, list[str]] = {}
    hook_decisions: dict[str, list[str]] = {}
    hook_failures: list[str] = []
    for row in hook_spans:
        attrs = span_attributes(row)
        hook_type = attrs.get("copilot_chat.hook_type")
        if not isinstance(hook_type, str) or not hook_type:
            hook_failures.append("execute_hook span missing copilot_chat.hook_type")
            continue
        normalized_type = event_name({"hook_event_name": hook_type}) or hook_type
        hook_counts[normalized_type] += 1
        result_kind = attrs.get("copilot_chat.hook_result_kind")
        if isinstance(result_kind, str) and result_kind:
            hook_result_kinds.setdefault(normalized_type, [])
            if result_kind not in hook_result_kinds[normalized_type]:
                hook_result_kinds[normalized_type].append(result_kind)
            if result_kind != "success":
                hook_failures.append(
                    f"{normalized_type}: OTel hook result kind is {result_kind!r}"
                )
        else:
            hook_failures.append(
                f"{normalized_type}: OTel hook result kind missing"
            )
        decision = attrs.get("github.copilot.hook.decision")
        if isinstance(decision, str) and decision:
            hook_decisions.setdefault(normalized_type, [])
            if decision not in hook_decisions[normalized_type]:
                hook_decisions[normalized_type].append(decision)

    result["hook_span_count"] = len(all_hook_spans)
    result["hook_span_under_root_count"] = len(hook_spans)
    result["hook_span_counts"] = dict(sorted(hook_counts.items()))
    result["hook_result_kinds"] = hook_result_kinds
    result["hook_decisions"] = hook_decisions
    result["missing_expected_hook_spans"] = [
        name for name in EXPECTED_EVENTS if hook_counts.get(name, 0) == 0
    ]
    result["hook_span_failures"] = hook_failures

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
    session_key: str | None = None,
) -> dict[str, Any]:
    all_event_files = sorted(state_dir.glob("*.events.jsonl")) if state_dir.exists() else []
    available_keys = [
        path.name[: -len(".events.jsonl")]
        for path in all_event_files
    ]
    selected_key: str | None = None
    selection_error: str | None = None

    if session_key:
        if session_key in available_keys:
            selected_key = session_key
        else:
            selection_error = f"requested session key not found: {session_key}"
    elif len(available_keys) == 1:
        selected_key = available_keys[0]
    elif len(available_keys) > 1:
        selection_error = (
            "multiple runtime sessions are present; pass --session-key explicitly"
        )

    event_files = (
        [state_dir / f"{selected_key}.events.jsonl"]
        if selected_key is not None
        else []
    )
    state_files = (
        [state_dir / f"{selected_key}.json"]
        if selected_key is not None and (state_dir / f"{selected_key}.json").exists()
        else []
    )

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

    current_workspace_revision: str | None = None
    workspace_digest_error: str | None = None
    if workspace is not None:
        try:
            current_workspace_revision = workspace_digest(workspace)
        except OSError as exc:
            workspace_digest_error = str(exc)

    final_records: list[dict[str, Any]] = []
    workspace_final_record: dict[str, Any] | None = None
    external_final_records: list[dict[str, Any]] = []
    if workspace is not None:
        workspace_final_record = read_json(workspace / ".otl-v2-1" / "final-record.json")
        if workspace_final_record is not None:
            final_records.append(workspace_final_record)
    for state in controller_states:
        final = state.get("final_record")
        if isinstance(final, dict):
            external_final_records.append(final)
            if final not in final_records:
                final_records.append(final)
    both_final_copies_present = (
        workspace_final_record is not None and len(external_final_records) == 1
    )

    expected_session_id = session_ids[0] if len(session_ids) == 1 else None
    final_record_assessments: list[dict[str, Any]] = []
    for record in final_records:
        errors: list[str] = []
        if record.get("schema") != "premium-v2.1-final-v1":
            errors.append("invalid schema")
        outcome = record.get("outcome")
        if outcome not in TERMINAL_OUTCOMES:
            errors.append("invalid outcome")
        trusted = record.get("trusted_complete")
        if not isinstance(trusted, bool):
            errors.append("trusted_complete must be boolean")
        elif trusted is not (outcome == "COMPLETE"):
            errors.append("trusted_complete/outcome mismatch")
        run_id = record.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            errors.append("run_id missing")
        elif expected_session_id is not None and run_id != expected_session_id:
            errors.append("run_id does not match selected hook session")
        revision = record.get("workspace_revision")
        if not isinstance(revision, str) or not revision:
            errors.append("workspace_revision missing")
        elif current_workspace_revision is None:
            errors.append("current workspace revision unavailable")
        elif revision != current_workspace_revision:
            errors.append("final record is stale for current workspace")
        if record.get("builder_dispatch_count") != 1:
            errors.append("final record builder_dispatch_count is not exactly one")
        if record.get("builder_count") != 1:
            errors.append("final record builder_count is not exactly one")
        if record.get("builder_agent_tool_completion_seen") is not True:
            errors.append("final record did not observe Builder agent-tool completion")
        if record.get("phase") not in {"ROOT_RECONCILE", "TERRA_TAKEOVER"}:
            errors.append("final record phase is not terminal-reconcilable")
        final_record_assessments.append(
            {
                "valid": not errors,
                "trusted_complete": trusted is True,
                "outcome": outcome,
                "run_id": run_id,
                "errors": errors,
            }
        )

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
    valid_complete_records = [
        item
        for item in final_record_assessments
        if item["valid"] and item["trusted_complete"]
    ]
    if not final_records:
        controller_final = "NOT_OBSERVED"
    elif len(final_records) > 1:
        # Equal records are deduplicated above. More than one record therefore
        # means workspace and external controller state disagree.
        controller_final = "CONFLICT"
    elif valid_complete_records:
        controller_final = "VALID_COMPLETE"
    elif all(item["valid"] for item in final_record_assessments):
        controller_final = "VALID_NONCOMPLETE"
    else:
        controller_final = "INVALID"

    lifecycle_counts_valid = (
        counts.get("SessionStart", 0) == 1
        and counts.get("UserPromptSubmit", 0) == 1
        and counts.get("Stop", 0) == 1
    )

    calibration_ready = (
        selection_error is None
        and selected_key is not None
        and len(session_ids) == 1
        and not missing_events
        and lifecycle_counts_valid
        and current_workspace_revision is not None
        and workspace_digest_error is None
        and builder_starts == 1
        and builder_stops == 1
        and receipt_count >= 1
        and collected_pass_receipts >= 1
        and both_final_copies_present
        and controller_final == "VALID_COMPLETE"
        and model_identity["root_terra"] == "OBSERVED"
        and model_identity["builder_luna"] == "OBSERVED"
        and otel.get("root_invoke_count") == 1
        and otel.get("builder_invoke_count") == 1
        and otel.get("disconnected_builder_invoke_count") == 0
        and not otel.get("missing_expected_hook_spans")
        and not otel.get("hook_span_failures")
        and not any(event.get("_parse_error") is True for event in events)
        and cli.get("parse_errors", 0) == 0
        and otel.get("parse_errors", 0) == 0
    )

    return {
        "schema": "premium-v2.1-runtime-trace-v1",
        "zero_ai": True,
        "state_dir": str(state_dir),
        "workspace": str(workspace) if workspace else None,
        "session_selection": {
            "requested_key": session_key,
            "available_keys": available_keys,
            "selected_key": selected_key,
            "ambiguous": len(available_keys) > 1 and session_key is None,
            "error": selection_error,
        },
        "hook_trace": {
            "status": hook_firing,
            "event_files": [str(path) for path in event_files],
            "event_count": len(events),
            "event_counts": dict(sorted(counts.items())),
            "missing_expected_events": missing_events,
            "session_ids": session_ids,
            "field_shapes": field_shapes,
            "parse_errors": sum(1 for event in events if event.get("_parse_error") is True),
            "single_mission_counts_valid": lifecycle_counts_valid,
        },
        "workspace_revision": {
            "current": current_workspace_revision,
            "error": workspace_digest_error,
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
            "final_record_sources": {
                "workspace_present": workspace_final_record is not None,
                "external_count": len(external_final_records),
                "both_expected_copies_present": both_final_copies_present,
            },
            "final_record_status": controller_final,
            "final_records": final_records,
            "final_record_assessments": final_record_assessments,
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
    parser.add_argument("--session-key")
    parser.add_argument("--require-calibration-ready", action="store_true")
    args = parser.parse_args(argv)

    report = summarize(
        args.state_dir.expanduser().resolve(),
        args.workspace.expanduser().resolve() if args.workspace else None,
        args.cli_output.expanduser().resolve() if args.cli_output else None,
        args.otel_output.expanduser().resolve() if args.otel_output else None,
        args.session_key,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.require_calibration_ready and not report["calibration"]["ready_for_enforce_mode_candidate"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
