from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "premium_v2_1_local_preflight.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


preflight = load_module("premium_v2_1_local_preflight", SCRIPT)


class PremiumV21LocalPreflightTests(unittest.TestCase):
    def test_experimental_plugin_contract_is_valid_and_audit_only(self) -> None:
        result = preflight.inspect_experimental_plugin()
        self.assertTrue(result["observed"])
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["hook_mode"], "audit")

    def test_agent_scoped_hook_setting_is_not_plugin_readiness_gate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            workspace = root / "workspace"
            workspace.mkdir()
            settings = root / "settings.json"
            settings.write_text(
                json.dumps({"chat.useCustomAgentHooks": False}),
                encoding="utf-8",
            )

            def fake_run(argv: list[str]):
                if "--version" in argv:
                    return {
                        "observed": True,
                        "command": argv,
                        "exit_code": 0,
                        "stdout": "1.134.0\ncommit\nx64",
                        "stderr": "",
                    }
                return {
                    "observed": True,
                    "command": argv,
                    "exit_code": 0,
                    "stdout": "",
                    "stderr": "",
                }

            output = io.StringIO()
            with (
                mock.patch.object(preflight.shutil, "which", return_value="/fake/code"),
                mock.patch.object(preflight, "run_command", side_effect=fake_run),
                contextlib.redirect_stdout(output),
            ):
                rc = preflight.main(
                    [
                        "--workspace",
                        str(workspace),
                        "--settings",
                        str(settings),
                    ]
                )

            self.assertEqual(rc, 0)
            report = json.loads(output.getvalue())
            scoped = report["settings_observations"]["agent_scoped_hooks"]
            self.assertTrue(scoped["observed_false_somewhere"])
            self.assertFalse(scoped["required_for_plugin_level_hooks"])
            self.assertEqual(
                report["configuration_status"],
                "READY_FOR_PLUGIN_INSTALL_OR_LIVE_AUDIT",
            )


    def test_windows_hook_interpreter_matches_hooks_json_command(self) -> None:
        with (
            mock.patch.object(preflight.platform, "system", return_value="Windows"),
            mock.patch.object(preflight.shutil, "which", return_value="C:/Python/py.exe"),
            mock.patch.object(
                preflight,
                "run_command",
                return_value={
                    "observed": True,
                    "command": ["C:/Python/py.exe", "-3", "--version"],
                    "exit_code": 0,
                    "stdout": "Python 3.12",
                    "stderr": "",
                },
            ),
        ):
            result = preflight.hook_interpreter_probe()

        self.assertEqual(
            result["command"],
            ["C:/Python/py.exe", "-3", "--version"],
        )
        self.assertIn("py -3", result["expected_hook_command"])
        self.assertEqual(result["exit_code"], 0)

    def test_unix_hook_interpreter_missing_is_not_observed(self) -> None:
        with (
            mock.patch.object(preflight.platform, "system", return_value="Linux"),
            mock.patch.object(preflight.shutil, "which", return_value=None),
        ):
            result = preflight.hook_interpreter_probe()

        self.assertFalse(result["observed"])
        self.assertIn("python3", result["expected_hook_command"])
        self.assertIn("not found", result["error"])


if __name__ == "__main__":
    unittest.main()
