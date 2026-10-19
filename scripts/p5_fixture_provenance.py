#!/usr/bin/env python3
"""Verify that a compact P5 fixture matches an immutable public artifact.

No network requests or model calls. Use ONLY the public P5 summary.json,
never a company trace. Output contains no source/session content.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

P5_SUMMARY_SHA256 = "9f678b2c60267e95f414b098d28da3c5de713d09c075b04147c5967784b5b504"
P5_ACTIONS_RUN = 38869234496
P5_ARTIFACT_ID = 12032631126


def compact(source: dict) -> dict:
    """Allowlist fields only; avoid leaking unused content/tool arguments."""
    if (not isinstance(source, dict) or source.get("schema") != 1 or
            source.get("sdk") != "@github/copilot-sdk@1.0.19"):
        raise ValueError("unexpected P5 summary schema/runtime")
    arms = source.get("arms")
    if (not isinstance(arms, list) or len(arms) != 2 or
            [a.get("mode") for a in arms] != ["sdk_default", "rc2_actual_plugin"]):
        raise ValueError("unexpected P5 arm set/order")
    result = {"schema": 1, "sdk": source["sdk"], "arms": []}
    for arm in arms:
        grading = arm["grading"]
        if not isinstance(grading, dict) or not isinstance(grading["checks"], dict):
            raise ValueError("missing independent grader checks")
        compact_arm = {
            "mode": arm["mode"],
            "acceptance": arm["acceptance"],
            "grading": {k: grading[k] for k in
                        ("checks", "failed_checks", "num_user_tests", "pass")},
            "durationMs": arm["durationMs"],
        }
        if arm["mode"] == "rc2_actual_plugin":
            compact_arm.update({k: arm[k] for k in
                               ("roleChain", "architectObserved", "reviewerObserved")})
        compact_arm.update({
            "modelObserved": arm["modelObserved"],
            "unexpectedPaths": arm["unexpectedPaths"],
            "error": arm["error"],
            "subagentStarts": arm["subagentStarts"],
            "subagentCompleted": arm["subagentCompleted"],
            "events": [
                {"type": e["type"], "name": e["name"]}
                for e in arm["events"] if e.get("type") == "tool.execution_start"
            ],
            "usage": [
                {"model": u["model"], "inputTokens": u["inputTokens"],
                 "outputTokens": u["outputTokens"], "copilotNanoAiu": u["copilotNanoAiu"]}
                for u in arm["usage"]
            ],
        })
        result["arms"].append(compact_arm)
    return result


def verify(raw: bytes, fixture: dict) -> None:
    if hashlib.sha256(raw).hexdigest() != P5_SUMMARY_SHA256:
        raise ValueError("P5 summary is not pinned public Actions source")
    if compact(json.loads(raw)) != fixture:
        raise ValueError("compact fixture deviates from pinned P5 public summary")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--fixture", required=True, type=Path)
    args = parser.parse_args()
    verify(args.source.read_bytes(),
           json.loads(args.fixture.read_text(encoding="utf-8")))
    print("P5_PROVENANCE_PASS: artifact=12032631126 summary_sha256=" +
          P5_SUMMARY_SHA256)


if __name__ == "__main__":
    main()
