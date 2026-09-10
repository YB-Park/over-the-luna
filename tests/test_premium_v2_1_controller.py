from __future__ import annotations

import os
import stat
import tempfile
import unittest
from pathlib import Path

from scripts.premium_v2_1_controller import (
    reconcile,
    stop_hook_response,
    workspace_digest,
)


def base_state() -> dict:
    return {
        "run_id": "run-1",
        "workspace_revision": "ws-1",
        "requested_outcome": "COMPLETE",
        "correction_count": 0,
        "obligations": {
            "U1": {
                "source": "U",
                "source_anchor": "user:1",
                "criterion": "Behavior X and Y must work",
                "blocking": True,
                "required": True,
                "history": [],
            }
        },
        "current": {
            "U1": {
                "source": "U",
                "criterion": "Behavior X and Y must work",
                "blocking": True,
                "required": True,
                "disposition": "VERIFIED",
                "evidence_refs": ["R1"],
            }
        },
        "receipts": {
            "R1": {
                "run_id": "run-1",
                "command_or_test_id": "pytest tests/test_contract.py",
                "collection_status": "COLLECTED",
                "result_class": "PASS",
                "exit_status": 0,
                "workspace_before": "ws-1",
                "workspace_after": "ws-1",
                "test_asset_identity": "sha256:test",
                "environment_identity": "python3.12:testenv",
            }
        },
        "user_events": [],
    }


class ReconciliationTests(unittest.TestCase):
    def test_verified_current_receipt_completes(self) -> None:
        result = reconcile(base_state())
        self.assertEqual(result.outcome, "COMPLETE")
        self.assertTrue(result.trusted_complete)

    def test_empty_obligation_capture_cannot_complete(self) -> None:
        state = base_state()
        state["obligations"] = {}
        state["current"] = {}
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("required user obligation" in e for e in result.errors))

    def test_missing_required_criterion_cannot_complete(self) -> None:
        state = base_state()
        state["current"] = {}
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("required obligation is missing" in e for e in result.errors))

    def test_u_to_a_authority_laundering_cannot_complete(self) -> None:
        state = base_state()
        state["current"]["U1"]["source"] = "A"
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("invalid authority transition" in e for e in result.errors))

    def test_blocking_downgrade_cannot_complete(self) -> None:
        state = base_state()
        state["current"]["U1"]["blocking"] = False
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_required_downgrade_cannot_complete(self) -> None:
        state = base_state()
        state["current"]["U1"]["required"] = False
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_same_id_scope_narrowing_cannot_complete(self) -> None:
        state = base_state()
        state["current"]["U1"]["criterion"] = "Behavior X must work"
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_missing_source_anchor_cannot_complete(self) -> None:
        state = base_state()
        state["obligations"]["U1"]["source_anchor"] = ""
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_missing_authority_history_cannot_complete(self) -> None:
        state = base_state()
        del state["obligations"]["U1"]["history"]
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_blocking_repository_obligation_cannot_disappear(self) -> None:
        state = base_state()
        state["obligations"]["R1"] = {
            "source": "R",
            "source_anchor": "repo:docs/api.md",
            "criterion": "Existing public API behavior is preserved",
            "blocking": True,
            "required": True,
            "history": [],
        }
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("R1: required obligation is missing" in e for e in result.errors))

    def test_unknown_new_blocking_row_requires_authority_capture(self) -> None:
        state = base_state()
        state["current"]["R2"] = {
            "source": "R",
            "criterion": "New repository invariant",
            "blocking": True,
            "required": True,
            "disposition": "OPEN",
            "evidence_refs": [],
        }
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("lacks controller-owned authority capture" in e for e in result.errors))

    def test_open_required_criterion_blocks(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "OPEN"
        state["current"]["U1"]["evidence_refs"] = []
        result = reconcile(state)
        self.assertEqual(result.outcome, "BLOCKED")
        self.assertIn("U1", result.blocking)

    def test_failed_required_criterion_fails(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "FAILED"
        state["current"]["U1"]["evidence_refs"] = []
        result = reconcile(state)
        self.assertEqual(result.outcome, "FAILED")

    def test_forged_waiver_cannot_complete(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "WAIVED_BY_USER"
        state["current"]["U1"]["evidence_refs"] = []
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("waiver is not authenticated" in e for e in result.errors))

    def test_authenticated_waiver_is_partial_never_complete(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "WAIVED_BY_USER"
        state["current"]["U1"]["evidence_refs"] = []
        state["user_events"] = [
            {"type": "waiver", "criterion_id": "U1", "authenticated": True}
        ]
        result = reconcile(state)
        self.assertEqual(result.outcome, "PARTIAL_WITH_USER_WAIVER")
        self.assertFalse(result.trusted_complete)

    def test_waiver_cannot_mask_another_open_requirement(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "WAIVED_BY_USER"
        state["current"]["U1"]["evidence_refs"] = []
        state["user_events"] = [
            {"type": "waiver", "criterion_id": "U1", "authenticated": True}
        ]
        state["obligations"]["U2"] = {
            "source": "U",
            "source_anchor": "user:2",
            "criterion": "Behavior Z must work",
            "blocking": True,
            "required": True,
            "history": [],
        }
        state["current"]["U2"] = {
            "disposition": "OPEN",
            "evidence_refs": [],
        }
        result = reconcile(state)
        self.assertEqual(result.outcome, "BLOCKED")
        self.assertFalse(result.trusted_complete)

    def test_stale_receipt_cannot_complete(self) -> None:
        state = base_state()
        state["receipts"]["R1"]["workspace_after"] = "ws-old"
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("stale" in e for e in result.errors))

    def test_wrong_run_receipt_cannot_complete(self) -> None:
        state = base_state()
        state["receipts"]["R1"]["run_id"] = "other-run"
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_uncollected_check_cannot_complete(self) -> None:
        state = base_state()
        state["receipts"]["R1"]["collection_status"] = "NO_TESTS_COLLECTED"
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_assertion_failure_cannot_be_receipt_pass(self) -> None:
        state = base_state()
        state["receipts"]["R1"]["result_class"] = "ASSERTION_FAIL"
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")

    def test_missing_test_asset_identity_cannot_complete(self) -> None:
        state = base_state()
        state["receipts"]["R1"]["test_asset_identity"] = ""
        result = reconcile(state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")


class StopHookTests(unittest.TestCase):
    def test_first_invalid_complete_is_blocked_once(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "OPEN"
        state["current"]["U1"]["evidence_refs"] = []
        output = stop_hook_response(state, {"stop_hook_active": False})
        specific = output["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "Stop")
        self.assertEqual(specific["decision"], "block")
        self.assertIn("not COMPLETE", specific["reason"])

    def test_already_continued_invalid_state_is_allowed_to_stop_without_completion(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "OPEN"
        state["current"]["U1"]["evidence_refs"] = []
        output = stop_hook_response(state, {"stop_hook_active": True})
        self.assertEqual(output, {})
        self.assertEqual(reconcile(state).outcome, "BLOCKED")

    def test_non_complete_requested_terminal_state_does_not_force_correction(self) -> None:
        state = base_state()
        state["requested_outcome"] = "BLOCKED"
        state["current"]["U1"]["disposition"] = "OPEN"
        state["current"]["U1"]["evidence_refs"] = []
        self.assertEqual(stop_hook_response(state, {"stop_hook_active": False}), {})


class WorkspaceDigestTests(unittest.TestCase):
    def test_digest_changes_for_content_mode_symlink_and_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            file_path = root / "a.txt"
            file_path.write_text("one", encoding="utf-8")
            d1 = workspace_digest(root)

            file_path.write_text("two", encoding="utf-8")
            d2 = workspace_digest(root)
            self.assertNotEqual(d1, d2)

            mode = file_path.stat().st_mode
            file_path.chmod(mode | stat.S_IXUSR)
            d3 = workspace_digest(root)
            self.assertNotEqual(d2, d3)

            link = root / "link"
            try:
                link.symlink_to("a.txt")
            except (OSError, NotImplementedError):
                return
            d4 = workspace_digest(root)
            self.assertNotEqual(d3, d4)

            link.unlink()
            d5 = workspace_digest(root)
            self.assertNotEqual(d4, d5)

    def test_git_directory_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.txt").write_text("stable", encoding="utf-8")
            git = root / ".git"
            git.mkdir()
            (git / "volatile").write_text("one", encoding="utf-8")
            d1 = workspace_digest(root)
            (git / "volatile").write_text("two", encoding="utf-8")
            d2 = workspace_digest(root)
            self.assertEqual(d1, d2)


if __name__ == "__main__":
    unittest.main()
