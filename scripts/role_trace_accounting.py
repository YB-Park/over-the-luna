#!/usr/bin/env python3
"""Offline Copilot role/cost accounting. Observations are not Host proof.

Accepts recorded public-session summary.json; no SDK, credentials, web, or
model calls. Output contains aggregate metrics, never prompts or tool data.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path


def _sum_metric(events: list, key: str) -> int | None:
    values = [event.get(key) for event in events]
    if not values or any(type(n) is not int or n < 0 for n in values):
        return None
    return sum(values)


def _pair_lifecycle(starts: list, completions: list) -> int:
    """Match only named lifecycle pairs; ID mismatch cannot count as a pair."""
    def key(event: dict):
        name = event.get("name")
        if not isinstance(name, str) or not name.strip():
            return None
        ident = event.get("toolCallId")
        return name.strip(), ident if isinstance(ident, str) and ident else None

    left = Counter(key(e) for e in starts if isinstance(e, dict))
    right = Counter(key(e) for e in completions if isinstance(e, dict))
    left.pop(None, None)
    right.pop(None, None)
    return sum(min(count, right.get(k, 0)) for k, count in left.items())


def account_arm(arm: dict, runtime: str) -> dict:
    if not isinstance(arm, dict):
        raise ValueError("arm must be an object")
    usage = arm.get("usage", [])
    events = arm.get("events", [])
    starts = arm.get("subagentStarts", [])
    done = arm.get("subagentCompleted", [])
    if not all(isinstance(xs, list) for xs in (usage, events, starts, done)):
        raise ValueError("usage/events/subagent fields must be lists")
    if not all(isinstance(x, dict) for x in usage + events):
        raise ValueError("usage/events entries must be objects")

    tool_starts = [e.get("name") for e in events
                   if e.get("type") == "tool.execution_start"]
    task_attempts = sum(name == "task" for name in tool_starts)
    named_pairs = _pair_lifecycle(starts, done)

    if named_pairs:
        role_status = "LIFECYCLE_ONLY_HANDOFF_UNVERIFIED"
    elif task_attempts:
        role_status = "TASK_ATTEMPTS_ONLY"
    else:
        role_status = "NO_NAMED_DELEGATION_OBSERVED"

    grading = arm.get("grading") if isinstance(arm.get("grading"), dict) else {}
    checks = grading.get("checks")
    accepted = all((
        arm.get("acceptance") is True,
        grading.get("pass") is True,
        isinstance(checks, dict) and bool(checks) and
            all(value is True for value in checks.values()),
        grading.get("failed_checks") == [],
        type(grading.get("num_user_tests")) is int and
            grading["num_user_tests"] > 0,
        arm.get("modelObserved") is True,
        "error" in arm and arm["error"] is None,
        arm.get("unexpectedPaths") == [],
    ))
    return {
        "mode": arm.get("mode"),
        "runtime": runtime,
        "qualityAccepted": accepted,
        "roleEvidenceStatus": role_status,
        "hostHandbackProven": False,
        "toolStarts": len(tool_starts),
        "taskAttempts": task_attempts,
        "pairedNamedLifecycleEvents": named_pairs,
        "durationMs": arm.get("durationMs"),
        "usageEvents": len(usage),
        "inputTokens": _sum_metric(usage, "inputTokens"),
        "outputTokens": _sum_metric(usage, "outputTokens"),
        "reportedCopilotNanoAiuSum": _sum_metric(usage, "copilotNanoAiu"),
    }


def account(data: dict) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("arms"), list):
        raise ValueError("expected summary object with arms list")
    runtime = "STANDALONE_SDK" if data.get("sdk") else "UNSPECIFIED"
    arms = [account_arm(a, runtime) for a in data["arms"]]
    result = {
        "schema": 1,
        "sourceSchema": data.get("schema"),
        "arms": arms,
        "warnings": [
            "tool start/complete is not proof of successful named delegation",
            "lifecycle events alone do not establish returned evidence or Host-native execution",
            "usage events and Copilot nano-AIU are not OpenAI API USD",
        ],
    }
    by_mode = {a["mode"]: a for a in arms}
    if "sdk_default" in by_mode and "rc2_actual_plugin" in by_mode:
        baseline, candidate = by_mode["sdk_default"], by_mode["rc2_actual_plugin"]
        delta = None
        pct = None
        if baseline["inputTokens"] is not None and candidate["inputTokens"] is not None:
            delta = candidate["inputTokens"] - baseline["inputTokens"]
            if baseline["inputTokens"] > 0:
                pct = round(100 * delta / baseline["inputTokens"], 1)
        result["comparison"] = {
            "inputTokenDelta": delta,
            "inputTokenDeltaPercent": pct,
            "bothQualityAccepted": baseline["qualityAccepted"] and candidate["qualityAccepted"],
            "councilContributionProven": False,
            "causalAttribution": "NOT_ESTABLISHED",
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, type=Path)
    args = parser.parse_args()
    with args.summary.open(encoding="utf-8") as fh:
        source = json.load(fh)
    print(json.dumps(account(source), ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
