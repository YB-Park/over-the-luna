#!/usr/bin/env python3
"""Zero-AI local runtime preflight for Premium v2.1.

This script never invokes Copilot chat/models. It records only host/configuration
facts that can be observed without an AI session. Live delegation, hook firing,
model identity, and model-command sandbox behavior remain NOT_OBSERVED until a
separately authorized development run.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

HOOK_SETTING = "chat.useCustomAgentHooks"


def run_command(argv: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "observed": False,
            "command": argv,
            "error": str(exc),
        }
    return {
        "observed": True,
        "command": argv,
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def candidate_settings_paths(workspace: Path | None) -> list[Path]:
    paths: list[Path] = []
    if workspace is not None:
        paths.append(workspace / ".vscode" / "settings.json")

    home = Path.home()
    system = platform.system()
    if system == "Darwin":
        paths.append(home / "Library" / "Application Support" / "Code" / "User" / "settings.json")
    elif system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            paths.append(Path(appdata) / "Code" / "User" / "settings.json")
    else:
        paths.append(home / ".config" / "Code" / "User" / "settings.json")
    return paths


def scan_hook_setting(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "value": None}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "path": str(path),
            "exists": True,
            "value": None,
            "error": str(exc),
        }

    # JSONC-safe narrow extraction. We deliberately do not claim full settings
    # precedence/profile resolution from this textual observation.
    matches = re.findall(
        r'["\']chat\.useCustomAgentHooks["\']\s*:\s*(true|false)',
        text,
        flags=re.IGNORECASE,
    )
    value: bool | None
    if not matches:
        value = None
    else:
        value = matches[-1].lower() == "true"
    return {
        "path": str(path),
        "exists": True,
        "value": value,
        "matches": len(matches),
    }


def structural_state_location(
    workspace: Path | None,
    state_dir: Path | None,
) -> dict[str, Any]:
    if state_dir is None:
        return {
            "observed": False,
            "status": "NOT_OBSERVED",
            "note": "No controller state directory was supplied.",
        }
    resolved_state = state_dir.expanduser().resolve()
    result: dict[str, Any] = {
        "observed": True,
        "path": str(resolved_state),
        "outside_workspace": None,
        "tamper_protection": "NOT_OBSERVED",
    }
    if workspace is not None:
        resolved_workspace = workspace.expanduser().resolve()
        try:
            resolved_state.relative_to(resolved_workspace)
        except ValueError:
            result["outside_workspace"] = True
        else:
            result["outside_workspace"] = False
    result["note"] = (
        "Outside-workspace placement is only structural separation. It does not "
        "prove that an agent execute tool cannot read or overwrite this path."
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--settings", type=Path, action="append", default=[])
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--code-command", default="code")
    args = parser.parse_args(argv)

    workspace = args.workspace.expanduser().resolve() if args.workspace else None

    code_path = shutil.which(args.code_command)
    code_version = (
        run_command([code_path, "--version"])
        if code_path
        else {
            "observed": False,
            "command": [args.code_command, "--version"],
            "error": "VS Code command not found on PATH",
        }
    )
    extensions = (
        run_command([code_path, "--list-extensions", "--show-versions"])
        if code_path
        else {
            "observed": False,
            "command": [args.code_command, "--list-extensions", "--show-versions"],
            "error": "VS Code command not found on PATH",
        }
    )

    copilot_versions: list[str] = []
    if extensions.get("observed") and extensions.get("exit_code") == 0:
        for line in str(extensions.get("stdout", "")).splitlines():
            lower = line.lower()
            if lower.startswith("github.copilot@") or lower.startswith("github.copilot-chat@"):
                copilot_versions.append(line.strip())

    settings_paths = list(args.settings)
    settings_paths.extend(candidate_settings_paths(workspace))
    deduped: list[Path] = []
    seen: set[str] = set()
    for path in settings_paths:
        key = str(path.expanduser().resolve())
        if key not in seen:
            seen.add(key)
            deduped.append(Path(key))

    settings = [scan_hook_setting(path) for path in deduped]
    observed_hook_true = any(item.get("value") is True for item in settings)
    observed_hook_false = any(item.get("value") is False for item in settings)

    report = {
        "schema": "premium-v2.1-local-preflight-v1",
        "zero_ai": True,
        "host": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "cwd": os.getcwd(),
        },
        "workspace": str(workspace) if workspace else None,
        "vscode": {
            "command_path": code_path,
            "version_command": code_version,
            "extension_command": extensions,
            "copilot_extensions": copilot_versions,
        },
        "agent_scoped_hooks_setting": {
            "setting": HOOK_SETTING,
            "files_scanned": settings,
            "observed_true_somewhere": observed_hook_true,
            "observed_false_somewhere": observed_hook_false,
            "effective_value": "NOT_PROVEN_BY_TEXT_SCAN",
        },
        "controller_state_location": structural_state_location(
            workspace,
            args.state_dir,
        ),
        "not_observed_without_live_ai_session": [
            "actual root backend model identity",
            "actual Luna child backend model identity",
            "live Terra-to-Luna delegation",
            "live Stop/SubagentStop hook firing",
            "model compliance with bounded Terra intake",
            "model-command filesystem/network sandbox enforcement",
            "background-writer quiescence during a real subagent transfer",
        ],
    }

    prerequisites = {
        "vscode_cli_observed": bool(
            code_version.get("observed") and code_version.get("exit_code") == 0
        ),
        "copilot_extension_observed": bool(copilot_versions),
        "agent_scoped_hooks_setting_observed_true": observed_hook_true,
    }
    report["configuration_prerequisites"] = prerequisites
    report["configuration_status"] = (
        "READY_FOR_NON_AI_HOOK_DIAGNOSTIC"
        if all(prerequisites.values())
        else "INCOMPLETE_OR_NOT_OBSERVED"
    )

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
