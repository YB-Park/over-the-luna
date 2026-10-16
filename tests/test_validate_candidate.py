import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_candidate import validate


CANDIDATE = Path(__file__).resolve().parents[1] / "experiments" / "next" / "candidate-plugin"


class ValidateCandidateTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name) / "candidate-plugin"
        shutil.copytree(CANDIDATE, self.root)

    def test_pristine_candidate_passes(self):
        self.assertEqual(validate(self.root), [])

    def test_rejects_tools_in_main(self):
        agent = self.root / "agents" / "over-the-luna-next.agent.md"
        agent.write_text(agent.read_text(encoding="utf-8").replace(
            "target: vscode\n", "target: vscode\ntools: []\n"
        ), encoding="utf-8")
        self.assertIn("candidate Main must omit tools", "\n".join(validate(self.root)))

    def test_rejects_pinned_model_in_main(self):
        agent = self.root / "agents" / "over-the-luna-next.agent.md"
        agent.write_text(agent.read_text(encoding="utf-8").replace(
            "target: vscode\n", "target: vscode\nmodel: gpt-4o\n"
        ), encoding="utf-8")
        self.assertIn("candidate Main must omit model", "\n".join(validate(self.root)))

    def test_rejects_additional_agent_leaf(self):
        (self.root / "agents" / "extra.agent.md").write_text("---\nname: Extra\n---\n")
        self.assertIn("exactly one agent", "\n".join(validate(self.root)))

    def test_rejects_additional_agent_markdown(self):
        (self.root / "agents" / "reviewer.md").write_text(
            "---\nname: Reviewer\n---\n", encoding="utf-8"
        )
        self.assertIn("exactly one agent", "\n".join(validate(self.root)))

    def test_rejects_bundled_skill(self):
        skill = self.root / "skills" / "audit" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: audit\n---\n", encoding="utf-8")
        self.assertIn("must not bundle skills", "\n".join(validate(self.root)))

    def test_rejects_missing_or_invalid_manifest(self):
        manifest = self.root / "plugin.json"
        manifest.unlink()
        self.assertIn("missing/invalid candidate manifest", "\n".join(validate(self.root)))
        manifest.write_text("{ invalid", encoding="utf-8")
        self.assertIn("missing/invalid candidate manifest", "\n".join(validate(self.root)))

    def test_rejects_bundled_mcp_files(self):
        for filename in ("mcp.json", ".mcp.json"):
            with self.subTest(filename=filename):
                path = self.root / filename
                path.write_text("{}", encoding="utf-8")
                self.assertIn("must not bundle MCP", "\n".join(validate(self.root)))
                path.unlink()


if __name__ == "__main__":
    unittest.main()
