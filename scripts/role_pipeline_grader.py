#!/usr/bin/env python3
"""Independent P5 acceptance and negative tests; no LLM keys inherited.

Grading operates on public, temporary copies of Over the Luna Next RC2.
The agents cannot inspect this grader from their tool-visible workspaces.
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

def execute(work, *args, timeout=40):
    env={"PATH":os.environ.get("PATH",""),"HOME":str(work),
         "PYTHONDONTWRITEBYTECODE":"1","LANG":"C.UTF-8"}
    return subprocess.run([sys.executable,*args],cwd=work,env=env,
        capture_output=True,text=True,timeout=timeout)

def symlink_case(work,relative):
    # This source is a public disposable fixture string, not a real secret.
    path=work/relative
    original=path.read_bytes()
    # Use valid original content at an OUTSIDE source path; otherwise
    # malformed YAML could make an agent symlink fail by coincidence.
    with tempfile.TemporaryDirectory(prefix="otl-public-outside-") as td:
        target=Path(td)/"original-bytes"
        target.write_bytes(original)
        path.unlink()
        path.symlink_to(target)
        try:
            v=execute(work,"scripts/validate_release.py")
            with tempfile.TemporaryDirectory(prefix="otl-grade-output-") as d:
                out=Path(d)/"test.zip"
                packed=execute(work,"-m","scripts.package_release","--output",str(out))
                return v.returncode!=0 and packed.returncode!=0 and not out.exists()
        finally:
            path.unlink()
            path.write_bytes(original)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--work",type=Path,required=True)
    args=p.parse_args()
    work=args.work.resolve()
    checks={}
    def note(k,v):checks[k]=bool(v)
    try:
        note("valid_candidate",execute(work,"scripts/validate_release.py").returncode==0)
        original=execute(work,"-m","unittest","discover","-s","tests","-p","test_release.py","-v")
        import re
        m=re.findall(r"Ran\s+(\d+)\s+tests?",original.stdout+original.stderr)
        count=int(m[-1]) if m else 0
        note("all_authored_tests_run",original.returncode==0 and count>=10)
        for f in ("scripts/validate_release.py","scripts/package_release.py","tests/test_release.py"):
            note("compile_"+Path(f).name,execute(work,"-m","py_compile",f).returncode==0)
        with tempfile.TemporaryDirectory(prefix="otl-grade-zip-") as d:
            zipfile_path=Path(d)/"pack.zip"
            result=execute(work,"-m","scripts.package_release","--output",str(zipfile_path))
            note("package_valid_root",result.returncode==0 and zipfile_path.is_file())
            if zipfile_path.exists():
                with zipfile.ZipFile(zipfile_path) as z:
                    note("package_allowlist_only",
                        set(z.namelist())=={"plugin.json","LICENSE","README.md","README.ko.md",
                             "docs/ROLE_TOPOLOGY.md","docs/HOST_DELEGATION_GATE.md",
                             "docs/PILOT_GUIDE.md", *("agents/"+p.name for p in
                              (work/"agents").iterdir())})
        for path in ("README.md","LICENSE","agents/over-the-luna-next.agent.md",
                     "docs/ROLE_TOPOLOGY.md","docs/HOST_DELEGATION_GATE.md",
                     "docs/PILOT_GUIDE.md"):
            note("deny_symlink_"+path.replace("/","_"),symlink_case(work,path))
        note("normal_sources_preserved", all((work/p).is_file() for p in
             ("plugin.json","README.md","LICENSE","README.ko.md")))
        summary={"pass":all(checks.values()),"checks":checks,
                 "num_user_tests":count,
                 "failed_checks":[k for k,v in checks.items() if not v]}
    except Exception as error:
        summary={"pass":False,"checks":checks,
                 "error":type(error).__name__,"num_user_tests":0}
    print(json.dumps(summary,sort_keys=True))
    if not summary["pass"]:sys.exit(1)

if __name__=="__main__":
    main()
