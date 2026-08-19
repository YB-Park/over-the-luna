#!/usr/bin/env python3
"""Summarize Copilot OTel tool ownership by nearest agent span."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from analyze_otel import OP_EXECUTE_TOOL, is_main_agent, load_spans, nearest_agent


def summarize_tool_ownership(path: Path) -> dict:
    spans = load_spans(path)
    by_span_id = {span.span_id: span for span in spans if span.span_id}
    by_agent: dict[str, Counter[str]] = defaultdict(Counter)

    for span in spans:
        if span.operation != OP_EXECUTE_TOOL:
            continue
        agent = nearest_agent(span, by_span_id)
        tool = span.tool_name or "unknown"
        by_agent[agent][tool] += 1

    main = Counter()
    leaf = Counter()
    for agent, tools in by_agent.items():
        if is_main_agent(agent):
            main.update(tools)
        else:
            leaf.update(tools)

    return {
        "main": dict(main),
        "leaf": dict(leaf),
        "by_agent": {agent: dict(tools) for agent, tools in sorted(by_agent.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize_tool_ownership(args.trace), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
