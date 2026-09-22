from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_CONTROLLER = ROOT / "scripts" / "premium_v2_1_controller.py"
PLUGIN_CONTROLLER = (
    ROOT
    / "experiments"
    / "premium_v2_1_plugin"
    / "scripts"
    / "controller.py"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


reference = load_module("premium_v2_1_reference_controller", ROOT_CONTROLLER)
plugin = load_module("premium_v2_1_plugin_controller_parity", PLUGIN_CONTROLLER)


def base_state() -> dict:
    return {
        "run_id": "run-1",
        "workspace_revision": "ws-1",
        "obligations": {
            "U1": {
                "source": "U",
                "source_anchor": "user:1",
                "criterion": "Requested behavior works",
                "blocking": True,
                "required": True,
                "history": [],
            }
        },
        "current": {
            "U1": {
                "source": "U",
                "criterion": "Requested behavior works",
                "blocking": True,
                "required": True,
                "disposition": "VERIFIED",
                "evidence_refs": ["E1"],
            }
        },
        "receipts": {
            "E1": {
                "run_id": "run-1",
                "command_or_test_id": "python -m unittest",
                "execution_eligible": True,
                "collection_status": "COLLECTED",
                "result_class": "PASS",
                "exit_status": 0,
                "workspace_before": "ws-0",
                "workspace_after": "ws-1",
                "test_asset_identity": "sha256:test",
                "environment_identity": "python:test",
            }
        },
        "user_events": [],
    }


class PremiumV21ControllerParityTests(unittest.TestCase):
    def assert_parity(self, state) -> None:
        ref_result = reference.reconcile(copy.deepcopy(state))
        plugin_result = plugin.reconcile(copy.deepcopy(state))
        self.assertEqual(plugin_result.outcome, ref_result.outcome)
        self.assertEqual(plugin_result.trusted_complete, ref_result.trusted_complete)
        self.assertEqual(plugin_result.blocking, ref_result.blocking)

    def test_valid_complete_parity(self) -> None:
        self.assert_parity(base_state())

    def test_open_blocker_parity(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "OPEN"
        state["current"]["U1"]["evidence_refs"] = []
        self.assert_parity(state)

    def test_failed_blocker_parity(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "FAILED"
        state["current"]["U1"]["evidence_refs"] = []
        self.assert_parity(state)

    def test_stale_receipt_parity(self) -> None:
        state = base_state()
        state["receipts"]["E1"]["workspace_after"] = "old"
        self.assert_parity(state)

    def test_non_execution_receipt_parity(self) -> None:
        state = base_state()
        state["receipts"]["E1"]["execution_eligible"] = False
        self.assert_parity(state)

    def test_forged_waiver_parity(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "WAIVED_BY_USER"
        state["current"]["U1"]["evidence_refs"] = []
        self.assert_parity(state)

    def test_authenticated_waiver_parity(self) -> None:
        state = base_state()
        state["current"]["U1"]["disposition"] = "WAIVED_BY_USER"
        state["current"]["U1"]["evidence_refs"] = []
        state["user_events"] = [
            {"type": "waiver", "criterion_id": "U1", "authenticated": True}
        ]
        self.assert_parity(state)

    def test_unknown_non_object_row_parity(self) -> None:
        state = base_state()
        state["current"]["junk"] = "not-an-object"
        self.assert_parity(state)
        self.assertEqual(reference.reconcile(state).outcome, "NO_VERIFIED_COMPLETION")

    def test_malformed_evidence_reference_parity(self) -> None:
        state = base_state()
        state["current"]["U1"]["evidence_refs"] = [{"id": "E1"}]
        self.assert_parity(state)
        self.assertEqual(reference.reconcile(state).outcome, "NO_VERIFIED_COMPLETION")

    def test_missing_required_repository_obligation_parity(self) -> None:
        state = base_state()
        state["obligations"]["R1"] = {
            "source": "R",
            "source_anchor": "repo:contract",
            "criterion": "Existing behavior is preserved",
            "blocking": True,
            "required": True,
            "history": [],
        }
        self.assert_parity(state)

    def test_non_mapping_state_parity(self) -> None:
        self.assert_parity([])


if __name__ == "__main__":
    unittest.main()
