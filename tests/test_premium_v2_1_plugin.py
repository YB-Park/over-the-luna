from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SCRIPTS = ROOT / "experiments" / "premium_v2_1_plugin" / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


controller = load_module("premium_v2_1_plugin_controller", PLUGIN_SCRIPTS / "controller.py")
# hook imports `controller` by name, so provide the plugin controller alias it expects.
import sys
sys.modules["controller"] = controller
hook = load_module("premium_v2_1_plugin_hook", PLUGIN_SCRIPTS / "hook.py")


class PluginControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / "workspace"
        self.workspace.mkdir()
        (self.workspace / "src.txt").write_text("base\n", encoding="utf-8")
        self.state_dir = Path(self.temp.name) / "state"
        self.old_state = os.environ.get("OTL_V2_1_STATE_DIR")
        os.environ["OTL_V2_1_STATE_DIR"] = str(self.state_dir)
        self.addCleanup(self._restore_env)

    def _restore_env(self) -> None:
        if self.old_state is None:
            os.environ.pop("OTL_V2_1_STATE_DIR", None)
        else:
            os.environ["OTL_V2_1_STATE_DIR"] = self.old_state

    def event(self, name: str, **extra):
        value = {
            "hook_event_name": name,
            "session_id": "session-1",
            "cwd": str(self.workspace),
            "timestamp": "2026-09-17T00:00:00Z",
        }
        value.update(extra)
        return value

    def test_user_prompt_captures_immutable_u0_and_proposal(self) -> None:
        event = self.event("UserPromptSubmit", prompt="Implement X and preserve Y")
        state, state_path, _ = hook.ensure_state(event)
        hook.init_user_obligation(event, state)
        hook.save_state(state_path, state)
        saved = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["obligations"]["U0"]["source"], "U")
        self.assertEqual(saved["obligations"]["U0"]["criterion"], "Implement X and preserve Y")
        proposal, _, _ = hook.metadata_paths(self.workspace)
        data = json.loads(proposal.read_text(encoding="utf-8"))
        self.assertEqual(data["current"]["U0"]["disposition"], "OPEN")

    def test_post_tool_runtime_receipt_can_support_complete(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, state_path, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)

        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_use_id="tool-1",
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        receipt = state["receipts"]["E1"]
        self.assertEqual(receipt["result_class"], "PASS")
        self.assertEqual(receipt["collection_status"], "COLLECTED")

        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {"disposition": "VERIFIED", "evidence_refs": ["E1"]}
        controller.atomic_json(proposal_path, proposal)

        result, record = hook.final_reconcile(self.event("Stop", stop_hook_active=False), state)
        self.assertEqual(result.outcome, "COMPLETE")
        self.assertTrue(record["trusted_complete"])

    def test_same_id_authority_laundering_never_completes(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Implement X and preserve Y")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)
        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "pytest -q"},
            tool_use_id="tool-1",
            tool_response={"exitCode": 0},
        )
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {
            "source": "A",
            "criterion": "Implement X",
            "blocking": False,
            "required": False,
            "disposition": "VERIFIED",
            "evidence_refs": ["E1"],
        }
        controller.atomic_json(proposal_path, proposal)
        result, _ = hook.final_reconcile(self.event("Stop", stop_hook_active=False), state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("authority transition" in e for e in result.errors))

    def test_forged_waiver_never_completes(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Implement X")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {"disposition": "WAIVED_BY_USER", "evidence_refs": []}
        controller.atomic_json(proposal_path, proposal)
        result, _ = hook.final_reconcile(self.event("Stop", stop_hook_active=False), state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("unauthenticated waiver" in e for e in result.errors))

    def test_discovered_repository_obligation_is_preserved(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Implement X")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)
        proposal = {
            "requested_outcome": "COMPLETE",
            "current": {"U0": {"disposition": "OPEN", "evidence_refs": []}},
            "discovered_obligations": [
                {
                    "id": "R1",
                    "source": "R",
                    "source_anchor": "docs/api.md",
                    "criterion": "Preserve public behavior Y",
                    "blocking": True,
                    "required": True,
                }
            ],
        }
        errors = hook.admit_discovered(proposal, state)
        self.assertEqual(errors, [])
        self.assertEqual(state["obligations"]["R1"]["criterion"], "Preserve public behavior Y")
        replacement = json.loads(json.dumps(proposal))
        replacement["discovered_obligations"][0]["criterion"] = "Preserve only Y-lite"
        errors = hook.admit_discovered(replacement, state)
        self.assertTrue(any("replace preserved" in e for e in errors))

    def test_enforce_mode_blocks_repo_tool_before_builder(self) -> None:
        state = {"phase": "ROOT_INTAKE", "builder_count": 0, "takeover": False}
        event = self.event("PreToolUse", tool_name="read_file", tool_input={"path": "src.txt"})
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_enforce_mode_allows_initial_agent_call(self) -> None:
        state = {"phase": "ROOT_INTAKE", "builder_count": 0, "takeover": False}
        event = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder", "prompt": "work"},
        )
        self.assertEqual(hook.pre_tool_decision(event, state, "enforce"), {})

    def test_enforce_mode_denies_second_agent_call(self) -> None:
        state = {"phase": "ROOT_RECONCILE", "builder_count": 1, "takeover": False}
        event = self.event("PreToolUse", tool_name="agent", tool_input={"agent": "Premium v2.1 Luna Builder"})
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_root_repo_tool_after_builder_marks_takeover(self) -> None:
        state = {"phase": "ROOT_RECONCILE", "builder_count": 1, "takeover": False}
        event = self.event("PreToolUse", tool_name="read_file", tool_input={"path": "src.txt"})
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output, {})
        self.assertEqual(state["phase"], "TERRA_TAKEOVER")
        self.assertTrue(state["takeover"])

    def test_metadata_edit_does_not_count_as_takeover(self) -> None:
        state = {"phase": "ROOT_RECONCILE", "builder_count": 1, "takeover": False}
        event = self.event(
            "PreToolUse",
            tool_name="edit_file",
            tool_input={"path": ".otl-v2-1/controller-proposal.json"},
        )
        hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(state["phase"], "ROOT_RECONCILE")
        self.assertFalse(state["takeover"])


if __name__ == "__main__":
    unittest.main()
