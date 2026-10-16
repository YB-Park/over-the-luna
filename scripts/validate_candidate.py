#!/usr/bin/env python3
"""Static validation of the deliberately tiny next product candidate.

This checks the *declaration*, not VS Code runtime tool/permission behavior.
Do not use as proof of native host compatibility or task quality.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "experiments" / "next" / "candidate-plugin"
AGENTS = ROOT / "agents"


def validate() -> list[str]:
    problems = []
    manifest_path = ROOT / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"missing/invalid candidate manifest: {exc}"]
    if manifest.get("name") != "over-the-luna-next":
        problems.append("candidate plugin identity unexpected")
    if manifest.get("agents") != "agents/":
        problems.append("candidate agents path must be agents/")
    if "$schema" in manifest:
        problems.append("candidate is legacy Copilot format; do not mix schema layouts")
    files = sorted(AGENTS.glob("*.agent.md"))
    if [x.name for x in files] != ["over-the-luna-next.agent.md"]:
        problems.append("candidate must contain exactly one agent, no leaves")
        return problems
    p = files[0]
    try:
        s = p.read_text(encoding="utf-8")
        marker = s.find("\n---\n", 4)
        if not s.startswith("---\n") or marker < 0:
            return ["invalid candidate frontmatter boundaries"]
        fm = yaml.safe_load(s[4:marker])
        body = s[marker + len("\n---\n"):].strip()
    except (OSError, yaml.YAMLError) as exc:
        return [f"candidate frontmatter unavailable: {exc}"]
    if not isinstance(fm, dict):
        return ["candidate YAML frontmatter is not a mapping"]
    if fm.get("name") != "Over the Luna Next (Research)":
        problems.append("research agent display name missing/duplicate risk")
    if fm.get("target") != "vscode":
        problems.append("candidate intended for VS Code")
    if fm.get("user-invocable") is not True:
        problems.append("candidate must remain manually selectable")
    if fm.get("disable-model-invocation") is not True:
        problems.append("candidate Main must not be a subagent")
    for key in ("tools", "agents", "model", "handoffs", "infer", "mcp-servers", "hooks"):
        if key in fm:
            problems.append(f"candidate Main must omit {key}; keep effective controls in host")
    if len(body) < 800:
        problems.append("candidate instructions unexpectedly absent")
    for marker in ("actual diff", "Run the tests you claim passed",
                   "security sandbox", "Explicit user authorization"):
        if marker not in body:
            problems.append(f"candidate missing safety/verification clause: {marker}")
    forbidden = (ROOT / "mcp.json", ROOT / ".mcp.json", ROOT / "hooks.json")
    if any(p.exists() for p in forbidden):
        problems.append("candidate must not bundle MCP servers/hooks")
    return problems


if __name__ == "__main__":
    failures = validate()
    if failures:
        for failure in failures:
            print("CANDIDATE_INVALID:", failure)
        sys.exit(1)
    print("CANDIDATE_STATIC_PASS: one visible Main, host-owned model/tools, no bundled secrets, leaf agents or hooks")
