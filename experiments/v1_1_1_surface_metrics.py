from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

ROUTE_RE = re.compile(r"Mode:\s*(SIMPLE|STANDARD|DEEP).*?Assurance:\s*(NONE|REVIEW|RISK)", re.S)
HANGUL_RE = re.compile(r"[가-힣]")
EXPECTED = {
    "tiny": ("SIMPLE", "NONE"),
    "broad": ("STANDARD", "REVIEW"),
    "broad_ko": ("STANDARD", "REVIEW"),
    "risk": (None, "RISK"),
    "detail": (None, None),
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    out = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            out.append(value)
    return out


def iter_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def attrs(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    result = {}
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, dict) or not isinstance(item.get("key"), str):
                continue
            raw = item.get("value")
            if isinstance(raw, dict):
                for key in ("stringValue", "intValue", "doubleValue", "boolValue"):
                    if key in raw:
                        raw = raw[key]
                        break
            result[item["key"]] = raw
    return result


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def read_exit(path: Path | None) -> int | None:
    if path is None or not path.exists():
        return None
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except ValueError:
        return 99


def read_ms(path: Path | None) -> int | None:
    if path is None or not path.exists():
        return None
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except ValueError:
        return None


def main_messages(events: list[dict[str, Any]]) -> list[str]:
    messages = []
    for event in events:
        if event.get("type") != "assistant.message" or event.get("agentId"):
            continue
        content = (event.get("data") or {}).get("content")
        if isinstance(content, str) and content.strip():
            messages.append(content.strip())
    return messages


def subagents(events: list[dict[str, Any]]) -> Counter[str]:
    names: Counter[str] = Counter()
    for event in events:
        if event.get("type") == "subagent.started":
            data = event.get("data") or {}
            name = data.get("agentName") or data.get("agentId") or "unknown"
            names[str(name)] += 1
    return names


def token_totals(path: Path) -> dict[str, int]:
    totals = {"input": 0, "output": 0, "reasoning": 0}
    if not path.exists():
        return totals
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        for obj in iter_dicts(raw):
            name = obj.get("name")
            a = attrs(obj.get("attributes"))
            op = a.get("gen_ai.operation.name")
            if op != "chat" and not (isinstance(name, str) and name.startswith("chat")):
                continue
            totals["input"] += as_int(a.get("gen_ai.usage.input_tokens"))
            totals["output"] += as_int(a.get("gen_ai.usage.output_tokens"))
            totals["reasoning"] += as_int(a.get("gen_ai.usage.reasoning_tokens"))
    return totals


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--variant", required=True)
    p.add_argument("--case", choices=EXPECTED, required=True)
    p.add_argument("--run-label")
    p.add_argument("--events", type=Path, required=True)
    p.add_argument("--otel", type=Path, required=True)
    p.add_argument("--candidate-exit", type=Path)
    p.add_argument("--hidden-exit", type=Path)
    p.add_argument("--candidate-start-ms", type=Path)
    p.add_argument("--candidate-first-output-ms", type=Path)
    p.add_argument("--candidate-end-ms", type=Path)
    p.add_argument("--json-out", type=Path, required=True)
    p.add_argument("--md-out", type=Path, required=True)
    a = p.parse_args()

    events = load_jsonl(a.events)
    messages = main_messages(events)
    joined = "\n".join(messages)
    final = messages[-1] if messages else ""
    match = ROUTE_RE.search(joined)
    mode = match.group(1) if match else None
    assurance = match.group(2) if match else None
    agents = subagents(events)
    reviewer = sum(n for name, n in agents.items() if "luna-reviewer" in name.lower())
    architect = sum(n for name, n in agents.items() if "luna-architect" in name.lower())

    candidate_exit = read_exit(a.candidate_exit)
    hidden_exit = read_exit(a.hidden_exit)
    start_ms = read_ms(a.candidate_start_ms)
    first_output_ms = read_ms(a.candidate_first_output_ms)
    end_ms = read_ms(a.candidate_end_ms)
    startup_ms = first_output_ms - start_ms if start_ms is not None and first_output_ms is not None else None
    total_ms = end_ms - start_ms if start_ms is not None and end_ms is not None else None
    after_first_output_ms = end_ms - first_output_ms if first_output_ms is not None and end_ms is not None else None

    expected_mode, expected_assurance = EXPECTED[a.case]
    failures = []
    if candidate_exit is None:
        failures.append("candidate process exit code missing")
    elif candidate_exit != 0:
        failures.append(f"candidate process exit={candidate_exit}")
    if not messages:
        failures.append("candidate produced no main assistant output")
    if expected_mode and mode != expected_mode:
        failures.append(f"mode expected {expected_mode}, got {mode}")
    if expected_assurance and assurance != expected_assurance:
        failures.append(f"assurance expected {expected_assurance}, got {assurance}")
    if a.case == "tiny" and (architect or reviewer):
        failures.append(f"tiny expected Architect=0 Reviewer=0, got {architect}/{reviewer}")
    if a.case in ("broad", "broad_ko") and (architect != 1 or reviewer != 1):
        failures.append(f"{a.case} expected Architect=1 Reviewer=1, got {architect}/{reviewer}")
    if a.case == "risk" and not (1 <= reviewer <= 2):
        failures.append(f"risk expected Reviewer=1..2, got {reviewer}")
    if a.case == "broad_ko" and len(HANGUL_RE.findall(final)) < 10:
        failures.append("broad_ko final response did not preserve Korean conversation language")
    if hidden_exit not in (None, 0):
        failures.append(f"hidden contract exit={hidden_exit}")

    tokens = token_totals(a.otel)
    data = {
        "run_label": a.run_label or f"{a.variant}-{a.case}",
        "variant": a.variant,
        "case": a.case,
        "gate_pass": not failures,
        "gate_failures": failures,
        "candidate_exit": candidate_exit,
        "mode": mode,
        "assurance": assurance,
        "main_message_count": len(messages),
        "visible_chars": len(joined),
        "final_chars": len(final),
        "visible_lines": len(joined.splitlines()),
        "boundary_markers": joined.count("Boundary sealed — work set:"),
        "architect_count": architect,
        "reviewer_count": reviewer,
        "subagents": dict(agents),
        "hidden_exit": hidden_exit,
        "hangul_chars_final": len(HANGUL_RE.findall(final)),
        "timing_ms": {
            "startup_to_first_output": startup_ms,
            "after_first_output": after_first_output_ms,
            "total": total_ms,
        },
        "otel_chat_tokens": tokens,
        "final_text": final,
    }
    a.json_out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = [
        f"# {data['run_label']}", "",
        f"- Gate: {'PASS' if not failures else 'FAIL'}",
        f"- Candidate exit: {candidate_exit}",
        f"- Route: {mode} / {assurance}",
        f"- Main visible messages: {len(messages)}",
        f"- Visible chars: {len(joined)}",
        f"- Final chars: {len(final)}",
        f"- OTel output tokens: {tokens['output']}",
        f"- OTel reasoning tokens: {tokens['reasoning']}",
        f"- Architect / Reviewer: {architect} / {reviewer}",
        f"- Startup to first output: {startup_ms if startup_ms is not None else 'n/a'} ms",
        f"- After first output: {after_first_output_ms if after_first_output_ms is not None else 'n/a'} ms",
        f"- Candidate total: {total_ms if total_ms is not None else 'n/a'} ms",
    ]
    if a.case == "broad_ko":
        md.append(f"- Hangul chars in final: {data['hangul_chars_final']}")
    if failures:
        md += ["", "## Gate failures"] + [f"- {x}" for x in failures]
    md += ["", "## Final text", "", final]
    a.md_out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
