#!/usr/bin/env python3
"""Parse one isolated Copilot CLI JSONL smoke result; no secrets or raw trace printed."""
from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = "P0B_AUTH_OK"

def verify(path: Path) -> int:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    messages = [
        ev.get("data", {}).get("content", "")
        for ev in events
        if ev.get("type") == "assistant.message"
        and isinstance(ev.get("data"), dict)
    ]
    starts = [ev for ev in events if ev.get("type") == "session.start"]
    observed = [
        ev.get("data", {}).get("model")
        for ev in starts
        if isinstance(ev.get("data"), dict)
        and isinstance(ev.get("data", {}).get("model"), str)
    ]
    if not messages or messages[-1].strip() != EXPECTED:
        print("INCONCLUSIVE: exact smoke response not found; no model success claimed.")
        print("Event kinds:", ",".join(sorted({str(e.get("type")) for e in events})))
        return 1
    if not observed:
        print("AUTH_AND_RESPONSE_OK; model ID not independently observed in session.start.")
        print("P0b model-identity gate remains INCONCLUSIVE.")
        return 0
    print("AUTH_AND_RESPONSE_OK; runtime session.start model:", observed[-1])
    if observed[-1].lower() != "gpt-6-luna":
        print("BLOCKED: configured model differs from observed session model.")
        return 1
    print("P0b Luna model identity verified in CLI session.start.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_one_shot.py path.jsonl")
    raise SystemExit(verify(Path(sys.argv[1])))
