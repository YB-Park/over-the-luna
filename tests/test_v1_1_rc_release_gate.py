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

# The RC wrapper imports the base module by filename, so make the experiments directory importable for this test.
import sys
sys.path.insert(0, str(EXPERIMENTS))
try:
    RC = load("v1_1_release_gate_evaluator_rc", "v1_1_release_gate_evaluator_rc.py")
finally:
    sys.path.pop(0)


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

    def test_local_generic_root_glob_is_rejected(self) -> None:
        event = {
            "type": "assistant.message",
            "data": {
                "toolRequests": [
                    {"name": "glob", "arguments": {"pattern": "*"}},
                    {"name": "apply_patch", "arguments": {}},
                ]
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text(json.dumps(event) + "\n", encoding="utf-8")
            failures = RC.generic_inventory_failures("local", str(path))
        self.assertEqual(len(failures), 1)
        self.assertIn("generic inventory glob", failures[0])

    def test_focused_test_glob_is_allowed(self) -> None:
        event = {
            "type": "assistant.message",
            "data": {
                "toolRequests": [
                    {"name": "glob", "arguments": {"pattern": "**/*test*"}},
                    {"name": "apply_patch", "arguments": {}},
                ]
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text(json.dumps(event) + "\n", encoding="utf-8")
            failures = RC.generic_inventory_failures("local", str(path))
        self.assertEqual(failures, [])

    def test_verbatim_diff_markers_are_required(self) -> None:
        good = "BEGIN_UNIFIED_DIFF\ndiff --git a/a b/a\n@@ -1 +1 @@\n-x\n+y\nEND_UNIFIED_DIFF"
        self.assertTrue(BASE.verbatim_patch(good))
        self.assertFalse(BASE.verbatim_patch(good.replace("END_UNIFIED_DIFF", "")))


if __name__ == "__main__":
    unittest.main()
