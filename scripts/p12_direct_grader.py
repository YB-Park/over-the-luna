#!/usr/bin/env python3
"""Independent offline P12 grader: real missing subagent toolCallId bug."""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IMPL="scripts/role_trace_accounting.py"
TEST="tests/test_role_trace_accounting.py"
HIDDEN="""
from scripts.role_trace_accounting import _pair_lifecycle
def e(name='Next Architect', ident=None):
    x={'name':name}
    if ident is not None: x['toolCallId']=ident
    return x
assert _pair_lifecycle([e()],[e()])==0, 'missing ids must not pair'
assert _pair_lifecycle([e(ident='')],[e(ident='')])==0
assert _pair_lifecycle([e(ident=12)],[e(ident=12)])==0
assert _pair_lifecycle([e(ident='a')],[e(ident='a')])==1
assert _pair_lifecycle([e(ident='a')],[e(ident='b')])==0
assert _pair_lifecycle([e(ident='a'),e(ident='a')],[e(ident='a')])==1
assert _pair_lifecycle([e(ident='a')],[e(name='Next Reviewer',ident='a')])==0
"""
def run(work,args):
    env={"PATH":os.environ.get("PATH",""),"HOME":tempfile.gettempdir(),
         "LANG":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1"}
    result=subprocess.run(args,cwd=work,env=env,stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL,timeout=35,check=False)
    return result.returncode==0
def hidden_pass(work):return run(work,[sys.executable,"-c",HIDDEN])
def grade(work,changed):
    checks={
      "only_expected_implementation_and_authored_regression_changed":
         sorted(changed)==sorted([IMPL,TEST]),
      "existing_and_authored_tests_pass":
         run(work,[sys.executable,"-m","unittest","discover",
                   "-s","tests","-p","test_role_trace_accounting.py"]),
      "independent_missing_id_oracle":hidden_pass(work),
    }
    return {"pass":all(checks.values()),"checks":checks}
def self_test():
    # Test a vulnerable and repaired TEMP copy, even after the public
    # research branch has legitimately fixed its original seeded defect.
    with tempfile.TemporaryDirectory(prefix="otl-p12-") as temp:
        work=Path(temp)
        for rel in (IMPL,TEST,"tests/fixtures/p5_role_accounting.json",
                    "scripts/p5_fixture_provenance.py"):
            to=work/rel
            to.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/rel,to)
        path=work/IMPL
        src=path.read_text(encoding="utf-8")
        marker="        return name.strip(), ident if isinstance(ident, str) and ident else None"
        fixed=("        if not isinstance(ident, str) or not ident:\n"
               "            return None\n"
               "        return name.strip(), ident")
        if src.count(marker)==1:
            vulnerable=src
        elif src.count(fixed)==1:
            vulnerable=src.replace(fixed,marker)
        else:
            raise ValueError("unexpected P12 source contract")
        path.write_text(vulnerable,encoding="utf-8")
        if hidden_pass(work):
            raise ValueError("negative oracle control failed")
        path.write_text(vulnerable.replace(marker,fixed),encoding="utf-8")
        if not hidden_pass(work):
            raise ValueError("positive oracle control failed")
        print("P12_ORACLE_PASS: temp vulnerable and fixed controls agree")
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--work",type=Path)
    p.add_argument("--changed",nargs="*",default=[])
    a=p.parse_args()
    if a.self_test:return self_test()
    if a.work is None:p.error("--work required")
    print(json.dumps(grade(a.work,a.changed),sort_keys=True))
if __name__=="__main__":main()
