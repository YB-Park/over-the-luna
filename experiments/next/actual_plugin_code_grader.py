#!/usr/bin/env python3
"""P4 deterministic external grading. Only public fixture data and no secrets.

Independently validates all preexisting code and newly discovered product
packaging false negatives. Agent has no shell/read access to this grader.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(work: Path, *args: str):
    return subprocess.run([sys.executable, *args], cwd=work,
                          capture_output=True, text=True, timeout=45, check=False)


def mutate_agent(plugin: Path, name: str):
    p = plugin / "agents" / name
    p.write_text("---\nname: Injected\nuser-invocable: true\n---\nUntrusted agent.\n",
                 encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    work = parser.parse_args().work.resolve()
    script = work / "scripts/validate_candidate.py"
    tests = work / "tests/test_validate_candidate.py"
    plugin = work / "experiments/next/candidate-plugin"
    checks = {}
    def check(k, v):
        checks[k] = bool(v)
    if not script.is_file() or not tests.is_file() or not plugin.is_dir():
        print(json.dumps({"pass": False, "reason": "fixture or authored test missing"}))
        raise SystemExit(1)
    check("default_valid", run(work, "scripts/validate_candidate.py").returncode == 0)
    check("explicit_root_valid",
          run(work, "scripts/validate_candidate.py","--root",str(plugin)).returncode==0)
    test_run=run(work,"-m","unittest","discover","-s","tests",
                 "-p","test_validate_candidate.py","-v")
    combined=test_run.stdout+test_run.stderr
    import re
    matches=re.findall(r"Ran\s+(\d+)\s+tests?",combined)
    test_count=int(matches[-1]) if matches else 0
    check("authored_tests_pass", test_run.returncode==0 and test_count>=8)
    check("authored_test_syntax",run(work,"-m","py_compile",str(tests)).returncode==0)
    mutants=[
       ("extra_plain_agent",lambda p:mutate_agent(p,"reviewer.md")),
       ("extra_dotted_agent",lambda p:mutate_agent(p,"reviewer.agent.md")),
       ("plugin_skill",lambda p:skill(p)),
       ("no_tools",lambda p:inject_frontmatter(p,"tools: []")),
       ("pinned_model",lambda p:inject_frontmatter(p,"model: gpt-6-luna")),
       ("invalid_manifest",lambda p:(p/"plugin.json").write_text("{bad",encoding="utf8")),
       ("missing_manifest",lambda p:(p/"plugin.json").unlink()),
       ("mcp",lambda p:(p/".mcp.json").write_text("{}",encoding="utf8"))
    ]
    with tempfile.TemporaryDirectory(prefix="otl-plugin-grade-") as td:
      for label,mod in mutants:
        dest=Path(td)/label
        shutil.copytree(plugin,dest)
        mod(dest)
        outcome=run(work,"scripts/validate_candidate.py","--root",str(dest))
        check("reject_"+label,outcome.returncode!=0)
    grade={"pass":all(checks.values()),"checks":checks,"num_user_tests":test_count,
           "failed_check_names":[k for k,v in checks.items() if not v]}
    print(json.dumps(grade,sort_keys=True))
    if not grade["pass"]:raise SystemExit(1)


def skill(plugin:Path):
    target=plugin/"skills"/"unexpected"/"SKILL.md"
    target.parent.mkdir(parents=True)
    target.write_text("---\nname: unexpected\n---\n",encoding="utf-8")


def inject_frontmatter(plugin:Path, field:str):
    target=plugin/"agents"/"over-the-luna-next.agent.md"
    source=target.read_text(encoding="utf8")
    target.write_text("---\n"+field+"\n"+source[4:],encoding="utf8")


if __name__=="__main__":
    main()
