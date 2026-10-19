#!/usr/bin/env python3
"""Offline, stdlib-only audit of the opt-in RC2 plugin archive. No extraction."""
from __future__ import annotations
import argparse
import hashlib
import json
import stat
import sys
import zipfile
from pathlib import Path

EXPECTED = frozenset((
    "plugin.json", "LICENSE", "README.md", "README.ko.md",
    "docs/ROLE_TOPOLOGY.md", "docs/HOST_DELEGATION_GATE.md",
    "docs/PILOT_GUIDE.md",
    "agents/over-the-luna-next.agent.md",
    "agents/next-architect.agent.md", "agents/next-reviewer.agent.md",
    "agents/next-skeptic.agent.md", "agents/next-researcher.agent.md",
    "agents/next-recovery.agent.md", "agents/next-sol-specialist.agent.md",
    "agents/next-sonnet-specialist.agent.md",
))
AGENTS=frozenset(p for p in EXPECTED if p.startswith("agents/"))
MAX_MEMBER=512_000
MAX_TOTAL=1_500_000

def verify(archive:Path)->dict[str,object]:
    try:
        if not archive.is_file():
            raise ValueError("archive not a regular file")
        if archive.stat().st_size>MAX_TOTAL:
            raise ValueError("archive too large")
        with zipfile.ZipFile(archive,"r") as z:
            members=z.infolist()
            names=[x.filename for x in members]
            if len(names)!=len(set(names)):
                raise ValueError("duplicate ZIP members")
            if set(names)!=EXPECTED:
                raise ValueError("ZIP member allowlist mismatch")
            if any(x.is_dir() or
                   (x.create_system==3 and
                    stat.S_IFMT(x.external_attr>>16) not in (0,stat.S_IFREG))
                   for x in members):
                raise ValueError("nonregular archive member")
            if any(x.file_size>MAX_MEMBER for x in members) or sum(
                x.file_size for x in members)>MAX_TOTAL:
                raise ValueError("uncompressed content limit exceeded")
            if z.testzip() is not None:
                raise ValueError("ZIP CRC failed")
            manifest=json.loads(z.read("plugin.json"))
            if not isinstance(manifest,dict):
                raise ValueError("plugin manifest not an object")
            if manifest.get("name")!="over-the-luna-next" or (
                manifest.get("version")!="2.0.0-rc.2" or
                manifest.get("agents")!="agents/") or "$schema" in manifest:
                raise ValueError("wrong plugin identity or version")
            for member in AGENTS:
                data=z.read(member)
                if not data.startswith(b"---\n") or b"\n---\n" not in data[4:]:
                    raise ValueError("invalid agent frontmatter envelope")
            guide=z.read("docs/PILOT_GUIDE.md").decode("utf-8")
            if "PILOT_DIRECT_OK" not in guide or "REVIEW_UNVERIFIED" not in guide:
                raise ValueError("missing pilot limitations/rollback guide")
    except (OSError,zipfile.BadZipFile,zipfile.LargeZipFile,
            UnicodeError,json.JSONDecodeError) as e:
        raise ValueError("invalid archive: "+type(e).__name__) from e
    return {"sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
            "files":len(EXPECTED),"agents":len(AGENTS),
            "identity":"over-the-luna-next@2.0.0-rc.2",
            "hostHandbackProven":False}

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive",required=True,type=Path)
    args=parser.parse_args()
    try:
        result=verify(args.archive)
    except ValueError as exc:
        print("PILOT_ARCHIVE_BLOCKED:",exc)
        return 1
    print("PILOT_ARCHIVE_PASS",
          "sha256="+str(result["sha256"]),
          "members="+str(result["files"]),
          "agents="+str(result["agents"]),
          "runtime_delegation=UNVERIFIED")
    return 0

if __name__=="__main__":
    sys.exit(main())
