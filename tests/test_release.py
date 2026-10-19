import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.validate_release import ROOT,MAIN,MODELS,validate
from scripts.package_release import FILES,package

class RoleTopologyCandidateTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.folder=Path(t.name)
        self.root=self.folder/"plugin"
        for name in FILES:
            source=ROOT/name
            dest=self.root/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,dest)

    def test_clean_topology(self):
        self.assertEqual(validate(self.root),[])

    def test_valid_ordinary_plugin_still_packages(self):
        output=self.folder/"ordinary.zip"
        package(self.root,output)
        self.assertTrue(output.is_file())

    def test_symlinked_release_sources_are_refused(self):
        # The outside file is public test content, never actual workspace secrets.
        outside=self.folder/"external.txt"
        for name in ("README.md","LICENSE","agents/"+MAIN,
                     "docs/ROLE_TOPOLOGY.md"):
            with self.subTest(path=name):
                target=self.root/name
                contents=target.read_bytes()
                outside.write_bytes(contents)
                target.unlink()
                target.symlink_to(outside)
                try:
                    self.assertTrue(validate(self.root),
                        "validator must reject symlinked package source")
                    with self.assertRaises(ValueError):
                        package(self.root,self.folder/"bad.zip")
                finally:
                    target.unlink()
                    target.write_bytes(contents)

    def test_main_cannot_pin_model_or_tools(self):
        file=self.root/"agents"/MAIN
        source=file.read_text()
        for field in ("tools: []","tools: [read]","model: GPT-6 Luna",
                      "agents: []","hooks: {}"):
            with self.subTest(field=field):
                file.write_text(source.replace("target: vscode\n","target: vscode\n"+field+"\n"))
                self.assertTrue(validate(self.root))
        file.write_text(source)

    def test_leaves_must_be_hidden_and_callable(self):
        file=self.root/"agents/next-architect.agent.md"
        source=file.read_text()
        for old,new in (("user-invocable: false","user-invocable: true"),
                        ("agents: []","agents: [Next Reviewer]"),
                        ("tools: ['read', 'search']","tools: []")):
            with self.subTest(new=new):
                file.write_text(source.replace(old,new))
                self.assertTrue(validate(self.root))
        file.write_text(source)

    def test_pinned_strong_models_and_research(self):
        cases=[("next-sol-specialist.agent.md","GPT-6.1 Sol","GPT-6 Luna"),
               ("next-sonnet-specialist.agent.md","Claude Sonnet 5.5","GPT-6 Luna"),
               ("next-researcher.agent.md","'web'","'edit'")]
        for name,old,new in cases:
            with self.subTest(name=name):
                file=self.root/"agents"/name
                original=file.read_text()
                file.write_text(original.replace(old,new))
                self.assertTrue(validate(self.root))
                file.write_text(original)

    def test_premium_substitution_requires_real_diff_and_distinct_routing(self):
        main_file=self.root/"agents"/MAIN
        main_text=main_file.read_text()
        for name in ("next-sol-specialist.agent.md","next-sonnet-specialist.agent.md"):
            agent=self.root/"agents"/name
            source=agent.read_text()
            self.assertIn("actual current diff",source)
            self.assertIn("VERIFY: patch evidence absent",source)
            with self.subTest(agent=name):
                agent.write_text(source.replace("When substituting for Next Reviewer",
                                                "When consulting"))
                self.assertTrue(validate(self.root),
                    "a premium substitute must reject absent patch evidence")
                agent.write_text(source)
        for marker in ("Investigation and assurance are separate decisions",
                       "Premium substitution, not accumulation"):
            with self.subTest(marker=marker):
                main_file.write_text(main_text.replace(marker, "omitted"))
                self.assertTrue(validate(self.root),
                    "a routing gate must not disappear from the packaged Main")
        main_file.write_text(main_text)
        self.assertEqual(validate(self.root),[])

    def test_missing_and_extra_roles(self):
        target=self.root/"agents/next-reviewer.agent.md"
        source=target.read_text()
        target.unlink()
        self.assertTrue(validate(self.root))
        target.write_text(source)
        added=self.root/"agents/secret.md"
        added.write_text("unapproved")
        self.assertTrue(validate(self.root))

    def test_bad_manifest(self):
        p=self.root/"plugin.json"
        source=p.read_text()
        for bad in ("{invalid","[]"):
            p.write_text(bad)
            self.assertTrue(validate(self.root))
        p.unlink()
        self.assertTrue(validate(self.root))
        p.write_text(source)

    def test_no_mcp_hooks_skills(self):
        for name in ("skills/a/SKILL.md","mcp.json",".mcp.json",
                     "hooks.json","hooks/tool.json"):
            with self.subTest(name=name):
                p=self.root/name
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text("unsafe")
                self.assertTrue(validate(self.root))
                p.unlink()

    def test_host_evidence_gate_is_packaged_without_corporate_data(self):
        path=self.root/"docs/HOST_DELEGATION_GATE.md"
        content=path.read_text(encoding="utf-8")
        self.assertIn("custom_agent_prompt",content)
        self.assertIn("DO NOT EXPORT",content)
        self.assertIn("Main → Architect",content)
        self.assertIn("INCONCLUSIVE",content)
        self.assertEqual(validate(self.root),[])

    def test_reproducible_package(self):
        a,b=self.folder/"a.zip",self.folder/"b.zip"
        sha,size=package(self.root,a)
        sha2,size2=package(self.root,b)
        self.assertEqual((sha,size),(sha2,size2))
        with zipfile.ZipFile(a) as f:
            self.assertEqual(set(f.namelist()),set(FILES))
            out=self.folder/"unpacked"
            f.extractall(out)
        self.assertEqual(validate(out),[])

    def test_fail_closed_packaging(self):
        (self.root/"agents/unexpected.agent.md").write_text("new")
        with self.assertRaises(ValueError):
            package(self.root,self.folder/"unsafe.zip")

if __name__=="__main__":
    unittest.main()
