#!/usr/bin/env python3
"""Static shape validation for the minimal RC, NOT a runtime security sandbox."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def validate(root: Path = ROOT) -> list[str]:
    root = Path(root)
    failures = []
    try:
        manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        return ["invalid or missing plugin.json: " + type(error).__name__]
    if not isinstance(manifest, dict):
        return ["plugin.json must contain a JSON object"]
    for key, value in (("name", "over-the-luna-next"),
                       ("version", "2.0.0-rc.1"), ("agents", "agents/")):
        if manifest.get(key) != value:
            failures.append(f"plugin.json {key} must be {value}")
    if "$schema" in manifest:
        failures.append("unexpected schema for legacy Copilot-format plugin")
    agents_dir = root / "agents"
    names = sorted(p.name for p in agents_dir.iterdir()) if agents_dir.is_dir() else []
    if names != ["over-the-luna-next.agent.md"]:
        return failures + ["agents/ must contain exactly one approved Main and no other files"]
    file = agents_dir / "over-the-luna-next.agent.md"
    text = file.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return failures + ["agent frontmatter missing"]
    split = text.find("\n---\n", 4)
    try:
        fm = yaml.safe_load(text[4:split])
    except yaml.YAMLError:
        return failures + ["invalid agent YAML"]
    if not isinstance(fm, dict):
        return failures + ["agent frontmatter must be a mapping"]
    for key, value in (("name","Over the Luna Next"), ("target","vscode"),
                       ("user-invocable",True), ("disable-model-invocation",True)):
        if fm.get(key) != value:
            failures.append(f"agent frontmatter {key} mismatch")
    for name in ("tools","agents","model","handoffs","infer","mcp-servers","hooks"):
        if name in fm:
            failures.append(f"Main must omit {name}; effective permissions belong to Host")
    body = text[split+len("\n---\n"):]
    for phrase in ("Run the tests you claim passed","actual diff","security sandbox",
                   "Explicit user authorization"):
        if phrase not in body:
            failures.append("required evidence/permission language missing: "+phrase)
    for rel in ("mcp.json",".mcp.json","hooks.json",".copilot-plugin",".claude-plugin",
                "skills","hooks","lsp","mcp"):
        if (root / rel).exists():
            failures.append("unexpected plugin extension: "+rel)
    if any(root.rglob("SKILL.md")):
        failures.append("unexpected bundled SKILL.md")
    return failures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    args = parser.parse_args()
    errs = validate(args.root)
    for err in errs:
        print("RELEASE_CANDIDATE_INVALID:",err)
    if errs: sys.exit(1)
    print("RELEASE_CANDIDATE_STATIC_PASS: one Main, host-owned model/tools, no bundled extensions")
