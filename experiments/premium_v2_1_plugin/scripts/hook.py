#!/usr/bin/env python3
"""Plugin lifecycle hook for the Premium v2.1 minimal cascade.

Default mode is audit: record real hook schemas and controller outcomes without
forcing extra AI turns. Set OTL_V2_1_HOOK_MODE=enforce after schema calibration.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
import platform
import re
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from controller import Reconciliation, atomic_json, reconcile, workspace_digest  # noqa: E402

BUILDER_NAME = "Premium v2.1 Luna Builder"
META_DIR = ".otl-v2-1"
VALID_PHASES = {
    "ROOT_INTAKE",
    "LUNA_DISPATCHED",
    "LUNA_MUTATING",
    "ROOT_RECONCILE",
    "TERRA_TAKEOVER",
}
TERMINAL_RECONCILABLE_PHASES = {"ROOT_RECONCILE", "TERRA_TAKEOVER"}


def first_value(event: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in event and event.get(name) is not None:
            return event.get(name)
    return None


def nonnegative_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 0:
        return value
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


@contextmanager
def state_lock(state_path: Path, timeout_seconds: float = 5.0):
    """Serialize hook state updates with a cross-platform lock file."""
    lock_path = state_path.with_name(state_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
                if age > 30:
                    lock_path.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= deadline:
                raise TimeoutError(f"controller state lock timeout: {lock_path}")
            time.sleep(0.05)
            continue
        else:
            try:
                os.write(fd, f"{os.getpid()} {time.time()}\n".encode("ascii"))
            finally:
                os.close(fd)
            break
    try:
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def trusted_run_id(event: dict[str, Any], state: dict[str, Any]) -> str:
    observed = event_session_id(event)
    if isinstance(observed, str) and observed:
        return observed
    prior = state.get("session_id_observed")
    if isinstance(prior, str) and prior:
        return prior
    return str(state.get("session_key") or "")


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
            "session_start_count": 0,
            "builder_count": 0,
            "builder_invocation_seen": False,
            "builder_dispatch_count": 0,
            "builder_tool_use_id": None,
            "builder_agent_tool_completion_seen": False,
            "takeover": False,
            "takeover_basis_ids": [],
            "obligations": {},
            "receipts": {},
            "user_events": [],
            "user_prompt_count": 0,
            "control_errors": [],
            "correction_count": 0,
        }
    return state, state_path, events_path


def handle_session_start(event: dict[str, Any], state: dict[str, Any]) -> None:
    start_count = nonnegative_int(state.get("session_start_count", 0))
    builder_count = nonnegative_int(state.get("builder_count", 0))
    prompt_count = nonnegative_int(state.get("user_prompt_count", 0))
    if start_count is None or builder_count is None or prompt_count is None:
        append_control_errors(
            state,
            ["malformed lifecycle counter in controller state"],
            event=event,
        )
        return

    state["session_start_count"] = start_count + 1
    prior_activity = (
        start_count > 0
        or bool(state.get("obligations"))
        or state.get("builder_invocation_seen") is True
        or builder_count > 0
        or prompt_count > 0
    )
    if prior_activity:
        append_control_errors(
            state,
            ["repeated/resumed SessionStart is unsupported in Premium v2.1 single-mission mode"],
            event=event,
        )
        return
    state["phase"] = "ROOT_INTAKE"


def save_state(path: Path, state: dict[str, Any]) -> None:
    atomic_json(path, state)


def init_user_obligation(event: dict[str, Any], state: dict[str, Any]) -> None:
    count = state.get("user_prompt_count", 0)
    if not isinstance(count, int) or count < 0:
        count = 0
    count += 1
    state["user_prompt_count"] = count
    if count > 1:
        append_control_errors(
            state,
            ["multiple UserPromptSubmit events are unsupported in Premium v2.1 single-mission mode"],
            event=event,
        )

    prompt = event.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        append_control_errors(
            state,
            ["UserPromptSubmit did not expose a non-empty prompt"],
            event=event,
        )
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


def is_builder_agent_tool(event: dict[str, Any]) -> bool:
    if not is_agent_tool(event):
        return False
    if is_builder_event(event):
        return True
    data = json.dumps(event_tool_input(event), sort_keys=True, default=str).lower()
    return BUILDER_NAME.lower() in data


def metadata_target_paths(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in {"path", "file", "file_path", "filepath", "target", "uri"}:
                if isinstance(child, str) and child.strip():
                    paths.append(child.strip())
            paths.extend(metadata_target_paths(child))
    elif isinstance(value, list):
        for child in value:
            paths.extend(metadata_target_paths(child))
    return paths


def is_metadata_only(event: dict[str, Any]) -> bool:
    # Never exempt command/search tools merely because their arguments mention
    # the metadata directory. Only path-targeted file operations can be
    # metadata-only; false negatives conservatively count as Terra takeover.
    name = event_tool_name(event).lower()
    if any(token in name for token in ("execute", "bash", "shell", "terminal", "command", "search", "glob", "rg")):
        return False
    paths = metadata_target_paths(event_tool_input(event))
    if not paths:
        return False

    metadata_root = (cwd_path(event) / META_DIR).resolve()
    for raw in paths:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = cwd_path(event) / candidate
        try:
            resolved = candidate.resolve()
            resolved.relative_to(metadata_root)
        except (OSError, ValueError):
            return False
    return True


def takeover_blocking_ids(event: dict[str, Any], state: dict[str, Any]) -> list[str]:
    """Return captured required criteria that explicitly justify Terra takeover.

    This is a consistency gate, not a semantic classifier. It only proves that
    the model-editable proposal left a captured required criterion FAILED or
    UNRESOLVED; it cannot prove that the residual is repository-local rather
    than infrastructure-only.
    """
    proposal_path, _, _ = metadata_paths(cwd_path(event))
    proposal = load_json(proposal_path, {})
    if not isinstance(proposal, dict):
        return []
    current = proposal.get("current")
    obligations = state.get("obligations")
    if not isinstance(current, dict) or not isinstance(obligations, dict):
        return []

    ids: list[str] = []
    for cid, obligation in obligations.items():
        if not isinstance(cid, str) or not isinstance(obligation, dict):
            continue
        if obligation.get("required") is not True or obligation.get("blocking") is not True:
            continue
        row = current.get(cid)
        if not isinstance(row, dict):
            continue
        if row.get("disposition") in {"FAILED", "UNRESOLVED"}:
            ids.append(cid)
    return sorted(ids)


def validate_event_context(event: dict[str, Any], state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    phase = state.get("phase")
    if phase not in VALID_PHASES:
        errors.append(f"invalid controller phase: {phase!r}")

    bound_cwd = state.get("cwd")
    if not isinstance(bound_cwd, str) or not bound_cwd:
        errors.append("controller workspace binding is missing")
    else:
        try:
            expected = Path(bound_cwd).expanduser().resolve()
            observed = cwd_path(event)
        except OSError as exc:
            errors.append(f"workspace binding could not be resolved: {exc}")
        else:
            if observed != expected:
                errors.append(
                    f"hook cwd drifted from bound workspace: expected={expected} observed={observed}"
                )
    append_control_errors(state, errors, event=event)
    return errors


def observe_pre_tool_phase(event: dict[str, Any], state: dict[str, Any]) -> list[str]:
    """Record routing attempts independently of enforce-mode decisions."""
    errors: list[str] = []
    phase = state.get("phase")
    agent_tool = is_agent_tool(event)
    builder_tool = is_builder_agent_tool(event)

    if agent_tool:
        if not builder_tool:
            errors.append("non-Builder subagent dispatch attempted")
        else:
            count = nonnegative_int(state.get("builder_dispatch_count", 0))
            if count is None:
                errors.append("malformed builder_dispatch_count in controller state")
            else:
                count += 1
                state["builder_dispatch_count"] = count
                if count == 1:
                    state["builder_tool_use_id"] = first_value(
                        event, "tool_use_id", "toolUseId"
                    )
                else:
                    errors.append("more than one Luna Builder dispatch attempted")
    elif phase == "ROOT_INTAKE":
        errors.append("repository/tool dispatch attempted before Builder ownership")
    elif phase in {"LUNA_DISPATCHED", "LUNA_MUTATING"}:
        # Root should not be issuing tools while the child owns mutation. Hook
        # payloads from the child share the session, so only record this when
        # runtime evidence identifies the current event as root-owned later.
        # The first live trace calibrates whether such ownership is observable.
        pass
    elif phase == "ROOT_RECONCILE" and not is_metadata_only(event):
        # A direct root repository tool is not necessarily a violation; it may
        # be the authorized Terra takeover and is adjudicated by the takeover
        # gate in pre_tool_decision / observe_post_tool_phase.
        pass

    append_control_errors(state, errors, event=event)
    return errors


def expected_builder_agent_completion(
    event: dict[str, Any], state: dict[str, Any]
) -> bool:
    if not is_builder_agent_tool(event):
        return False
    if state.get("builder_agent_tool_completion_seen") is True:
        return False
    if nonnegative_int(state.get("builder_dispatch_count", 0)) != 1:
        return False
    if nonnegative_int(state.get("builder_count", 0)) != 1:
        return False
    if state.get("phase") != "ROOT_RECONCILE":
        return False

    expected_id = state.get("builder_tool_use_id")
    observed_id = first_value(event, "tool_use_id", "toolUseId")
    if isinstance(expected_id, str) and expected_id:
        if not isinstance(observed_id, str) or observed_id != expected_id:
            return False
    return True


def _deny_pre_tool(reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def pre_tool_decision(event: dict[str, Any], state: dict[str, Any], mode: str) -> dict[str, Any]:
    if mode != "enforce":
        return {}
    phase = state.get("phase")
    if phase not in VALID_PHASES:
        return _deny_pre_tool(
            f"Premium v2.1 controller phase is invalid ({phase!r}); refusing untracked execution."
        )
    agent_tool = is_agent_tool(event)
    builder_tool = is_builder_agent_tool(event)
    metadata_only = is_metadata_only(event)
    builder_count = nonnegative_int(state.get("builder_count", 0))
    builder_seen = state.get("builder_invocation_seen", False)
    if builder_count is None or not isinstance(builder_seen, bool):
        return _deny_pre_tool(
            "Premium v2.1 controller lifecycle state is malformed; refusing untracked execution."
        )

    if phase == "ROOT_INTAKE":
        if not agent_tool:
            return _deny_pre_tool(
                "Premium v2.1 bounded intake permits only the single Luna Builder invocation before repository work."
            )
        if not builder_tool:
            return _deny_pre_tool(
                "Premium v2.1 bounded intake permits only Premium v2.1 Luna Builder as the first and only subagent."
            )
        if builder_seen is True or builder_count >= 1:
            return _deny_pre_tool(
                "Premium v2.1 permits exactly one Luna Builder invocation."
            )
        # Mark dispatch at PreToolUse so a missing SubagentStart event cannot
        # silently authorize a second child invocation.
        state["builder_invocation_seen"] = True
        state["phase"] = "LUNA_DISPATCHED"
        return {}

    if agent_tool:
        return _deny_pre_tool(
            "Premium v2.1 permits exactly one Luna Builder invocation and no later subagent call."
        )

    if phase == "ROOT_RECONCILE" and not metadata_only:
        blocking_ids = takeover_blocking_ids(event, state)
        if not blocking_ids:
            return _deny_pre_tool(
                "Premium v2.1 Terra takeover requires a captured blocking criterion "
                "left FAILED or UNRESOLVED by the Luna attempt."
            )
        state["phase"] = "TERRA_TAKEOVER"
        state["takeover"] = True
        state["takeover_basis_ids"] = blocking_ids
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


def execution_command(event: dict[str, Any]) -> str | None:
    tool_input = event_tool_input(event)
    if not isinstance(tool_input, dict):
        return None
    for key in ("command", "cmd", "script"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def is_execution_tool(event: dict[str, Any]) -> bool:
    command = execution_command(event)
    if command is None:
        return False
    name = event_tool_name(event).lower()
    return any(
        token in name
        for token in (
            "execute",
            "terminal",
            "shell",
            "bash",
            "command",
            "powershell",
            "test",
        )
    )


def command_identity(event: dict[str, Any]) -> str:
    command = execution_command(event)
    if command is not None:
        return command[:500]
    tool_input = event_tool_input(event)
    return f"{event_tool_name(event) or 'tool'}:{hashlib.sha256(json.dumps(tool_input, sort_keys=True, default=str).encode()).hexdigest()[:16]}"


def observe_post_tool_phase(event: dict[str, Any], state: dict[str, Any]) -> list[str]:
    """Persist phase violations even if PreToolUse enforcement was bypassed.

    Command-hook timeouts can be fail-open on supported runtimes. PostToolUse is
    therefore a defense-in-depth signal: it cannot prevent the already executed
    call, but it can ensure the run never becomes trusted COMPLETE unnoticed.
    """
    phase = state.get("phase")
    agent_tool = is_agent_tool(event)
    metadata_only = is_metadata_only(event)
    errors: list[str] = []

    if agent_tool and expected_builder_agent_completion(event, state):
        state["builder_agent_tool_completion_seen"] = True
    elif phase in {"ROOT_INTAKE", "LUNA_DISPATCHED"}:
        if agent_tool:
            # A completed agent call without an observed Builder lifecycle is
            # caught here and again by final lifecycle cardinality checks.
            errors.append(
                f"agent tool completed before an observed Builder lifecycle: phase={phase!r}"
            )
        else:
            errors.append(
                f"repository/tool work completed before Builder ownership: phase={phase!r}"
            )
    elif phase == "ROOT_RECONCILE":
        if agent_tool:
            errors.append("unexpected subagent tool completed after the single Builder attempt")
        elif not metadata_only:
            blocking_ids = takeover_blocking_ids(event, state)
            if not blocking_ids:
                errors.append(
                    "Terra repository work completed without a captured FAILED/UNRESOLVED blocking criterion"
                )
            else:
                state["phase"] = "TERRA_TAKEOVER"
                state["takeover"] = True
                state["takeover_basis_ids"] = blocking_ids
    elif phase == "TERRA_TAKEOVER" and agent_tool:
        errors.append("subagent tool completed during Terra takeover")
    elif phase not in VALID_PHASES:
        errors.append(f"tool completed while controller phase was invalid: {phase!r}")

    append_control_errors(state, errors, event=event)
    return errors


def record_post_tool(event: dict[str, Any], state: dict[str, Any]) -> None:
    cwd = cwd_path(event)
    try:
        revision = workspace_digest(cwd)
    except OSError:
        revision = "DIGEST_ERROR"
    response = event_tool_result(event)
    execution_eligible = is_execution_tool(event)
    exit_code = recursive_exit_code(response) if execution_eligible else None
    receipt_id = f"E{len(state.get('receipts', {})) + 1}"
    receipt = {
        "run_id": trusted_run_id(event, state),
        "tool_use_id": first_value(event, "tool_use_id", "toolUseId"),
        "tool_name": event_tool_name(event),
        "command_or_test_id": command_identity(event),
        "execution_eligible": execution_eligible,
        "collection_status": "COLLECTED" if execution_eligible and exit_code is not None else "OBSERVED",
        "result_class": "PASS" if execution_eligible and exit_code == 0 else ("ASSERTION_FAIL" if execution_eligible and isinstance(exit_code, int) else "UNCLASSIFIED"),
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
                    "execution_eligible": r.get("execution_eligible"),
                    "collection_status": r.get("collection_status"),
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


def append_control_errors(
    state: dict[str, Any],
    errors: list[str],
    *,
    event: dict[str, Any] | None = None,
) -> None:
    if not errors:
        return
    records = state.setdefault("control_errors", [])
    if not isinstance(records, list):
        records = []
        state["control_errors"] = records
    event_name = (
        str(first_value(event or {}, "hook_event_name", "hookEventName", "event_name", "eventName") or "")
        if event is not None
        else ""
    )
    for error in errors:
        record = {
            "error": error,
            "hook_event_name": event_name,
            "tool_use_id": first_value(event or {}, "tool_use_id", "toolUseId"),
        }
        if record not in records:
            records.append(record)


def sync_proposal_authority(event: dict[str, Any], state: dict[str, Any]) -> list[str]:
    """Capture repository-derived obligations as soon as they become observable.

    Once an R obligation appears in the model-editable proposal, it is copied
    into controller-owned external state. Later deletion from the proposal does
    not delete the captured obligation.
    """
    proposal_path, _, _ = metadata_paths(cwd_path(event))
    proposal = load_json(proposal_path, {})
    if not isinstance(proposal, dict):
        errors = ["controller proposal must be an object"]
        append_control_errors(state, errors, event=event)
        return errors
    errors = admit_discovered(proposal, state)
    append_control_errors(state, errors, event=event)
    return errors


def noncomplete_visibility_output(result: Reconciliation) -> dict[str, Any]:
    if result.outcome == "COMPLETE":
        return {}
    return {
        "systemMessage": (
            f"Premium v2.1 trusted controller outcome: {result.outcome}. "
            "The agent's final prose is not a trusted completion signal."
        )
    }


def final_reconcile(event: dict[str, Any], state: dict[str, Any]) -> tuple[Reconciliation, dict[str, Any]]:
    cwd = cwd_path(event)
    proposal_path, _, final_path = metadata_paths(cwd)
    proposal = load_json(proposal_path, {})
    if not isinstance(proposal, dict):
        proposal = {}
    admission_errors = admit_discovered(proposal, state)
    persisted = state.get("control_errors", [])
    if isinstance(persisted, list):
        admission_errors.extend(
            str(item.get("error"))
            for item in persisted
            if isinstance(item, dict) and isinstance(item.get("error"), str)
        )
    try:
        revision = workspace_digest(cwd)
    except OSError:
        revision = "DIGEST_ERROR"
    run_id = trusted_run_id(event, state)
    controller_state = {
        "run_id": run_id,
        "workspace_revision": revision,
        "obligations": state.get("obligations", {}),
        "current": proposal.get("current", {}),
        "receipts": state.get("receipts", {}),
        "user_events": state.get("user_events", []),
    }
    result = reconcile(controller_state)
    session_start_count = nonnegative_int(state.get("session_start_count", 0))
    if session_start_count != 1:
        admission_errors.append(
            f"exactly one SessionStart required; observed {state.get('session_start_count', 0)!r}"
        )
    user_prompt_count = nonnegative_int(state.get("user_prompt_count", 0))
    if user_prompt_count != 1:
        admission_errors.append(
            f"exactly one UserPromptSubmit required; observed {state.get('user_prompt_count', 0)!r}"
        )
    builder_dispatch_count = nonnegative_int(state.get("builder_dispatch_count", 0))
    if builder_dispatch_count != 1:
        admission_errors.append(
            "exactly one Luna Builder dispatch required; "
            f"observed {state.get('builder_dispatch_count', 0)!r}"
        )
    builder_count = nonnegative_int(state.get("builder_count", 0))
    if builder_count != 1:
        admission_errors.append(
            f"exactly one Luna Builder start required; observed {state.get('builder_count', 0)!r}"
        )
    phase = state.get("phase")
    if phase not in TERMINAL_RECONCILABLE_PHASES:
        admission_errors.append(
            f"final reconciliation requires a terminal-reconcilable phase; observed {phase!r}"
        )
    if state.get("weak_session_key") is True:
        admission_errors.append("session_id not observed; trusted completion unavailable")
    if admission_errors:
        result = Reconciliation("NO_VERIFIED_COMPLETION", tuple(sorted(set(result.errors + tuple(admission_errors)))), result.blocking)
    record = {
        "schema": "premium-v2.1-final-v1",
        "run_id": run_id,
        "session_id": event_session_id(event),
        "workspace_revision": revision,
        "phase": state.get("phase"),
        "session_start_count": state.get("session_start_count"),
        "user_prompt_count": state.get("user_prompt_count"),
        "builder_dispatch_count": state.get("builder_dispatch_count"),
        "builder_count": state.get("builder_count"),
        "builder_agent_tool_completion_seen": state.get("builder_agent_tool_completion_seen"),
        "takeover": state.get("takeover"),
        "takeover_basis_ids": state.get("takeover_basis_ids", []),
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
    mode = os.environ.get("OTL_V2_1_HOOK_MODE", "audit").lower()
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        if mode == "enforce":
            print(
                json.dumps(
                    {
                        "continue": False,
                        "stopReason": "Premium v2.1 received malformed hook input; refusing untracked execution.",
                        "systemMessage": f"JSONDecodeError: {exc}",
                    },
                    sort_keys=True,
                )
            )
        else:
            print(json.dumps({"systemMessage": f"Premium v2.1 hook received invalid JSON: {exc}"}))
        return 0
    if not isinstance(event, dict):
        if mode == "enforce":
            print(
                json.dumps(
                    {
                        "continue": False,
                        "stopReason": "Premium v2.1 received non-object hook input; refusing untracked execution.",
                    },
                    sort_keys=True,
                )
            )
        else:
            print("{}")
        return 0

    output: dict[str, Any] = {}
    state_path, _, _, _ = session_paths(event)
    try:
        with state_lock(state_path):
            state, state_path, events_path = ensure_state(event)
            append_event(events_path, event)
            event_name = str(first_value(event, "hook_event_name", "hookEventName", "event_name", "eventName") or "")
            context_errors = validate_event_context(event, state)
            if mode == "enforce" and context_errors:
                output = {
                    "continue": False,
                    "stopReason": "Premium v2.1 runtime context drifted or is malformed; refusing untracked execution.",
                    "systemMessage": "; ".join(context_errors),
                }
            elif event_name in {"SessionStart", "sessionStart"}:
                handle_session_start(event, state)
            elif event_name in {"UserPromptSubmit", "userPromptSubmit", "userPromptSubmitted"}:
                init_user_obligation(event, state)
            elif event_name in {"PreToolUse", "preToolUse"}:
                observe_pre_tool_phase(event, state)
                output = pre_tool_decision(event, state, mode)
            elif event_name in {"PostToolUse", "postToolUse"}:
                observe_post_tool_phase(event, state)
                record_post_tool(event, state)
                sync_proposal_authority(event, state)
            elif event_name in {"SubagentStart", "subagentStart"}:
                if is_builder_event(event):
                    state["builder_invocation_seen"] = True
                    count = nonnegative_int(state.get("builder_count", 0))
                    if count is None:
                        append_control_errors(
                            state,
                            ["malformed builder_count in controller state"],
                            event=event,
                        )
                    else:
                        state["builder_count"] = count + 1
                    state["phase"] = "LUNA_MUTATING"
                else:
                    append_control_errors(
                        state,
                        ["unexpected non-Builder subagent started"],
                        event=event,
                    )
            elif event_name in {"SubagentStop", "subagentStop"}:
                if is_builder_event(event):
                    state["phase"] = "ROOT_RECONCILE"
                else:
                    append_control_errors(
                        state,
                        ["unexpected non-Builder subagent stopped"],
                        event=event,
                    )
            elif event_name in {"Stop", "agentStop", "stop"}:
                result, record = final_reconcile(event, state)
                requested = record.get("requested_outcome")
                if mode == "enforce" and requested == "COMPLETE" and result.outcome != "COMPLETE":
                    stop_active = first_value(event, "stop_hook_active", "stopHookActive") is True
                    correction_count = nonnegative_int(state.get("correction_count", 0))
                    if correction_count is None:
                        append_control_errors(
                            state,
                            ["malformed correction_count in controller state"],
                            event=event,
                        )
                        output = {
                            "continue": False,
                            "stopReason": "Premium v2.1 controller state is malformed; refusing trusted completion.",
                        }
                    elif not stop_active and correction_count < 1:
                        state["correction_count"] = correction_count + 1
                        output = {
                            "hookSpecificOutput": {
                                "hookEventName": "Stop",
                                "decision": "block",
                                "reason": "Trusted Premium v2.1 controller outcome is not COMPLETE. Reconcile the existing obligations/evidence once without weakening scope or fabricating a waiver.",
                            }
                        }
                if mode == "enforce" and not output:
                    output = noncomplete_visibility_output(result)
            else:
                append_control_errors(
                    state,
                    [f"unrecognized hook event name: {event_name!r}"],
                    event=event,
                )
                if mode == "enforce":
                    output = {
                        "continue": False,
                        "stopReason": "Premium v2.1 received an unrecognized hook event; refusing untracked execution.",
                        "systemMessage": f"unrecognized hook event name: {event_name!r}",
                    }
                else:
                    output = {
                        "systemMessage": (
                            "Premium v2.1 audit trace includes an unrecognized hook event: "
                            f"{event_name!r}"
                        )
                    }

            save_state(state_path, state)
    except TimeoutError as exc:
        if mode == "enforce":
            output = {
                "continue": False,
                "stopReason": "Premium v2.1 controller state lock unavailable; refusing untracked execution.",
                "systemMessage": str(exc),
            }
        else:
            output = {
                "systemMessage": "Premium v2.1 audit trace incomplete because controller state lock was unavailable."
            }
    except Exception as exc:
        if mode == "enforce":
            output = {
                "continue": False,
                "stopReason": "Premium v2.1 controller hook failed; refusing untracked execution.",
                "systemMessage": f"{type(exc).__name__}: {exc}",
            }
        else:
            output = {
                "systemMessage": (
                    "Premium v2.1 audit trace is incomplete because the hook adapter "
                    f"failed: {type(exc).__name__}: {exc}"
                )
            }

    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
