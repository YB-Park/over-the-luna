# v1.1 fresh Luna review ablation — first results

These results test the incremental value of one fresh read-only Luna Reviewer on the **exact same completed patch**. They do not yet define the v1.1 policy.

Both tasks were real research-infrastructure changes rather than seeded reviewer traps. In each run Main followed the released Over the Luna policy normally. After Main finished and validation ran, the working-tree diff was frozen. One externally forced `Luna Reviewer` then received the requirement, validation output, exact diff, and a concrete rubric. The reviewer had no mutation tools, and pre/post-review diff hashes were identical.

## Sample 1 — OTel tool-ownership attribution

Task: extend `scripts/analyze_otel.py` so `execute_tool` spans are attributed to Main vs Council while preserving global totals, expose first mutation owner, and add focused tests.

### Main before forced review

- Route: `Mode: SIMPLE — direct Luna`
- Automatic subagents: 0
- Automatic Reviewer: **0**
- Model calls: 6
- Tool calls: 9
- OTel input/output tokens: 134,885 / 2,130
- Focused/full repository tests: pass
- Modified files: `scripts/analyze_otel.py`, `tests/test_analyze_otel.py`

The patch reused the existing `nearest_agent` traversal, added Main/Council counters and `first_mutation_agent`, and extended the existing attribution test.

### Fresh Reviewer

- Reviewer calls: 1
- Tool calls: 0
- OTel input/output tokens: 6,702 / 668
- Mutation: none; exact diff hash unchanged

Reviewer returned one `must-fix` and one `should-fix`, centered on unknown/orphan span ownership and test coverage.

### Adjudication

The `must-fix` was **factually wrong as stated**. It claimed unknown/orphan tools would fall into Council because the new split uses `main if is_main_agent(agent) else council`. But the unchanged `nearest_agent()` implementation falls back to the literal `"main"` when no parent agent is found, so the actual ambiguous behavior is the opposite: unknown ownership can collapse into Main.

The coverage criticism was also overstated: the changed test already has a Main-owned `runSubagent` tool under the root agent and a Council-owned `apply_patch` under `Luna Architect`, so distinct parent chains are exercised. Explicit orphan coverage is not present and remains a reasonable future question.

Classification:

- unique verified actionable findings: **0**;
- false-positive/speculative findings: **1 review containing materially incorrect claims**;
- useful question surfaced: whether unknown ownership should be explicit rather than default-Main;
- accepted repair caused by review: **none**.

This sample is evidence that a fresh review pass is not automatically performance-positive. A cheap reviewer can still create rework pressure if it does not inspect the unchanged context that its claim depends on.

## Sample 2 — paid Copilot workflow guard

Task: add a runtime contract ensuring any workflow with `permissions.copilot-requests: write` is manual-only (`workflow_dispatch`) and rejects automatic triggers, with a synthetic negative regression and no false positive for the normal validation workflow.

### Main before forced review

- Route: `Mode: SIMPLE — direct Luna`
- Automatic subagents: 0
- Automatic Reviewer: **0**
- Model calls: 8
- Tool calls: 14
- OTel input/output tokens: 139,654 / 2,488
- Full repository tests: 9/9 pass

Main correctly noticed that the one-shot experiment workflow itself still had a temporary PR trigger during the experiment, converted it to `workflow_dispatch`, handled PyYAML 1.1 parsing of the GitHub Actions `on` key through the boolean `True` fallback, and added positive/negative contract tests.

### Fresh Reviewer

- Reviewer calls: 1
- Tool calls: 0
- OTel input/output tokens: 6,346 / 447
- Mutation: none; exact diff hash unchanged
- Verdict: `PASS`

Classification:

- unique verified actionable findings: **0**;
- false positives: **0**;
- accepted repair caused by review: **none**;
- value delivered: independent PASS/assurance only.

The paid-workflow contract from this sample was subsequently adopted into the research branch because it is independently useful experiment safety infrastructure.

## Two-sample observations

### 1. Reviewer-policy adherence is a concrete runtime gap

Both changes are non-trivial enough that the current Main contract says they should normally receive one Luna Reviewer. Actual automatic Reviewer invocation was **0/2**.

This is stronger evidence than raw SIMPLE frequency. The problem is not merely that Main selected SIMPLE; it is that the single routing label appears to frame the entire trajectory strongly enough that the later independent-assurance rule did not fire in either completed mutation.

### 2. Forcing one Reviewer is not yet proven to improve correctness

Across these first two exact-patch samples:

- forced Reviewer passes: 2;
- unique verified actionable findings: 0;
- no-op/PASS reviews: 1;
- review with materially incorrect finding(s): 1;
- reviewer-caused accepted repairs: 0.

Typical incremental reviewer spend in these samples was only about 6–7K OTel input tokens and under 700 output tokens, so the compute cost is modest relative to Main. But low cost alone is not enough; reviewer precision matters because false positives impose human/rework cost.

### 3. The next candidate should separate assurance from investigation explicitly

The next experiment should not lower the SIMPLE threshold. Instead test a candidate Main contract with a distinct post-implementation assurance decision, for example conceptually:

- execution/investigation: `DIRECT | ISOLATE | DEEP`;
- assurance after concrete mutation: `NONE | REVIEW | RISK`.

The key candidate state is `DIRECT + REVIEW`: Main can keep a clear local implementation direct, then one fresh Luna receives the concrete diff + validation evidence.

The experiment must test both **adherence** (does the Reviewer actually run when the contract says REVIEW?) and **incremental quality** (are its findings precise enough to help?). A higher invocation rate without better verified outcomes is not success.
