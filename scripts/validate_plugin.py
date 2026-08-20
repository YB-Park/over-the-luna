#!/usr/bin/env python3
"""Validate the v1.1 ambient-tools RC soak candidate."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
EXPECTED_VERSION = "1.1.0-rc.1"
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
COUNCIL_NAMES = {
    "Luna Planner",
    "Luna Architect",
    "Luna Skeptic",
    "Luna Researcher",
    "Luna Tool Worker",
    "Luna Recovery",
    "Luna Reviewer",
}
STRICT_TOOLS = {
    "luna-planner": set(),
    "luna-architect": {"read", "search"},
    "luna-skeptic": {"read", "search"},
    "luna-researcher": {"read", "search", "web"},
    "luna-recovery": {"read", "search"},
    "luna-reviewer": {"read", "search"},
    "premium-review": {"read", "search"},
}
LANGUAGE_MARKER = "same natural language as the user's latest substantive request"


def parse(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("missing closing frontmatter delimiter")
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a mapping")
    return fm, parts[2].strip()


def base_model(value: str) -> str:
    return re.sub(r"\s+\(copilot\)$", "", value).strip()


def need(errors: list[str], path: Path, body: str, *markers: str) -> None:
    for marker in markers:
        if marker not in body:
            errors.append(f"{path}: missing contract marker {marker!r}")


def main() -> int:
    errors: list[str] = []
    plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    if plugin.get("version") != EXPECTED_VERSION:
        errors.append(f"plugin.json: RC soak branch must remain {EXPECTED_VERSION}")
    if plugin.get("agents", "agents/") != "agents/":
        errors.append("plugin.json: agents path must remain agents/")
    if (ROOT / ".mcp.json").exists() or "mcpServers" in plugin or "mcp-servers" in plugin:
        errors.append("plugin must not bundle MCP configuration")

    files = sorted(AGENTS_DIR.glob("*.agent.md"))
    actual_ids = {p.name.removesuffix(".agent.md") for p in files}
    if actual_ids != EXPECTED_AGENT_IDS:
        errors.append(
            "agents/: ambient v1.1 RC layout mismatch; "
            f"missing={sorted(EXPECTED_AGENT_IDS-actual_ids)} extra={sorted(actual_ids-EXPECTED_AGENT_IDS)}"
        )

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
        expected_visible = agent_id in {"over-the-luna", "premium-review"}
        if bool(fm.get("user-invocable", True)) != expected_visible:
            errors.append(f"{path}: user-invocable should be {expected_visible}")
        if expected_visible and fm.get("disable-model-invocation") is not True:
            errors.append(f"{path}: visible agent must disable model invocation")
        if not expected_visible and fm.get("disable-model-invocation") is True:
            errors.append(f"{path}: hidden Luna leaf must remain model-invocable")
        if agent_id != "over-the-luna" and fm.get("agents", []) != []:
            errors.append(f"{path}: every non-Main agent must remain a non-recursive leaf")
        if "tools" in fm:
            tools = fm.get("tools")
            if not isinstance(tools, list) or not all(isinstance(x, str) for x in tools):
                errors.append(f"{path}: tools must be a string list")
            elif "*" in tools:
                errors.append(f"{path}: wildcard '*' is rejected on the VS Code/Copilot CLI path")
        if not body:
            errors.append(f"{path}: instruction body is empty")

    main_agent = parsed.get("over-the-luna")
    if main_agent:
        path, fm, body = main_agent
        if "tools" in fm:
            errors.append(f"{path}: ambient Main must omit tools to preserve VS Code-owned tool state")
        if "agents" in fm:
            errors.append(f"{path}: ambient Main must omit agents; Council is instruction-sealed")
        need(
            errors,
            path,
            body,
            "Parallelize thinking; serialize mutation.",
            "Main owns the work, not all of the thinking.",
            "Delegation allow-list is nevertheless strict at the instruction level.",
            "Luna Planner`, `Luna Architect`, `Luna Skeptic`, `Luna Researcher`, `Luna Tool Worker`, `Luna Recovery`, `Luna Reviewer",
            "Never choose another installed custom agent",
            "AMBIENT_AGENT_UNAVAILABLE: agent/runSubagent",
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
        )
        handoffs = fm.get("handoffs")
        if not isinstance(handoffs, list) or len(handoffs) != 1:
            errors.append(f"{path}: expose exactly one Premium Review handoff")
        else:
            h = handoffs[0]
            if not isinstance(h, dict):
                errors.append(f"{path}: Premium Review handoff must be a mapping")
            else:
                if h.get("label") != "Premium Review" or h.get("agent") != "Premium Review":
                    errors.append(f"{path}: handoff must target exact Premium Review agent")
                if h.get("send") is not False:
                    errors.append(f"{path}: Premium Review must remain human-clicked send:false")
                model = h.get("model")
                if not isinstance(model, str) or base_model(model) != "Claude Sonnet 5":
                    errors.append(f"{path}: Premium Review handoff must pin Claude Sonnet 5")
                prompt = h.get("prompt")
                if not isinstance(prompt, str) or LANGUAGE_MARKER not in prompt:
                    errors.append(f"{path}: Premium Review handoff must preserve the user's conversation language")

    for agent_id, expected in STRICT_TOOLS.items():
        if agent_id not in parsed:
            continue
        path, fm, _ = parsed[agent_id]
        if set(fm.get("tools", [])) != expected:
            errors.append(f"{path}: strict leaf tool boundary drifted; expected {sorted(expected)}")

    tool_worker = parsed.get("luna-tool-worker")
    if tool_worker and "tools" in tool_worker[1]:
        errors.append(f"{tool_worker[0]}: Tool Worker must omit tools to inherit selected integration tools")

    architect = parsed.get("luna-architect")
    if architect:
        need(errors, architect[0], architect[2], "DECISION", "EVIDENCE", "RELATIONSHIPS", "MUTATION_TARGETS", "UNRESOLVED", "Never inspect `.git`")

    reviewer = parsed.get("luna-reviewer")
    if reviewer:
        need(errors, reviewer[0], reviewer[2], "BEGIN_UNIFIED_DIFF", "END_UNIFIED_DIFF", "4 concrete files", "8 total read/search calls", "INVARIANT_CHALLENGED")

    premium = parsed.get("premium-review")
    if premium:
        path, fm, body = premium
        need(
            errors,
            path,
            body,
            "human-selected premium review",
            LANGUAGE_MARKER,
            "NEEDS_EXTERNAL_VERIFICATION",
            "Do not recommend or invoke another premium model",
            "One Premium Review is the v1.1 visible premium decision",
        )
        if fm.get("handoffs"):
            errors.append(f"{path}: Premium Review must not escalate to another premium model")

    if not COUNCIL_NAMES.issubset(names):
        errors.append(f"agents/: missing exact Council display names: {sorted(COUNCIL_NAMES-names)}")

    if errors:
        print("Over the Luna v1.1 RC validation FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Over the Luna v1.1 RC validation passed: "
        f"{len(files)} agents, manifest v{plugin['version']}, ambient Main tools, instruction-sealed Council, one human Premium Review, language continuity"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
