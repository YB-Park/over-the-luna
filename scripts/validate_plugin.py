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

# Use GitHub's documented primary aliases only. Compatible aliases such as
# shell/Bash/PowerShell work, but primary aliases make behavior easier to audit.
ALLOWED_TOOLS = {"agent", "todo", "read", "search", "edit", "execute", "web"}

VISIBLE_AGENT_IDS = {"over-the-luna", "luna-solo", "opus-critical-reviewer"}
EDITOR_AGENT_IDS = {"luna-solo", "luna-implementer", "kimi-deep-worker", "mai-mechanical"}
REVIEWER_AGENT_IDS = {"luna-reviewer", "sonnet-reviewer", "opus-critical-reviewer"}

EXPECTED_COORDINATOR_WORKERS = {
    "Luna Explorer",
    "Luna Researcher",
    "Luna Implementer",
    "Luna Reviewer",
    "Kimi Deep Worker",
    "MAI Mechanical",
    "Sonnet Reviewer",
}


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
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
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

    files = sorted(AGENTS_DIR.glob("*.agent.md"))
    if not files:
        fail(errors, "agents/: no .agent.md files found")

    parsed: dict[str, tuple[Path, dict, str]] = {}
    names: dict[str, str] = {}

    for path in files:
        agent_id = path.name.removesuffix(".agent.md")
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

        tools = frontmatter.get("tools", [])
        if not isinstance(tools, list) or not all(isinstance(tool, str) for tool in tools):
            fail(errors, f"{path}: tools must be a YAML string list")
            tools = []
        for tool in tools:
            if tool not in ALLOWED_TOOLS:
                fail(errors, f"{path}: use documented primary tool aliases only; got {tool!r}")

        agents = frontmatter.get("agents", [])
        if not isinstance(agents, list) or not all(isinstance(agent, str) for agent in agents):
            fail(errors, f"{path}: agents must be a YAML string list")
            agents = []
        if agents and "agent" not in tools:
            fail(errors, f"{path}: non-empty agents list requires the 'agent' tool")

        expected_user_invocable = agent_id in VISIBLE_AGENT_IDS
        actual_user_invocable = frontmatter.get("user-invocable", True)
        if bool(actual_user_invocable) != expected_user_invocable:
            fail(
                errors,
                f"{path}: user-invocable should be {str(expected_user_invocable).lower()} for this role",
            )

        if not body:
            fail(errors, f"{path}: instruction body must not be empty")

    agent_ids = set(parsed)

    # Validate references after all names and IDs are known.
    for agent_id, (path, frontmatter, _) in parsed.items():
        for worker_name in frontmatter.get("agents", []):
            if worker_name not in names:
                fail(errors, f"{path}: unknown subagent display name {worker_name!r}")

        for handoff in frontmatter.get("handoffs", []) or []:
            if not isinstance(handoff, dict):
                fail(errors, f"{path}: each handoff must be a mapping")
                continue
            target = handoff.get("agent")
            if target not in agent_ids:
                fail(errors, f"{path}: handoff references unknown agent id {target!r}")
            handoff_model = handoff.get("model")
            if handoff_model is not None:
                if not isinstance(handoff_model, str):
                    fail(errors, f"{path}: handoff model must be a string")
                elif base_handoff_model(handoff_model) not in ALLOWED_MODELS:
                    fail(errors, f"{path}: unsupported handoff model {handoff_model!r}")

    # Role contracts: these are deliberate architecture constraints, not generic VS Code rules.
    coordinator = parsed.get("over-the-luna")
    if coordinator:
        path, fm, _ = coordinator
        if set(fm.get("tools", [])) != {"agent", "todo"}:
            fail(errors, f"{path}: coordinator must remain router-only with agent + todo")
        if set(fm.get("agents", [])) != EXPECTED_COORDINATOR_WORKERS:
            fail(errors, f"{path}: coordinator worker allow-list drifted")

    for agent_id in EDITOR_AGENT_IDS:
        if agent_id in parsed:
            path, fm, _ = parsed[agent_id]
            tools = set(fm.get("tools", []))
            if not {"edit", "execute", "read", "search"}.issubset(tools):
                fail(errors, f"{path}: implementation role must have read/search/edit/execute")

    for agent_id in REVIEWER_AGENT_IDS:
        if agent_id in parsed:
            path, fm, _ = parsed[agent_id]
            if "edit" in set(fm.get("tools", [])):
                fail(errors, f"{path}: reviewer must not have edit capability")

    for agent_id, (path, fm, _) in parsed.items():
        if agent_id != "over-the-luna" and fm.get("agents", []):
            fail(errors, f"{path}: workers must not delegate recursively")

    if errors:
        print("Over the Luna validation FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Over the Luna validation passed: {len(files)} agents, plugin v{plugin['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
