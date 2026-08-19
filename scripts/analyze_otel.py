#!/usr/bin/env python3
"""Summarize VS Code Copilot OTel JSONL for Over the Luna experiments.

The VS Code Copilot file exporter writes one JSON-serialized ReadableSpan per line.
This script intentionally uses only standard/observed GenAI attributes and tolerates
minor shape differences between OpenTelemetry SDK versions.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

OP_INVOKE_AGENT = "invoke_agent"
OP_CHAT = "chat"
OP_EXECUTE_TOOL = "execute_tool"

ATTR_OPERATION = "gen_ai.operation.name"
ATTR_AGENT = "gen_ai.agent.name"
ATTR_MODEL_REQUEST = "gen_ai.request.model"
ATTR_MODEL_RESPONSE = "gen_ai.response.model"
ATTR_TOOL = "gen_ai.tool.name"
ATTR_CONVERSATION = "gen_ai.conversation.id"
ATTR_CHAT_SESSION = "copilot_chat.chat_session_id"
ATTR_INPUT = "gen_ai.usage.input_tokens"
ATTR_OUTPUT = "gen_ai.usage.output_tokens"
ATTR_CACHE_READ = "gen_ai.usage.cache_read.input_tokens"
ATTR_CACHE_CREATE = "gen_ai.usage.cache_creation.input_tokens"
ATTR_REASONING = "gen_ai.usage.reasoning_tokens"

REVIEW_AGENT_HINTS = ("reviewer", "review")
MUTATION_TOOL_HINTS = (
    "apply_patch",
    "create",
    "edit",
    "insert_edit",
    "multi_replace",
    "replace_string",
    "write",
)


@dataclass
class Span:
    name: str
    attributes: dict[str, Any]
    trace_id: str | None
    span_id: str | None
    parent_span_id: str | None
    raw: dict[str, Any]

    @property
    def operation(self) -> str:
        value = self.attributes.get(ATTR_OPERATION)
        if isinstance(value, str):
            return value
        if self.name.startswith("invoke_agent"):
            return OP_INVOKE_AGENT
        if self.name.startswith("chat"):
            return OP_CHAT
        if self.name.startswith("execute_tool"):
            return OP_EXECUTE_TOOL
        return ""

    @property
    def agent_name(self) -> str:
        value = self.attributes.get(ATTR_AGENT)
        if isinstance(value, str) and value:
            return value
        if self.operation == OP_INVOKE_AGENT:
            suffix = self.name.removeprefix("invoke_agent").strip()
            return suffix or "unknown"
        return ""

    @property
    def tool_name(self) -> str:
        value = self.attributes.get(ATTR_TOOL)
        if isinstance(value, str) and value:
            return value
        if self.operation == OP_EXECUTE_TOOL:
            return self.name.removeprefix("execute_tool").strip()
        return ""

    @property
    def model(self) -> str:
        value = self.attributes.get(ATTR_MODEL_RESPONSE) or self.attributes.get(ATTR_MODEL_REQUEST)
        return value if isinstance(value, str) else "unknown"


@dataclass
class TokenUsage:
    input: int = 0
    output: int = 0
    cache_read: int = 0
    cache_create: int = 0
    reasoning: int = 0

    def add_span(self, span: Span) -> None:
        self.input += as_int(span.attributes.get(ATTR_INPUT))
        self.output += as_int(span.attributes.get(ATTR_OUTPUT))
        self.cache_read += as_int(span.attributes.get(ATTR_CACHE_READ))
        self.cache_create += as_int(span.attributes.get(ATTR_CACHE_CREATE))
        self.reasoning += as_int(span.attributes.get(ATTR_REASONING))

    def to_dict(self) -> dict[str, int]:
        return {
            "input": self.input,
            "output": self.output,
            "cache_read": self.cache_read,
            "cache_create": self.cache_create,
            "reasoning": self.reasoning,
        }


@dataclass
class Summary:
    span_count: int = 0
    invoke_agent_count: int = 0
    chat_count: int = 0
    tool_count: int = 0
    subagent_count: int = 0
    reviewer_invocations: int = 0
    mode: str = "UNKNOWN"
    first_mutation_tool: str | None = None
    total_tokens: TokenUsage = field(default_factory=TokenUsage)
    main_tokens: TokenUsage = field(default_factory=TokenUsage)
    council_tokens: TokenUsage = field(default_factory=TokenUsage)
    by_agent_tokens: dict[str, TokenUsage] = field(default_factory=dict)
    by_model_tokens: dict[str, TokenUsage] = field(default_factory=dict)
    tools: Counter[str] = field(default_factory=Counter)
    agents: Counter[str] = field(default_factory=Counter)

    def to_dict(self) -> dict[str, Any]:
        return {
            "span_count": self.span_count,
            "invoke_agent_count": self.invoke_agent_count,
            "chat_count": self.chat_count,
            "tool_count": self.tool_count,
            "subagent_count": self.subagent_count,
            "reviewer_invocations": self.reviewer_invocations,
            "mode": self.mode,
            "first_mutation_tool": self.first_mutation_tool,
            "tokens": {
                "total": self.total_tokens.to_dict(),
                "main": self.main_tokens.to_dict(),
                "council": self.council_tokens.to_dict(),
                "by_agent": {k: v.to_dict() for k, v in sorted(self.by_agent_tokens.items())},
                "by_model": {k: v.to_dict() for k, v in sorted(self.by_model_tokens.items())},
            },
            "agents": dict(self.agents.most_common()),
            "tools": dict(self.tools.most_common()),
        }


def as_int(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return 0
    return 0


def normalize_attributes(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not isinstance(value, list):
        return {}
    result: dict[str, Any] = {}
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


def get_span_context(raw: dict[str, Any]) -> tuple[str | None, str | None]:
    for key in ("spanContext", "_spanContext"):
        ctx = raw.get(key)
        if isinstance(ctx, dict):
            trace_id = ctx.get("traceId")
            span_id = ctx.get("spanId")
            return (
                trace_id if isinstance(trace_id, str) else None,
                span_id if isinstance(span_id, str) else None,
            )
    trace_id = raw.get("traceId")
    span_id = raw.get("spanId")
    return (
        trace_id if isinstance(trace_id, str) else None,
        span_id if isinstance(span_id, str) else None,
    )


def get_parent_span_id(raw: dict[str, Any]) -> str | None:
    direct = raw.get("parentSpanId")
    if isinstance(direct, str):
        return direct
    for key in ("parentSpanContext", "_parentSpanContext"):
        ctx = raw.get(key)
        if isinstance(ctx, dict):
            value = ctx.get("spanId")
            if isinstance(value, str):
                return value
    return None


def looks_like_span(raw: dict[str, Any]) -> bool:
    name = raw.get("name")
    if not isinstance(name, str):
        return False
    attrs = normalize_attributes(raw.get("attributes"))
    operation = attrs.get(ATTR_OPERATION)
    return isinstance(operation, str) or name.startswith(("invoke_agent", "chat", "execute_tool"))


def recursively_find_spans(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if looks_like_span(value):
            yield value
            return
        for child in value.values():
            yield from recursively_find_spans(child)
    elif isinstance(value, list):
        for child in value:
            yield from recursively_find_spans(child)


def load_spans(path: Path) -> list[Span]:
    spans: list[Span] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        for raw in recursively_find_spans(parsed):
            trace_id, span_id = get_span_context(raw)
            spans.append(
                Span(
                    name=str(raw.get("name", "")),
                    attributes=normalize_attributes(raw.get("attributes")),
                    trace_id=trace_id,
                    span_id=span_id,
                    parent_span_id=get_parent_span_id(raw),
                    raw=raw,
                )
            )
    return spans


def detect_mode(spans: Iterable[Span]) -> str:
    haystack = "\n".join(json.dumps(span.raw, ensure_ascii=False) for span in spans)
    for mode in ("DEEP", "STANDARD", "SIMPLE", "DIRECT", "ISOLATE"):
        if f"Mode: {mode}" in haystack:
            return mode
    return "UNKNOWN"


def is_mutation_tool(name: str) -> bool:
    lowered = name.lower()
    return any(hint in lowered for hint in MUTATION_TOOL_HINTS)


def nearest_agent(span: Span, by_span_id: dict[str, Span]) -> str:
    cursor = span
    visited: set[str] = set()
    while cursor.parent_span_id and cursor.parent_span_id not in visited:
        visited.add(cursor.parent_span_id)
        parent = by_span_id.get(cursor.parent_span_id)
        if parent is None:
            break
        if parent.operation == OP_INVOKE_AGENT:
            return parent.agent_name
        cursor = parent
    return "main"


def summarize(spans: list[Span]) -> Summary:
    summary = Summary(span_count=len(spans), mode=detect_mode(spans))
    by_span_id = {span.span_id: span for span in spans if span.span_id}

    roots = [span for span in spans if span.operation == OP_INVOKE_AGENT and not span.parent_span_id]
    root_ids = {span.span_id for span in roots if span.span_id}

    for span in spans:
        if span.operation == OP_INVOKE_AGENT:
            summary.invoke_agent_count += 1
            agent = span.agent_name or "unknown"
            summary.agents[agent] += 1
            if span.span_id not in root_ids:
                summary.subagent_count += 1
            if any(hint in agent.lower() for hint in REVIEW_AGENT_HINTS):
                summary.reviewer_invocations += 1
            continue

        if span.operation == OP_EXECUTE_TOOL:
            summary.tool_count += 1
            tool = span.tool_name or "unknown"
            summary.tools[tool] += 1
            if summary.first_mutation_tool is None and is_mutation_tool(tool):
                summary.first_mutation_tool = tool
            continue

        if span.operation != OP_CHAT:
            continue

        summary.chat_count += 1
        summary.total_tokens.add_span(span)
        agent = nearest_agent(span, by_span_id)
        model = span.model

        agent_usage = summary.by_agent_tokens.setdefault(agent, TokenUsage())
        agent_usage.add_span(span)
        model_usage = summary.by_model_tokens.setdefault(model, TokenUsage())
        model_usage.add_span(span)

        if agent == "main" or agent.lower() in {"over the luna", "copilot", "agent"}:
            summary.main_tokens.add_span(span)
        else:
            summary.council_tokens.add_span(span)

    return summary


def render_markdown(summary: Summary) -> str:
    total = summary.total_tokens.to_dict()
    main = summary.main_tokens.to_dict()
    council = summary.council_tokens.to_dict()
    lines = [
        "# Over the Luna trace summary",
        "",
        f"- Mode detected: **{summary.mode}**",
        f"- Agent invocations: **{summary.invoke_agent_count}** (subagents: {summary.subagent_count})",
        f"- Reviewer invocations: **{summary.reviewer_invocations}**",
        f"- Model calls: **{summary.chat_count}**",
        f"- Tool calls: **{summary.tool_count}**",
        f"- First mutation tool: **{summary.first_mutation_tool or 'not detected'}**",
        f"- Tokens total: input {total['input']}, output {total['output']}, cache-read {total['cache_read']}, cache-create {total['cache_create']}, reasoning {total['reasoning']}",
        f"- Main tokens: input {main['input']}, output {main['output']}",
        f"- Council/reviewer tokens: input {council['input']}, output {council['output']}",
        "",
        "## Agent calls",
    ]
    if summary.agents:
        lines.extend(f"- {name}: {count}" for name, count in summary.agents.most_common())
    else:
        lines.append("- none detected")
    lines.extend(["", "## Tool calls"])
    if summary.tools:
        lines.extend(f"- {name}: {count}" for name, count in summary.tools.most_common())
    else:
        lines.append("- none detected")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path, help="VS Code Copilot OTel JSONL file")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    spans = load_spans(args.trace)
    summary = summarize(spans)
    if args.json:
        print(json.dumps(summary.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(render_markdown(summary), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
