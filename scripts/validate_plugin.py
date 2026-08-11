#!/usr/bin/env python3
"""Static validation for Over the Luna's VS Code agent plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"

ALLOWED_MODELS = {
    "GPT-5.6 Luna",
    "Claude Sonnet 5",
    "Claude Opus 4.8",
    "Kimi K2.7 Code",
    "MAI-Code-1-Flash",
    "Claude Haiku 4.5",
}

# Strict roles use documented primary aliases. Ambient-capable roles deliberately
# use only "*" so arbitrary user-configured MCP and extension tools remain usable.
ALLOWED_TOOLS = {"*", "agent", "todo", "read", "search", "edit", "execute", "web"}

EXPECTED_AGENT_IDS = {
    "over-the-luna",
    "luna-explorer",
    "luna-researcher",
    "luna-tool-worker",
    "luna-implementer",
    "luna-reviewer",
    "kimi-deep-worker",
    "mai-mechanical",
    "sonnet-reviewer",
    "opus-critical-reviewer",
}

VISIBLE_AGENT_IDS = {"over-the-luna", "opus-critical-reviewer"}
MANUAL_ONLY_AGENT_IDS = VISIBLE_AGENT_IDS
FORBIDDEN_AGENT_IDS = {"luna-solo"}

AMBIENT_TOOL_AGENT_IDS = {
    "luna-tool-worker",
    "luna-implementer",
    "kimi-deep-worker",
    "mai-mechanical",
}

STRICT_TOOLSETS = {
    "over-the-luna": {"agent", "todo"},
    "luna-explorer": {"read", "search"},
    "luna-researcher": {"read", "search", "web"},
    "luna-reviewer": {"read", "search"},
    "sonnet-reviewer": {"read", "search"},
    "opus-critical-reviewer": {"read", "search", "web"},
}

REVIEWER_AGENT_IDS = {"luna-reviewer", "sonnet-reviewer", "opus-critical-reviewer"}

EXPECTED_COORDINATOR_WORKERS = {
    "Luna Explorer",
    "Luna Researcher",
    "Luna Tool Worker",
    "Luna Implementer",
    "Luna Reviewer",
    "Kimi Deep Worker",
    "MAI Mechanical",
    "Sonnet Reviewer",
}

AMBIENT_POLICY_MARKERS = (
    "AMBIENT_TOOL_UNAVAILABLE",
    "untrusted",
    "External side effects",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path) -> tuple[dict, str]:
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


def model_names(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and value and all(isinstance(item, str) for item in value):
        return value
    return []


def base_handoff_model(value: str) -> str:
    return re.sub(r"\s+\(copilot\)$", "", value).strip()


def main() -> int:
    errors: list[str] = []

    plugin_path = ROOT / "plugin.json"
    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR plugin.json: {exc}")
        return 1

    if not re.fullmatch(r"[a-z0-9-]{1,64}", str(plugin.get("name", ""))):
        fail(errors, "plugin.json: name must be kebab-case and <=64 characters")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))):
        fail(errors, "plugin.json: version must be semantic x.y.z")
    if plugin.get("agents", "agents/") != "agents/":
        fail(errors, "plugin.json: agents path must remain agents/")

    # Product boundary: use the developer's existing VS Code MCP configuration.
    # Do not silently acquire ownership of servers, credentials, or trust policy.
    for key in ("mcpServers", "mcp-servers"):
        if key in plugin:
            fail(errors, f"plugin.json: do not bundle MCP servers via {key}; ambient user tools are the compatibility boundary")
    if (ROOT / ".mcp.json").exists():
        fail(errors, ".mcp.json: this plugin must not bundle MCP servers; use ambient user/workspace MCP configuration")

    files = sorted(AGENTS_DIR.glob("*.agent.md"))
    if not files:
        fail(errors, "agents/: no .agent.md files found")

    actual_agent_ids = {path.name.removesuffix(".agent.md") for path in files}
    if actual_agent_ids != EXPECTED_AGENT_IDS:
        missing = sorted(EXPECTED_AGENT_IDS - actual_agent_ids)
        extra = sorted(actual_agent_ids - EXPECTED_AGENT_IDS)
        if missing:
            fail(errors, f"agents/: missing expected agents: {', '.join(missing)}")
        if extra:
            fail(errors, f"agents/: unexpected agents require architecture review: {', '.join(extra)}")

    parsed: dict[str, tuple[Path, dict, str]] = {}
    names: dict[str, str] = {}

    for path in files:
        agent_id = path.name.removesuffix(".agent.md")
        if agent_id in FORBIDDEN_AGENT_IDS:
            fail(errors, f"{path}: direct-mode wrappers belong to VS Code's built-in Agent, not this harness plugin")

        try:
            frontmatter, body = parse_frontmatter(path)
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{path}: {exc}")
            continue

        parsed[agent_id] = (path, frontmatter, body)

        name = frontmatter.get("name")
        if not isinstance(name, str) or not name.strip():
            fail(errors, f"{path}: name is required")
        elif name in names:
            fail(errors, f"{path}: duplicate display name {name!r} (also {names[name]})")
        else:
            names[name] = agent_id

        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            fail(errors, f"{path}: description is required")

        if frontmatter.get("target") != "vscode":
            fail(errors, f"{path}: target must be 'vscode'")

        models = model_names(frontmatter.get("model"))
        if not models:
            fail(errors, f"{path}: model must be a string or non-empty string list")
        for model in models:
            if model not in ALLOWED_MODELS:
                fail(errors, f"{path}: unsupported project model {model!r}")

        # Require an explicit declaration for auditability. Ambient roles use ["*"]
        # instead of omitting tools, even though both mean all available tools.
        tools = frontmatter.get("tools")
        if not isinstance(tools, list) or not tools or not all(isinstance(tool, str) for tool in tools):
            fail(errors, f"{path}: tools must be a non-empty YAML string list")
            tools = []
        for tool in tools:
            if tool not in ALLOWED_TOOLS:
                fail(errors, f"{path}: unsupported tool declaration {tool!r}")

        # Per-agent MCP configuration is not the VS Code compatibility strategy.
        # Arbitrary user/workspace MCPs are inherited through ambient wildcard tools.
        for key in ("mcp-servers", "mcpServers"):
            if key in frontmatter:
                fail(errors, f"{path}: do not configure MCP servers in agent frontmatter via {key}")

        agents = frontmatter.get("agents", [])
        if not isinstance(agents, list) or not all(isinstance(agent, str) for agent in agents):
            fail(errors, f"{path}: agents must be a YAML string list")
            agents = []
        if agents and "agent" not in tools and "*" not in tools:
            fail(errors, f"{path}: non-empty agents list requires the 'agent' tool")

        expected_user_invocable = agent_id in VISIBLE_AGENT_IDS
        actual_user_invocable = frontmatter.get("user-invocable", True)
        if bool(actual_user_invocable) != expected_user_invocable:
            fail(errors, f"{path}: user-invocable should be {str(expected_user_invocable).lower()} for this role")

        if agent_id in MANUAL_ONLY_AGENT_IDS and frontmatter.get("disable-model-invocation") is not True:
            fail(errors, f"{path}: user-facing entry/handoff agents must set disable-model-invocation: true")
        if agent_id not in MANUAL_ONLY_AGENT_IDS and frontmatter.get("disable-model-invocation") is True:
            fail(errors, f"{path}: worker must remain available for model/subagent invocation")

        if not body:
            fail(errors, f"{path}: instruction body must not be empty")

    agent_ids = set(parsed)

    # Validate references after all names and IDs are known.
    for _, (path, frontmatter, _) in parsed.items():
        for worker_name in frontmatter.get("agents", []):
            if worker_name not in names:
                fail(errors, f"{path}: unknown subagent display name {worker_name!r}")

        handoffs = frontmatter.get("handoffs", []) or []
        if not isinstance(handoffs, list):
            fail(errors, f"{path}: handoffs must be a list")
            continue
        for handoff in handoffs:
            if not isinstance(handoff, dict):
                fail(errors, f"{path}: each handoff must be a mapping")
                continue
            target = handoff.get("agent")
            if target not in agent_ids:
                fail(errors, f"{path}: handoff references unknown agent id {target!r}")
            elif target not in VISIBLE_AGENT_IDS:
                fail(errors, f"{path}: handoff target {target!r} must be user-visible")
            if not isinstance(handoff.get("label"), str) or not handoff.get("label", "").strip():
                fail(errors, f"{path}: each handoff needs a non-empty label")
            if not isinstance(handoff.get("prompt"), str) or not handoff.get("prompt", "").strip():
                fail(errors, f"{path}: each handoff needs a non-empty prompt")
            handoff_model = handoff.get("model")
            if handoff_model is not None:
                if not isinstance(handoff_model, str):
                    fail(errors, f"{path}: handoff model must be a string")
                elif base_handoff_model(handoff_model) not in ALLOWED_MODELS:
                    fail(errors, f"{path}: unsupported handoff model {handoff_model!r}")

    # Architecture contracts.
    coordinator = parsed.get("over-the-luna")
    if coordinator:
        path, fm, body = coordinator
        if fm.get("model") != "Claude Sonnet 5":
            fail(errors, f"{path}: full harness coordinator must be Claude Sonnet 5 for deterministic routing/cost tier")
        if set(fm.get("tools", [])) != STRICT_TOOLSETS["over-the-luna"]:
            fail(errors, f"{path}: coordinator must remain router-only with agent + todo")
        if set(fm.get("agents", [])) != EXPECTED_COORDINATOR_WORKERS:
            fail(errors, f"{path}: coordinator worker allow-list drifted")
        if "Never infer an external side effect" not in body:
            fail(errors, f"{path}: coordinator must keep the explicit external-mutation boundary")
        if "AMBIENT_TOOL_UNAVAILABLE" not in body:
            fail(errors, f"{path}: coordinator must preserve ambient-tool failure visibility")

    # Ambient roles must preserve arbitrary MCP/extension compatibility. Do not
    # replace "*" with a built-in allow-list, or existing user tools disappear.
    for agent_id in AMBIENT_TOOL_AGENT_IDS:
        if agent_id not in parsed:
            continue
        path, fm, body = parsed[agent_id]
        if fm.get("tools") != ["*"]:
            fail(errors, f"{path}: ambient-capable role must declare exactly tools: ['*']")
        if fm.get("agents", []) != []:
            fail(errors, f"{path}: ambient worker must not delegate recursively")
        for marker in AMBIENT_POLICY_MARKERS:
            if marker not in body:
                fail(errors, f"{path}: ambient safety policy missing marker {marker!r}")

    # Strict roles deliberately do not inherit arbitrary MCP/extension tools.
    for agent_id, expected_tools in STRICT_TOOLSETS.items():
        if agent_id not in parsed:
            continue
        path, fm, _ = parsed[agent_id]
        actual_tools = set(fm.get("tools", []))
        if actual_tools != expected_tools:
            fail(errors, f"{path}: strict tool boundary drifted; expected {sorted(expected_tools)}, got {sorted(actual_tools)}")
        if "*" in actual_tools:
            fail(errors, f"{path}: strict role must never receive ambient wildcard tools")

    for agent_id in REVIEWER_AGENT_IDS:
        if agent_id not in parsed:
            continue
        path, fm, body = parsed[agent_id]
        tools = set(fm.get("tools", []))
        if "edit" in tools or "execute" in tools or "*" in tools:
            fail(errors, f"{path}: reviewer must remain structurally non-mutating and non-ambient")
        if "NEEDS_EXTERNAL_VERIFICATION" not in body:
            fail(errors, f"{path}: reviewer must explicitly surface unverifiable ambient external state")

    # Only the coordinator may invoke subagents. All workers and handoff agents
    # remain leaf nodes even when ambient wildcard tools include the agent toolset.
    for agent_id, (path, fm, _) in parsed.items():
        if agent_id != "over-the-luna" and fm.get("agents", []) != []:
            fail(errors, f"{path}: workers/entry agents must not delegate recursively")

    if errors:
        print("Over the Luna validation FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Over the Luna validation passed: {len(files)} agents, plugin v{plugin['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
