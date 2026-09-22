from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "premium_v2_1_make_smoke_workspace.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


smoke = load_module("premium_v2_1_make_smoke_workspace", SCRIPT)


class PremiumV21SmokeWorkspaceTests(unittest.TestCase):
    def test_fixture_starts_with_one_focused_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workspace = Path(td) / "smoke"
            result = smoke.create_workspace(workspace)

            self.assertEqual(result["purpose"], "runtime calibration only; never product scoring")
            intent = (workspace / ".premium-v2-1-smoke.json").read_text(encoding="utf-8")
            self.assertIn('"promotion holdout"', intent)
            settings = json.loads(
                (workspace / ".vscode" / "settings.json").read_text(encoding="utf-8")
            )
            self.assertIs(settings["chat.plugins.enabled"], True)
            self.assertEqual(
                settings["chat.pluginLocations"],
                {str(smoke.PLUGIN): True},
            )
            self.assertEqual(result["plugin_location"], str(smoke.PLUGIN))
            self.assertIs(settings["github.copilot.chat.otel.enabled"], True)
            self.assertEqual(
                settings["github.copilot.chat.otel.exporterType"],
                "file",
            )
            self.assertIs(
                settings["github.copilot.chat.otel.captureContent"],
                False,
            )
            otel_output = Path(settings["github.copilot.chat.otel.outfile"])
            self.assertEqual(otel_output, Path(result["otel_output"]))
            self.assertNotEqual(otel_output.parent, workspace)
            self.assertFalse(str(otel_output).startswith(str(workspace) + os.sep))

            proc = subprocess.run(
                [sys.executable, "-m", "unittest", "-v"],
                cwd=workspace,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("test_increment", proc.stderr + proc.stdout)

    def test_refuses_to_overwrite_nonempty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workspace = Path(td) / "smoke"
            workspace.mkdir()
            (workspace / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(ValueError):
                smoke.create_workspace(workspace)


if __name__ == "__main__":
    unittest.main()
