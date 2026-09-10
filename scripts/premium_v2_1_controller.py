#!/usr/bin/env python3
"""Deterministic acceptance controller for the Premium v2.1 experiment.

This module intentionally proves only record consistency. It does not decide
whether extracted criteria are semantically complete or whether a test is
relevant to a requirement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

VALID_SOURCES = {"U", "R", "A"}
VALID_DISPOSITIONS = {
    "OPEN",
    "VERIFIED",
    "FAILED",
    "UNRESOLVED",
    "WAIVED_BY_USER",
}
TERMINAL_OUTCOMES = {
    "COMPLETE",
    "BLOCKED",
    "FAILED",
    "PARTIAL_WITH_USER_WAIVER",
    "NO_VERIFIED_COMPLETION",
}


@dataclass(frozen=True)
class Reconciliation:
    outcome: str
    errors: tuple[str, ...]
    blocking: tuple[str, ...]

    @property
    def trusted_complete(self) -> bool:
        return self.outcome == "COMPLETE"


def _require_mapping(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def _string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _authenticated_waivers(state: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    events = state.get("user_events", [])
    if not isinstance(events, list):
        return result
    for event in events:
        if not isinstance(event, dict):
            continue
        if (
            event.get("type") == "waiver"
            and event.get("authenticated") is True
            and isinstance(event.get("criterion_id"), str)
            and event.get("criterion_id")
        ):
            result.add(event["criterion_id"])
    return result


def _receipt_is_current(
    receipt: dict[str, Any],
    *,
    run_id: str,
    workspace_revision: str,
) -> tuple[bool, str]:
    if receipt.get("run_id") != run_id:
        return False, "receipt belongs to another run"
    if receipt.get("collection_status") != "COLLECTED":
        return False, "receipt did not collect the executable check"
    if receipt.get("result_class") != "PASS":
        return False, f"receipt result is {receipt.get('result_class')!r}, not PASS"
    if receipt.get("workspace_after") != workspace_revision:
        return False, "receipt is stale for the current workspace"
    if not _string(receipt.get("command_or_test_id")):
        return False, "receipt is missing command/test identity"
    if not _string(receipt.get("test_asset_identity")):
        return False, "receipt is missing test asset identity"
    if not _string(receipt.get("environment_identity")):
        return False, "receipt is missing environment identity"
    return True, ""


def reconcile(state: dict[str, Any]) -> Reconciliation:
    """Return the trusted controller outcome for a proposed terminal state."""

    errors: list[str] = []
    blockers: list[str] = []

    if not isinstance(state, dict):
        return Reconciliation(
            "NO_VERIFIED_COMPLETION",
            ("state must be an object",),
            (),
        )

    run_id = _string(state.get("run_id"))
    workspace_revision = _string(state.get("workspace_revision"))
    if not run_id:
        errors.append("run_id is required")
    if not workspace_revision:
        errors.append("workspace_revision is required")

    obligations = _require_mapping(state.get("obligations"), "obligations", errors)
    current = _require_mapping(state.get("current"), "current", errors)
    receipts = _require_mapping(state.get("receipts", {}), "receipts", errors)
    waivers = _authenticated_waivers(state)

    active_required_waiver = False
    saw_failed = False
    saw_open = False
    required_user_obligations = 0

    for criterion_id, obligation_value in obligations.items():
        if not isinstance(criterion_id, str) or not criterion_id:
            errors.append("obligation IDs must be non-empty strings")
            continue

        obligation = _require_mapping(
            obligation_value, f"obligation {criterion_id}", errors
        )
        source = obligation.get("source")
        criterion = obligation.get("criterion")
        source_anchor = obligation.get("source_anchor")
        blocking = obligation.get("blocking")
        required = obligation.get("required", blocking)
        history = obligation.get("history")

        if source not in VALID_SOURCES:
            errors.append(f"{criterion_id}: invalid authority source {source!r}")
        if not isinstance(criterion, str) or not criterion.strip():
            errors.append(f"{criterion_id}: original criterion content is required")
        if not isinstance(source_anchor, str) or not source_anchor.strip():
            errors.append(f"{criterion_id}: original source anchor is required")
        if not isinstance(history, list):
            errors.append(f"{criterion_id}: authority transition history must be a list")
        if _bool(blocking) is None:
            errors.append(f"{criterion_id}: blocking must be boolean")
        if _bool(required) is None:
            errors.append(f"{criterion_id}: required must be boolean")
        if source == "U" and required is True:
            required_user_obligations += 1

        row_value = current.get(criterion_id)
        if not isinstance(row_value, dict):
            if required is True:
                errors.append(f"{criterion_id}: required obligation is missing")
            continue
        row = row_value

        # Authority-bearing fields are immutable after capture. A model may echo
        # them, but any changed echo is an invalid transition.
        for key, expected in (
            ("source", source),
            ("criterion", criterion),
            ("blocking", blocking),
            ("required", required),
        ):
            if key in row and row.get(key) != expected:
                errors.append(
                    f"{criterion_id}: invalid authority transition for {key}: "
                    f"{expected!r} -> {row.get(key)!r}"
                )

        disposition = row.get("disposition")
        if disposition not in VALID_DISPOSITIONS:
            errors.append(f"{criterion_id}: invalid disposition {disposition!r}")
            continue

        if required is not True:
            # Non-required rows cannot independently grant completion.
            continue

        if disposition == "WAIVED_BY_USER":
            if criterion_id not in waivers:
                errors.append(f"{criterion_id}: waiver is not authenticated")
                continue
            active_required_waiver = True
            continue

        if disposition == "FAILED":
            saw_failed = True
            blockers.append(criterion_id)
            continue

        if disposition in {"OPEN", "UNRESOLVED"}:
            saw_open = True
            blockers.append(criterion_id)
            continue

        if disposition == "VERIFIED":
            evidence_refs = row.get("evidence_refs", [])
            if not isinstance(evidence_refs, list) or not all(
                isinstance(ref, str) and ref for ref in evidence_refs
            ):
                errors.append(f"{criterion_id}: evidence_refs must be string IDs")
                continue

            for receipt_id in evidence_refs:
                receipt_value = receipts.get(receipt_id)
                if not isinstance(receipt_value, dict):
                    errors.append(
                        f"{criterion_id}: missing executable receipt {receipt_id!r}"
                    )
                    continue
                ok, reason = _receipt_is_current(
                    receipt_value,
                    run_id=run_id,
                    workspace_revision=workspace_revision,
                )
                if not ok:
                    errors.append(
                        f"{criterion_id}: invalid receipt {receipt_id!r}: {reason}"
                    )

    if required_user_obligations == 0:
        errors.append("at least one required user obligation must be captured")

    # Current rows must not smuggle in a replacement for a captured ID through
    # duplicate-looking unknown IDs. Unknown annotations are allowed only when
    # explicitly non-required.
    for criterion_id, row_value in current.items():
        if criterion_id in obligations:
            continue
        if not isinstance(row_value, dict):
            errors.append(f"{criterion_id}: unknown criterion row must be an object")
            continue
        if row_value.get("blocking") is True or row_value.get("required") is True:
            errors.append(
                f"{criterion_id}: new required/blocking criterion lacks "
                "controller-owned authority capture"
            )

    if errors:
        return Reconciliation(
            "NO_VERIFIED_COMPLETION",
            tuple(sorted(set(errors))),
            tuple(sorted(set(blockers))),
        )

    if saw_failed:
        return Reconciliation(
            "FAILED",
            (),
            tuple(sorted(set(blockers))),
        )

    if saw_open:
        return Reconciliation(
            "BLOCKED",
            (),
            tuple(sorted(set(blockers))),
        )

    if active_required_waiver:
        return Reconciliation(
            "PARTIAL_WITH_USER_WAIVER",
            (),
            (),
        )

    return Reconciliation("COMPLETE", (), ())


def workspace_digest(
    root: Path,
    *,
    exclude_names: Iterable[str] = (".git",),
) -> str:
    """Hash relevant worktree bytes, symlink targets, paths, and executable bits."""

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


def stop_hook_response(
    state: dict[str, Any],
    hook_input: dict[str, Any],
) -> dict[str, Any]:
    """Produce VS Code-compatible Stop-hook output.

    A first invalid COMPLETE request gets one correction continuation. A second
    attempt is allowed to stop, but the controller remains
    NO_VERIFIED_COMPLETION/BLOCKED/FAILED rather than manufacturing COMPLETE.
    """

    result = reconcile(state)
    requested = state.get("requested_outcome", "COMPLETE")
    already_continued = hook_input.get("stop_hook_active") is True
    correction_count = state.get("correction_count", 0)
    if not isinstance(correction_count, int) or correction_count < 0:
        correction_count = 0

    if requested != "COMPLETE":
        return {}

    if result.outcome == "COMPLETE":
        return {}

    if not already_continued and correction_count < 1:
        reason_parts = [
            f"Trusted controller outcome is {result.outcome}, not COMPLETE."
        ]
        if result.errors:
            reason_parts.append("Record errors: " + "; ".join(result.errors[:6]))
        if result.blocking:
            reason_parts.append(
                "Blocking criteria: " + ", ".join(result.blocking[:10])
            )
        reason_parts.append(
            "Reconcile the existing criterion register and evidence once. "
            "Do not invent a waiver or drop/narrow an obligation."
        )
        return {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "decision": "block",
                "reason": " ".join(reason_parts),
            }
        }

    # The platform may still show model prose. Empty hook output merely allows
    # termination; the trusted controller outcome remains non-COMPLETE.
    return {}


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected top-level JSON object")
    return value


def _cmd_reconcile(args: argparse.Namespace) -> int:
    result = reconcile(_load_json(Path(args.state)))
    print(
        json.dumps(
            {
                "outcome": result.outcome,
                "trusted_complete": result.trusted_complete,
                "errors": list(result.errors),
                "blocking": list(result.blocking),
            },
            sort_keys=True,
        )
    )
    return 0 if result.outcome in TERMINAL_OUTCOMES else 2


def _cmd_digest(args: argparse.Namespace) -> int:
    print(workspace_digest(Path(args.workspace)))
    return 0


def _cmd_stop_hook(args: argparse.Namespace) -> int:
    state = _load_json(Path(args.state))
    hook_input = json.load(sys.stdin)
    if not isinstance(hook_input, dict):
        raise ValueError("hook input must be a JSON object")
    print(json.dumps(stop_hook_response(state, hook_input), sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    reconcile_parser = sub.add_parser("reconcile")
    reconcile_parser.add_argument("--state", required=True)
    reconcile_parser.set_defaults(func=_cmd_reconcile)

    digest_parser = sub.add_parser("digest")
    digest_parser.add_argument("workspace")
    digest_parser.set_defaults(func=_cmd_digest)

    hook_parser = sub.add_parser("stop-hook")
    hook_parser.add_argument("--state", required=True)
    hook_parser.set_defaults(func=_cmd_stop_hook)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
