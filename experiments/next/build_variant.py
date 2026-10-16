#!/usr/bin/env python3
"""Build model-only Over the Luna variants for GPT-5.6 vs GPT-6 qualification."""

from __future__ import annotations

import argparse
import difflib
import json
import shutil
from pathlib import Path

CONTROL = "GPT-5.6 Luna"
CANDIDATE = "GPT-6 Luna"
AUTOMATIC_AGENT_IDS = {
    "over-the-luna",
    "luna-planner",
    "luna-architect",
    "luna-skeptic",
    "luna-researcher",
    "luna-tool-worker",
    "luna-recovery",
    "luna-reviewer",
}


def build(source: Path, output: Path, model: str) -> None:
    if model not in {CONTROL, CANDIDATE}:
        raise SystemExit(f"unsupported model: {model}")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copy2(source / "plugin.json", output / "plugin.json")
    shutil.copytree(source / "agents", output / "agents")

    changed = []
    for agent_id in sorted(AUTOMATIC_AGENT_IDS):
        path = output / "agents" / f"{agent_id}.agent.md"
        text = path.read_text(encoding="utf-8")
        needle = f"model: {CONTROL}"
        count = text.count(needle)
        if count != 1:
            raise SystemExit(f"{path}: expected exactly one {needle!r}, found {count}")
        if model == CANDIDATE:
            text = text.replace(needle, f"model: {CANDIDATE}", 1)
            path.write_text(text, encoding="utf-8")
            changed.append(str(path.relative_to(output)))

    premium = (output / "agents" / "premium-review.agent.md").read_text(encoding="utf-8")
    if "model: Claude Sonnet 5" not in premium or CANDIDATE in premium:
        raise SystemExit("Premium Review model boundary drifted")

    manifest = {
        "model": model,
        "automatic_agents": sorted(AUTOMATIC_AGENT_IDS),
        "changed_paths": changed,
    }
    (output / "qualification-variant.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def verify_pair(source: Path, control_dir: Path, candidate_dir: Path) -> None:
    build(source, control_dir, CONTROL)
    build(source, candidate_dir, CANDIDATE)

    allowed = {
        f"agents/{agent_id}.agent.md" for agent_id in AUTOMATIC_AGENT_IDS
    } | {"qualification-variant.json"}

    control_files = {
        str(p.relative_to(control_dir))
        for p in control_dir.rglob("*")
        if p.is_file()
    }
    candidate_files = {
        str(p.relative_to(candidate_dir))
        for p in candidate_dir.rglob("*")
        if p.is_file()
    }
    if control_files != candidate_files:
        raise SystemExit("variant file sets differ")

    unexpected = []
    model_line_changes = 0
    for rel in sorted(control_files):
        a = (control_dir / rel).read_text(encoding="utf-8")
        b = (candidate_dir / rel).read_text(encoding="utf-8")
        if a == b:
            continue
        if rel not in allowed:
            unexpected.append(rel)
            continue
        if rel.startswith("agents/"):
            diff = list(difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm=""))
            removed = [x for x in diff if x == f"-model: {CONTROL}"]
            added = [x for x in diff if x == f"+model: {CANDIDATE}"]
            other = [
                x for x in diff
                if x.startswith(("+", "-"))
                and not x.startswith(("+++", "---"))
                and x not in {f"-model: {CONTROL}", f"+model: {CANDIDATE}"}
            ]
            if len(removed) != 1 or len(added) != 1 or other:
                raise SystemExit(f"{rel}: non-model diff detected: {other}")
            model_line_changes += 1

    if unexpected:
        raise SystemExit(f"unexpected variant differences: {unexpected}")
    if model_line_changes != len(AUTOMATIC_AGENT_IDS):
        raise SystemExit(
            f"expected {len(AUTOMATIC_AGENT_IDS)} model-only agent diffs, got {model_line_changes}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", choices=[CONTROL, CANDIDATE])
    parser.add_argument("--verify-pair", action="store_true")
    parser.add_argument("--control-output", type=Path)
    parser.add_argument("--candidate-output", type=Path)
    args = parser.parse_args()

    if args.verify_pair:
        if not args.control_output or not args.candidate_output:
            parser.error("--verify-pair requires --control-output and --candidate-output")
        verify_pair(args.source, args.control_output, args.candidate_output)
        print("model-only variant verification passed")
        return

    if not args.output or not args.model:
        parser.error("--output and --model are required unless --verify-pair is used")
    build(args.source, args.output, args.model)


if __name__ == "__main__":
    main()
