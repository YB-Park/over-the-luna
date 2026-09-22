#!/usr/bin/env python3
"""Deterministic record-consistency controller for Premium v2.1.

This controller does not prove semantic correctness. It preserves captured
obligations, authenticates runtime receipts, and refuses trusted completion when
recorded blocking state is unresolved, stale, or authority-laundered.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

VALID_DISPOSITIONS = {"OPEN", "VERIFIED", "FAILED", "UNRESOLVED", "WAIVED_BY_USER"}
INVALID_WORKSPACE_REVISIONS = {"DIGEST_ERROR"}


@dataclass(frozen=True)
class Reconciliation:
    outcome: str
    errors: tuple[str, ...]
    blocking: tuple[str, ...]

    @property
    def trusted_complete(self) -> bool:
        return self.outcome == "COMPLETE"


def workspace_digest(root: Path, exclude_names: Iterable[str] = (".git", ".otl-v2-1")) -> str:
    root = root.resolve()
    excluded = set(exclude_names)
    h = hashlib.sha256()
    entries: list[Path] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part in excluded for part in rel.parts):
            continue
        entries.append(path)
    for path in sorted(entries, key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        executable = bool(info.st_mode & stat.S_IXUSR)
        if path.is_symlink():
            kind, payload = "L", os.readlink(path).encode("utf-8", "surrogateescape")
        elif path.is_file():
            kind, payload = "F", path.read_bytes()
        elif path.is_dir():
            kind, payload = "D", b""
        else:
            kind, payload = "O", b""
        h.update(kind.encode())
        h.update(b"\0")
        h.update(rel.encode("utf-8", "surrogateescape"))
        h.update(b"\0")
        h.update(b"x" if executable else b"-")
        h.update(b"\0")
        h.update(hashlib.sha256(payload).digest())
    return h.hexdigest()


def _valid_receipt(receipt: dict[str, Any], run_id: str, revision: str) -> tuple[bool, str]:
    if revision in INVALID_WORKSPACE_REVISIONS:
        return False, "workspace revision is unavailable"
    if receipt.get("workspace_after") in INVALID_WORKSPACE_REVISIONS:
        return False, "receipt workspace revision is unavailable"
    if receipt.get("execution_eligible") is not True:
        return False, "receipt is not from an execution tool"
    if receipt.get("run_id") != run_id:
        return False, "wrong run"
    if receipt.get("collection_status") != "COLLECTED":
        return False, "check was not collected"
    if receipt.get("result_class") != "PASS":
        return False, f"result is {receipt.get('result_class')!r}"
    if receipt.get("workspace_after") != revision:
        return False, "stale workspace receipt"
    if not receipt.get("command_or_test_id"):
        return False, "missing command identity"
    if not receipt.get("test_asset_identity"):
        return False, "missing test asset identity"
    if not receipt.get("environment_identity"):
        return False, "missing environment identity"
    return True, ""


def reconcile(state: dict[str, Any]) -> Reconciliation:
    errors: list[str] = []
    blockers: list[str] = []
    if not isinstance(state, dict):
        return Reconciliation(
            "NO_VERIFIED_COMPLETION",
            ("state must be an object",),
            (),
        )
    run_id = state.get("run_id")
    revision = state.get("workspace_revision")
    obligations = state.get("obligations")
    current = state.get("current")
    receipts = state.get("receipts", {})
    waivers = {
        e.get("criterion_id")
        for e in state.get("user_events", [])
        if isinstance(e, dict) and e.get("type") == "waiver" and e.get("authenticated") is True
    }
    if not isinstance(run_id, str) or not run_id:
        errors.append("run_id required")
    if not isinstance(revision, str) or not revision:
        errors.append("workspace_revision required")
    elif revision in INVALID_WORKSPACE_REVISIONS:
        errors.append("workspace_revision unavailable")
    if not isinstance(obligations, dict):
        obligations = {}
        errors.append("obligations must be an object")
    if not isinstance(current, dict):
        current = {}
        errors.append("current must be an object")
    if not isinstance(receipts, dict):
        receipts = {}
        errors.append("receipts must be an object")

    required_u = 0
    any_waiver = False
    any_failed = False
    any_open = False

    for cid, obligation in obligations.items():
        if not isinstance(cid, str) or not cid or not isinstance(obligation, dict):
            errors.append("invalid obligation record")
            continue
        source = obligation.get("source")
        criterion = obligation.get("criterion")
        anchor = obligation.get("source_anchor")
        blocking = obligation.get("blocking")
        required = obligation.get("required")
        history = obligation.get("history")
        if source not in {"U", "R", "A"}:
            errors.append(f"{cid}: invalid source")
        if not isinstance(criterion, str) or not criterion.strip():
            errors.append(f"{cid}: criterion required")
        if not isinstance(anchor, str) or not anchor.strip():
            errors.append(f"{cid}: source anchor required")
        if not isinstance(blocking, bool) or not isinstance(required, bool):
            errors.append(f"{cid}: blocking/required must be boolean")
        if not isinstance(history, list):
            errors.append(f"{cid}: history must be a list")
        if source == "U" and required is True:
            required_u += 1

        row = current.get(cid)
        if not isinstance(row, dict):
            if required is True:
                errors.append(f"{cid}: required obligation missing from current state")
            continue
        for key, expected in (("source", source), ("criterion", criterion), ("blocking", blocking), ("required", required)):
            if key in row and row.get(key) != expected:
                errors.append(f"{cid}: invalid authority transition for {key}")
        disposition = row.get("disposition")
        if disposition not in VALID_DISPOSITIONS:
            errors.append(f"{cid}: invalid disposition")
            continue
        if required is not True:
            continue
        if disposition == "WAIVED_BY_USER":
            if cid not in waivers:
                errors.append(f"{cid}: unauthenticated waiver")
            else:
                any_waiver = True
            continue
        if disposition == "FAILED":
            any_failed = True
            blockers.append(cid)
            continue
        if disposition in {"OPEN", "UNRESOLVED"}:
            any_open = True
            blockers.append(cid)
            continue
        refs = row.get("evidence_refs", [])
        if (
            not isinstance(refs, list)
            or not refs
            or not all(isinstance(rid, str) and rid for rid in refs)
        ):
            errors.append(f"{cid}: VERIFIED requires evidence_refs as non-empty string IDs")
            continue
        for rid in refs:
            receipt = receipts.get(rid)
            if not isinstance(receipt, dict):
                errors.append(f"{cid}: missing receipt {rid!r}")
                continue
            ok, reason = _valid_receipt(receipt, str(run_id), str(revision))
            if not ok:
                errors.append(f"{cid}: invalid receipt {rid!r}: {reason}")

    if required_u == 0:
        errors.append("at least one required user obligation must be captured")
    for cid, row in current.items():
        if cid in obligations:
            continue
        if not isinstance(row, dict):
            errors.append(f"{cid}: unknown criterion row must be an object")
            continue
        if row.get("blocking") is True or row.get("required") is True:
            errors.append(f"{cid}: required row lacks controller-owned authority capture")

    if errors:
        return Reconciliation("NO_VERIFIED_COMPLETION", tuple(sorted(set(errors))), tuple(sorted(set(blockers))))
    if any_failed:
        return Reconciliation("FAILED", (), tuple(sorted(set(blockers))))
    if any_open:
        return Reconciliation("BLOCKED", (), tuple(sorted(set(blockers))))
    if any_waiver:
        return Reconciliation("PARTIAL_WITH_USER_WAIVER", (), ())
    return Reconciliation("COMPLETE", (), ())


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
