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
        state = {
            "receipts": {
                "E1": {
                    "collection_status": "COLLECTED",
                    "result_class": "PASS",
                }
            },
            "final_record": {
                "schema": "premium-v2.1-final-v1",
                "outcome": "COMPLETE",
                "trusted_complete": True,
            },
        }
        (self.state_dir / "session.json").write_text(
            json.dumps(state),
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

    def test_complete_audit_trace_is_enforce_candidate(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli)

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

        report = reporter.summarize(self.state_dir, self.workspace, cli)

        self.assertEqual(report["delegation"]["status"], "NOT_OBSERVED")
        self.assertIn("SubagentStop", report["hook_trace"]["missing_expected_events"])
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_wrong_builder_model_does_not_establish_backend_identity(self) -> None:
        self.write_jsonl(self.state_dir / "session.events.jsonl", self.complete_hook_events())
        self.write_controller_state()
        cli = self.write_cli_identity(builder_model="gpt-5.6-terra")

        report = reporter.summarize(self.state_dir, self.workspace, cli)

        self.assertEqual(report["backend_identity"]["root_terra"], "OBSERVED")
        self.assertEqual(report["backend_identity"]["builder_luna"], "NOT_OBSERVED")
        self.assertFalse(report["calibration"]["ready_for_enforce_mode_candidate"])

    def test_camelcase_cli_event_names_are_normalized(self) -> None:
        events = [
            {"eventName": "sessionStart"},
            {"eventName": "userPromptSubmitted"},
            {"eventName": "preToolUse"},
            {"eventName": "postToolUse"},
            {
                "eventName": "subagentStart",
                "agentType": "custom",
                "agentName": "Premium v2.1 Luna Builder",
            },
            {
                "eventName": "subagentStop",
                "agentType": "custom",
                "agentName": "Premium v2.1 Luna Builder",
            },
            {"eventName": "agentStop"},
        ]
        self.write_jsonl(self.state_dir / "session.events.jsonl", events)
        self.write_controller_state()
        cli = self.write_cli_identity()

        report = reporter.summarize(self.state_dir, self.workspace, cli)

        self.assertEqual(report["hook_trace"]["missing_expected_events"], [])
        self.assertTrue(report["calibration"]["ready_for_enforce_mode_candidate"])


if __name__ == "__main__":
    unittest.main()
