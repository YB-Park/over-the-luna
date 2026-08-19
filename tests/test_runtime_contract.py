from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"{path}: missing YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise AssertionError(f"{path}: malformed YAML frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise AssertionError(f"{path}: frontmatter must be a mapping")
    return data


class RuntimeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agents: dict[str, dict] = {}
        for path in sorted(AGENTS_DIR.glob("*.agent.md")):
            frontmatter = parse_frontmatter(path)
            name = frontmatter.get("name")
            self.assertIsInstance(name, str, f"{path}: agent name is required")
            self.agents[name] = frontmatter

    def test_custom_handoffs_resolve_to_exact_agent_names(self) -> None:
        """VS Code resolves handoff targets through the loaded custom-agent name."""
        known_names = set(self.agents)
        for source_name, frontmatter in self.agents.items():
            for handoff in frontmatter.get("handoffs", []) or []:
                target = handoff.get("agent")
                self.assertIn(
                    target,
                    known_names,
                    (
                        f"{source_name}: handoff target {target!r} does not resolve to a loaded "
                        "custom-agent name. Use the exact `name` from the target .agent.md file."
                    ),
                )

    def test_premium_handoffs_never_auto_send(self) -> None:
        for source_name, frontmatter in self.agents.items():
            for handoff in frontmatter.get("handoffs", []) or []:
                if handoff.get("model") in {
                    "Claude Sonnet 5 (copilot)",
                    "Claude Opus 4.8 (copilot)",
                }:
                    self.assertIs(
                        handoff.get("send"),
                        False,
                        f"{source_name}: premium handoff must remain explicit and non-auto-send",
                    )


if __name__ == "__main__":
    unittest.main()
