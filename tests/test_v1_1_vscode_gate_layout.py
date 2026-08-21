import json
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / 'agents'
COUNCIL = {'Luna Planner','Luna Architect','Luna Skeptic','Luna Researcher','Luna Tool Worker','Luna Recovery','Luna Reviewer'}
MAIN_TOOLS = {'read','search','edit','execute','agent','todo','web'}


def fm(path):
    text = path.read_text(encoding='utf-8')
    return yaml.safe_load(text.split('---\n', 2)[1])


class V11SchemaGateLayoutTests(unittest.TestCase):
    def test_main_schema_wiring(self):
        main = fm(AGENTS / 'over-the-luna.agent.md')
        self.assertEqual(set(main['tools']), MAIN_TOOLS)
        self.assertEqual(set(main['agents']), COUNCIL)
        self.assertNotIn('*', main['tools'])
        self.assertEqual(len(main['handoffs']), 1)
        self.assertEqual(main['handoffs'][0]['agent'], 'Premium Review')
        self.assertIs(main['handoffs'][0]['send'], False)

    def test_old_premium_menu_absent(self):
        self.assertFalse((AGENTS / 'sonnet-reviewer.agent.md').exists())
        self.assertFalse((AGENTS / 'opus-critical-reviewer.agent.md').exists())

    def test_version_stays_unreleased(self):
        plugin = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(plugin['version'], '1.0.0')


if __name__ == '__main__':
    unittest.main()
