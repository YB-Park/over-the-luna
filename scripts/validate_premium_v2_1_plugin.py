#!/usr/bin/env python3
"""Static validator for the isolated Premium v2.1 experimental plugin."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "experiments" / "premium_v2_1_plugin"
AGENTS = PLUGIN / "agents"
EXPECTED_HOOKS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "SubagentStart",
    "SubagentStop",
    "Stop",
}


def parse_agent(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("missing closing frontmatter")
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be an object")
    return fm, parts[2]


def main() -> int:
    errors: list[str] = []

    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != "over-the-luna-premium-v2-1-experiment":
        errors.append("plugin name drifted")
    if manifest.get("version") != "0.0.1":
        errors.append("experimental plugin version must remain 0.0.1 before development freeze")
    if manifest.get("agents") != "agents/":
        errors.append("plugin agents path must remain agents/")
    if manifest.get("hooks") != "hooks.json":
        errors.append("plugin must explicitly reference hooks.json")

    files = {p.name: p for p in AGENTS.glob("*.agent.md")}
    expected = {"premium-cascade-v2-1.agent.md", "luna-builder-v2-1.agent.md"}
    if set(files) != expected:
        errors.append(f"experimental plugin must contain exactly {sorted(expected)}")

    root_path = files.get("premium-cascade-v2-1.agent.md")
    builder_path = files.get("luna-builder-v2-1.agent.md")
    if root_path:
        fm, body = parse_agent(root_path)
        if fm.get("name") != "Premium Cascade v2.1 (Experimental)":
            errors.append("root display name drifted")
        if fm.get("target") != "vscode" or fm.get("model") != "GPT-5.6 Terra":
            errors.append("root must target VS Code with GPT-5.6 Terra")
        if fm.get("disable-model-invocation") is not True:
            errors.append("root must remain user-selected / not model-invocable")
        if set(fm.get("tools", [])) != {"read", "search", "edit", "execute", "agent"}:
            errors.append("root tool surface drifted")
        if fm.get("agents") != ["Premium v2.1 Luna Builder"]:
            errors.append("root must allow exactly one Luna Builder")
        for marker in (
            "one Luna Builder attempt",
            "do not read/search repository files",
            "do not invoke any agent again",
            "one Terra takeover",
            "A model sentence saying \"complete\" is not the trusted controller result.",
        ):
            if marker not in body:
                errors.append(f"root missing contract marker {marker!r}")

    if builder_path:
        fm, body = parse_agent(builder_path)
        if fm.get("name") != "Premium v2.1 Luna Builder":
            errors.append("Builder display name drifted")
        if fm.get("target") != "vscode" or fm.get("model") != "GPT-5.6 Luna":
            errors.append("Builder must target VS Code with GPT-5.6 Luna")
        if fm.get("user-invocable") is not False:
            errors.append("Builder must remain hidden")
        if set(fm.get("tools", [])) != {"read", "search", "edit", "execute"}:
            errors.append("Builder tool surface drifted")
        if fm.get("agents") != []:
            errors.append("Builder must remain non-recursive")
        for marker in (
            "first and only Luna implementation trajectory",
            "at most one ordinary self-repair",
            "SUPPORTED_STATE_EXCLUSIONS",
            "Never fabricate a user waiver.",
        ):
            if marker not in body:
                errors.append(f"Builder missing contract marker {marker!r}")

    hooks = json.loads((PLUGIN / "hooks.json").read_text(encoding="utf-8"))
    if hooks.get("version") != 1:
        errors.append("hooks.json must declare version 1 for Copilot hook compatibility")
    hook_map = hooks.get("hooks")
    if not isinstance(hook_map, dict):
        errors.append("hooks.json must contain a hooks object")
    else:
        if set(hook_map) != EXPECTED_HOOKS:
            errors.append(
                f"hook event set drifted: missing={sorted(EXPECTED_HOOKS-set(hook_map))} "
                f"extra={sorted(set(hook_map)-EXPECTED_HOOKS)}"
            )
        for event, entries in hook_map.items():
            if not isinstance(entries, list) or len(entries) != 1:
                errors.append(f"{event}: expected exactly one plugin hook")
                continue
            item = entries[0]
            if not isinstance(item, dict) or item.get("type") != "command":
                errors.append(f"{event}: hook must be command type")
                continue
            if "${PLUGIN_ROOT}/scripts/hook.py" not in str(item.get("command", "")):
                errors.append(f"{event}: hook must invoke plugin-local hook.py")
            env = item.get("env")
            if not isinstance(env, dict) or env.get("OTL_V2_1_HOOK_MODE") != "audit":
                errors.append(f"{event}: pre-calibration hook mode must remain audit")

    hook_script = (PLUGIN / "scripts" / "hook.py").read_text(encoding="utf-8")
    for marker in (
        'mode = os.environ.get("OTL_V2_1_HOOK_MODE", "audit")',
        'state["phase"] = "TERRA_TAKEOVER"',
        'state["builder_count"]',
        '"NO_VERIFIED_COMPLETION"',
    ):
        if marker not in hook_script:
            errors.append(f"hook controller missing marker {marker!r}")

    if errors:
        print("Premium v2.1 plugin validation FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Premium v2.1 plugin validation passed: 2 agents, 7 lifecycle hooks, version-1 audit-mode pre-calibration boundary")
    return 0


if __name__ == "__main__":
    sys.exit(main())
