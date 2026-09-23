from __future__ import annotations

import contextlib
import importlib.util
import io
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

    def test_second_user_prompt_is_persisted_control_error(self) -> None:
        first = self.event("UserPromptSubmit", prompt="Implement X")
        state, _, _ = hook.ensure_state(first)
        hook.init_user_obligation(first, state)
        self.assertEqual(state["user_prompt_count"], 1)

        second = self.event("UserPromptSubmit", prompt="Now also implement Y")
        hook.init_user_obligation(second, state)

        self.assertEqual(state["user_prompt_count"], 2)
        self.assertEqual(state["obligations"]["U0"]["criterion"], "Implement X")
        self.assertTrue(
            any(
                "multiple UserPromptSubmit" in item.get("error", "")
                for item in state["control_errors"]
            )
        )

    def test_second_session_start_before_prompt_is_control_error(self) -> None:
        start = self.event("SessionStart")
        state, _, _ = hook.ensure_state(start)
        hook.handle_session_start(start, state)
        self.assertEqual(state["session_start_count"], 1)

        hook.handle_session_start(self.event("SessionStart"), state)

        self.assertEqual(state["session_start_count"], 2)
        self.assertTrue(
            any(
                "repeated/resumed SessionStart" in item.get("error", "")
                for item in state["control_errors"]
            )
        )

    def test_final_reconcile_requires_one_session_start(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)
        state["builder_count"] = 1
        state["phase"] = "ROOT_RECONCILE"

        result, record = hook.final_reconcile(self.event("Stop"), state)

        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(any("exactly one SessionStart" in e for e in result.errors))

    def test_first_session_start_after_prompt_is_order_tolerant(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Implement X")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)

        hook.handle_session_start(self.event("SessionStart"), state)

        self.assertEqual(state["session_start_count"], 1)
        self.assertEqual(state["phase"], "ROOT_INTAKE")
        self.assertFalse(
            any(
                "repeated/resumed SessionStart" in item.get("error", "")
                for item in state["control_errors"]
            )
        )

    def test_second_session_start_after_prompt_is_control_error(self) -> None:
        start = self.event("SessionStart")
        state, _, _ = hook.ensure_state(start)
        hook.handle_session_start(start, state)
        hook.init_user_obligation(
            self.event("UserPromptSubmit", prompt="Implement X"),
            state,
        )
        state["phase"] = "ROOT_RECONCILE"

        hook.handle_session_start(self.event("SessionStart"), state)

        self.assertEqual(state["phase"], "ROOT_RECONCILE")
        self.assertTrue(
            any(
                "repeated/resumed SessionStart" in item.get("error", "")
                for item in state["control_errors"]
            )
        )

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
        hook.handle_session_start(self.event("SessionStart"), state)
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

        state["builder_dispatch_count"] = 1
        state["builder_count"] = 1
        state["builder_invocation_seen"] = True
        state["builder_agent_tool_completion_seen"] = True
        state["phase"] = "ROOT_RECONCILE"
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

    def test_discovered_repository_obligation_survives_later_proposal_deletion(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Implement X")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)

        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["discovered_obligations"] = [
            {
                "id": "R1",
                "source": "R",
                "source_anchor": "docs/api.md",
                "criterion": "Preserve public behavior Y",
                "blocking": True,
                "required": True,
            }
        ]
        controller.atomic_json(proposal_path, proposal)
        self.assertEqual(hook.sync_proposal_authority(self.event("PostToolUse"), state), [])
        self.assertIn("R1", state["obligations"])

        proposal["discovered_obligations"] = []
        controller.atomic_json(proposal_path, proposal)
        result, _ = hook.final_reconcile(self.event("Stop", stop_hook_active=False), state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("R1: required obligation missing" in e for e in result.errors))

    def test_invalid_discovered_obligation_replacement_is_persisted(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Implement X")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)

        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        original = {
            "id": "R1",
            "source": "R",
            "source_anchor": "docs/api.md",
            "criterion": "Preserve public behavior Y",
            "blocking": True,
            "required": True,
        }
        proposal["discovered_obligations"] = [original]
        controller.atomic_json(proposal_path, proposal)
        hook.sync_proposal_authority(self.event("PostToolUse", tool_use_id="tool-1"), state)

        proposal["discovered_obligations"] = [
            {**original, "criterion": "Preserve only Y-lite"}
        ]
        controller.atomic_json(proposal_path, proposal)
        errors = hook.sync_proposal_authority(
            self.event("PostToolUse", tool_use_id="tool-2"),
            state,
        )
        self.assertTrue(any("replace preserved" in e for e in errors))
        self.assertTrue(state["control_errors"])

        # Even restoring the editable proposal does not erase the observed
        # controller-authority violation.
        proposal["discovered_obligations"] = [original]
        controller.atomic_json(proposal_path, proposal)
        result, _ = hook.final_reconcile(self.event("Stop", stop_hook_active=False), state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertTrue(any("replace preserved" in e for e in result.errors))

    def test_enforce_mode_blocks_repo_tool_before_builder(self) -> None:
        state = {"phase": "ROOT_INTAKE", "builder_count": 0, "takeover": False}
        event = self.event("PreToolUse", tool_name="read_file", tool_input={"path": "src.txt"})
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_malformed_lifecycle_counter_denies_enforce_tool(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": "corrupt",
            "builder_invocation_seen": False,
            "takeover": False,
        }
        event = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
        )
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("malformed", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_malformed_builder_count_never_trusted_complete(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)
        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {"disposition": "VERIFIED", "evidence_refs": ["E1"]}
        controller.atomic_json(proposal_path, proposal)
        state["builder_count"] = "corrupt"
        state["phase"] = "ROOT_RECONCILE"

        result, record = hook.final_reconcile(self.event("Stop"), state)

        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(any("exactly one Luna Builder start" in e for e in result.errors))

    def test_enforce_mode_denies_non_builder_agent_during_intake(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "takeover": False,
        }
        event = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Some Other Agent"},
        )
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertFalse(state["builder_invocation_seen"])

    def test_initial_builder_dispatch_is_marked_before_subagent_start(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "takeover": False,
        }
        event = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder", "prompt": "work"},
        )
        self.assertEqual(hook.pre_tool_decision(event, state, "enforce"), {})
        self.assertTrue(state["builder_invocation_seen"])
        self.assertEqual(state["phase"], "LUNA_DISPATCHED")

        # Even if SubagentStart were lost, a second child dispatch is denied.
        second = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(second["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_execute_tool_mentioning_metadata_is_not_metadata_only(self) -> None:
        event = self.event(
            "PreToolUse",
            tool_name="execute",
            tool_input={
                "command": "python -c \"print('x')\"",
                "path": ".otl-v2-1/controller-proposal.json",
            },
        )
        self.assertFalse(hook.is_metadata_only(event))

    def test_missing_builder_lifecycle_never_trusted_complete(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)
        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {"disposition": "VERIFIED", "evidence_refs": ["E1"]}
        controller.atomic_json(proposal_path, proposal)

        result, record = hook.final_reconcile(
            self.event("Stop", stop_hook_active=False),
            state,
        )
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(any("exactly one Luna Builder start" in error for error in result.errors))

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
        state = {
            "phase": "ROOT_RECONCILE",
            "builder_count": 1,
            "takeover": False,
            "obligations": {
                "U0": {"blocking": True, "required": True},
            },
        }
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        controller.atomic_json(
            proposal_path,
            {
                "requested_outcome": "COMPLETE",
                "current": {
                    "U0": {"disposition": "UNRESOLVED", "evidence_refs": []},
                },
                "discovered_obligations": [],
            },
        )
        event = self.event("PreToolUse", tool_name="read_file", tool_input={"path": "src.txt"})
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output, {})
        self.assertEqual(state["phase"], "TERRA_TAKEOVER")
        self.assertTrue(state["takeover"])
        self.assertEqual(state["takeover_basis_ids"], ["U0"])

    def test_root_repo_tool_without_blocking_residual_is_denied(self) -> None:
        state = {
            "phase": "ROOT_RECONCILE",
            "builder_count": 1,
            "takeover": False,
            "obligations": {
                "U0": {"blocking": True, "required": True},
            },
        }
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        controller.atomic_json(
            proposal_path,
            {
                "requested_outcome": "COMPLETE",
                "current": {
                    "U0": {"disposition": "VERIFIED", "evidence_refs": ["E1"]},
                },
                "discovered_obligations": [],
            },
        )
        event = self.event("PreToolUse", tool_name="read_file", tool_input={"path": "src.txt"})
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(state["phase"], "ROOT_RECONCILE")
        self.assertFalse(state["takeover"])

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

    def test_cli_vscode_compatible_tool_result_is_collected(self) -> None:
        state = {
            "session_key": "fallback",
            "receipts": {},
            "last_workspace_revision": None,
        }
        event = self.event(
            "PostToolUse",
            tool_name="Bash",
            tool_input={"command": "python -m unittest"},
            tool_result={
                "result_type": "success",
                "text_result_for_llm": "Process exited with code 0",
            },
        )
        hook.record_post_tool(event, state)
        receipt = state["receipts"]["E1"]
        self.assertEqual(receipt["collection_status"], "COLLECTED")
        self.assertEqual(receipt["result_class"], "PASS")
        self.assertEqual(receipt["exit_status"], 0)

    def test_non_execution_tool_cannot_forge_pass_receipt_from_text(self) -> None:
        state = {
            "session_key": "fallback",
            "receipts": {},
            "last_workspace_revision": None,
        }
        event = self.event(
            "PostToolUse",
            tool_name="read_file",
            tool_input={"path": "src.txt"},
            tool_response="Documentation example: Process exited with code 0",
        )
        hook.record_post_tool(event, state)
        receipt = state["receipts"]["E1"]
        self.assertFalse(receipt["execution_eligible"])
        self.assertEqual(receipt["collection_status"], "OBSERVED")
        self.assertEqual(receipt["result_class"], "UNCLASSIFIED")
        self.assertIsNone(receipt["exit_status"])

    def test_command_bearing_terminal_tool_is_execution_eligible(self) -> None:
        event = self.event(
            "PostToolUse",
            tool_name="runTerminalCommand",
            tool_input={"command": "python -m unittest"},
            tool_response={"exitCode": 0},
        )
        self.assertTrue(hook.is_execution_tool(event))
        self.assertEqual(hook.execution_command(event), "python -m unittest")

    def test_camelcase_runtime_fields_are_normalized(self) -> None:
        event = {
            "sessionId": "cli-session",
            "toolName": "Agent",
            "toolArgs": {"agent": "Premium v2.1 Luna Builder"},
            "agentName": "Premium v2.1 Luna Builder",
        }
        self.assertEqual(hook.event_session_id(event), "cli-session")
        self.assertEqual(hook.event_tool_name(event), "Agent")
        self.assertEqual(hook.event_tool_input(event)["agent"], "Premium v2.1 Luna Builder")
        self.assertEqual(hook.event_agent_name(event), "Premium v2.1 Luna Builder")
        self.assertTrue(hook.is_agent_tool(event))


    def test_builder_match_uses_concrete_name_when_agent_type_is_generic(self) -> None:
        event = self.event(
            "SubagentStart",
            agent_type="custom",
            agent_name="Premium v2.1 Luna Builder",
        )
        self.assertTrue(hook.is_builder_event(event))
        self.assertEqual(hook.event_agent_name(event), "Premium v2.1 Luna Builder")



    def test_weak_session_key_never_trusted_complete(self) -> None:
        event = {
            "hook_event_name": "UserPromptSubmit",
            "cwd": str(self.workspace),
            "timestamp": "2026-09-17T00:00:00Z",
            "prompt": "Make the local check pass",
        }
        state, _, _ = hook.ensure_state(event)
        hook.init_user_obligation(event, state)
        self.assertTrue(state["weak_session_key"])

        post = {
            "hook_event_name": "PostToolUse",
            "cwd": str(self.workspace),
            "timestamp": "2026-09-17T00:00:01Z",
            "tool_name": "execute",
            "tool_input": {"command": "python -m unittest"},
            "tool_response": "Process exited with code 0",
        }
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {"disposition": "VERIFIED", "evidence_refs": ["E1"]}
        controller.atomic_json(proposal_path, proposal)

        stop = {
            "hook_event_name": "Stop",
            "cwd": str(self.workspace),
            "timestamp": "2026-09-17T00:00:02Z",
            "stop_hook_active": False,
        }
        result, record = hook.final_reconcile(stop, state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(any("session_id not observed" in e for e in result.errors))

    def test_digest_error_never_trusted_complete(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)

        original_digest = hook.workspace_digest
        hook.workspace_digest = lambda _: (_ for _ in ()).throw(OSError("digest failed"))
        self.addCleanup(setattr, hook, "workspace_digest", original_digest)

        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        self.assertEqual(state["receipts"]["E1"]["workspace_after"], "DIGEST_ERROR")

        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {"disposition": "VERIFIED", "evidence_refs": ["E1"]}
        controller.atomic_json(proposal_path, proposal)

        result, record = hook.final_reconcile(self.event("Stop", stop_hook_active=False), state)
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])

    def test_state_lock_cleans_up_lock_file(self) -> None:
        state_path = self.state_dir / "session.json"
        with hook.state_lock(state_path):
            lock_path = state_path.with_name(state_path.name + ".lock")
            self.assertTrue(lock_path.exists())
        self.assertFalse(lock_path.exists())


    def test_enforce_mode_rejects_non_builder_agent_during_intake(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "takeover": False,
        }
        event = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Some Other Agent", "prompt": "work"},
        )
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertFalse(state["builder_invocation_seen"])

    def test_initial_builder_dispatch_is_marked_before_subagent_start(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "takeover": False,
        }
        event = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder", "prompt": "work"},
        )
        self.assertEqual(hook.pre_tool_decision(event, state, "enforce"), {})
        self.assertTrue(state["builder_invocation_seen"])
        self.assertEqual(state["phase"], "LUNA_DISPATCHED")

        second = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(second["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_command_merely_mentioning_metadata_is_not_metadata_only(self) -> None:
        event = self.event(
            "PreToolUse",
            tool_name="bash",
            tool_input={
                "command": "cat .otl-v2-1/controller-proposal.json && cat src.txt"
            },
        )
        self.assertFalse(hook.is_metadata_only(event))

    def test_file_operation_targeting_only_metadata_is_metadata_only(self) -> None:
        event = self.event(
            "PreToolUse",
            tool_name="edit_file",
            tool_input={"path": ".otl-v2-1/controller-proposal.json"},
        )
        self.assertTrue(hook.is_metadata_only(event))

    def test_nested_lookalike_metadata_directory_is_not_exempt(self) -> None:
        nested = self.workspace / "src" / ".otl-v2-1"
        nested.mkdir(parents=True)
        event = self.event(
            "PreToolUse",
            tool_name="edit_file",
            tool_input={"path": "src/.otl-v2-1/controller-proposal.json"},
        )
        self.assertFalse(hook.is_metadata_only(event))

    def test_absolute_root_metadata_path_is_exempt(self) -> None:
        event = self.event(
            "PreToolUse",
            tool_name="edit_file",
            tool_input={
                "path": str(self.workspace / ".otl-v2-1" / "controller-proposal.json"),
            },
        )
        self.assertTrue(hook.is_metadata_only(event))

    def test_final_reconcile_requires_exactly_one_builder_start(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)

        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {
            "disposition": "VERIFIED",
            "evidence_refs": ["E1"],
        }
        controller.atomic_json(proposal_path, proposal)

        state["phase"] = "ROOT_RECONCILE"
        state["builder_count"] = 0
        result, record = hook.final_reconcile(
            self.event("Stop", stop_hook_active=False),
            state,
        )
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(any("exactly one Luna Builder start" in e for e in result.errors))

    def test_final_reconcile_rejects_incomplete_builder_lifecycle(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.init_user_obligation(prompt, state)

        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {
            "disposition": "VERIFIED",
            "evidence_refs": ["E1"],
        }
        controller.atomic_json(proposal_path, proposal)

        state["builder_count"] = 1
        state["phase"] = "LUNA_MUTATING"
        result, record = hook.final_reconcile(
            self.event("Stop", stop_hook_active=False),
            state,
        )
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(any("terminal-reconcilable phase" in e for e in result.errors))


    def test_post_tool_catches_pre_builder_repository_work(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "takeover": False,
            "control_errors": [],
        }
        event = self.event(
            "PostToolUse",
            tool_name="read_file",
            tool_input={"path": "src.txt"},
            tool_response="ok",
        )
        errors = hook.observe_post_tool_phase(event, state)
        self.assertTrue(errors)
        self.assertTrue(any("before Builder ownership" in e for e in errors))
        self.assertTrue(state["control_errors"])

    def test_post_tool_marks_takeover_if_pretool_was_bypassed(self) -> None:
        state = {
            "phase": "ROOT_RECONCILE",
            "builder_count": 1,
            "builder_invocation_seen": True,
            "takeover": False,
            "control_errors": [],
            "obligations": {
                "U0": {"blocking": True, "required": True},
            },
        }
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        controller.atomic_json(
            proposal_path,
            {
                "requested_outcome": "COMPLETE",
                "current": {
                    "U0": {"disposition": "FAILED", "evidence_refs": []},
                },
                "discovered_obligations": [],
            },
        )
        event = self.event(
            "PostToolUse",
            tool_name="read_file",
            tool_input={"path": "src.txt"},
            tool_response="ok",
        )
        self.assertEqual(hook.observe_post_tool_phase(event, state), [])
        self.assertEqual(state["phase"], "TERRA_TAKEOVER")
        self.assertTrue(state["takeover"])
        self.assertEqual(state["takeover_basis_ids"], ["U0"])

    def test_post_tool_bypass_without_blocking_residual_is_control_error(self) -> None:
        state = {
            "phase": "ROOT_RECONCILE",
            "builder_count": 1,
            "builder_invocation_seen": True,
            "takeover": False,
            "control_errors": [],
            "obligations": {
                "U0": {"blocking": True, "required": True},
            },
        }
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        controller.atomic_json(
            proposal_path,
            {
                "requested_outcome": "COMPLETE",
                "current": {
                    "U0": {"disposition": "VERIFIED", "evidence_refs": ["E1"]},
                },
                "discovered_obligations": [],
            },
        )
        event = self.event(
            "PostToolUse",
            tool_name="read_file",
            tool_input={"path": "src.txt"},
            tool_response="ok",
        )
        errors = hook.observe_post_tool_phase(event, state)
        self.assertTrue(any("without a captured FAILED/UNRESOLVED" in e for e in errors))
        self.assertTrue(state["control_errors"])
        self.assertFalse(state["takeover"])

    def test_post_tool_rejects_agent_after_builder_if_pretool_was_bypassed(self) -> None:
        state = {
            "phase": "ROOT_RECONCILE",
            "builder_count": 1,
            "builder_invocation_seen": True,
            "takeover": False,
            "control_errors": [],
        }
        event = self.event(
            "PostToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
            tool_response="done",
        )
        errors = hook.observe_post_tool_phase(event, state)
        self.assertTrue(any("after the single Builder attempt" in e for e in errors))
        self.assertTrue(state["control_errors"])


    def test_malformed_json_stops_enforce_session(self) -> None:
        old_stdin = hook.sys.stdin
        old_mode = os.environ.get("OTL_V2_1_HOOK_MODE")
        os.environ["OTL_V2_1_HOOK_MODE"] = "enforce"
        hook.sys.stdin = io.StringIO("{not-json")
        self.addCleanup(setattr, hook.sys, "stdin", old_stdin)
        if old_mode is None:
            self.addCleanup(os.environ.pop, "OTL_V2_1_HOOK_MODE", None)
        else:
            self.addCleanup(os.environ.__setitem__, "OTL_V2_1_HOOK_MODE", old_mode)

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(hook.main(), 0)

        payload = json.loads(out.getvalue())
        self.assertIs(payload["continue"], False)
        self.assertIn("malformed hook input", payload["stopReason"])

    def test_non_object_input_stops_enforce_session(self) -> None:
        old_stdin = hook.sys.stdin
        old_mode = os.environ.get("OTL_V2_1_HOOK_MODE")
        os.environ["OTL_V2_1_HOOK_MODE"] = "enforce"
        hook.sys.stdin = io.StringIO("[]")
        self.addCleanup(setattr, hook.sys, "stdin", old_stdin)
        if old_mode is None:
            self.addCleanup(os.environ.pop, "OTL_V2_1_HOOK_MODE", None)
        else:
            self.addCleanup(os.environ.__setitem__, "OTL_V2_1_HOOK_MODE", old_mode)

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(hook.main(), 0)

        payload = json.loads(out.getvalue())
        self.assertIs(payload["continue"], False)
        self.assertIn("non-object hook input", payload["stopReason"])


    def test_noncomplete_controller_outcome_has_user_visible_warning(self) -> None:
        result = controller.Reconciliation("BLOCKED", (), ("U0",))
        output = hook.noncomplete_visibility_output(result)
        self.assertIn("systemMessage", output)
        self.assertIn("BLOCKED", output["systemMessage"])
        self.assertIn("not a trusted completion signal", output["systemMessage"])

    def test_complete_controller_outcome_has_no_warning(self) -> None:
        result = controller.Reconciliation("COMPLETE", (), ())
        self.assertEqual(hook.noncomplete_visibility_output(result), {})


    def test_invalid_phase_denies_enforce_tool(self) -> None:
        state = {
            "phase": "CORRUPT",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "takeover": False,
        }
        event = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
        )
        output = hook.pre_tool_decision(event, state, "enforce")
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("phase is invalid", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_invalid_final_phase_never_trusted_complete(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.handle_session_start(self.event("SessionStart"), state)
        hook.init_user_obligation(prompt, state)
        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {
            "disposition": "VERIFIED",
            "evidence_refs": ["E1"],
        }
        controller.atomic_json(proposal_path, proposal)
        state["builder_count"] = 1
        state["phase"] = "CORRUPT"

        result, record = hook.final_reconcile(
            self.event("Stop", stop_hook_active=False),
            state,
        )
        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(
            any("terminal-reconcilable phase" in e for e in result.errors)
        )

    def test_workspace_binding_drift_is_persisted(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "cwd": str(self.workspace),
            "control_errors": [],
        }
        other = Path(self.temp.name) / "other"
        other.mkdir()
        event = self.event("PreToolUse", cwd=str(other))
        errors = hook.validate_event_context(event, state)
        self.assertTrue(any("cwd drifted" in e for e in errors))
        self.assertTrue(state["control_errors"])

    def test_workspace_binding_match_is_clean(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "cwd": str(self.workspace),
            "control_errors": [],
        }
        self.assertEqual(
            hook.validate_event_context(self.event("PreToolUse"), state),
            [],
        )

    def test_unexpected_subagent_lifecycle_persists_control_error(self) -> None:
        state = {
            "control_errors": [],
        }
        event = self.event(
            "SubagentStart",
            agent_type="Other Agent",
        )
        hook.append_control_errors(
            state,
            ["unexpected non-Builder subagent started"],
            event=event,
        )
        self.assertTrue(
            any(
                item.get("error") == "unexpected non-Builder subagent started"
                for item in state["control_errors"]
            )
        )

    def test_post_tool_invalid_phase_persists_control_error(self) -> None:
        state = {
            "phase": "CORRUPT",
            "builder_count": 1,
            "takeover": False,
            "control_errors": [],
        }
        event = self.event(
            "PostToolUse",
            tool_name="read_file",
            tool_input={"path": "src.txt"},
            tool_response="ok",
        )
        errors = hook.observe_post_tool_phase(event, state)
        self.assertTrue(any("phase was invalid" in e for e in errors))
        self.assertTrue(state["control_errors"])


    def test_expected_builder_agent_posttool_is_not_second_subagent(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "builder_dispatch_count": 0,
            "builder_tool_use_id": None,
            "builder_agent_tool_completion_seen": False,
            "takeover": False,
            "control_errors": [],
        }
        dispatch = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
            tool_use_id="builder-call-1",
        )
        self.assertEqual(hook.observe_pre_tool_phase(dispatch, state), [])
        self.assertEqual(state["builder_dispatch_count"], 1)
        self.assertEqual(state["builder_tool_use_id"], "builder-call-1")

        state["builder_invocation_seen"] = True
        state["builder_count"] = 1
        state["phase"] = "ROOT_RECONCILE"
        completion = self.event(
            "PostToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
            tool_use_id="builder-call-1",
            tool_response="builder completed",
        )
        self.assertEqual(hook.observe_post_tool_phase(completion, state), [])
        self.assertTrue(state["builder_agent_tool_completion_seen"])
        self.assertEqual(state["control_errors"], [])

    def test_builder_agent_posttool_with_wrong_tool_id_is_rejected(self) -> None:
        state = {
            "phase": "ROOT_RECONCILE",
            "builder_count": 1,
            "builder_invocation_seen": True,
            "builder_dispatch_count": 1,
            "builder_tool_use_id": "builder-call-1",
            "builder_agent_tool_completion_seen": False,
            "takeover": False,
            "control_errors": [],
        }
        completion = self.event(
            "PostToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
            tool_use_id="other-call",
            tool_response="builder completed",
        )
        errors = hook.observe_post_tool_phase(completion, state)
        self.assertTrue(any("unexpected subagent tool" in e for e in errors))
        self.assertFalse(state["builder_agent_tool_completion_seen"])

    def test_second_builder_dispatch_attempt_is_persisted_in_audit_state(self) -> None:
        state = {
            "phase": "ROOT_INTAKE",
            "builder_count": 0,
            "builder_invocation_seen": False,
            "builder_dispatch_count": 0,
            "builder_tool_use_id": None,
            "builder_agent_tool_completion_seen": False,
            "takeover": False,
            "control_errors": [],
        }
        first = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
            tool_use_id="builder-call-1",
        )
        second = self.event(
            "PreToolUse",
            tool_name="agent",
            tool_input={"agent": "Premium v2.1 Luna Builder"},
            tool_use_id="builder-call-2",
        )
        self.assertEqual(hook.observe_pre_tool_phase(first, state), [])
        errors = hook.observe_pre_tool_phase(second, state)
        self.assertTrue(any("more than one Luna Builder dispatch" in e for e in errors))
        self.assertEqual(state["builder_dispatch_count"], 2)
        self.assertTrue(state["control_errors"])


    def test_final_reconcile_rejects_missing_builder_agent_tool_completion(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.handle_session_start(self.event("SessionStart"), state)
        hook.init_user_obligation(prompt, state)
        post = self.event(
            "PostToolUse",
            tool_name="execute",
            tool_input={"command": "python -m unittest"},
            tool_response="Process exited with code 0",
        )
        hook.record_post_tool(post, state)
        proposal_path, _, _ = hook.metadata_paths(self.workspace)
        proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
        proposal["current"]["U0"] = {
            "disposition": "VERIFIED",
            "evidence_refs": ["E1"],
        }
        controller.atomic_json(proposal_path, proposal)
        state["builder_dispatch_count"] = 1
        state["builder_count"] = 1
        state["builder_invocation_seen"] = True
        state["builder_agent_tool_completion_seen"] = False
        state["phase"] = "ROOT_RECONCILE"

        result, record = hook.final_reconcile(
            self.event("Stop", stop_hook_active=False),
            state,
        )

        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(
            any("agent-tool completion" in e for e in result.errors)
        )

    def test_final_reconcile_rejects_inconsistent_takeover_phase(self) -> None:
        prompt = self.event("UserPromptSubmit", prompt="Make the local check pass")
        state, _, _ = hook.ensure_state(prompt)
        hook.handle_session_start(self.event("SessionStart"), state)
        hook.init_user_obligation(prompt, state)
        state["builder_dispatch_count"] = 1
        state["builder_count"] = 1
        state["builder_invocation_seen"] = True
        state["builder_agent_tool_completion_seen"] = True
        state["phase"] = "TERRA_TAKEOVER"
        state["takeover"] = False
        state["takeover_basis_ids"] = []

        result, record = hook.final_reconcile(
            self.event("Stop", stop_hook_active=False),
            state,
        )

        self.assertEqual(result.outcome, "NO_VERIFIED_COMPLETION")
        self.assertFalse(record["trusted_complete"])
        self.assertTrue(any("takeover=true" in e for e in result.errors))
        self.assertTrue(any("captured takeover basis" in e for e in result.errors))


    def test_malformed_existing_external_state_is_not_reinitialized(self) -> None:
        event = self.event("SessionStart")
        state_path, _, _, _ = hook.session_paths(event)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text("{broken", encoding="utf-8")

        with self.assertRaises(ValueError):
            hook.ensure_state(event)

    def test_wrong_schema_existing_external_state_is_rejected(self) -> None:
        event = self.event("SessionStart")
        state_path, _, key, _ = hook.session_paths(event)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(
                {
                    "schema": "other",
                    "session_key": key,
                    "cwd": str(self.workspace),
                }
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            hook.ensure_state(event)

    def test_wrong_session_key_inside_existing_state_is_rejected(self) -> None:
        event = self.event("SessionStart")
        state_path, _, _, _ = hook.session_paths(event)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(
                {
                    "schema": "premium-v2.1-session-v1",
                    "session_key": "forged",
                    "cwd": str(self.workspace),
                }
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            hook.ensure_state(event)


if __name__ == "__main__":
    unittest.main()
