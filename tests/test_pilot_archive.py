"""Negative tests for opt-in pilot ZIP inspection. No model/IO uploads."""
from __future__ import annotations
import hashlib
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.package_release import package
from scripts.pilot_archive import verify, EXPECTED
from scripts.validate_release import ROOT,PACKAGE_FILES

class PilotArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work=Path(self.temp.name)
        self.zip=self.work/"pilot.zip"
        package(ROOT,self.zip)

    def rewrite(self,extra=None,remove=None,replace=None,duplicate=None,symlink=None):
        with zipfile.ZipFile(self.zip) as z:
            files={i.filename:z.read(i.filename) for i in z.infolist()}
        files.pop(remove,None)
        if replace:
            files[replace[0]]=replace[1]
        if extra:
            files[extra[0]]=extra[1]
        with zipfile.ZipFile(self.zip,"w") as z:
            for name,content in files.items():
                info=zipfile.ZipInfo(name)
                info.create_system=3
                info.external_attr=(stat.S_IFLNK|0o777)<<16 if name==symlink \
                    else (stat.S_IFREG|0o644)<<16
                z.writestr(info,content)
            if duplicate:
                z.writestr(duplicate,files[duplicate])

    def test_valid_rc2_archive(self):
        good_hash=hashlib.sha256(self.zip.read_bytes()).hexdigest()
        result=verify(self.zip,expected_sha256=good_hash)
        self.assertEqual(result["agents"],8)
        self.assertFalse(result["hostHandbackProven"])
        self.assertEqual(EXPECTED,set(PACKAGE_FILES))

    def test_reject_unknown_or_traversal(self):
        for name in ("../outside.txt","scripts/exfiltrate.py"):
            with self.subTest(name=name):
                package(ROOT,self.zip)
                self.rewrite(extra=(name,b"not allowed"))
                with self.assertRaises(ValueError):verify(self.zip)

    def test_reject_missing_and_duplicate(self):
        self.rewrite(remove="docs/PILOT_GUIDE.md")
        with self.assertRaises(ValueError):verify(self.zip)
        package(ROOT,self.zip)
        self.rewrite(duplicate="plugin.json")
        with self.assertRaises(ValueError):verify(self.zip)

    def test_reject_symlink_member(self):
        self.rewrite(symlink="README.md")
        with self.assertRaises(ValueError):verify(self.zip)

    def test_reject_wrong_plugin_manifest(self):
        for payload in (b"not json",b"[]",
                        json.dumps({"name":"over-the-luna-next",
                            "version":"2.0.0-rc.1","agents":"agents/"}).encode()):
            with self.subTest(payload=payload[:12]):
                package(ROOT,self.zip)
                self.rewrite(replace=("plugin.json",payload))
                with self.assertRaises(ValueError):verify(self.zip)

    def test_reject_repacked_unsafe_architect_even_if_structurally_valid(self):
        trusted=hashlib.sha256(self.zip.read_bytes()).hexdigest()
        with zipfile.ZipFile(self.zip) as z:
            original=z.read("agents/next-architect.agent.md")
        self.assertIn(b"tools: ['read', 'search']",original)
        tampered=original.replace(b"tools: ['read', 'search']",
                                  b"tools: ['edit', 'search']",1)
        self.rewrite(replace=("agents/next-architect.agent.md",tampered))
        # The ZIP still has the same 15 paths and valid CRCs; structure alone
        # would accept the modified permissions. The trusted digest must not.
        self.assertEqual(verify(self.zip)["files"],15)
        with self.assertRaisesRegex(ValueError,"SHA-256 differs"):
            verify(self.zip,expected_sha256=trusted)

    def test_bad_pinned_checksum_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"SHA-256 format"):
            verify(self.zip,expected_sha256="not-a-sha")
        with self.assertRaisesRegex(ValueError,"SHA-256 differs"):
            verify(self.zip,expected_sha256="0"*64)

    def test_reject_missing_pilot_safety_conditions(self):
        self.rewrite(replace=("docs/PILOT_GUIDE.md",b"an unsafe quickstart"))
        with self.assertRaises(ValueError):verify(self.zip)

if __name__=="__main__":
    unittest.main()
