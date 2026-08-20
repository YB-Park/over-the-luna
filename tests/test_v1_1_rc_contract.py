from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
MAIN = EXPERIMENTS / "v1_1_candidate_rc2.agent.md"
ARCHITECT = EXPERIMENTS / "v1_1_candidate_architect_packet_v3.agent.md"
REVIEWER = EXPERIMENTS / "v1_1_candidate_reviewer_rc.agent.md"
PREMIUM = EXPERIMENTS / "v1_1_candidate_premium_review.agent.md"


def parse(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0] != "":
        raise AssertionError(f"{path}: malformed frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise AssertionError(f"{path}: frontmatter must be a mapping")
    return data, parts[2]


class V11ReleaseCandidateContractTests(unittest.TestCase):
    def test_main_contract(self) -> None:
        frontmatter, body = parse(MAIN)
        self.assertEqual(frontmatter["name"], "Over the Luna")
        self.assertEqual(frontmatter["model"], "GPT-5.6 Luna")
        self.assertNotIn("tools", frontmatter)
        self.assertTrue(frontmatter["disable-model-invocation"])
        self.assertIn("agent/runSubagent", body)
        self.assertIn("three narrow `rg` locator calls total", body)
        self.assertIn("three semantic source/test files", body)
        self.assertIn("one such file", body)
        self.assertIn("do not call `glob` at all", body)
        self.assertIn("Boundary sealed", body)
        self.assertIn("BEGIN_UNIFIED_DIFF", body)
        self.assertIn("END_UNIFIED_DIFF", body)
        self.assertIn("exactly once total", body)
        self.assertIn("never retry Luna Reviewer", body)
        self.assertIn("at least one post-change named Luna Reviewer is mandatory", body)
        self.assertIn("one visible **human decision**", body)

    def test_leaf_contracts_are_non_recursive_and_read_only(self) -> None:
        for path, expected_name in ((ARCHITECT, "Luna Architect"), (REVIEWER, "Luna Reviewer")):
            with self.subTest(path=path.name):
                frontmatter, _ = parse(path)
                self.assertEqual(frontmatter["name"], expected_name)
                self.assertIs(frontmatter["user-invocable"], False)
                self.assertEqual(frontmatter["tools"], ["read", "search"])
                self.assertEqual(frontmatter["agents"], [])

    def test_reviewer_requires_concrete_artifact_and_has_hard_budget(self) -> None:
        _, body = parse(REVIEWER)
        self.assertIn("BEGIN_UNIFIED_DIFF", body)
        self.assertIn("END_UNIFIED_DIFF", body)
        self.assertIn("diff --git", body)
        self.assertIn("@@", body)
        self.assertIn("4 concrete files", body)
        self.assertIn("8 total read/search calls", body)
        self.assertIn("never inspect `.git`", body.lower())
        self.assertIn("Cosmetic whitespace", body)

    def test_premium_handoff_is_one_human_initiated_sonnet_decision(self) -> None:
        frontmatter, body = parse(MAIN)
        handoffs = frontmatter["handoffs"]
        self.assertEqual(len(handoffs), 1)
        self.assertEqual(handoffs[0]["label"], "Premium Review")
        self.assertEqual(handoffs[0]["agent"], "Premium Review")
        self.assertIs(handoffs[0].get("send"), False)
        self.assertEqual(handoffs[0]["model"], "Claude Sonnet 5 (copilot)")
        self.assertNotIn("Opus Critical Reviewer", str(handoffs))
        self.assertIn("surface that fact rather than silently substituting another model", body)

        premium_frontmatter, premium_body = parse(PREMIUM)
        self.assertEqual(premium_frontmatter["name"], "Premium Review")
        self.assertEqual(premium_frontmatter["model"], "Claude Sonnet 5")
        self.assertTrue(premium_frontmatter["disable-model-invocation"])
        self.assertEqual(premium_frontmatter["tools"], ["read", "search"])
        self.assertEqual(premium_frontmatter["agents"], [])
        self.assertIn("human-selected premium review", premium_body)
        self.assertIn("Do not recommend or invoke another premium model", premium_body)


if __name__ == "__main__":
    unittest.main()
