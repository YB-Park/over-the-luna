from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
WORKFLOWS = ROOT / ".github" / "workflows"
MAIN = EXPERIMENTS / "v1_1_candidate_integrated_v3.agent.md"
ARCHITECT = EXPERIMENTS / "v1_1_candidate_architect_packet_v3.agent.md"
REVIEWER = EXPERIMENTS / "v1_1_candidate_invariant_reviewer.agent.md"


def parse_agent(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"{path}: missing YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError(f"{path}: malformed YAML frontmatter")
    frontmatter = yaml.safe_load(parts[1])
    if not isinstance(frontmatter, dict):
        raise AssertionError(f"{path}: frontmatter must be a mapping")
    return frontmatter, parts[2]


class V11CandidateContractTests(unittest.TestCase):
    def test_all_experimental_agent_frontmatter_parses(self) -> None:
        """Catch YAML/frontmatter mistakes before a paid runtime probe discovers them."""
        paths = sorted(EXPERIMENTS.glob("*.agent.md"))
        self.assertTrue(paths, "expected experimental agent candidates")
        for path in paths:
            with self.subTest(path=path.name):
                frontmatter, _ = parse_agent(path)
                self.assertIsInstance(frontmatter.get("name"), str)
                self.assertEqual(frontmatter.get("target"), "vscode")

    def test_v3_main_preserves_ambient_tools_and_explicit_leaf_allowlist(self) -> None:
        frontmatter, body = parse_agent(MAIN)
        self.assertEqual(frontmatter["name"], "Over the Luna")
        self.assertEqual(frontmatter["model"], "GPT-5.6 Luna")
        self.assertTrue(frontmatter["disable-model-invocation"])
        self.assertNotIn(
            "tools",
            frontmatter,
            "Main tools omission is intentional so selected built-in/MCP/extension tools are not replaced",
        )
        self.assertEqual(
            frontmatter["agents"],
            [
                "Luna Planner",
                "Luna Architect",
                "Luna Skeptic",
                "Luna Researcher",
                "Luna Tool Worker",
                "Luna Recovery",
                "Luna Reviewer",
            ],
        )
        self.assertIn("agent/runSubagent", body)
        self.assertIn("Mandatory pre-discovery gate", body)
        self.assertIn("Boundary sealed", body)
        self.assertIn("git ls-files", body)
        self.assertIn("Normal REVIEW budget = one Reviewer total", body)
        self.assertIn("concrete review packet", body)

    def test_v3_architect_is_read_only_and_returns_complete_work_set(self) -> None:
        frontmatter, body = parse_agent(ARCHITECT)
        self.assertEqual(frontmatter["name"], "Luna Architect")
        self.assertIs(frontmatter["user-invocable"], False)
        self.assertEqual(frontmatter["tools"], ["read", "search"])
        self.assertEqual(frontmatter["agents"], [])
        self.assertIn("post-handback work set", body)
        self.assertIn("focused test files", body)
        self.assertIn("acceptance-critical helper", body)
        self.assertIn("Never inspect `.git`", body)

    def test_reviewer_is_read_only_artifact_first_and_bounded(self) -> None:
        frontmatter, body = parse_agent(REVIEWER)
        self.assertEqual(frontmatter["name"], "Luna Reviewer")
        self.assertIs(frontmatter["user-invocable"], False)
        self.assertEqual(frontmatter["tools"], ["read", "search"])
        self.assertEqual(frontmatter["agents"], [])
        self.assertIn("Artifact precondition", body)
        self.assertIn("VERIFY: completed patch artifact missing", body)
        self.assertIn("Mandatory invariant challenge before PASS", body)
        self.assertIn("at most **4 concrete files**", body)
        self.assertIn("**8 total read/search calls**", body)
        self.assertIn("Never inspect `.git`", body)

    def test_premium_handoffs_are_exact_and_never_auto_send(self) -> None:
        frontmatter, _ = parse_agent(MAIN)
        handoffs = frontmatter.get("handoffs") or []
        self.assertEqual([h["agent"] for h in handoffs], ["Sonnet Reviewer", "Opus Critical Reviewer"])
        for handoff in handoffs:
            self.assertIs(handoff.get("send"), False)

    def test_no_one_shot_paid_workflow_is_left_in_branch(self) -> None:
        leftovers = sorted(path.name for path in WORKFLOWS.glob("*_once.yml"))
        self.assertEqual(leftovers, [], f"temporary paid experiment workflows remain: {leftovers}")


if __name__ == "__main__":
    unittest.main()
