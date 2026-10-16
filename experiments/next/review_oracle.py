#!/usr/bin/env python3
"""Independent executable oracle; no LLM access required. Assertions are never included in model prompts."""
import json
from pathlib import Path

cases=json.loads((Path(__file__).parent / "review_cases.json").read_text())
expected={}
for case in cases:
    scope={"__name__":"candidate"}
    try:
        exec(compile(case["candidate"],case["name"],"exec"),scope)
        exec(compile(case["oracle"],case["name"]+":oracle","exec"),scope)
        outcome="PASS"
    except (AssertionError,ValueError,TypeError,NameError,KeyError,AttributeError,IndexError):
        outcome="MUST-FIX"
    expected[case["name"]]=outcome
assert len(expected)==5 and list(expected.values()).count("PASS")==2 and list(expected.values()).count("MUST-FIX")==3, "benchmark fixture labels corrupted"
print(json.dumps(expected,sort_keys=True))
