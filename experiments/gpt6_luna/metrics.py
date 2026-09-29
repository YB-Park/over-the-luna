#!/usr/bin/env python3
"""Extract model-qualification signals from Copilot CLI event/OTEL artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def read_event_text(path: Path) -> str:
    if not path.exists():
        return ""
    parts: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            parts.append(raw)
        else:
            parts.extend(strings(obj))
    return "\n".join(parts)


def count_name(text: str, name: str) -> int:
    return len(re.findall(re.escape(name), text, flags=re.IGNORECASE))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--case", required=True)
    p.add_argument("--run-label", required=True)
    p.add_argument("--events", type=Path, required=True)
    p.add_argument("--otel", type=Path, required=True)
    p.add_argument("--hidden", type=Path, required=True)
    p.add_argument("--contract", type=Path, required=True)
    p.add_argument("--candidate-exit", type=Path, required=True)
    p.add_argument("--start-ms", type=Path)
    p.add_argument("--first-output-ms", type=Path)
    p.add_argument("--end-ms", type=Path)
    p.add_argument("--diff", type=Path)
    p.add_argument("--status", type=Path)
    p.add_argument("--json-out", type=Path, required=True)
    args = p.parse_args()

    text = read_event_text(args.events)

    try:
        hidden = json.loads(args.hidden.read_text(encoding="utf-8"))
    except Exception:
        hidden = {"pass": False, "failures": ["hidden result missing or invalid"]}
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except Exception:
        contract = {}

    try:
        candidate_exit = int(args.candidate_exit.read_text().strip())
    except Exception:
        candidate_exit = -999

    def ms(path: Path | None):
        if not path or not path.exists():
            return None
        try:
            return int(path.read_text().strip())
        except Exception:
            return None

    start = ms(args.start_ms)
    first = ms(args.first_output_ms)
    end = ms(args.end_ms)

    route_match = re.search(
        r"Mode:\s*(SIMPLE|STANDARD|DEEP).*?Assurance:\s*(NONE|REVIEW|RISK)",
        text,
        re.S,
    )
    route = route_match.group(1) if route_match else None
    assurance = route_match.group(2) if route_match else None

    result = {
        "model": args.model,
        "case": args.case,
        "run_label": args.run_label,
        "candidate_exit": candidate_exit,
        "hidden_pass": bool(hidden.get("pass")),
        "hidden_failures": hidden.get("failures", []),
        "route": route,
        "assurance": assurance,
        "boundary_sealed": "Boundary sealed" in text,
        "boundary_reopen": "Boundary reopen:" in text,
        "architect_mentions": count_name(text, "Luna Architect"),
        "reviewer_mentions": count_name(text, "Luna Reviewer"),
        "recovery_mentions": count_name(text, "Luna Recovery"),
        "premium_mentions": count_name(text, "Premium Review"),
        "events_bytes": args.events.stat().st_size if args.events.exists() else 0,
        "otel_bytes": args.otel.stat().st_size if args.otel.exists() else 0,
        "elapsed_ms": (end - start) if start is not None and end is not None else None,
        "first_output_ms": (first - start) if start is not None and first is not None else None,
        "diff_bytes": args.diff.stat().st_size if args.diff and args.diff.exists() else 0,
        "status": (
            args.status.read_text(encoding="utf-8", errors="replace")
            if args.status and args.status.exists()
            else ""
        ),
    }

    changed_paths = []
    for raw in result["status"].splitlines():
        if len(raw) >= 4:
            changed_paths.append(raw[3:].strip())
    result["changed_paths"] = changed_paths

    contract_failures = []
    if route != contract.get("route"):
        contract_failures.append(f"route expected {contract.get('route')}, got {route}")
    if assurance != contract.get("assurance"):
        contract_failures.append(
            f"assurance expected {contract.get('assurance')}, got {assurance}"
        )
    if contract.get("boundary_required") and not result["boundary_sealed"]:
        contract_failures.append("required sealed boundary marker missing")
    allowed = set(contract.get("allowed_changed_paths", []))
    unexpected = sorted(set(changed_paths) - allowed)
    if unexpected:
        contract_failures.append(f"unexpected changed paths: {unexpected}")

    result["contract_failures"] = contract_failures
    result["contract_pass"] = not contract_failures
    result["gate_pass"] = (
        result["candidate_exit"] == 0
        and result["hidden_pass"]
        and result["contract_pass"]
    )

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
