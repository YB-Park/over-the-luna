from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
EXPERIMENTS = ROOT / "experiments"


class V11VSCodeGateLayoutTests(unittest.TestCase):
    def test_real_agents_are_exact_rc2_gate_candidates(self) -> None:
        pairs = {
            AGENTS / "over-the-luna.agent.md": EXPERIMENTS / "v1_1_candidate_rc2.agent.md",
            AGENTS / "luna-architect.agent.md": EXPERIMENTS / "v1_1_candidate_architect_packet_v3.agent.md",
            AGENTS / "luna-reviewer.agent.md": EXPERIMENTS / "v1_1_candidate_reviewer_rc.agent.md",
            AGENTS / "premium-review.agent.md": EXPERIMENTS / "v1_1_candidate_premium_review.agent.md",
        }
        for product_path, candidate_path in pairs.items():
            with self.subTest(product=product_path.name):
                self.assertEqual(
                    product_path.read_text(encoding="utf-8"),
                    candidate_path.read_text(encoding="utf-8"),
                    f"{product_path} drifted from the evidence-backed VS Code gate candidate",
                )

    def test_v1_0_two_model_menu_is_not_in_gate_layout(self) -> None:
        self.assertFalse((AGENTS / "sonnet-reviewer.agent.md").exists())
        self.assertFalse((AGENTS / "opus-critical-reviewer.agent.md").exists())

    def test_gate_branch_does_not_accidentally_bump_release_version(self) -> None:
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(
            plugin["version"],
            "1.0.0",
            "The VS Code gate is an integration candidate, not authorization to publish v1.1.0",
        )


if __name__ == "__main__":
    unittest.main()
