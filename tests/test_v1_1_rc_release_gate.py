from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENTS / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load("v1_1_release_gate_evaluator_v6", "v1_1_release_gate_evaluator_v6.py")

import sys
sys.path.insert(0, str(EXPERIMENTS))
try:
    RC2 = load("v1_1_release_gate_evaluator_rc2", "v1_1_release_gate_evaluator_rc2.py")
finally:
    sys.path.pop(0)


def write_events(requests: list[dict]) -> Path:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
    event = {"type": "assistant.message", "data": {"toolRequests": requests}}
    tmp.write(json.dumps(event) + "\n")
    tmp.close()
    return Path(tmp.name)


class RcReleaseGateTests(unittest.TestCase):
    def test_absolute_sealed_work_set_is_normalized(self) -> None:
        self.assertEqual(
            BASE.sealed_paths(
                "Boundary sealed — work set: "
                "/home/runner/work/_temp/fixture/accounts/reporting/summary.py, "
                "/home/runner/work/_temp/fixture/tests/test_accounts.py"
            ),
            {"accounts/reporting/summary.py", "tests/test_accounts.py"},
        )

    def test_any_simple_orientation_glob_is_rejected(self) -> None:
        path = write_events([
            {"name": "glob", "arguments": {"pattern": "**/*test*"}},
            {"name": "apply_patch", "arguments": {}},
        ])
        try:
            failures = RC2.extra_failures("local", str(path))
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(len(failures), 1)
        self.assertIn("glob is forbidden", failures[0])

    def test_readme_is_rejected_during_simple_orientation(self) -> None:
        path = write_events([
            {"name": "view", "arguments": {"path": "/tmp/fixture/README.md"}},
            {"name": "apply_patch", "arguments": {}},
        ])
        try:
            failures = RC2.extra_failures("local", str(path))
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(len(failures), 1)
        self.assertIn("background prose", failures[0])

    def test_narrow_rg_and_direct_reads_are_allowed(self) -> None:
        path = write_events([
            {"name": "rg", "arguments": {"pattern": "update_headers"}},
            {"name": "view", "arguments": {"path": "/tmp/fixture/client/headers.py"}},
            {"name": "apply_patch", "arguments": {}},
        ])
        try:
            failures = RC2.extra_failures("local", str(path))
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(failures, [])

    def test_verbatim_diff_markers_are_required(self) -> None:
        good = "BEGIN_UNIFIED_DIFF\ndiff --git a/a b/a\n@@ -1 +1 @@\n-x\n+y\nEND_UNIFIED_DIFF"
        self.assertTrue(BASE.verbatim_patch(good))
        self.assertFalse(BASE.verbatim_patch(good.replace("END_UNIFIED_DIFF", "")))


if __name__ == "__main__":
    unittest.main()
