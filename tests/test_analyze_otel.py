from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_otel import load_spans, summarize


def span(
    name: str,
    operation: str,
    span_id: str,
    *,
    parent: str | None = None,
    attributes: dict | None = None,
) -> dict:
    attrs = {"gen_ai.operation.name": operation}
    attrs.update(attributes or {})
    value = {
        "name": name,
        "attributes": attrs,
        "spanContext": {"traceId": "trace-1", "spanId": span_id},
    }
    if parent:
        value["parentSpanContext"] = {"traceId": "trace-1", "spanId": parent}
    return value


class AnalyzeOtelTests(unittest.TestCase):
    def test_attributes_main_and_council_tokens_and_review(self) -> None:
        events = [
            span(
                "invoke_agent Over the Luna",
                "invoke_agent",
                "root",
                attributes={"gen_ai.agent.name": "Over the Luna"},
            ),
            span(
                "chat GPT-5.6 Luna",
                "chat",
                "main-chat-1",
                parent="root",
                attributes={
                    "gen_ai.response.model": "GPT-5.6 Luna",
                    "gen_ai.usage.input_tokens": 100,
                    "gen_ai.usage.output_tokens": 20,
                },
            ),
            span(
                "execute_tool runSubagent",
                "execute_tool",
                "delegate",
                parent="root",
                attributes={"gen_ai.tool.name": "runSubagent"},
            ),
            span(
                "invoke_agent Luna Architect",
                "invoke_agent",
                "architect",
                parent="delegate",
                attributes={"gen_ai.agent.name": "Luna Architect"},
            ),
            span(
                "chat GPT-5.6 Luna",
                "chat",
                "architect-chat",
                parent="architect",
                attributes={
                    "gen_ai.response.model": "GPT-5.6 Luna",
                    "gen_ai.usage.input_tokens": 60,
                    "gen_ai.usage.output_tokens": 10,
                },
            ),
            span(
                "execute_tool apply_patch",
                "execute_tool",
                "edit",
                parent="root",
                attributes={"gen_ai.tool.name": "apply_patch"},
            ),
            span(
                "invoke_agent Luna Reviewer",
                "invoke_agent",
                "reviewer",
                parent="root",
                attributes={"gen_ai.agent.name": "Luna Reviewer"},
            ),
            span(
                "chat GPT-5.6 Luna",
                "chat",
                "review-chat",
                parent="reviewer",
                attributes={
                    "gen_ai.response.model": "GPT-5.6 Luna",
                    "gen_ai.usage.input_tokens": 40,
                    "gen_ai.usage.output_tokens": 8,
                    "content": "Mode: STANDARD — Luna Architect",
                },
            ),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "trace.jsonl"
            path.write_text("\n".join(json.dumps(event) for event in events), encoding="utf-8")
            summary = summarize(load_spans(path))

        self.assertEqual(summary.mode, "STANDARD")
        self.assertEqual(summary.invoke_agent_count, 3)
        self.assertEqual(summary.subagent_count, 2)
        self.assertEqual(summary.reviewer_invocations, 1)
        self.assertEqual(summary.first_mutation_tool, "apply_patch")
        self.assertEqual(summary.total_tokens.input, 200)
        self.assertEqual(summary.total_tokens.output, 38)
        self.assertEqual(summary.main_tokens.input, 100)
        self.assertEqual(summary.council_tokens.input, 100)
        self.assertEqual(summary.tools["runSubagent"], 1)
        self.assertEqual(summary.tools["apply_patch"], 1)

    def test_accepts_otlp_attribute_array_shape(self) -> None:
        raw = {
            "resourceSpans": [
                {
                    "scopeSpans": [
                        {
                            "spans": [
                                {
                                    "name": "chat GPT-5.6 Luna",
                                    "traceId": "trace-2",
                                    "spanId": "chat-1",
                                    "attributes": [
                                        {"key": "gen_ai.operation.name", "value": {"stringValue": "chat"}},
                                        {"key": "gen_ai.usage.input_tokens", "value": {"intValue": "12"}},
                                        {"key": "gen_ai.usage.output_tokens", "value": {"intValue": "3"}},
                                    ],
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "trace.jsonl"
            path.write_text(json.dumps(raw), encoding="utf-8")
            summary = summarize(load_spans(path))

        self.assertEqual(summary.chat_count, 1)
        self.assertEqual(summary.total_tokens.input, 12)
        self.assertEqual(summary.total_tokens.output, 3)


if __name__ == "__main__":
    unittest.main()
