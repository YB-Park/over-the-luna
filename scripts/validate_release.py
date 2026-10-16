#!/usr/bin/env python3
"""Static RC2 role-topology checks: declaration only, NOT effective Host security."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
MAIN="over-the-luna-next.agent.md"
MODELS={
 "next-architect.agent.md":("Next Architect","GPT-6 Luna",["read","search"]),
 "next-reviewer.agent.md":("Next Reviewer","GPT-6 Luna",["read","search"]),
 "next-skeptic.agent.md":("Next Skeptic","GPT-6 Luna",["read","search"]),
 "next-researcher.agent.md":("Next Researcher","GPT-6 Luna",["read","search","web"]),
 "next-recovery.agent.md":("Next Recovery","GPT-6 Luna",["read","search"]),
 "next-sol-specialist.agent.md":("Next Sol Specialist","GPT-6.1 Sol",["read","search"]),
 "next-sonnet-specialist.agent.md":("Next Sonnet Specialist","Claude Sonnet 5.5",["read","search"]),
}
EXPECTED={MAIN,*MODELS}
FORBIDDEN_KEYS={"handoffs","infer","mcp-servers","hooks"}
BLOCK_EXTENSIONS=("mcp.json",".mcp.json","hooks.json",".copilot-plugin",".claude-plugin",
                  "skills","hooks","lsp","mcp")


def parse_agent(file:Path, errors:list[str]) -> tuple[dict,str]:
    try: text=file.read_text(encoding="utf-8")
    except OSError as ex:
        errors.append(f"{file.name}: missing: {type(ex).__name__}")
        return {}, ""
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"{file.name}: invalid frontmatter")
        return {}, ""
    stop=text.index("\n---\n",4)
    try: data=yaml.safe_load(text[4:stop])
    except yaml.YAMLError:
        errors.append(f"{file.name}: invalid YAML")
        return {}, ""
    if not isinstance(data,dict):
        errors.append(f"{file.name}: frontmatter not mapping")
        return {}, ""
    return data,text[stop+len("\n---\n"):]


def validate(root:Path=ROOT) -> list[str]:
    root=Path(root)
    errors=[]
    try: manifest=json.loads((root/"plugin.json").read_text(encoding="utf-8"))
    except (OSError,UnicodeError,ValueError) as ex:
        return [f"invalid plugin.json: {type(ex).__name__}"]
    if not isinstance(manifest,dict):return ["plugin.json must be object"]
    for key,wanted in (("name","over-the-luna-next"),("version","2.0.0-rc.2"),
                       ("agents","agents/")):
        if manifest.get(key)!=wanted: errors.append(f"plugin {key} mismatch")
    if "$schema" in manifest: errors.append("unexpected schema entry")

    folder=root/"agents"
    actual={p.name for p in folder.iterdir()} if folder.is_dir() else set()
    if actual!=EXPECTED: errors.append(f"agent file set mismatch missing={sorted(EXPECTED-actual)} extra={sorted(actual-EXPECTED)}")
    roles=set()
    for filename in sorted(EXPECTED&actual):
        meta,body=parse_agent(folder/filename,errors)
        if not meta:continue
        name=meta.get("name")
        if not isinstance(name,str) or name in roles:errors.append(f"{filename}: duplicate/invalid name")
        roles.add(name)
        if meta.get("target")!="vscode": errors.append(f"{filename}: target != vscode")
        if FORBIDDEN_KEYS.intersection(meta):
            errors.append(f"{filename}: forbidden control keys {sorted(FORBIDDEN_KEYS.intersection(meta))}")
        if filename==MAIN:
            if name!="Over the Luna Next": errors.append("Main name mismatch")
            if meta.get("user-invocable") is not True:errors.append("Main hidden")
            if meta.get("disable-model-invocation") is not True:errors.append("Main subagent callable")
            for key in ("model","tools","agents"):
                if key in meta:errors.append(f"Main {key} must be host-owned")
            if not all(k in body for k in ("Next Architect","Next Reviewer",
                "Next Sol Specialist","Next Sonnet Specialist",
                "actual diff","security sandbox")):
                errors.append("Main missing orchestration/evidence language")
        else:
            expectedName,expectedModel,expectedTools=MODELS[filename]
            if name!=expectedName:errors.append(f"{filename}: incorrect role name")
            if meta.get("user-invocable") is not False:errors.append(f"{filename}: visible leaf")
            if meta.get("disable-model-invocation") is True:errors.append(f"{filename}: cannot be invoked")
            if meta.get("model")!=expectedModel:errors.append(f"{filename}: model mismatch")
            if meta.get("tools")!=expectedTools:errors.append(f"{filename}: tools mismatch")
            if meta.get("agents")!=[]:errors.append(f"{filename}: recursion declaration mismatch")
            if not body.strip():errors.append(f"{filename}: empty instructions")
    for ext in BLOCK_EXTENSIONS:
        if (root/ext).exists():errors.append(f"bundled extension forbidden: {ext}")
    if any(root.rglob("SKILL.md")):errors.append("SKILL.md bundles forbidden")
    return errors

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    a=parser.parse_args()
    problems=validate(a.root)
    for problem in problems:print("RC2_INVALID:",problem)
    if problems:sys.exit(1)
    print("RC2_STATIC_PASS: one Main, seven distinct leaves, pinned role models, nonempty leaf read lists; Host enforcement NOT verified")
