#!/usr/bin/env python3
"""Create the tiny, non-heldout Premium v2.1 runtime smoke workspace.

This fixture is intentionally synthetic. It must never be counted as a product
benchmark or promotion holdout.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = (ROOT / "experiments" / "premium_v2_1_plugin").resolve()


COUNTER = '''def increment(value: int) -> int:
    """Return value incremented by one."""
    return value - 1
'''

TEST = '''import unittest

from counter import increment


class CounterTests(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(increment(4), 5)
        self.assertEqual(increment(-1), 0)


if __name__ == "__main__":
    unittest.main()
'''

INTENT = {
    "schema": "premium-v2.1-runtime-smoke-fixture-v1",
    "purpose": "runtime calibration only; never product scoring",
    "expected_initial_test": "FAIL",
    "minimal_expected_patch": "return value + 1",
    "prohibited_use": [
        "promotion holdout",
        "capability win",
        "cost frontier claim",
    ],
}


def create_workspace(output: Path) -> dict[str, object]:
    output = output.expanduser().resolve()
    otel_output = (output.parent / f"{output.name}-copilot-otel.jsonl").resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"refusing non-empty smoke workspace: {output}")
    if otel_output.exists():
        raise ValueError(
            f"refusing existing smoke OTel output; archive/remove it first: {otel_output}"
        )
    output.mkdir(parents=True, exist_ok=True)

    (output / "counter.py").write_text(COUNTER, encoding="utf-8")
    (output / "test_counter.py").write_text(TEST, encoding="utf-8")
    (output / ".premium-v2-1-smoke.json").write_text(
        json.dumps(INTENT, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    vscode = output / ".vscode"
    vscode.mkdir(exist_ok=True)
    (vscode / "settings.json").write_text(
        json.dumps(
            {
                "chat.plugins.enabled": True,
                "chat.pluginLocations": {
                    str(PLUGIN): True,
                },
                "github.copilot.chat.otel.enabled": True,
                "github.copilot.chat.otel.exporterType": "file",
                "github.copilot.chat.otel.outfile": str(otel_output),
                "github.copilot.chat.otel.captureContent": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    git = shutil.which("git")
    git_initialized = False
    if git:
        init = subprocess.run(
            [git, "init", "-q"],
            cwd=output,
            check=False,
            capture_output=True,
            text=True,
        )
        if init.returncode == 0:
            subprocess.run(
                [
                    git,
                    "add",
                    "counter.py",
                    "test_counter.py",
                    ".premium-v2-1-smoke.json",
                    ".vscode/settings.json",
                ],
                cwd=output,
                check=True,
            )
            subprocess.run(
                [
                    git,
                    "-c",
                    "user.name=Premium v2.1 smoke",
                    "-c",
                    "user.email=smoke@example.invalid",
                    "commit",
                    "-qm",
                    "synthetic runtime smoke baseline",
                ],
                cwd=output,
                check=True,
            )
            git_initialized = True

    return {
        "workspace": str(output),
        "git_initialized": git_initialized,
        "purpose": INTENT["purpose"],
        "plugin_location": str(PLUGIN),
        "vscode_workspace_setting": str(vscode / "settings.json"),
        "otel_output": str(otel_output),
        "next_check": f"cd {output} && python -m unittest -v",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = create_workspace(args.output)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
