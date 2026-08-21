from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

EXPECTED_LABELS = (
    "control-broad",
    "economy-broad-r1",
    "economy-broad-r2",
    "control-risk",
    "economy-risk",
    "control-broad-ko",
    "economy-broad-ko",
)


def pct(candidate: int, control: int) -> float | None:
    if not control:
        return None
    return (candidate / control - 1) * 100


def fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:+.1f}%"


def fmt_ms(value: int | None) -> str:
    if value is None:
        return "n/a"
    if value >= 1000:
        return f"{value / 1000:.1f}s"
    return f"{value}ms"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--json-out", type=Path, required=True)
    p.add_argument("--md-out", type=Path, required=True)
    p.add_argument("--blind-out", type=Path, required=True)
    p.add_argument("--key-out", type=Path, required=True)
    a = p.parse_args()

    rows = []
    for path in a.root.rglob("metrics.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict) and data.get("run_label"):
            rows.append(data)

    by_label = {r["run_label"]: r for r in rows}
    missing = [label for label in EXPECTED_LABELS if label not in by_label]
    hard_gates_pass = not missing and all(bool(by_label[label].get("gate_pass")) for label in EXPECTED_LABELS)

    control_broad = by_label.get("control-broad")
    econ_broad = [by_label.get("economy-broad-r1"), by_label.get("economy-broad-r2")]
    econ_broad = [r for r in econ_broad if r]
    broad_reductions = [pct(r["visible_chars"], control_broad["visible_chars"]) for r in econ_broad] if control_broad else []
    avg_broad_reduction = sum(x for x in broad_reductions if x is not None) / len(broad_reductions) if broad_reductions and all(x is not None for x in broad_reductions) else None

    startup_anomalies = []
    for label in EXPECTED_LABELS:
        row = by_label.get(label)
        if not row:
            continue
        startup = (row.get("timing_ms") or {}).get("startup_to_first_output")
        if isinstance(startup, int) and startup >= 120_000:
            startup_anomalies.append({"run_label": label, "startup_ms": startup})

    ko_control = by_label.get("control-broad-ko")
    ko_economy = by_label.get("economy-broad-ko")
    risk_control = by_label.get("control-risk")
    risk_economy = by_label.get("economy-risk")

    ko_reduction = pct(ko_economy["visible_chars"], ko_control["visible_chars"]) if ko_control and ko_economy else None
    risk_reduction = pct(risk_economy["visible_chars"], risk_control["visible_chars"]) if risk_control and risk_economy else None

    candidate_ready = bool(hard_gates_pass and avg_broad_reduction is not None and avg_broad_reduction <= -25.0)
    status = "READY_FOR_HUMAN_PREFERENCE" if candidate_ready else "HOLD"

    payload = {
        "runs_found": len(rows),
        "expected_runs": len(EXPECTED_LABELS),
        "missing": missing,
        "hard_gates_pass": hard_gates_pass,
        "economy_broad_visible_reductions_pct": broad_reductions,
        "economy_broad_average_visible_reduction_pct": avg_broad_reduction,
        "economy_broad_ko_visible_reduction_pct": ko_reduction,
        "economy_risk_visible_reduction_pct": risk_reduction,
        "startup_anomalies": startup_anomalies,
        "status": status,
        "runs": rows,
    }
    a.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# v1.1.1 Surface Economy — Phase 2 aggregate",
        "",
        f"Runs found: **{len(rows)} / {len(EXPECTED_LABELS)}**",
        f"Hard gates: **{'PASS' if hard_gates_pass else 'FAIL'}**",
        f"Decision state: **{status}**",
        "",
        "| Run | Gate | Route | Visible chars | Startup → first output | After first output |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for label in EXPECTED_LABELS:
        row = by_label.get(label)
        if not row:
            lines.append(f"| {label} | MISSING | — | — | — | — |")
            continue
        timing = row.get("timing_ms") or {}
        lines.append(
            f"| {label} | {'PASS' if row.get('gate_pass') else 'FAIL'} | "
            f"{row.get('mode')} / {row.get('assurance')} | {row.get('visible_chars')} | "
            f"{fmt_ms(timing.get('startup_to_first_output'))} | {fmt_ms(timing.get('after_first_output'))} |"
        )

    lines += [
        "",
        "## Economy deltas",
        "",
        f"- Broad repeat 1 vs fresh control: {fmt_pct(broad_reductions[0]) if len(broad_reductions) > 0 else 'missing'}",
        f"- Broad repeat 2 vs fresh control: {fmt_pct(broad_reductions[1]) if len(broad_reductions) > 1 else 'missing'}",
        f"- Broad average: {fmt_pct(avg_broad_reduction)}",
        f"- Korean broad vs control: {fmt_pct(ko_reduction)}",
        f"- RISK vs control: {fmt_pct(risk_reduction)}",
        "",
        "## Startup observation",
        "",
    ]
    if startup_anomalies:
        for item in startup_anomalies:
            lines.append(f"- {item['run_label']}: startup anomaly {fmt_ms(item['startup_ms'])}")
    else:
        lines.append("- No startup-to-first-output delay >= 120s observed.")
    lines += [
        "",
        "## Promotion rule",
        "",
        "- Every targeted correctness/routing/language gate must pass.",
        "- Economy broad must average at least 25% less visible output than the fresh control.",
        "- Startup anomalies are reported separately and do not fail the prompt candidate by themselves.",
        "- Human preference on anonymized outputs is the final qualitative check before v1.1.1 promotion.",
    ]
    a.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    pairs = [
        ("Broad implementation", "control-broad", "economy-broad-r1"),
        ("Korean broad implementation", "control-broad-ko", "economy-broad-ko"),
        ("RISK implementation", "control-risk", "economy-risk"),
    ]
    rng = random.Random(20260821)
    blind_lines = [
        "# Blind preference check",
        "",
        "For each pair, choose A or B based on usefulness, clarity, and appropriate brevity. Do not reward brevity if important verification or risk information is lost.",
    ]
    key = {}
    for idx, (title, control_label, economy_label) in enumerate(pairs, start=1):
        left = by_label.get(control_label)
        right = by_label.get(economy_label)
        if not left or not right:
            continue
        entries = [("control", left), ("economy", right)]
        rng.shuffle(entries)
        key[str(idx)] = {"A": entries[0][0], "B": entries[1][0], "title": title}
        blind_lines += [
            "",
            f"## Pair {idx} — {title}",
            "",
            "### A",
            "",
            entries[0][1].get("final_text", ""),
            "",
            "### B",
            "",
            entries[1][1].get("final_text", ""),
        ]
    a.blind_out.write_text("\n".join(blind_lines) + "\n", encoding="utf-8")
    a.key_out.write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
