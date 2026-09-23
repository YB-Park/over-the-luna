from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "premium_v2_1_collect_smoke_evidence.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


collector = load_module("premium_v2_1_collect_smoke_evidence", SCRIPT)


class PremiumV21SmokeEvidenceCollectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.state_dir = self.root / "state"
        self.state_dir.mkdir()
        self.output = self.root / "evidence"
        self.otel = self.root / "smoke-otel.jsonl"

        (self.workspace / ".premium-v2-1-smoke.json").write_text(
            json.dumps(collector.smoke_fixture.INTENT, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        vscode = self.workspace / ".vscode"
        vscode.mkdir()
        (vscode / "settings.json").write_text(
            json.dumps(
                {
                    "github.copilot.chat.otel.outfile": str(self.otel),
                }
            ),
            encoding="utf-8",
        )
        meta = self.workspace / ".otl-v2-1"
        meta.mkdir()
        for name in (
            "controller-proposal.json",
            "receipt-index.json",
            "final-record.json",
        ):
            (meta / name).write_text("{}\n", encoding="utf-8")

        (self.workspace / "counter.py").write_text(
            collector.smoke_fixture.COUNTER.replace("return value - 1", "return value + 1"),
            encoding="utf-8",
        )
        (self.workspace / "test_counter.py").write_text(
            collector.smoke_fixture.TEST,
            encoding="utf-8",
        )
        self.otel.write_text("{}\n", encoding="utf-8")

    def write_session(self, key: str, *, cwd: Path | None = None) -> None:
        target = cwd or self.workspace
        events = [
            {
                "hook_event_name": "SessionStart",
                "session_id": f"session-{key}",
                "cwd": str(target),
            }
        ]
        (self.state_dir / f"{key}.events.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in events),
            encoding="utf-8",
        )
        (self.state_dir / f"{key}.json").write_text(
            json.dumps({"schema": "premium-v2.1-session-v1"}),
            encoding="utf-8",
        )

    def test_collects_matching_session_and_hash_manifest(self) -> None:
        self.write_session("abc")

        manifest = collector.collect(
            self.workspace,
            state_dir=self.state_dir,
            output=self.output,
        )

        self.assertEqual(manifest["selected_session_key"], "abc")
        self.assertEqual(manifest["focused_test_exit"], 0)
        self.assertTrue(manifest["trace_snapshot_before_collector_test"])
        self.assertTrue((self.output / "trace-report.json").exists())
        self.assertTrue((self.output / "manifest.json").exists())
        self.assertIn("raw/hook_events.jsonl", manifest["artifacts"])
        self.assertEqual(
            len(manifest["artifacts"]["raw/hook_events.jsonl"]["sha256"]),
            64,
        )

    def test_refuses_ambiguous_matching_sessions(self) -> None:
        self.write_session("abc")
        self.write_session("def")

        with self.assertRaises(ValueError):
            collector.collect(
                self.workspace,
                state_dir=self.state_dir,
                output=self.output,
            )

    def test_explicit_session_key_resolves_ambiguity(self) -> None:
        self.write_session("abc")
        self.write_session("def")

        manifest = collector.collect(
            self.workspace,
            state_dir=self.state_dir,
            output=self.output,
            session_key="def",
        )
        self.assertEqual(manifest["selected_session_key"], "def")

    def test_refuses_non_smoke_workspace(self) -> None:
        (self.workspace / ".premium-v2-1-smoke.json").write_text(
            json.dumps({"schema": "other"}),
            encoding="utf-8",
        )
        self.write_session("abc")

        with self.assertRaises(ValueError):
            collector.collect(
                self.workspace,
                state_dir=self.state_dir,
                output=self.output,
            )

    def test_refuses_missing_otel(self) -> None:
        self.write_session("abc")
        self.otel.unlink()

        with self.assertRaises(ValueError):
            collector.collect(
                self.workspace,
                state_dir=self.state_dir,
                output=self.output,
            )


    def test_refuses_evidence_output_inside_workspace(self) -> None:
        self.write_session("abc")
        inside = self.workspace / "evidence"

        with self.assertRaises(ValueError):
            collector.collect(
                self.workspace,
                state_dir=self.state_dir,
                output=inside,
            )


    def test_refuses_changed_focused_test_asset(self) -> None:
        self.write_session("abc")
        (self.workspace / "test_counter.py").write_text(
            "import unittest\n",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            collector.collect(
                self.workspace,
                state_dir=self.state_dir,
                output=self.output,
            )


if __name__ == "__main__":
    unittest.main()
