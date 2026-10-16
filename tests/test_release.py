import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.validate_release import ROOT, validate
from scripts.package_release import FILES, package

class CandidateReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/"candidate"
        for name in FILES:
            dest=self.root/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/name,dest)

    def test_pristine(self):
        self.assertEqual(validate(self.root),[])

    def test_forbidden_main_settings(self):
        agent=self.root/"agents/over-the-luna-next.agent.md"
        source=agent.read_text()
        for field in ("tools: []","model: gpt-6-luna","agents: []",
                      "mcp-servers: {}","hooks: {}"):
            with self.subTest(field=field):
                agent.write_text(source.replace("target: vscode\n",
                                               "target: vscode\n"+field+"\n"))
                self.assertTrue(validate(self.root))
        agent.write_text(source)

    def test_extra_agent_markdown(self):
        for name in ("other.md","other.agent.md","README.md"):
            p=self.root/"agents"/name
            with self.subTest(name=name):
                p.write_text("unknown")
                self.assertTrue(validate(self.root))
                p.unlink()

    def test_mcp_hooks_skills(self):
        for name in ("skills/a/SKILL.md","mcp.json",".mcp.json",
                     "hooks.json","hooks/tool.json"):
            p=self.root/name
            with self.subTest(name=name):
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text("unknown")
                self.assertTrue(validate(self.root))
                p.unlink()

    def test_manifest_corruption(self):
        p=self.root/"plugin.json"
        good=p.read_text()
        for bad in ("{bad","[]"):
            p.write_text(bad)
            self.assertTrue(validate(self.root))
        p.unlink()
        self.assertTrue(validate(self.root))
        p.write_text(good)

    def test_deterministic_allowlisted_package(self):
        a,b=Path(self.temp.name)/"a.zip",Path(self.temp.name)/"b.zip"
        digest,_=package(self.root,a)
        digest2,_=package(self.root,b)
        self.assertEqual(digest,digest2)
        with zipfile.ZipFile(a) as zf:
            self.assertEqual(set(zf.namelist()),set(FILES))
            restored=Path(self.temp.name)/"unpacked"
            zf.extractall(restored)
        self.assertEqual(validate(restored),[])

    def test_fail_closed_packaging(self):
        (self.root/"agents/another.md").write_text("unexpected")
        with self.assertRaises(ValueError):
            package(self.root,Path(self.temp.name)/"unsafe.zip")

if __name__=="__main__":
    unittest.main()
