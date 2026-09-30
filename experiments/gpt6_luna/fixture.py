#!/usr/bin/env python3
"""Deterministic fixture generator and hidden grader for Luna model qualification."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

CASES = (
    "mechanical_none",
    "local_review",
    "broad_contract",
    "reviewer_trap",
    "risk_idempotency",
)

CASE_CONTRACTS = {
    "mechanical_none": {
        "route": "SIMPLE",
        "assurance": "NONE",
        "architect_required": False,
        "reviewer_required": False,
        "boundary_required": False,
        "allowed_changed_paths": ["src/settings.py", "tests/test_settings.py"],
    },
    "local_review": {
        "route": "SIMPLE",
        "assurance": "REVIEW",
        "architect_required": False,
        "reviewer_required": True,
        "boundary_required": False,
        "allowed_changed_paths": ["src/headers.py", "tests/test_headers.py"],
    },
    "broad_contract": {
        "route": "STANDARD",
        "assurance": "REVIEW",
        "architect_required": True,
        "reviewer_required": True,
        "boundary_required": True,
        "allowed_changed_paths": ["src/exporter.py", "tests/test_exporter.py"],
    },
    "reviewer_trap": {
        "route": "SIMPLE",
        "assurance": "REVIEW",
        "architect_required": False,
        "reviewer_required": True,
        "boundary_required": False,
        "allowed_changed_paths": ["src/ranges.py", "tests/test_ranges.py"],
    },
    "risk_idempotency": {
        "route": "SIMPLE",
        "assurance": "RISK",
        "architect_required": False,
        "reviewer_required": True,
        "boundary_required": False,
        "allowed_changed_paths": ["src/ledger.py", "tests/test_ledger.py"],
    },
}


def write(root: Path, rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip(), encoding="utf-8")


def prepare(case: str, root: Path, task_file: Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    write(root, ".gitignore", "__pycache__/\\n*.pyc\\n")
    write(root, "pyproject.toml", """
[project]
name = "luna-qualification-fixture"
version = "0.0.0"
requires-python = ">=3.11"
""")

    if case == "mechanical_none":
        write(root, "src/settings.py", """
DEFAULT_RETRIES = 3
""")
        write(root, "tests/test_settings.py", """
from src.settings import DEFAULT_RETRIES

def test_default_retries():
    assert DEFAULT_RETRIES == 3
""")
        task = """Change DEFAULT_RETRIES from 3 to 5 in src/settings.py and update its exact regression assertion in tests/test_settings.py. Do not change any other behavior."""

    elif case == "local_review":
        write(root, "src/headers.py", """
def normalize_name(name: str) -> str:
    return name.strip().lower()

def create_header(name: str, value: str) -> tuple[str, str]:
    return normalize_name(name), value

def update_header(name: str, value: str) -> tuple[str, str]:
    return normalize_name(name), value
""")
        write(root, "tests/test_headers.py", """
from src.headers import create_header, update_header

def test_normalizes_names():
    assert create_header(" X-ID ", "a") == ("x-id", "a")
    assert update_header(" X-ID ", "b") == ("x-id", "b")
""")
        task = """In the named create_header and update_header behavior, reject header names that are blank after trimming by raising ValueError("header name must not be blank"). Preserve the existing normalization and value behavior. Add focused regression coverage."""

    elif case == "broad_contract":
        write(root, "src/identity.py", """
def canonical_account_id(raw: str) -> str:
    value = raw.strip().lower()
    if not value.startswith("acct_"):
        value = "acct_" + value
    return value
""")
        write(root, "src/models.py", """
from dataclasses import dataclass

@dataclass
class Account:
    account_id: str
    display_name: str
""")
        write(root, "src/exporter.py", """
from .models import Account

def export_account(account: Account) -> dict[str, str]:
    return {
        "id": account.account_id,
        "name": account.display_name,
    }
""")
        write(root, "src/audit.py", """
from .identity import canonical_account_id

def audit_key(account_id: str) -> str:
    return "account/" + canonical_account_id(account_id)
""")
        write(root, "tests/test_exporter.py", """
from src.exporter import export_account
from src.models import Account

def test_export_account():
    assert export_account(Account("ACCT_ABC", "A")) == {"id": "ACCT_ABC", "name": "A"}
""")
        task = """Update account export so the public payload's id follows this repository's established canonical account-ID contract instead of emitting the raw stored value. Discover and reuse the existing contract rather than inventing a new normalization rule. Add focused regression coverage."""

    elif case == "reviewer_trap":
        write(root, "src/ranges.py", """
def clamp_window(start: int, end: int, limit: int) -> tuple[int, int]:
    if start < 0 or end < 0:
        raise ValueError("negative boundary")
    if start > end:
        raise ValueError("reversed window")
    return min(start, limit), min(end, limit)
""")
        write(root, "tests/test_ranges.py", """
from src.ranges import clamp_window

def test_clamps_end():
    assert clamp_window(2, 12, 10) == (2, 10)
""")
        task = """Change clamp_window so a window that starts at or beyond limit is rejected with ValueError("window starts outside limit"), while preserving all existing validation and clamping behavior. Add focused regression coverage, including the boundary at start == limit."""

    elif case == "risk_idempotency":
        write(root, "src/ledger.py", """
class Ledger:
    def __init__(self) -> None:
        self.entries: list[tuple[str, int]] = []

    def apply_charge(self, event_id: str, amount: int) -> None:
        self.entries.append((event_id, amount))

    @property
    def total(self) -> int:
        return sum(amount for _, amount in self.entries)
""")
        write(root, "tests/test_ledger.py", """
from src.ledger import Ledger

def test_charge_changes_total():
    ledger = Ledger()
    ledger.apply_charge("evt-1", 7)
    assert ledger.total == 7
""")
        task = """Make Ledger.apply_charge idempotent by event_id: replaying the same event_id must not apply the amount twice, while distinct event_ids still apply independently. Preserve first-write semantics if a duplicate event_id arrives with a different amount. Add focused regression coverage. Treat this as a persistence/data-integrity contract."""

    else:
        raise SystemExit(f"unknown case: {case}")

    task_file.parent.mkdir(parents=True, exist_ok=True)
    task_file.write_text(task + "\n", encoding="utf-8")


def load_module(root: Path, rel: str, name: str):
    path = root / rel
    module = type(sys)(name)
    module.__file__ = str(path)
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
    return module


def hidden(case: str, root: Path) -> tuple[bool, list[str]]:
    failures: list[str] = []
    try:
        if case == "mechanical_none":
            mod = load_module(root, "src/settings.py", "fixture_settings")
            if mod.DEFAULT_RETRIES != 5:
                failures.append("DEFAULT_RETRIES must be 5")
            test_text = (root / "tests/test_settings.py").read_text(encoding="utf-8")
            if "DEFAULT_RETRIES == 5" not in test_text:
                failures.append("exact regression assertion was not updated")

        elif case == "local_review":
            mod = load_module(root, "src/headers.py", "fixture_headers")
            for fn_name in ("create_header", "update_header"):
                fn = getattr(mod, fn_name)
                try:
                    fn("   ", "v")
                except ValueError as exc:
                    if str(exc) != "header name must not be blank":
                        failures.append(f"{fn_name}: wrong error message")
                else:
                    failures.append(f"{fn_name}: blank name accepted")
            if mod.create_header(" X-ID ", "a") != ("x-id", "a"):
                failures.append("create_header normalization regressed")
            if mod.update_header(" X-ID ", "b") != ("x-id", "b"):
                failures.append("update_header normalization regressed")

        elif case == "broad_contract":
            sys.path.insert(0, str(root))
            try:
                from src.exporter import export_account
                from src.models import Account
                result = export_account(Account("  ABC  ", "A"))
                if result != {"id": "acct_abc", "name": "A"}:
                    failures.append(f"export does not reuse canonical contract: {result!r}")
                result2 = export_account(Account("ACCT_XY", "B"))
                if result2["id"] != "acct_xy":
                    failures.append("existing acct_ prefix is not canonicalized")
            finally:
                sys.path.pop(0)
                for key in [k for k in list(sys.modules) if k == "src" or k.startswith("src.")]:
                    sys.modules.pop(key, None)

        elif case == "reviewer_trap":
            mod = load_module(root, "src/ranges.py", "fixture_ranges")
            for start in (10, 11):
                try:
                    mod.clamp_window(start, 12, 10)
                except ValueError as exc:
                    if str(exc) != "window starts outside limit":
                        failures.append(f"start={start}: wrong error {exc!r}")
                else:
                    failures.append(f"start={start}: should be rejected")
            if mod.clamp_window(2, 12, 10) != (2, 10):
                failures.append("end clamping regressed")
            checks = [
                ((-1, 3, 10), "negative boundary"),
                ((5, 4, 10), "reversed window"),
            ]
            for args, expected in checks:
                try:
                    mod.clamp_window(*args)
                except ValueError as exc:
                    if str(exc) != expected:
                        failures.append(f"{args}: validation precedence/message regressed")
                else:
                    failures.append(f"{args}: expected validation error")

        elif case == "risk_idempotency":
            mod = load_module(root, "src/ledger.py", "fixture_ledger")
            ledger = mod.Ledger()
            ledger.apply_charge("evt-1", 7)
            ledger.apply_charge("evt-1", 99)
            ledger.apply_charge("evt-2", 5)
            ledger.apply_charge("evt-2", 5)
            if ledger.total != 12:
                failures.append(f"idempotent total should be 12, got {ledger.total}")
            if ledger.entries != [("evt-1", 7), ("evt-2", 5)]:
                failures.append(f"first-write event semantics wrong: {ledger.entries!r}")

        else:
            failures.append(f"unknown case: {case}")
    except Exception as exc:
        failures.append(f"exception during hidden grading: {type(exc).__name__}: {exc}")
    return not failures, failures


def apply_golden(case: str, root: Path) -> None:
    if case == "mechanical_none":
        write(root, "src/settings.py", "DEFAULT_RETRIES = 5\n")
        write(root, "tests/test_settings.py", """
from src.settings import DEFAULT_RETRIES

def test_default_retries():
    assert DEFAULT_RETRIES == 5
""")
    elif case == "local_review":
        write(root, "src/headers.py", """
def normalize_name(name: str) -> str:
    value = name.strip().lower()
    if not value:
        raise ValueError("header name must not be blank")
    return value

def create_header(name: str, value: str) -> tuple[str, str]:
    return normalize_name(name), value

def update_header(name: str, value: str) -> tuple[str, str]:
    return normalize_name(name), value
""")
    elif case == "broad_contract":
        write(root, "src/exporter.py", """
from .identity import canonical_account_id
from .models import Account

def export_account(account: Account) -> dict[str, str]:
    return {
        "id": canonical_account_id(account.account_id),
        "name": account.display_name,
    }
""")
    elif case == "reviewer_trap":
        write(root, "src/ranges.py", """
def clamp_window(start: int, end: int, limit: int) -> tuple[int, int]:
    if start < 0 or end < 0:
        raise ValueError("negative boundary")
    if start > end:
        raise ValueError("reversed window")
    if start >= limit:
        raise ValueError("window starts outside limit")
    return min(start, limit), min(end, limit)
""")
    elif case == "risk_idempotency":
        write(root, "src/ledger.py", """
class Ledger:
    def __init__(self) -> None:
        self.entries: list[tuple[str, int]] = []
        self._seen: set[str] = set()

    def apply_charge(self, event_id: str, amount: int) -> None:
        if event_id in self._seen:
            return
        self._seen.add(event_id)
        self.entries.append((event_id, amount))

    @property
    def total(self) -> int:
        return sum(amount for _, amount in self.entries)
""")
    else:
        raise SystemExit(f"unknown case: {case}")


def selftest(case: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"luna-{case}-") as td:
        root = Path(td) / "repo"
        task = Path(td) / "task.txt"
        prepare(case, root, task)
        ok_before, _ = hidden(case, root)
        if ok_before:
            raise SystemExit(f"{case}: baseline unexpectedly passes hidden gate")
        apply_golden(case, root)
        ok_after, failures = hidden(case, root)
        if not ok_after:
            raise SystemExit(f"{case}: golden result fails hidden gate: {failures}")
        if not task.read_text(encoding="utf-8").strip():
            raise SystemExit(f"{case}: task text missing")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("prepare")
    p.add_argument("--case", choices=CASES, required=True)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--task-file", type=Path, required=True)

    h = sub.add_parser("hidden")
    h.add_argument("--case", choices=CASES, required=True)
    h.add_argument("--root", type=Path, required=True)
    h.add_argument("--json-out", type=Path)

    s = sub.add_parser("selftest")
    s.add_argument("--case", choices=CASES + ("all",), required=True)

    c = sub.add_parser("contract")
    c.add_argument("--case", choices=CASES, required=True)
    c.add_argument("--json-out", type=Path)

    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.case, args.root, args.task_file)
    elif args.command == "contract":
        payload = {"case": args.case, **CASE_CONTRACTS[args.case]}
        text = json.dumps(payload, indent=2)
        print(text)
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(text + "\n", encoding="utf-8")
    elif args.command == "hidden":
        ok, failures = hidden(args.case, args.root)
        payload = {"case": args.case, "pass": ok, "failures": failures}
        print(json.dumps(payload, ensure_ascii=False))
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        raise SystemExit(0 if ok else 1)
    else:
        cases = CASES if args.case == "all" else (args.case,)
        for case in cases:
            selftest(case)
            print(f"{case}: fixture self-test passed")


if __name__ == "__main__":
    main()
