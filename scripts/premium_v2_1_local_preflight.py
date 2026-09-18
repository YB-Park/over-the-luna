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

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "experiments" / "premium_v2_1_plugin"
AGENT_SCOPED_HOOK_SETTING = "chat.useCustomAgentHooks"
EXPECTED_PLUGIN_HOOKS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "SubagentStart",
    "SubagentStop",
    "Stop",
}


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


def inspect_experimental_plugin() -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": str(PLUGIN),
        "observed": False,
        "valid": False,
        "format": "copilot",
        "hook_mode": None,
        "errors": [],
    }
    manifest_path = PLUGIN / "plugin.json"
    hooks_path = PLUGIN / "hooks.json"
    if not manifest_path.exists() or not hooks_path.exists():
        result["errors"].append("experimental plugin manifest/hooks.json missing")
        return result
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result["errors"].append(str(exc))
        return result

    result["observed"] = True
    if manifest.get("$schema"):
        result["errors"].append("experiment must remain legacy Copilot-format during this calibration")
    if manifest.get("name") != "over-the-luna-premium-v2-1-experiment":
        result["errors"].append("unexpected experimental plugin name")
    if manifest.get("agents") != "agents/":
        result["errors"].append("experimental plugin agents path drifted")
    if manifest.get("hooks") != "hooks.json":
        result["errors"].append("experimental plugin must reference root hooks.json")

    hook_map = hooks.get("hooks") if isinstance(hooks, dict) else None
    if not isinstance(hook_map, dict):
        result["errors"].append("hooks.json missing hooks object")
        return result
    if set(hook_map) != EXPECTED_PLUGIN_HOOKS:
        result["errors"].append("plugin hook event set drifted")

    modes: set[str] = set()
    for event, entries in hook_map.items():
        if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
            result["errors"].append(f"{event}: expected exactly one command hook")
            continue
        item = entries[0]
        if item.get("type") != "command":
            result["errors"].append(f"{event}: hook must be command type")
        if "${PLUGIN_ROOT}/scripts/hook.py" not in str(item.get("command", "")):
            result["errors"].append(f"{event}: plugin-local hook.py is not referenced")
        env = item.get("env")
        if isinstance(env, dict) and isinstance(env.get("OTL_V2_1_HOOK_MODE"), str):
            modes.add(env["OTL_V2_1_HOOK_MODE"].lower())
        else:
            result["errors"].append(f"{event}: OTL_V2_1_HOOK_MODE missing")

    result["hook_mode"] = next(iter(modes)) if len(modes) == 1 else sorted(modes)
    if modes != {"audit"}:
        result["errors"].append("pre-calibration plugin hooks must remain in audit mode")
    result["valid"] = not result["errors"]
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
    plugin_contract = inspect_experimental_plugin()

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
            "setting": AGENT_SCOPED_HOOK_SETTING,
            "files_scanned": settings,
            "observed_true_somewhere": observed_hook_true,
            "observed_false_somewhere": observed_hook_false,
            "effective_value": "NOT_PROVEN_BY_TEXT_SCAN",
            "required_for_plugin_level_hooks": False,
            "note": (
                "Observed for diagnostics only. Premium v2.1 uses plugin-level hooks; "
                "this agent-scoped setting is not a readiness gate."
            ),
        },
        "experimental_plugin": plugin_contract,
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
        "experimental_plugin_static_contract_valid": bool(plugin_contract.get("valid")),
        "plugin_hooks_still_audit_mode": plugin_contract.get("hook_mode") == "audit",
    }
    report["configuration_prerequisites"] = prerequisites
    report["manual_runtime_prerequisites_not_proven_by_this_script"] = [
        "chat.plugins.enabled / organization policy permits Agent Plugins",
        "the experimental Copilot-format plugin can be installed/enabled in this VS Code profile",
        "plugin hooks are permitted by the active Agent Host policy",
        "Premium Cascade v2.1 (Experimental) is selectable as a custom agent",
    ]
    report["configuration_status"] = (
        "READY_FOR_PLUGIN_INSTALL_OR_LIVE_AUDIT"
        if all(prerequisites.values())
        else "INCOMPLETE_OR_NOT_OBSERVED"
    )

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
