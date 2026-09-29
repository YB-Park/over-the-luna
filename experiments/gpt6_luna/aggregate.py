#!/usr/bin/env python3
"""Aggregate matched GPT-5.6/GPT-6 Luna artifacts without auto-selecting a winner."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--json-out", type=Path, required=True)
    p.add_argument("--md-out", type=Path, required=True)
    args = p.parse_args()

    rows = []
    for path in sorted(args.root.rglob("metrics.json")):
        try:
            rows.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception as exc:
            rows.append({"artifact": str(path), "parse_error": str(exc)})

    summary = defaultdict(
        lambda: {"runs": 0, "hidden_pass": 0, "gate_pass": 0, "elapsed_ms": []}
    )
    for row in rows:
        if "model" not in row:
            continue
        s = summary[row["model"]]
        s["runs"] += 1
        s["hidden_pass"] += int(bool(row.get("hidden_pass")))
        s["gate_pass"] += int(bool(row.get("gate_pass")))
        if isinstance(row.get("elapsed_ms"), int):
            s["elapsed_ms"].append(row["elapsed_ms"])

    out = {
        "note": "Descriptive aggregate only. It intentionally does not rank or auto-promote a model.",
        "rows": rows,
        "by_model": {},
    }
    for model, s in summary.items():
        out["by_model"][model] = {
            "runs": s["runs"],
            "hidden_pass": s["hidden_pass"],
            "gate_pass": s["gate_pass"],
            "mean_elapsed_ms": (
                round(sum(s["elapsed_ms"]) / len(s["elapsed_ms"]))
                if s["elapsed_ms"]
                else None
            ),
        }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# GPT-6 Luna qualification aggregate",
        "",
        "Descriptive results only; no winner or migration decision is encoded in this script.",
        "",
        "| Model | Runs | Hidden pass | Gate pass | Mean elapsed ms |",
        "|---|---:|---:|---:|---:|",
    ]
    for model in sorted(out["by_model"]):
        s = out["by_model"][model]
        lines.append(
            f"| {model} | {s['runs']} | {s['hidden_pass']} | "
            f"{s['gate_pass']} | {s['mean_elapsed_ms'] or '-'} |"
        )
    lines += [
        "",
        "Inspect per-run patches, trajectories, routing, and telemetry before drawing conclusions.",
    ]
    args.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
