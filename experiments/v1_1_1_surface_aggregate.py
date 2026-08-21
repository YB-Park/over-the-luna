from __future__ import annotations

import argparse
import json
from pathlib import Path

VARIANTS = ("control", "naive", "semantic", "economy")
CASES = ("tiny", "broad", "detail")


def pct(candidate: int, control: int) -> str:
    if not control:
        return "n/a"
    return f"{(candidate / control - 1) * 100:+.1f}%"


def ratio(candidate: int, control: int) -> str:
    if not control:
        return "n/a"
    return f"{candidate / control:.2f}x"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--json-out", type=Path, required=True)
    p.add_argument("--md-out", type=Path, required=True)
    a = p.parse_args()

    rows = []
    for path in a.root.rglob("metrics.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict) and data.get("variant") and data.get("case"):
            rows.append(data)

    by_key = {(r["variant"], r["case"]): r for r in rows}
    controls = {case: by_key.get(("control", case)) for case in CASES}
    summary = []
    for variant in VARIANTS:
        vr = [by_key.get((variant, case)) for case in CASES]
        present = [r for r in vr if r]
        gates = all(bool(r.get("gate_pass")) for r in present) and len(present) == len(CASES)
        tiny = by_key.get((variant, "tiny")); broad = by_key.get((variant, "broad")); detail = by_key.get((variant, "detail"))
        ct, cb, cd = controls["tiny"], controls["broad"], controls["detail"]
        item = {
            "variant": variant,
            "all_phase1_gates_pass": gates,
            "tiny_visible_vs_control": pct(tiny["visible_chars"], ct["visible_chars"]) if tiny and ct else "missing",
            "broad_visible_vs_control": pct(broad["visible_chars"], cb["visible_chars"]) if broad and cb else "missing",
            "broad_reasoning_vs_control": ratio(broad["otel_chat_tokens"]["reasoning"], cb["otel_chat_tokens"]["reasoning"]) if broad and cb else "missing",
            "detail_final_vs_control": ratio(detail["final_chars"], cd["final_chars"]) if detail and cd else "missing",
        }
        summary.append(item)

    payload = {"runs_found": len(rows), "runs": rows, "summary": summary}
    a.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# v1.1.1 Surface Economy — Phase 1 aggregate", "",
        f"Runs found: **{len(rows)} / 12**", "",
        "| Variant | Gates | Tiny visible Δ | Broad visible Δ | Broad reasoning | Detail final length |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in summary:
        lines.append(
            f"| {r['variant']} | {'PASS' if r['all_phase1_gates_pass'] else 'FAIL'} | "
            f"{r['tiny_visible_vs_control']} | {r['broad_visible_vs_control']} | "
            f"{r['broad_reasoning_vs_control']} | {r['detail_final_vs_control']} |"
        )
    lines += [
        "", "## Selection notes", "",
        "- A variant with any hard-gate failure is ineligible regardless of brevity.",
        "- Prefer large visible reduction on `tiny`/`broad` without a material reasoning collapse on `broad`.",
        "- `detail` is a reverse gate: an explicit request for detail must still produce a substantively detailed answer.",
        "- Human preference should compare anonymized final outputs after the hard gates, not replace them.",
    ]
    a.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
