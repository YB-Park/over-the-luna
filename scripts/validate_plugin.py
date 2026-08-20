#!/usr/bin/env python3
"""Static validation for the Over the Luna v1.1 VS Code gate plugin.

This branch is an integration candidate, not a published release. Keep the
manifest version at 1.0.0 until the authenticated real-VS-Code gate passes.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"

EXPECTED_VERSION = "1.0.0"
EXPECTED_AGENT_IDS = {
    "over-the-luna",
    "luna-planner",
    "luna-architect",
    "luna-skeptic",
    "luna-researcher",
    "luna-tool-worker",
    "luna-recovery",
    "luna-reviewer",
    "premium-review",
}
FORBIDDEN_AGENT_IDS = {
    "luna-solo",
    "luna-implementer",
    "luna-explorer",
    "kimi-deep-worker",
    "mai-mechanical",
    "sonnet-reviewer",
    "opus-critical-reviewer",
}

LUNA_CORE_IDS = {
    "over-the-luna",
    "luna-planner",
    "luna-architect",
    "luna-skeptic",
    "luna-researcher",
    "luna-tool-worker",
    "luna-recovery",
    "luna-reviewer",
}
VISIBLE_AGENT_IDS = {"over-the-luna", "premium-review"}
MANUAL_ONLY_IDS = VISIBLE_AGENT_IDS

STRICT_TOOLSETS = {
    "luna-planner": set(),
    "luna-architect": {"read", "search"},
    "luna-skeptic": {"read", "search"},
    "luna-researcher": {"read", "search", "web"},
    "luna-recovery": {"read", "search"},
    "luna-reviewer": {"read", "search"},
    "premium-review": {"read", "search"},
}
INHERITED_TOOL_IDS = {"over-the-luna", "luna-tool-worker"}

EXPECTED_MAIN_AGENTS = {
    "Luna Planner",
    "Luna Architect",
    "Luna Skeptic",
    "Luna Researcher",
    "Luna Tool Worker",
    "Luna Recovery",
    "Luna Reviewer",
}

ALLOWED_MODELS = {"GPT-5.6 Luna", "Claude Sonnet 5"}
ALLOWED_EXPLICIT_TOOLS = {"read", "search", "web", "agent", "todo", "edit", "execute"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("missing closing YAML frontmatter delimiter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, parts[2].strip()


def base_handoff_model(value: str) -> str:
    return re.sub(r"\s+\(copilot\)$", "", value).strip()


def require_markers(errors: list[str], path: Path, body: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        if marker not in body:
            fail(errors, f"{path}: missing contract marker {marker!r}")


def main() -> int:
    errors: list[str] = []

    try:
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR plugin.json: {exc}")
        return 1

    if plugin.get("version") != EXPECTED_VERSION:
        fail(
            errors,
            f"plugin.json: VS Code gate must stay at {EXPECTED_VERSION}; version bump requires release authorization",
        )
    if plugin.get("agents", "agents/") != "agents/":
        fail(errors, "plugin.json: agents path must remain agents/")
    for key in ("mcpServers", "mcp-servers"):
        if key in plugin:
            fail(errors, f"plugin.json: do not bundle MCP servers via {key}")
    if (ROOT / ".mcp.json").exists():
        fail(errors, ".mcp.json: this plugin must not bundle MCP servers")

    files = sorted(AGENTS_DIR.glob("*.agent.md"))
    actual_ids = {path.name.removesuffix(".agent.md") for path in files}
    if actual_ids != EXPECTED_AGENT_IDS:
        missing = sorted(EXPECTED_AGENT_IDS - actual_ids)
        extra = sorted(actual_ids - EXPECTED_AGENT_IDS)
        if missing:
            fail(errors, f"agents/: missing expected gate agents: {', '.join(missing)}")
        if extra:
            fail(errors, f"agents/: unexpected gate agents: {', '.join(extra)}")
    forbidden_present = actual_ids & FORBIDDEN_AGENT_IDS
    if forbidden_present:
        fail(errors, f"agents/: forbidden/retired agents present: {', '.join(sorted(forbidden_present))}")

    parsed: dict[str, tuple[Path, dict[str, Any], str]] = {}
    names: dict[str, str] = {}

    for path in files:
        agent_id = path.name.removesuffix(".agent.md")
        try:
            fm, body = parse_frontmatter(path)
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{path}: {exc}")
            continue
        parsed[agent_id] = (path, fm, body)

        name = fm.get("name")
        if not isinstance(name, str) or not name.strip():
            fail(errors, f"{path}: name is required")
        elif name in names:
            fail(errors, f"{path}: duplicate display name {name!r}")
        else:
            names[name] = agent_id

        if not isinstance(fm.get("description"), str) or not fm.get("description", "").strip():
            fail(errors, f"{path}: description is required")
        if fm.get("target") != "vscode":
            fail(errors, f"{path}: target must be vscode")

        model = fm.get("model")
        if not isinstance(model, str) or model not in ALLOWED_MODELS:
            fail(errors, f"{path}: model must be one exact supported gate model string")
        if agent_id in LUNA_CORE_IDS and model != "GPT-5.6 Luna":
            fail(errors, f"{path}: automatic core must be Luna-only")
        if agent_id == "premium-review" and model != "Claude Sonnet 5":
            fail(errors, f"{path}: the single v1.1 Premium Review candidate must pin Claude Sonnet 5")

        expected_visible = agent_id in VISIBLE_AGENT_IDS
        if bool(fm.get("user-invocable", True)) != expected_visible:
            fail(errors, f"{path}: user-invocable should be {str(expected_visible).lower()}")
        if agent_id in MANUAL_ONLY_IDS and fm.get("disable-model-invocation") is not True:
            fail(errors, f"{path}: visible agents must set disable-model-invocation: true")
        if agent_id not in MANUAL_ONLY_IDS and fm.get("disable-model-invocation") is True:
            fail(errors, f"{path}: hidden Luna council agent must remain subagent-invocable")

        if "tools" in fm:
            tools = fm["tools"]
            if not isinstance(tools, list) or not all(isinstance(tool, str) for tool in tools):
                fail(errors, f"{path}: tools must be a YAML string list")
                tools = []
            for tool in tools:
                if tool == "*":
                    fail(errors, f"{path}: do not use global tools '*' in VS Code custom agents")
                elif tool not in ALLOWED_EXPLICIT_TOOLS:
                    fail(errors, f"{path}: unsupported explicit tool {tool!r}")

        for key in ("mcpServers", "mcp-servers"):
            if key in fm:
                fail(errors, f"{path}: do not configure MCP servers in agent frontmatter")

        agents = fm.get("agents", [])
        if not isinstance(agents, list) or not all(isinstance(item, str) for item in agents):
            fail(errors, f"{path}: agents must be a YAML string list")
        if not body:
            fail(errors, f"{path}: instruction body must not be empty")

    for agent_id in INHERITED_TOOL_IDS:
        if agent_id in parsed:
            path, fm, _ = parsed[agent_id]
            if "tools" in fm:
                fail(errors, f"{path}: inherited-tool role must omit tools")

    for agent_id, expected_tools in STRICT_TOOLSETS.items():
        if agent_id in parsed:
            path, fm, _ = parsed[agent_id]
            if "tools" not in fm:
                fail(errors, f"{path}: strict role must declare tools explicitly")
            elif set(fm.get("tools", [])) != expected_tools:
                fail(errors, f"{path}: strict tool boundary drifted; expected {sorted(expected_tools)}")

    for agent_id, (path, fm, _) in parsed.items():
        if agent_id != "over-the-luna" and fm.get("agents", []) != []:
            fail(errors, f"{path}: every council/reviewer agent must remain a leaf with agents: []")
        for child_name in fm.get("agents", []):
            if child_name not in names:
                fail(errors, f"{path}: unknown subagent display name {child_name!r}")

    main_agent = parsed.get("over-the-luna")
    if main_agent:
        path, fm, body = main_agent
        if set(fm.get("agents", [])) != EXPECTED_MAIN_AGENTS:
            fail(errors, f"{path}: Main Luna council allow-list drifted")
        require_markers(
            errors,
            path,
            body,
            (
                "Parallelize thinking; serialize mutation.",
                "Main owns the work, not all of the thinking.",
                "three narrow `rg` locator calls total",
                "do not call `glob` at all during SIMPLE orientation",
                "Mode: <SIMPLE|STANDARD|DEEP>",
                "Assurance: <NONE|REVIEW|RISK>",
                "Boundary sealed — work set:",
                "BEGIN_UNIFIED_DIFF",
                "END_UNIFIED_DIFF",
                "never retry Luna Reviewer",
                "at least one post-change named Luna Reviewer is mandatory",
                "one visible **human decision**",
                "surface that fact rather than silently substituting another model",
            ),
        )

        handoffs = fm.get("handoffs", [])
        if not isinstance(handoffs, list):
            fail(errors, f"{path}: handoffs must be a list")
        elif len(handoffs) != 1:
            fail(errors, f"{path}: v1.1 gate must expose exactly one Premium Review handoff")
        else:
            handoff = handoffs[0]
            if not isinstance(handoff, dict):
                fail(errors, f"{path}: Premium Review handoff must be a mapping")
            else:
                target = handoff.get("agent")
                label = handoff.get("label")
                model = handoff.get("model")
                if label != "Premium Review" or target != "Premium Review":
                    fail(errors, f"{path}: premium handoff must be the single exact Premium Review target")
                if handoff.get("send") is not False:
                    fail(errors, f"{path}: Premium Review must require a visible human click (send: false)")
                if not isinstance(model, str) or base_handoff_model(model) != "Claude Sonnet 5":
                    fail(errors, f"{path}: Premium Review handoff must target Claude Sonnet 5")
                if isinstance(target, str) and target not in names:
                    fail(errors, f"{path}: Premium Review target does not resolve to a loaded exact agent name")

    architect = parsed.get("luna-architect")
    if architect:
        path, _, body = architect
        require_markers(
            errors,
            path,
            body,
            (
                "DECISION",
                "EVIDENCE",
                "RELATIONSHIPS",
                "MUTATION_TARGETS",
                "UNRESOLVED",
                "complete **post-handback work set**",
                "Never inspect `.git`",
            ),
        )

    reviewer = parsed.get("luna-reviewer")
    if reviewer:
        path, fm, body = reviewer
        tools = set(fm.get("tools", []))
        if "edit" in tools or "execute" in tools:
            fail(errors, f"{path}: Reviewer must remain structurally non-mutating")
        require_markers(
            errors,
            path,
            body,
            (
                "BEGIN_UNIFIED_DIFF",
                "END_UNIFIED_DIFF",
                "diff --git",
                "@@",
                "4 concrete files",
                "8 total read/search calls",
                "never inspect `.git`",
                "Cosmetic whitespace",
                "INVARIANT_CHALLENGED",
            ),
        )

    premium = parsed.get("premium-review")
    if premium:
        path, fm, body = premium
        tools = set(fm.get("tools", []))
        if "edit" in tools or "execute" in tools:
            fail(errors, f"{path}: Premium Review must remain structurally non-mutating")
        require_markers(
            errors,
            path,
            body,
            (
                "human-selected premium review",
                "NEEDS_EXTERNAL_VERIFICATION",
                "Do not recommend or invoke another premium model",
                "One Premium Review is the v1.1 visible premium decision",
            ),
        )
        if fm.get("handoffs"):
            fail(errors, f"{path}: Premium Review must not expose another premium escalation")

    compact_markers = {
        "luna-planner": "Return no more than 12 bullets",
        "luna-skeptic": "Return no more than 8",
        "luna-researcher": "Return no more than 8 bullets",
        "luna-tool-worker": "Return no more than 10 bullets",
        "luna-recovery": "Return no more than 10 bullets",
    }
    for agent_id, marker in compact_markers.items():
        if agent_id in parsed and marker not in parsed[agent_id][2]:
            fail(errors, f"{parsed[agent_id][0]}: compact-output contract missing {marker!r}")

    if errors:
        print("Over the Luna v1.1 VS Code gate validation FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Over the Luna v1.1 VS Code gate validation passed: {len(files)} agents, "
        f"manifest v{plugin['version']}, Luna-only automatic core, one human Premium Review"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
