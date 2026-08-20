from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "v1_1_release_gate_evaluator_v6.py"
SPEC = importlib.util.spec_from_file_location("v1_1_release_gate_evaluator_v6", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReleaseGateEvaluatorTests(unittest.TestCase):
    def test_normalize_fixture_absolute_path(self) -> None:
        self.assertEqual(
            MODULE.normalize("/home/runner/work/_temp/fixture/accounts/core/identity.py"),
            "accounts/core/identity.py",
        )

    def test_normalize_relative_path(self) -> None:
        self.assertEqual(MODULE.normalize("./tests/test_accounts.py"), "tests/test_accounts.py")

    def test_sealed_paths_accept_relative_comma_list(self) -> None:
        content = (
            "Boundary sealed — work set: accounts/reporting/summary.py, "
            "tests/test_accounts.py, accounts/core/identity.py"
        )
        self.assertEqual(
            MODULE.sealed_paths(content),
            {
                "accounts/reporting/summary.py",
                "tests/test_accounts.py",
                "accounts/core/identity.py",
            },
        )

    def test_sealed_paths_normalize_absolute_paths(self) -> None:
        content = (
            "Boundary sealed — work set: "
            "/home/runner/work/_temp/fixture/accounts/reporting/summary.py, "
            "/home/runner/work/_temp/fixture/tests/test_accounts.py"
        )
        self.assertEqual(
            MODULE.sealed_paths(content),
            {"accounts/reporting/summary.py", "tests/test_accounts.py"},
        )

    def test_sealed_paths_accept_backticks(self) -> None:
        content = "Boundary sealed — work set: `app/config.py`, `tests/test_config.py`"
        self.assertEqual(MODULE.sealed_paths(content), {"app/config.py", "tests/test_config.py"})

    def test_verbatim_patch_requires_markers_headers_and_hunks(self) -> None:
        good = (
            "BEGIN_UNIFIED_DIFF\n"
            "diff --git a/a.py b/a.py\n"
            "@@ -1 +1 @@\n-old\n+new\n"
            "END_UNIFIED_DIFF"
        )
        self.assertTrue(MODULE.verbatim_patch(good))
        self.assertFalse(MODULE.verbatim_patch(good.replace("BEGIN_UNIFIED_DIFF\n", "")))
        self.assertFalse(MODULE.verbatim_patch(good.replace("diff --git", "diff")))
        self.assertFalse(MODULE.verbatim_patch(good.replace("@@ -1 +1 @@", "")))

    def test_tooling_metadata_classification(self) -> None:
        self.assertTrue(MODULE.is_tooling_metadata("pyproject.toml"))
        self.assertTrue(MODULE.is_tooling_metadata("requirements-dev.txt"))
        self.assertFalse(MODULE.is_tooling_metadata("client/ids.py"))


if __name__ == "__main__":
    unittest.main()
