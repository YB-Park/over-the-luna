from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "premium_v2_1_trace_report.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


reporter = load_module("premium_v2_1_trace_report", SCRIPT)


class PremiumV21TraceReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state_dir = self.root / "state"
        self.state_dir.mkdir()
        self.workspace = self.root / "workspace"
        (self.workspace / ".otl-v2-1").mkdir(parents=True)

    def write_jsonl(self, path: Path, rows: list[dict]) -> None:
        path.write_text(
            "".join(json.dumps(row) + "\n" for row in rows),
            encoding="utf-8",
        )

    def complete_hook_events(self) -> list[dict]:
        base = {"session_id": "session-1", "cwd": str(self.workspace)}
        return [
            {**base, "hook_event_name": "SessionStart"},
            {**base, "hook_event_name": "UserPromptSubmit", "prompt": "Fix increment"},
            {
                **base,
                "hook_event_name": "PreToolUse",
                "tool_name": "agent",
                "tool_input": {"agent": "Premium v2.1 Luna Builder"},
            },
            {
                **base,
                "hook_event_name": "SubagentStart",
                "agent_type": "custom",
                "agent_name": "Premium v2.1 Luna Builder",
            },
            {
                **base,
                "hook_event_name": "PostToolUse",
                "tool_name": "execute",
                "tool_response": "Process exited with code 0",
            },
            {
                **base,
                "hook_event_name": "SubagentStop",
                "agent_type": "custom",
                "agent_name": "Premium v2.1 Luna Builder",
            },
            {**base, "hook_event_name": "Stop", "stop_hook_active": False},
        ]

    def write_controller_state(self) -> None:
        revision = reporter.workspace_digest(self.workspace)
        state = {
            "receipts": {
                "E1": {
                    "collection_status": "COLLECTED",
                    "result_class": "PASS",
                }
            },
            "final_record": {
                "schema": "premium-v2.1-final-v1",
                "run_id": "session-1",
                "workspace_revision": revision,
                "phase": "ROOT_RECONCILE",
                "builder_count": 1,
                "takeover": False,
                "outcome": "COMPLETE",
                "trusted_complete": True,
            },
        }
        (self.state_dir / "session.json").write_text(
            json.dumps(state),
            encoding="utf-8",
        )
        (self.workspace / ".otl-v2-1" / "final-record.json").write_text(
            json.dumps(state["final_record"]),
            encoding="utf-8",
        )

    def write_cli_identity(self, *, builder_model: str = "gpt-5.6-luna") -> Path:
        path = self.root / "cli.jsonl"
        self.write_jsonl(
            path,
            [
                {"type": "model.call_start", "data": {"model": "gpt-5.6-terra"}},
                {
                    "type": "subagent.completed",
                    "data": {
                        "agentDisplayName": "Premium v2.1 Luna Builder",
                        "model": builder_model,
                        "totalToolCalls": 3,
                    },
                },
                {"type": "session.usage_checkpoint", "data": {"totalNanoAiu": 2_500_000_000}},
            ],
        )
        return path

    def write_otel_identity(
        self,
        *,
        root_model: str = "gpt-5.6-terra",
        builder_model: str = "gpt-5.6-luna",
    ) -> Path:
        path = self.root / "otel.jsonl"
        self.write_jsonl(
            path,
            [
                {
                    "type": "span",
                    "name": "invoke_agent Premium Cascade v2.1",
                    "spanId": "root-invoke",
                    "attributes": {
                        "gen_ai.operation.name": "invoke_agent",
                        "gen_ai.agent.name": "Premium Cascade v2.1 (Experimental)",
                        "gen_ai.request.model": "gpt-5.6-terra",
                        "server.address": "api.githubcopilot.com",
                        "github.copilot.nano_aiu": 2_500_000_000,
                    },
                },
                {
                    "type": "span",
                    "name": f"chat {root_model}",
                    "spanId": "root-chat",
                    "parentSpanId": "root-invoke",
                    "attributes": {
                        "gen_ai.operation.name": "chat",
                        "gen_ai.request.model": "gpt-5.6-terra",
                        "gen_ai.response.model": root_model,
                    },
                },
                {
                    "type": "span",
                    "name": "invoke_agent Premium v2.1 Luna Builder",
                    "spanId": "builder-invoke",
                    "parentSpanId": "root-invoke",
                    "attributes": {
                        "gen_ai.operation.name": "invoke_agent",
                        "gen_ai.agent.name": "Premium v2.1 Luna Builder",
                        "gen_ai.request.model": "gpt-5.6-luna",
                    },
                },
                {
                    "type": "span",
                    "name": f"chat {builder_model}",
                    "spanId": "builder-chat",
                    "parentSpanId": "builder-invoke",
                    "attributes": {
                        "gen_ai.operation.name": "chat",
                        "gen_ai.request.model": "gpt-5.6-luna",
                        "gen_ai.response.model": builder_model,
                    },
                },
            ],
        )
        return path

    def test_complete_audit_trace_is_enforce_candidate(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["hook_trace"]["missing_expected_events"], [])
        self.assertTrue(report["delegation"]["exactly_one_complete_builder_lifecycle"])
        self.assertEqual(report["backend_identity"]["root_terra"], "OBSERVED")
        self.assertEqual(report["backend_identity"]["builder_luna"], "OBSERVED")
        self.assertTrue(report["calibration"]["ready_for_enforce_mode_candidate"])
        self.assertEqual(report["cli"]["usage_credits"], 2.5)

    def test_missing_builder_stop_fails_closed(self) -> None:
        events = [
            event
            for event in self.complete_hook_events()
            if event.get("hook_event_name") != "SubagentStop"
        ]
        self.write_jsonl(self.state_dir / "session.events.jsonl", events)
        self.write_controller_state()
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["delegation"]["status"], "NOT_OBSERVED")
        self.assertIn("SubagentStop", report["hook_trace"]["missing_expected_events"])
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_wrong_builder_model_does_not_establish_backend_identity(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity(builder_model="gpt-5.6-terra")
        otel = self.write_otel_identity(builder_model="gpt-5.6-terra")

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["backend_identity"]["root_terra"], "OBSERVED")
        self.assertEqual(report["backend_identity"]["builder_luna"], "CONFLICT")
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_camelcase_cli_event_names_are_normalized(self) -> None:
        base = {"sessionId": "session-1"}
        events = [
            {**base, "eventName": "sessionStart"},
            {**base, "eventName": "userPromptSubmitted"},
            {**base, "eventName": "preToolUse"},
            {**base, "eventName": "postToolUse"},
            {
                **base,
                "eventName": "subagentStart",
                "agentType": "custom",
                "agentName": "Premium v2.1 Luna Builder",
            },
            {
                **base,
                "eventName": "subagentStop",
                "agentType": "custom",
                "agentName": "Premium v2.1 Luna Builder",
            },
            {**base, "eventName": "agentStop"},
        ]
        self.write_jsonl(self.state_dir / "session.events.jsonl", events)
        self.write_controller_state()
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["hook_trace"]["missing_expected_events"], [])
        self.assertTrue(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_agent_host_invoke_spans_can_establish_resolved_identity(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity()
        otel = self.root / "invoke-only-otel.jsonl"
        self.write_jsonl(
            otel,
            [
                {
                    "type": "span",
                    "spanId": "root",
                    "attributes": {
                        "gen_ai.operation.name": "invoke_agent",
                        "gen_ai.agent.name": "Premium Cascade v2.1 (Experimental)",
                        "gen_ai.request.model": "gpt-5.6-terra",
                        "gen_ai.response.model": "gpt-5.6-terra",
                    },
                },
                {
                    "type": "span",
                    "spanId": "builder",
                    "parentSpanId": "root",
                    "attributes": {
                        "gen_ai.operation.name": "invoke_agent",
                        "gen_ai.agent.name": "Premium v2.1 Luna Builder",
                        "gen_ai.request.model": "gpt-5.6-luna",
                        "gen_ai.response.model": "gpt-5.6-luna",
                    },
                },
            ],
        )

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["otel"]["root_invoke_selection"], "named_root_agent")
        self.assertEqual(report["backend_identity"]["root_terra"], "OBSERVED")
        self.assertEqual(report["backend_identity"]["builder_luna"], "OBSERVED")
        self.assertTrue(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_unscoped_legacy_terra_event_does_not_prove_root_identity(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, None)

        self.assertEqual(report["backend_identity"]["root_terra"], "NOT_OBSERVED")
        self.assertEqual(
            report["backend_identity"]["legacy_unscoped_model_call_models"],
            ["gpt-5.6-terra"],
        )
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_wrong_root_resolved_model_is_conflict(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity()
        otel = self.write_otel_identity(root_model="gpt-5.6-luna")

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["backend_identity"]["root_terra"], "CONFLICT")
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_multiple_state_sessions_require_explicit_selection(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        other_events = [
            {**event, "session_id": "session-2"}
            for event in self.complete_hook_events()
        ]
        self.write_jsonl(self.state_dir / "other.events.jsonl", other_events)
        (self.state_dir / "other.json").write_text(
            json.dumps({"final_record": {"schema": "premium-v2.1-final-v1"}}),
            encoding="utf-8",
        )
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertTrue(report["session_selection"]["ambiguous"])
        self.assertIsNone(report["session_selection"]["selected_key"])
        self.assertEqual(report["hook_trace"]["event_count"], 0)
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_explicit_session_key_selects_one_runtime(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        self.write_jsonl(
            self.state_dir / "other.events.jsonl",
            [{"session_id": "session-2", "hook_event_name": "SessionStart"}],
        )
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(
            self.state_dir,
            self.workspace,
            cli,
            otel,
            "session",
        )

        self.assertEqual(report["session_selection"]["selected_key"], "session")
        self.assertFalse(report["session_selection"]["ambiguous"])
        self.assertTrue(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_noncomplete_final_record_blocks_enforce_candidate(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        state_path = self.state_dir / "session.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["final_record"]["outcome"] = "BLOCKED"
        state["final_record"]["trusted_complete"] = False
        state_path.write_text(json.dumps(state), encoding="utf-8")
        (self.workspace / ".otl-v2-1" / "final-record.json").write_text(
            json.dumps(state["final_record"]),
            encoding="utf-8",
        )
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["controller"]["final_record_status"], "VALID_NONCOMPLETE")
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_wrong_run_final_record_is_invalid(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        state_path = self.state_dir / "session.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["final_record"]["run_id"] = "other-session"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        (self.workspace / ".otl-v2-1" / "final-record.json").write_text(
            json.dumps(state["final_record"]),
            encoding="utf-8",
        )
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["controller"]["final_record_status"], "INVALID")
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])


    def test_workspace_change_after_final_record_is_invalid(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        (self.workspace / "changed.txt").write_text("changed\n", encoding="utf-8")
        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["controller"]["final_record_status"], "INVALID")
        self.assertTrue(
            any(
                "stale for current workspace" in error
                for item in report["controller"]["final_record_assessments"]
                for error in item["errors"]
            )
        )
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_conflicting_workspace_and_external_final_records_fail_closed(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        state = json.loads((self.state_dir / "session.json").read_text(encoding="utf-8"))
        workspace_record = dict(state["final_record"])
        workspace_record["outcome"] = "BLOCKED"
        workspace_record["trusted_complete"] = False
        (self.workspace / ".otl-v2-1" / "final-record.json").write_text(
            json.dumps(workspace_record),
            encoding="utf-8",
        )
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertEqual(report["controller"]["final_record_status"], "CONFLICT")
        self.assertEqual(len(report["controller"]["final_records"]), 2)
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_duplicate_session_start_is_not_single_mission_calibration(self) -> None:
        events = self.complete_hook_events()
        events.insert(1, {**events[0]})
        self.write_jsonl(self.state_dir / "session.events.jsonl", events)
        self.write_controller_state()
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertFalse(report["hook_trace"]["single_mission_counts_valid"])
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])


    def test_missing_workspace_final_copy_blocks_calibration(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        (self.workspace / ".otl-v2-1" / "final-record.json").unlink()
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertFalse(
            report["controller"]["final_record_sources"]["both_expected_copies_present"]
        )
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_missing_external_final_copy_blocks_calibration(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        state_path = self.state_dir / "session.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.pop("final_record")
        state_path.write_text(json.dumps(state), encoding="utf-8")
        cli = self.write_cli_identity()
        otel = self.write_otel_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli, otel)

        self.assertFalse(
            report["controller"]["final_record_sources"]["both_expected_copies_present"]
        )
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])


if __name__ == "__main__":
    unittest.main()
