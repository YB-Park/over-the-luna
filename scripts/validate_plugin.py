#!/usr/bin/env python3
"""Validate the v1.1 schema-strict VS Code Gate A fallback candidate."""

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
    "over-the-luna", "luna-planner", "luna-architect", "luna-skeptic",
    "luna-researcher", "luna-tool-worker", "luna-recovery", "luna-reviewer",
    "premium-review",
}
COUNCIL = {
    "Luna Planner", "Luna Architect", "Luna Skeptic", "Luna Researcher",
    "Luna Tool Worker", "Luna Recovery", "Luna Reviewer",
}
MAIN_TOOLS = {"read", "search", "edit", "execute", "agent", "todo", "web"}
STRICT_TOOLS = {
    "luna-planner": set(),
    "luna-architect": {"read", "search"},
    "luna-skeptic": {"read", "search"},
    "luna-researcher": {"read", "search", "web"},
    "luna-recovery": {"read", "search"},
    "luna-reviewer": {"read", "search"},
    "premium-review": {"read", "search"},
}


def parse(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0] != "":
        raise ValueError("malformed frontmatter")
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a mapping")
    return fm, parts[2].strip()


def base_model(value: str) -> str:
    return re.sub(r"\s+\(copilot\)$", "", value).strip()


def need(errors: list[str], path: Path, body: str, *markers: str) -> None:
    for marker in markers:
        if marker not in body:
            errors.append(f"{path}: missing marker {marker!r}")


def main() -> int:
    errors: list[str] = []
    plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    if plugin.get("version") != EXPECTED_VERSION:
        errors.append(f"plugin.json: Gate A branch must remain {EXPECTED_VERSION}")
    if plugin.get("agents", "agents/") != "agents/":
        errors.append("plugin.json: agents path must remain agents/")
    if (ROOT / ".mcp.json").exists() or "mcpServers" in plugin or "mcp-servers" in plugin:
        errors.append("plugin must not bundle MCP configuration")

    files = sorted(AGENTS_DIR.glob("*.agent.md"))
    ids = {p.name.removesuffix(".agent.md") for p in files}
    if ids != EXPECTED_AGENT_IDS:
        errors.append(f"agents/: schema Gate layout mismatch; missing={sorted(EXPECTED_AGENT_IDS-ids)} extra={sorted(ids-EXPECTED_AGENT_IDS)}")

    parsed: dict[str, tuple[Path, dict[str, Any], str]] = {}
    names: set[str] = set()
    for path in files:
        agent_id = path.name.removesuffix(".agent.md")
        try:
            fm, body = parse(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: {exc}")
            continue
        parsed[agent_id] = (path, fm, body)
        name = fm.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{path}: name required")
        elif name in names:
            errors.append(f"{path}: duplicate display name {name!r}")
        else:
            names.add(name)
        if fm.get("target") != "vscode":
            errors.append(f"{path}: target must be vscode")
        expected_model = "Claude Sonnet 5" if agent_id == "premium-review" else "GPT-5.6 Luna"
        if fm.get("model") != expected_model:
            errors.append(f"{path}: expected model {expected_model!r}")
        visible = agent_id in {"over-the-luna", "premium-review"}
        if bool(fm.get("user-invocable", True)) != visible:
            errors.append(f"{path}: user-invocable should be {visible}")
        if visible and fm.get("disable-model-invocation") is not True:
            errors.append(f"{path}: visible agent must disable model invocation")
        if not visible and fm.get("disable-model-invocation") is True:
            errors.append(f"{path}: hidden Luna leaf must remain model-invocable")
        if agent_id != "over-the-luna" and fm.get("agents", []) != []:
            errors.append(f"{path}: non-Main agent must remain a leaf")
        tools = fm.get("tools")
        if isinstance(tools, list) and "*" in tools:
            errors.append(f"{path}: wildcard '*' is not portable on the VS Code/Copilot CLI path")

    main_agent = parsed.get("over-the-luna")
    if main_agent:
        path, fm, body = main_agent
        if set(fm.get("tools", [])) != MAIN_TOOLS:
            errors.append(f"{path}: schema Main tools drifted; expected {sorted(MAIN_TOOLS)}")
        if set(fm.get("agents", [])) != COUNCIL:
            errors.append(f"{path}: schema Main Council allow-list drifted")
        need(errors, path, body,
             "schema-strict subagent wiring",
             "AMBIENT_TOOL_UNAVAILABLE",
             "Parallelize thinking; serialize mutation.",
             "Mode: <SIMPLE|STANDARD|DEEP>",
             "Assurance: <NONE|REVIEW|RISK>",
             "Boundary sealed — work set:",
             "BEGIN_UNIFIED_DIFF", "END_UNIFIED_DIFF",
             "never retry Luna Reviewer",
             "at least one post-change named Luna Reviewer is mandatory",
             "one visible **human decision**")
        handoffs = fm.get("handoffs")
        if not isinstance(handoffs, list) or len(handoffs) != 1:
            errors.append(f"{path}: expose exactly one Premium Review handoff")
        else:
            h = handoffs[0]
            if h.get("label") != "Premium Review" or h.get("agent") != "Premium Review" or h.get("send") is not False:
                errors.append(f"{path}: Premium Review handoff contract drifted")
            model = h.get("model")
            if not isinstance(model, str) or base_model(model) != "Claude Sonnet 5":
                errors.append(f"{path}: Premium Review must pin Claude Sonnet 5")

    for agent_id, expected in STRICT_TOOLS.items():
        if agent_id in parsed and set(parsed[agent_id][1].get("tools", [])) != expected:
            errors.append(f"{parsed[agent_id][0]}: strict leaf tools drifted; expected {sorted(expected)}")
    if "luna-tool-worker" in parsed and "tools" in parsed["luna-tool-worker"][1]:
        errors.append(f"{parsed['luna-tool-worker'][0]}: Tool Worker must omit tools")

    if "luna-architect" in parsed:
        need(errors, parsed["luna-architect"][0], parsed["luna-architect"][2], "DECISION", "EVIDENCE", "RELATIONSHIPS", "MUTATION_TARGETS", "UNRESOLVED")
    if "luna-reviewer" in parsed:
        need(errors, parsed["luna-reviewer"][0], parsed["luna-reviewer"][2], "BEGIN_UNIFIED_DIFF", "END_UNIFIED_DIFF", "4 concrete files", "8 total read/search calls", "INVARIANT_CHALLENGED")
    if "premium-review" in parsed:
        p, fm, body = parsed["premium-review"]
        need(errors, p, body, "human-selected premium review", "NEEDS_EXTERNAL_VERIFICATION", "One Premium Review is the v1.1 visible premium decision")
        if fm.get("handoffs"):
            errors.append(f"{p}: Premium Review must not escalate")

    if errors:
        print("Over the Luna v1.1 schema-strict Gate A validation FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Over the Luna v1.1 schema-strict Gate A validation passed: {len(files)} agents, manifest v{plugin['version']}, explicit Council + agent tool, one Premium Review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
