#!/usr/bin/env python3
"""Independent, secret-free grading for the SDK native-like vs Next instruction trial.

Never run this in a process with credentials or model APIs. The caller must
execute it with a minimal environment and outside of model tool availability.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def cmd(work: Path, *args: str):
    return subprocess.run([sys.executable, *args], cwd=work, capture_output=True,
                          text=True, timeout=40, check=False)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, required=True)
    args = p.parse_args()
    work = args.work.resolve()
    plugin = work / "experiments/next/candidate-plugin"
    script = work / "scripts/validate_candidate.py"
    tests = work / "tests/test_validate_candidate.py"
    checks = {}
    diagnostics = []

    def check(label, ok):
        checks[label] = bool(ok)
        if not ok:
            diagnostics.append(label)

    if not script.is_file() or not plugin.is_dir():
        print(json.dumps({"pass": False, "checks": {}, "errors": ["work fixture missing"]}))
        raise SystemExit(1)

    check("default_candidate_pass", cmd(work, "scripts/validate_candidate.py").returncode == 0)
    check("explicit_root_pass",
          cmd(work, "scripts/validate_candidate.py", "--root", str(plugin)).returncode == 0)

    if tests.is_file():
        test_run = cmd(work, "-m", "unittest", "discover", "-s", "tests",
                       "-p", "test_validate_candidate.py", "-v")
        combined = test_run.stdout + test_run.stderr
        matches = re.findall(r"Ran\s+(\d+)\s+tests?", combined)
        num = int(matches[-1]) if matches else 0
        check("authored_tests_run", test_run.returncode == 0 and num >= 6)
        check("authored_test_syntax",
              cmd(work, "-m", "py_compile", str(tests)).returncode == 0)
    else:
        num = 0
        check("authored_tests_run", False)
        check("authored_test_syntax", False)

    mutations = (
        ("no_tools", lambda p: mutate_frontmatter(p, "tools: []")),
        ("model_pin", lambda p: mutate_frontmatter(p, "model: GPT-6 Luna")),
        ("extra_leaf", lambda p: (p / "agents/extra.agent.md").write_text(
            "---\nname: Extra\ntarget: vscode\n---\nExtra agent.\n", encoding="utf-8")),
        ("invalid_manifest", lambda p: (p / "plugin.json").write_text("{bad-json",
                                                                       encoding="utf-8")),
        ("missing_manifest", lambda p: (p / "plugin.json").unlink()),
        ("dot_mcp", lambda p: (p / ".mcp.json").write_text("{}", encoding="utf-8")),
        ("plain_mcp", lambda p: (p / "mcp.json").write_text("{}", encoding="utf-8")),
    )
    with tempfile.TemporaryDirectory(prefix="otl-safety-grader-") as td:
        for label, modifier in mutations:
            dest = Path(td) / label
            shutil.copytree(plugin, dest)
            modifier(dest)
            got = cmd(work, "scripts/validate_candidate.py", "--root", str(dest))
            check("mutant_" + label + "_rejected", got.returncode != 0)
    result = {"pass": all(checks.values()), "checks": checks,
              "num_user_tests": num, "failed_check_names": diagnostics}
    print(json.dumps(result, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


def mutate_frontmatter(plugin: Path, extra: str):
    file = plugin / "agents/over-the-luna-next.agent.md"
    content = file.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    file.write_text("---\n" + extra + "\n" + content[4:], encoding="utf-8")


if __name__ == "__main__":
    main()
