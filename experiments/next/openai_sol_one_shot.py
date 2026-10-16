#!/usr/bin/env python3
"""One tiny, manually gated OpenAI Responses API smoke. No retries or tools.

The API key is read from OPENAI_API_KEY and never printed. The output records
only model identity, usage and a categorical verdict, not raw content.
"""
from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = "gpt-6.1-sol"
BASE = "https://api.openai.com/v1"


def request_json(path: str, key: str, payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(
        BASE + path,
        data=body,
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        method="POST" if payload is not None else "GET",
    )
    try:
        with urlopen(request, timeout=70) as response:
            return json.load(response)
    except HTTPError as exc:
        # Do not print raw response bodies, request headers, or credentials.
        code = "unknown"
        try:
            raw = json.loads(exc.read(4096).decode("utf-8"))
            code = str(raw.get("error", {}).get("code") or raw.get("error", {}).get("type") or "unknown")
        except (ValueError, UnicodeError, AttributeError):
            pass
        print(f"OPENAI_API_BLOCKED: HTTP {exc.code}, code={code}", flush=True)
        raise SystemExit(1)
    except URLError:
        print("OPENAI_API_BLOCKED: network error", flush=True)
        raise SystemExit(1)


def main() -> int:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        print("OPENAI_API_BLOCKED: OPENAI_API_KEY Actions Secret missing or empty")
        return 1

    details = request_json("/models/" + MODEL, key)
    observed_catalog_model = details.get("id")
    if observed_catalog_model != MODEL:
        print("OPENAI_MODEL_GATE_INCONCLUSIVE: unexpected model metadata")
        return 1
    print("OPENAI_MODEL_METADATA_OK: " + MODEL, flush=True)

    # This is the ONLY billable inference request. Fixed max output (including
    # reasoning tokens), minimal input, low reasoning, no tools, no retries.
    result = request_json("/responses", key, {
        "model": MODEL,
        "input": "Reply with exactly SOL_API_OK. Do not add any other text.",
        "reasoning": {"effort": "low"},
        "max_output_tokens": 256,
        "store": False,
        "tools": [],
    })
    observed = str(result.get("model") or "unknown")
    usage = result.get("usage") or {}
    inp = int(usage.get("input_tokens") or 0)
    out = int(usage.get("output_tokens") or 0)
    print("OPENAI_OBSERVED_MODEL: " + observed, flush=True)
    print(f"OPENAI_USAGE: input_tokens={inp}, output_tokens={out}", flush=True)
    print(f"OPENAI_STANDARD_RATE_ESTIMATE_USD: {(2*inp+10*out)/1_000_000:.6f}", flush=True)
    print("NOTE: estimate excludes caching/other tiers; dashboard is billing source of truth.")

    chunks = []
    for item in result.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    chunks.append(str(content.get("text") or ""))
    answer = "".join(chunks).strip()
    if not observed.startswith(MODEL):
        print("OPENAI_SOL_MODEL_ID_MISMATCH")
        return 1
    if result.get("status") != "completed" or answer != "SOL_API_OK":
        print("OPENAI_SOL_INCONCLUSIVE: response/status did not meet exact smoke criterion")
        return 1
    print("OPENAI_SOL_DIRECT_API_PASS: exact model family, completed answer, usage captured")
    return 0


if __name__ == "__main__":
    sys.exit(main())
