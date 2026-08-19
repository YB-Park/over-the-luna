# v1.1 assurance candidate — boundary results

This file records two additional controlled Copilot runtime probes against `research/v1.1-assurance-candidate`. They test whether the separate Assurance checkpoint improves Reviewer adherence **without** turning tiny work into ceremony.

Both probes ran with GPT-5.6 Luna, no premium model, Main as the only mutation owner, and the same candidate contract used in the first integrated assurance result.

## Sample 2 — tiny documentation mutation

Task: change exactly one Markdown heading in `experiments/ASSURANCE_CANDIDATE_2026-08-19.md` and make no other semantic change.

Observed:

- `Mode: SIMPLE — direct Luna`
- `Assurance: NONE — tiny mechanical change`
- agent invocations: 1
- subagents: 0
- Reviewer invocations: **0**
- model calls: 4
- tool calls: 4 (`view`: 1, `apply_patch`: 1, `bash`: 2)
- OTel input/output: 58,499 / 400
- session nanoAIU: 520,173,000
- premium requests: 0
- exact mutation: one heading only.

### Interpretation

The candidate did **not** turn the new assurance checkpoint into an unconditional review tax. It kept a genuinely tiny, explicit, mechanically verifiable edit direct and reviewer-free.

This is the first positive precision signal for `Assurance: NONE`.

## Sample 3 — Assurance marker telemetry

Task: extend `scripts/analyze_otel.py` so the optional Copilot CLI event stream can recover `Assurance: NONE|REVIEW|RISK` independently of the existing Mode marker; expose assurance in JSON/Markdown; preserve Mode behavior and content-capture-off design; add focused tests for chunked text and UNKNOWN/default behavior.

Observed:

- `Mode: SIMPLE — direct Luna`
- `Assurance: REVIEW — Luna Reviewer`
- actual OTel Reviewer child invocation: **1**
- model calls: 10
- tool calls: 19
- OTel total input/output: 234,502 / 4,896
- Main input/output: 191,545 / 3,267
- Reviewer input/output: 42,957 / 1,629
- Reviewer read-only tool calls: 9 `view` calls
- Main mutation calls: 2 `apply_patch`
- Main validation calls: 5 `bash`
- Reviewer mutation: 0
- premium requests: 0
- Reviewer subagent duration: about 20.1 s
- final focused analyzer tests: **7/7 pass**.

### Reviewer findings

The Reviewer accepted the implementation shape but found two specific test-coverage gaps:

1. no integration-level proof that a positive Assurance marker travels through `--events` into the final machine-readable/Markdown summary path;
2. no regression proof that an Assurance-only event stream leaves trace-derived Mode unchanged.

Main classified these as concrete coverage gaps rather than implementation defects, accepted both, added focused integration/independence regression coverage, and reran the suite successfully.

Classification:

- unique actionable Reviewer findings that changed the final patch: **2**;
- rejected/out-of-scope Reviewer findings: **0**;
- unsupported must-fix findings: **0**;
- accepted repair performed by Main: **1 test-strengthening pass**;
- Reviewer mutation: **0**.

## Candidate adherence across three mutation samples

So far:

| Sample | Mutation class | Mode | Assurance | Actual Reviewer | Review changed final patch? |
| --- | --- | --- | --- | ---: | --- |
| OTel tool ownership | non-trivial local | SIMPLE | REVIEW | 1 | yes — nested nearest-agent coverage |
| Exact heading edit | tiny mechanical | SIMPLE | NONE | 0 | n/a |
| Assurance telemetry | non-trivial local | SIMPLE | REVIEW | 1 | yes — two integration/independence tests |

The important observation is that **all three stayed SIMPLE**. The candidate changed assurance behavior without lowering or inflating the investigation route.

For the two non-trivial mutations, the old/released policy had previously shown automatic Reviewer adherence of 0/2 in exact-patch ablations. The candidate has now shown integrated Reviewer adherence of 2/2 on two non-trivial tasks while still skipping review on the tiny mutation.

## Quality and cost interpretation

The first forced-review ablation demonstrated that a fresh Reviewer can also produce materially wrong findings, so invocation rate is not a sufficient success metric.

The integrated candidate results are more encouraging because Main is explicitly required to adjudicate Reviewer evidence:

- integrated sample 1: one useful coverage finding accepted, one pre-existing/out-of-scope design concern rejected;
- integrated sample 3: two useful coverage findings accepted;
- tiny sample: no Reviewer purchased.

However, integrated review is not free. Reviewer tokens are only part of the cost; review can trigger additional Main adjudication, repair, and revalidation turns. In these samples that extra trajectory cost is material. The architecture should therefore optimize **expected verified value per assurance trajectory**, not simply maximize review frequency.

## Current evidence-based position

Do not lower the SIMPLE threshold.

The two-axis candidate is now the leading architecture hypothesis because it has demonstrated the desired runtime shape:

> direct implementation can remain direct, while independent assurance is decided afterward.

This is still a small, self-hosted sample. Before treating it as a v1.1 product contract, the next evidence gate should use tasks outside the harness's own small repository so that the result is not dominated by prompt/repository familiarity.
