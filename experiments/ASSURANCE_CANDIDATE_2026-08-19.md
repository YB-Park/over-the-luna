# v1.1 assurance candidate — integrated runtime result

This file records one controlled Copilot runtime comparison of the two-axis assurance candidate against the released/baseline policy. It is evidence, not a v1.1 release decision.

## Candidate contract

The candidate keeps `SIMPLE / STANDARD / DEEP` as the investigation/execution-support decision and adds a distinct post-mutation assurance checkpoint after focused validation:

- `Assurance: NONE` only for tiny, obvious, mechanically validated mutations;
- `Assurance: REVIEW` for other non-trivial completed mutations: exactly one fresh Luna Reviewer;
- `Assurance: RISK` for genuinely high-risk work: at most two distinct review rubrics.

Main remains the only mutation owner. Reviewer findings are evidence that Main must adjudicate rather than commands to accept mechanically. The SIMPLE threshold itself is unchanged.

## Controlled comparison task

The live candidate probe reused the exact task from baseline review-ablation Sample 1:

> Improve `scripts/analyze_otel.py` so `execute_tool` spans are attributed to the nearest invoking agent, preserve global tool totals, expose Main-versus-Council tool counts and first mutation owner, and add focused regression tests.

The candidate branch did not contain the baseline experiment's generated patch, so Main implemented the task from the same research-code starting point.

## Baseline behavior on the same task

Released/baseline policy:

- `Mode: SIMPLE — direct Luna`
- automatic Reviewer: **0**
- model calls: 6
- tool calls: 9
- OTel Main input/output: 134,885 / 2,130
- session nanoAIU: 1,133,239,000
- observed session event span: about 24.3 s
- focused/full tests passed in that baseline run.

A separately forced exact-patch Luna Reviewer then cost 6,702 / 668 OTel input/output tokens and returned materially incorrect claims about orphan ownership, causing no accepted repair. That external review was deliberately not integrated into Main's trajectory.

## Candidate integrated behavior

Candidate policy:

- `Mode: SIMPLE — direct Luna`
- visible checkpoint: `Assurance: REVIEW — Luna Reviewer`
- actual OTel child invocation: `over-the-luna:luna-reviewer` **1**
- model calls: 11
- tool calls: 16
- OTel total input/output: 248,844 / 5,310
- Main input/output: 238,256 / 3,639
- Reviewer input/output: 10,588 / 1,671
- reviewer tool calls: 2 read-only `view` calls
- Main owned both `apply_patch` mutations and both validation `bash` calls
- premium requests: 0
- session nanoAIU: 2,029,086,000
- observed session event span: about 61.8 s
- Reviewer subagent duration reported by Copilot: about 21.9 s.

The one-shot paid workflow used to launch this probe was deleted as soon as the run was queued. The branch returned to the manual-only paid-workflow invariant and its normal static CI passed. The triggering SHA intentionally violated the paid-workflow guard, so a post-run *full repository* validation saw that temporary workflow and failed only `test_paid_workflows_are_manual_only`. Main's task-focused analyzer suite passed 5/5 before and after the accepted review repair.

## Reviewer findings and Main adjudication

The Reviewer returned two `should-fix` observations.

### 1. Trace-ID collision concern — rejected for this scoped change

The Reviewer noted that the existing parent lookup indexes spans by `span_id` without `trace_id`, so multiple merged traces could theoretically collide.

This is a legitimate design question in the pre-existing traversal but was not a defect introduced by the task's tool-attribution patch. The original requirement explicitly asked to reuse the existing parent traversal rather than redesign it. Main classified this as out of scope and did not create rework from it.

This is evidence that the candidate's "Reviewer is evidence, not authority" instruction worked in this sample.

### 2. Nearest nested-agent coverage — accepted

The Reviewer observed that the first regression fixture proved Main versus one Council ancestor but did not directly prove **nearest** ownership when invoking agents are nested.

Main accepted this as a useful test-adequacy finding, amended the fixture to contain `Luna Architect -> Luna Skeptic -> apply_patch`, asserted the innermost `Luna Skeptic` owns the mutation, and reran the focused suite successfully.

Classification:

- unique actionable review finding that changed the final patch: **1**;
- reviewer concern deliberately rejected after adjudication: **1**;
- unsupported must-fix findings: **0**;
- accepted repair performed by Main: **1**;
- mutation by Reviewer: **0**.

## Interpretation

### The assurance split fixed the observed adherence problem in this sample

The most important result is structural: the task stayed `SIMPLE`, yet the candidate still executed an actual fresh Reviewer. This is exactly the behavior the single-axis policy failed to produce in both prior non-trivial mutation samples.

This supports separating **how to investigate/implement** from **whether the completed mutation deserves independent assurance** rather than lowering the SIMPLE threshold.

### Review can improve the artifact, but the full trajectory cost matters

The Reviewer itself was a modest fraction of total tokens, but integrated review created additional Main turns for adjudication, repair, and revalidation. Relative to the baseline Main-only run, total OTel input and session nanoAIU increased materially, and observed session duration more than doubled.

The correct cost unit is therefore not "one Reviewer call." It is:

> reviewer + adjudication + accepted repair + revalidation

That extra compute bought a concrete nested-ownership regression test in this sample. More tasks are required to determine whether the expected value is positive often enough for `REVIEW` to be a common non-trivial default.

### Next experiment

Do not broaden the candidate or lower SIMPLE yet. Repeat the integrated candidate on several task archetypes with the same measurements:

1. tiny mechanical mutation — should choose `Assurance: NONE` and avoid ceremony;
2. clear non-trivial local behavior — should stay direct but invoke exactly one Reviewer;
3. broad-pattern discovery — Architect isolation should remain independent of the later assurance decision;
4. consequential assumption/high-risk change — test whether `RISK` remains bounded and distinct rather than duplicative.

Success requires both **adherence** and **verified incremental value**. A higher Reviewer invocation rate by itself is not a win.
