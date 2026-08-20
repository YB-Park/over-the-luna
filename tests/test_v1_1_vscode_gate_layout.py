from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
EXPERIMENTS = ROOT / "experiments"


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0] != "":
        raise AssertionError(f"{path}: malformed frontmatter")
    return yaml.safe_load(parts[1]), parts[2]


class V11VSCodeGateLayoutTests(unittest.TestCase):
    def test_leaf_and_premium_agents_match_evidence_backed_candidates(self) -> None:
        pairs = {
            AGENTS / "luna-architect.agent.md": EXPERIMENTS / "v1_1_candidate_architect_packet_v3.agent.md",
            AGENTS / "luna-reviewer.agent.md": EXPERIMENTS / "v1_1_candidate_reviewer_rc.agent.md",
            AGENTS / "premium-review.agent.md": EXPERIMENTS / "v1_1_candidate_premium_review.agent.md",
        }
        for product_path, candidate_path in pairs.items():
            with self.subTest(product=product_path.name):
                self.assertEqual(product_path.read_text(encoding="utf-8"), candidate_path.read_text(encoding="utf-8"))

    def test_main_is_the_ambient_gate_candidate(self) -> None:
        main = AGENTS / "over-the-luna.agent.md"
        fm, body = frontmatter(main)
        self.assertNotIn("tools", fm)
        self.assertNotIn("agents", fm)
        self.assertIn("Delegation allow-list is nevertheless strict at the instruction level.", body)
        for name in (
            "Luna Planner",
            "Luna Architect",
            "Luna Skeptic",
            "Luna Researcher",
            "Luna Tool Worker",
            "Luna Recovery",
            "Luna Reviewer",
        ):
            self.assertIn(name, body)
        self.assertIn("Never choose another installed custom agent", body)
        self.assertIn("AMBIENT_AGENT_UNAVAILABLE: agent/runSubagent", body)
        handoffs = fm["handoffs"]
        self.assertEqual(len(handoffs), 1)
        self.assertEqual(handoffs[0]["agent"], "Premium Review")
        self.assertIs(handoffs[0]["send"], False)

    def test_v1_0_two_model_menu_and_wildcard_wiring_are_not_in_gate_layout(self) -> None:
        self.assertFalse((AGENTS / "sonnet-reviewer.agent.md").exists())
        self.assertFalse((AGENTS / "opus-critical-reviewer.agent.md").exists())
        fm, _ = frontmatter(AGENTS / "over-the-luna.agent.md")
        self.assertNotIn("*", fm.get("tools", []))

    def test_gate_branch_does_not_accidentally_bump_release_version(self) -> None:
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(
            plugin["version"],
            "1.0.0",
            "The VS Code gate is an integration candidate, not authorization to publish v1.1.0",
        )


if __name__ == "__main__":
    unittest.main()
