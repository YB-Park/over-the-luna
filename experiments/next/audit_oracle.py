#!/usr/bin/env python3
"""No-credit audit of the P1b grader's blind spots. NOT a retroactive regrade.

Use the exact pinned original qualification fixture; don't modify its branch.
Regression checks run only on local golden/mutant fixture files with no API
tokens in the environment. Never execute untrusted model-generated tests in
a process containing credentials.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import runpy
import sys
import tempfile
from pathlib import Path


def load_fixture(path: Path):
    spec = importlib.util.spec_from_file_location("qualification_fixture", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load pinned qualification fixture")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unload_workspace_modules() -> None:
    for name in list(sys.modules):
        if name == "src" or name.startswith("src.") or name == "tests" or name.startswith("tests."):
            sys.modules.pop(name, None)


def run_focused_regressions(case: str, root: Path, problems: list[str]) -> None:
    # Compile ALL relevant Python code, not just imported production modules.
    for folder in ("src", "tests"):
        for file in sorted((root / folder).rglob("*.py")):
            try:
                compile(file.read_text(encoding="utf-8"), str(file), "exec")
            except (SyntaxError, UnicodeError) as err:
                problems.append(f"invalid Python in {file.relative_to(root)}: {type(err).__name__}")
    if problems:
        return
    test_path = root / "tests" / {
        "broad_contract": "test_exporter.py",
        "risk_idempotency": "test_ledger.py",
    }[case]
    unload_workspace_modules()
    sys.path.insert(0, str(root))
    try:
        namespace = runpy.run_path(str(test_path), run_name="__audit_tests__")
        tests = [(name, value) for name, value in namespace.items()
                 if name.startswith("test_") and callable(value)]
        if not tests:
            problems.append("no callable focused regression tests")
        for name, test in tests:
            try:
                test()
            except Exception as exc:
                problems.append(f"regression {name} failed: {type(exc).__name__}")
    except Exception as exc:
        problems.append(f"test module load failed: {type(exc).__name__}")
    finally:
        sys.path.remove(str(root))
        unload_workspace_modules()


def check_actual_helper_reuse(root: Path, problems: list[str]) -> None:
    # Instrument BEFORE exporter imports the helper. This checks a call to the
    # shared helper in tested execution, not a keyword in the source.
    unload_workspace_modules()
    sys.path.insert(0, str(root))
    try:
        identity = importlib.import_module("src.identity")
        original = identity.canonical_account_id
        observed = []

        def recording_helper(raw: str) -> str:
            observed.append(raw)
            return original(raw)

        identity.canonical_account_id = recording_helper
        exporter = importlib.import_module("src.exporter")
        account = importlib.import_module("src.models").Account("  probe  ", "Audit")
        got = exporter.export_account(account)
        if got != {"id": "acct_probe", "name": "Audit"}:
            problems.append("export account contract failed under helper probe")
        if "  probe  " not in observed:
            problems.append("canonical_account_id helper not invoked on exported account")
    except Exception as exc:
        problems.append(f"helper contract probe failed: {type(exc).__name__}")
    finally:
        sys.path.remove(str(root))
        unload_workspace_modules()


def strict_grade(case: str, root: Path, fixture) -> tuple[bool, list[str]]:
    ok, problems = fixture.hidden(case, root)
    problems = list(problems)
    run_focused_regressions(case, root, problems)
    if case == "broad_contract":
        check_actual_helper_reuse(root, problems)
    return not problems, problems


def selftest(fixture) -> None:
    for case in ("broad_contract", "risk_idempotency"):
        with tempfile.TemporaryDirectory(prefix="otl-audit-") as tmp:
            root = Path(tmp) / "work"
            fixture.prepare(case, root, Path(tmp) / "task.txt")
            fixture.apply_golden(case, root)
            test_path = root / "tests" / ("test_exporter.py" if case == "broad_contract" else "test_ledger.py")

            if case == "broad_contract":
                # A newly discovered defect: the original fixture's golden
                # implementation passes hidden() but leaves the OLD assertion
                # in test_exporter.py, which fails. Preserve this proof.
                old_ok, _ = fixture.hidden(case, root)
                new_ok, stale_problems = strict_grade(case, root, fixture)
                assert old_ok and not new_ok and any(
                    "regression test_export_account failed" in p for p in stale_problems
                ), "stale golden regression test must be rejected"
                print("ORACLE_COUNTEREXAMPLE_PASS: original golden has stale failing test")
                # Repair only this temporary golden workspace, NOT historical
                # fixture source, in order to verify a truly passing baseline.
                test_path.write_text(
                    "from src.exporter import export_account\n"
                    "from src.models import Account\n\n"
                    "def test_export_account():\n"
                    "    assert export_account(Account('  ABC  ', 'A')) == "
                    "{'id': 'acct_abc', 'name': 'A'}\n"
                    "    assert export_account(Account('ACCT_XY', 'B')) == "
                    "{'id': 'acct_xy', 'name': 'B'}\n",
                    encoding="utf-8",
                )
            old_ok, _ = fixture.hidden(case, root)
            new_ok, new_problems = strict_grade(case, root, fixture)
            assert old_ok and new_ok, f"{case} repaired golden unexpectedly fails: {new_problems}"

            test_backup = test_path.read_text(encoding="utf-8")
            test_path.write_text("def invalid_syntax(:\n", encoding="utf-8")
            old_ok, _ = fixture.hidden(case, root)
            new_ok, problems = strict_grade(case, root, fixture)
            assert old_ok and not new_ok and any("invalid Python" in p for p in problems), (
                f"{case}: broken regression tests must not PASS"
            )
            test_path.write_text(test_backup, encoding="utf-8")
            print(f"ORACLE_COUNTEREXAMPLE_PASS: {case} old_grader_accepted_broken_test; strict_rejected")

            if case == "broad_contract":
                exporter = root / "src" / "exporter.py"
                exporter.write_text(
                    "from .models import Account\n"
                    "def export_account(account: Account) -> dict[str, str]:\n"
                    "    value = account.account_id.strip().lower()\n"
                    "    if not value.startswith('acct_'):\n"
                    "        value = 'acct_' + value\n"
                    "    return {'id': value, 'name': account.display_name}\n",
                    encoding="utf-8",
                )
                old_ok, _ = fixture.hidden(case, root)
                new_ok, problems = strict_grade(case, root, fixture)
                assert old_ok and not new_ok and any("helper not invoked" in p for p in problems), (
                    "helper duplication must not be accepted as helper reuse"
                )
                print("ORACLE_COUNTEREXAMPLE_PASS: old_grader_accepted_duplicated_helper; strict_rejected")
    print("STRICT_GRADER_AUDIT_PASS: both goldens accepted, both audit counterexamples rejected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("selftest", "grade"))
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--case", choices=("broad_contract", "risk_idempotency"))
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    fixture = load_fixture(args.fixture)
    if args.command == "selftest":
        selftest(fixture)
    else:
        if not args.case or args.root is None:
            parser.error("grade requires --case and --root")
        passed, failures = strict_grade(args.case, args.root, fixture)
        print("STRICT_GRADE:", "PASS" if passed else "FAIL")
        for failure in failures:
            print("CHECK:", failure)
        if not passed:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
