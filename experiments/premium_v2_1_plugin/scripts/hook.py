#!/usr/bin/env python3
"""Plugin lifecycle hook for the Premium v2.1 minimal cascade.

Default mode is audit: record real hook schemas and controller outcomes without
forcing extra AI turns. Set OTL_V2_1_HOOK_MODE=enforce after schema calibration.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from controller import Reconciliation, atomic_json, reconcile, workspace_digest  # noqa: E402

BUILDER_NAME = "Premium v2.1 Luna Builder"
META_DIR = ".otl-v2-1"


def first_value(event: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in event and event.get(name) is not None:
            return event.get(name)
    return None


def event_session_id(event: dict[str, Any]) -> Any:
    return first_value(event, "session_id", "sessionId")


def event_tool_name(event: dict[str, Any]) -> str:
    return str(first_value(event, "tool_name", "toolName") or "")


def event_tool_input(event: dict[str, Any]) -> Any:
    value = first_value(event, "tool_input", "toolArgs")
    return {} if value is None else value


def event_tool_result(event: dict[str, Any]) -> Any:
    # VS Code currently supplies tool_response. Copilot CLI's VS Code-compatible
    # payload uses tool_result, while native camelCase hooks use toolResult.
    return first_value(event, "tool_response", "tool_result", "toolResult")


def event_agent_names(event: dict[str, Any]) -> list[str]:
    # Keep every documented name/type variant. Some runtimes expose both a
    # generic type and a concrete custom-agent name, so matching only the first
    # field can miss the Builder lifecycle.
    names: list[str] = []
    for key in (
        "agent_type",
        "agent_name",
        "agentName",
        "agent_display_name",
        "agentDisplayName",
    ):
        value = event.get(key)
        if isinstance(value, str) and value and value not in names:
            names.append(value)
    return names


def event_agent_name(event: dict[str, Any]) -> str:
    names = event_agent_names(event)
    if BUILDER_NAME in names:
        return BUILDER_NAME
    return names[0] if names else ""


def is_builder_event(event: dict[str, Any]) -> bool:
    return BUILDER_NAME in event_agent_names(event)


def state_root() -> Path:
    configured = os.environ.get("OTL_V2_1_STATE_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".copilot" / "over-the-luna-v2-1" / "state").resolve()


def session_key(event: dict[str, Any]) -> tuple[str, bool]:
    sid = event_session_id(event)
    if isinstance(sid, str) and sid:
        return hashlib.sha256(sid.encode()).hexdigest()[:24], False
    cwd = str(event.get("cwd") or os.getcwd())
    return hashlib.sha256(cwd.encode()).hexdigest()[:24], True


def session_paths(event: dict[str, Any]) -> tuple[Path, Path, str, bool]:
    key, weak = session_key(event)
    root = state_root()
    return root / f"{key}.json", root / f"{key}.events.jsonl", key, weak


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, sort_keys=True, default=str) + "\n")


def cwd_path(event: dict[str, Any]) -> Path:
    cwd = event.get("cwd")
    return Path(cwd).resolve() if isinstance(cwd, str) and cwd else Path.cwd().resolve()


def metadata_paths(cwd: Path) -> tuple[Path, Path, Path]:
    root = cwd / META_DIR
    return root / "controller-proposal.json", root / "receipt-index.json", root / "final-record.json"


def ensure_state(event: dict[str, Any]) -> tuple[dict[str, Any], Path, Path]:
    state_path, events_path, key, weak = session_paths(event)
    state = load_json(state_path, {})
    if not isinstance(state, dict) or not state:
        state = {
            "schema": "premium-v2.1-session-v1",
            "session_key": key,
            "session_id_observed": event_session_id(event),
            "weak_session_key": weak,
            "cwd": str(cwd_path(event)),
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "takeover": False,
            "obligations": {},
            "receipts": {},
            "user_events": [],
            "correction_count": 0,
        }
    return state, state_path, events_path


def save_state(path: Path, state: dict[str, Any]) -> None:
    atomic_json(path, state)


def init_user_obligation(event: dict[str, Any], state: dict[str, Any]) -> None:
    prompt = event.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return
    if "U0" not in state["obligations"]:
        state["obligations"]["U0"] = {
            "source": "U",
            "source_anchor": "UserPromptSubmit:original",
            "criterion": prompt.strip(),
            "blocking": True,
            "required": True,
            "history": [],
        }
    cwd = cwd_path(event)
    proposal_path, receipt_index_path, _ = metadata_paths(cwd)
    if not proposal_path.exists():
        atomic_json(
            proposal_path,
            {
                "requested_outcome": "COMPLETE",
                "current": {"U0": {"disposition": "OPEN", "evidence_refs": []}},
                "discovered_obligations": [],
            },
        )
    if not receipt_index_path.exists():
        atomic_json(receipt_index_path, {"receipts": []})


def flatten_strings(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            out.extend(flatten_strings(v))
    elif isinstance(value, list):
        for v in value:
            out.extend(flatten_strings(v))
    return out


def is_agent_tool(event: dict[str, Any]) -> bool:
    name = event_tool_name(event).lower()
    data = json.dumps(event_tool_input(event), sort_keys=True, default=str).lower()
    return "agent" in name or "subagent" in name or BUILDER_NAME.lower() in data


def is_metadata_only(event: dict[str, Any]) -> bool:
    strings = flatten_strings(event_tool_input(event))
    matching = [s for s in strings if META_DIR in s]
    return bool(matching) and all((META_DIR in s) or ("controller" in s.lower()) for s in strings if "/" in s or "\\" in s)


def pre_tool_decision(event: dict[str, Any], state: dict[str, Any], mode: str) -> dict[str, Any]:
    if mode != "enforce":
        return {}
    phase = state.get("phase")
    agent_tool = is_agent_tool(event)
    metadata_only = is_metadata_only(event)
    if phase == "ROOT_INTAKE" and not agent_tool and not metadata_only:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Premium v2.1 bounded intake requires the single Luna Builder attempt before repository work.",
            }
        }
    if state.get("builder_count", 0) >= 1 and agent_tool:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Premium v2.1 permits exactly one Luna Builder invocation and no later subagent call.",
            }
        }
    if phase == "ROOT_RECONCILE" and not metadata_only and not agent_tool:
        state["phase"] = "TERRA_TAKEOVER"
        state["takeover"] = True
    return {}


def recursive_exit_code(value: Any) -> int | None:
    if isinstance(value, dict):
        for key, v in value.items():
            if key.lower() in {"exitcode", "exit_code", "returncode", "return_code"} and isinstance(v, int):
                return v
        for v in value.values():
            found = recursive_exit_code(v)
            if found is not None:
                return found
    elif isinstance(value, list):
        for v in value:
            found = recursive_exit_code(v)
            if found is not None:
                return found
    elif isinstance(value, str):
        patterns = [
            r"(?:exit|return)\s*(?:code|status)?\s*[:=]?\s*(-?\d+)",
            r"process exited with code\s+(-?\d+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, value, flags=re.IGNORECASE)
            if match:
                return int(match.group(1))
    return None


def command_identity(event: dict[str, Any]) -> str:
    tool_input = event_tool_input(event)
    if isinstance(tool_input, dict):
        for key in ("command", "cmd", "script", "input"):
            value = tool_input.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()[:500]
    return f"{event_tool_name(event) or 'tool'}:{hashlib.sha256(json.dumps(tool_input, sort_keys=True, default=str).encode()).hexdigest()[:16]}"


def record_post_tool(event: dict[str, Any], state: dict[str, Any]) -> None:
    cwd = cwd_path(event)
    try:
        revision = workspace_digest(cwd)
    except OSError:
        revision = "DIGEST_ERROR"
    response = event_tool_result(event)
    exit_code = recursive_exit_code(response)
    receipt_id = f"E{len(state.get('receipts', {})) + 1}"
    receipt = {
        "run_id": str(event_session_id(event) or state.get("session_key")),
        "tool_use_id": first_value(event, "tool_use_id", "toolUseId"),
        "tool_name": event_tool_name(event),
        "command_or_test_id": command_identity(event),
        "collection_status": "COLLECTED" if exit_code is not None else "OBSERVED",
        "result_class": "PASS" if exit_code == 0 else ("ASSERTION_FAIL" if isinstance(exit_code, int) else "UNCLASSIFIED"),
        "exit_status": exit_code,
        "workspace_before": state.get("last_workspace_revision"),
        "workspace_after": revision,
        "test_asset_identity": hashlib.sha256(json.dumps(event_tool_input(event), sort_keys=True, default=str).encode()).hexdigest(),
        "environment_identity": f"premium-v2.1-hook-v1|{platform.system()}|py{platform.python_version()}",
    }
    state.setdefault("receipts", {})[receipt_id] = receipt
    state["last_workspace_revision"] = revision
    _, receipt_index_path, _ = metadata_paths(cwd)
    atomic_json(
        receipt_index_path,
        {
            "receipts": [
                {
                    "id": rid,
                    "tool_name": r.get("tool_name"),
                    "command_or_test_id": r.get("command_or_test_id"),
                    "result_class": r.get("result_class"),
                    "exit_status": r.get("exit_status"),
                    "workspace_after": r.get("workspace_after"),
                }
                for rid, r in state["receipts"].items()
            ]
        },
    )


def admit_discovered(proposal: dict[str, Any], state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    discoveries = proposal.get("discovered_obligations", [])
    if not isinstance(discoveries, list):
        return ["discovered_obligations must be a list"]
    for item in discoveries:
        if not isinstance(item, dict):
            errors.append("discovered obligation must be an object")
            continue
        cid = item.get("id")
        expected = {
            "source": item.get("source"),
            "source_anchor": item.get("source_anchor"),
            "criterion": item.get("criterion"),
            "blocking": item.get("blocking"),
            "required": item.get("required"),
        }
        if not isinstance(cid, str) or not cid or cid == "U0":
            errors.append("invalid discovered obligation ID")
            continue
        if expected["source"] != "R" or expected["blocking"] is not True or expected["required"] is not True:
            errors.append(f"{cid}: discovered blocking obligation must be source R and required/blocking true")
            continue
        if not isinstance(expected["source_anchor"], str) or not expected["source_anchor"]:
            errors.append(f"{cid}: source_anchor required")
            continue
        if not isinstance(expected["criterion"], str) or not expected["criterion"]:
            errors.append(f"{cid}: criterion required")
            continue
        existing = state["obligations"].get(cid)
        if existing is None:
            state["obligations"][cid] = {**expected, "history": []}
        else:
            for key, value in expected.items():
                if existing.get(key) != value:
                    errors.append(f"{cid}: attempted to replace preserved repository obligation")
                    break
    return errors


def final_reconcile(event: dict[str, Any], state: dict[str, Any]) -> tuple[Reconciliation, dict[str, Any]]:
    cwd = cwd_path(event)
    proposal_path, _, final_path = metadata_paths(cwd)
    proposal = load_json(proposal_path, {})
    if not isinstance(proposal, dict):
        proposal = {}
    admission_errors = admit_discovered(proposal, state)
    try:
        revision = workspace_digest(cwd)
    except OSError:
        revision = "DIGEST_ERROR"
    run_id = str(event_session_id(event) or state.get("session_key"))
    controller_state = {
        "run_id": run_id,
        "workspace_revision": revision,
        "obligations": state.get("obligations", {}),
        "current": proposal.get("current", {}),
        "receipts": state.get("receipts", {}),
        "user_events": state.get("user_events", []),
    }
    result = reconcile(controller_state)
    if admission_errors:
        result = Reconciliation("NO_VERIFIED_COMPLETION", tuple(sorted(set(result.errors + tuple(admission_errors)))), result.blocking)
    record = {
        "schema": "premium-v2.1-final-v1",
        "run_id": run_id,
        "session_id": event_session_id(event),
        "workspace_revision": revision,
        "phase": state.get("phase"),
        "builder_count": state.get("builder_count"),
        "takeover": state.get("takeover"),
        "requested_outcome": proposal.get("requested_outcome", "COMPLETE"),
        "outcome": result.outcome,
        "trusted_complete": result.trusted_complete,
        "errors": list(result.errors),
        "blocking": list(result.blocking),
    }
    state["final_record"] = record
    state["last_workspace_revision"] = revision
    atomic_json(final_path, record)
    return result, record


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"systemMessage": f"Premium v2.1 hook received invalid JSON: {exc}"}))
        return 0
    if not isinstance(event, dict):
        print("{}")
        return 0

    mode = os.environ.get("OTL_V2_1_HOOK_MODE", "audit").lower()
    state, state_path, events_path = ensure_state(event)
    append_event(events_path, event)
    event_name = str(event.get("hook_event_name") or "")
    output: dict[str, Any] = {}

    if event_name == "SessionStart":
        state["phase"] = "ROOT_INTAKE"
    elif event_name == "UserPromptSubmit":
        init_user_obligation(event, state)
    elif event_name == "PreToolUse":
        output = pre_tool_decision(event, state, mode)
    elif event_name == "PostToolUse":
        record_post_tool(event, state)
    elif event_name == "SubagentStart":
        if is_builder_event(event):
            state["builder_count"] = int(state.get("builder_count", 0)) + 1
            state["phase"] = "LUNA_MUTATING"
    elif event_name == "SubagentStop":
        if is_builder_event(event):
            state["phase"] = "ROOT_RECONCILE"
    elif event_name == "Stop":
        result, record = final_reconcile(event, state)
        requested = record.get("requested_outcome")
        if mode == "enforce" and requested == "COMPLETE" and result.outcome != "COMPLETE":
            if event.get("stop_hook_active") is not True and int(state.get("correction_count", 0)) < 1:
                state["correction_count"] = int(state.get("correction_count", 0)) + 1
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "Stop",
                        "decision": "block",
                        "reason": "Trusted Premium v2.1 controller outcome is not COMPLETE. Reconcile the existing obligations/evidence once without weakening scope or fabricating a waiver.",
                    }
                }

    save_state(state_path, state)
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
