# Premium v2.1 — External Adversarial Review Prompt

Use this prompt when handing the Premium v2.1 experiment to an independent
engineer or AI reviewer.

## Review target

Repository: `YB-Park/over-the-luna`  
Branch: `experiment/premium-v2-1-minimal-cascade`  
Approved design closure:
`5e1c7ac425acf2e35b2b015260301f150af2c65d`  
Pre-live frozen code:
`8290643334712493f06978a40ec3acb9b4d6c2b4`  
Zero-AI baseline:
GitHub Actions run `35800930744`, **153/153 PASS**

Do not review stable main as though it were this experiment. Do not propose
reviving the retired broad Premium architecture unless you first demonstrate
that the approved minimal experiment is invalid as an experiment.

## Required reading order

1. `docs/PREMIUM_V2_1_PRE_LIVE_FREEZE.md`
2. `docs/PREMIUM_V2_1_PRE_LIVE_ADVERSARIAL_REVIEW.md`
3. `docs/PREMIUM_V2_1_MINIMAL_CASCADE_RFC.md`
4. `docs/PREMIUM_V2_1_IMPLEMENTATION_RESULTS.md`
5. `experiments/premium_v2_1_plugin/agents/premium-cascade-v2-1.agent.md`
6. `experiments/premium_v2_1_plugin/agents/luna-builder-v2-1.agent.md`
7. `experiments/premium_v2_1_plugin/hooks.json`
8. `experiments/premium_v2_1_plugin/scripts/hook.py`
9. `experiments/premium_v2_1_plugin/scripts/controller.py`
10. `scripts/premium_v2_1_controller.py`
11. `scripts/premium_v2_1_trace_report.py`
12. relevant `tests/test_premium_v2_1_*.py`

If a live smoke evidence bundle is available, review it only after understanding
the frozen code and then verify its `manifest.json` hashes.

## Review stance

Assume the authors are wrong until the evidence survives concrete attack.

Do not reward:
- a large passing test count by itself;
- polished agent prose;
- a passing synthetic code fix by itself;
- frontmatter model names as backend identity;
- file hashes as proof of semantic correctness;
- external state placement as tamper resistance.

Prefer executable counterexamples over architectural opinions.

## Questions you must attack

At minimum attempt counterexamples for:

1. criterion omission or authority laundering;
2. deletion/narrowing/re-sourcing of required U/R obligations;
3. forged, stale, non-execution, or irrelevant receipts;
4. validation followed by semantic mutation;
5. workspace/external final-record disagreement;
6. second or wrong subagent dispatch through alternate tool shapes;
7. pre-Builder root work that escapes detection;
8. Terra takeover without legitimate blocking evidence;
9. metadata-only path/command/symlink abuse;
10. resumed/multi-prompt session authority confusion;
11. cross-session trace or state mixing;
12. root/Builder model identity misattribution;
13. disconnected or stale OTel span attribution;
14. malformed hook input/state and exception paths;
15. hook timeout or missing PostToolUse behavior;
16. normal Builder Agent-tool wrapper completion being mistaken for a second
    subagent, or vice versa;
17. workspace-digest exclusions and hidden nested content;
18. changed/weakened validation assets;
19. background writers / quiescence gaps;
20. same-user controller-state tampering;
21. semantic irrelevance of technically passing evidence;
22. infrastructure failure mislabeled as semantic residual;
23. any assertion in docs that is stronger than the evidence;
24. any test that proves only its fixture rather than the intended invariant.

## Required classification

For every material finding, classify it as exactly one primary category:

- **DETERMINISTIC_CONTROLLER_BUG**
- **HOOK_ADAPTER_OR_RUNTIME_BUG**
- **SEMANTIC_MODEL_JUDGMENT_LIMIT**
- **SECURITY_BOUNDARY_LIMIT**
- **EXPERIMENT_DESIGN_PROBLEM**
- **DOCUMENTATION_OR_CLAIM_OVERREACH**

State whether the finding:
- can create false trusted COMPLETE;
- can cause false BLOCKED/NO_VERIFIED_COMPLETION only;
- can cause unauthorized spend/tool activity;
- affects only observability/reviewability;
- is already an explicitly documented limitation.

## Evidence standard

For a blocker, provide:
- exact file/function or runtime artifact;
- minimal adversarial input/event/state;
- expected behavior;
- actual behavior;
- why an existing test does not already cover it.

For a runtime claim, cite raw live evidence. If the fact was not observed, say
`NOT_OBSERVED` rather than inferring it from documentation or configuration.

## Requested output

Produce these sections:

### 1. Critical blockers
Only findings that should block the next stated experiment step.

### 2. High-value non-blocking findings
Real issues that do not invalidate the next audit-only step.

### 3. Counterexamples attempted but resisted
Name the attack and the exact invariant/test that defeated it.

### 4. Claims that exceed evidence
Quote or point to the claim and state the strongest defensible replacement.

### 5. Runtime unknowns
Facts that cannot be decided from the repository alone.

### 6. Minimal fixes
Prefer the smallest change that closes each concrete issue. Do not redesign the
entire system without demonstrating why a local fix is insufficient.

### 7. Review disposition
Choose one:

- `BLOCK_AUDIT_SMOKE`
- `ALLOW_AUDIT_SMOKE_ONLY`
- `AUDIT_TRACE_REQUIRES_PARSER_FIX_AND_REPEAT`
- `ALLOW_SEPARATE_ENFORCE_MODE_RETEST`

Do **not** use a pre-live repository review to issue a product-promotion verdict.

## Forbidden shortcuts

Do not:
- treat H1/H2/H3/H4 as fresh holdouts;
- recommend tuning the frozen v1 candidate;
- modify stable main to simplify the experiment;
- reintroduce broad L/T/M routing by default;
- add an Architect/Verifier/Auditor merely for reassurance;
- call state tamper-proof because it is outside the workspace;
- call completion semantically correct because the deterministic controller
  returned COMPLETE.
