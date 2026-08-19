# v1.1 reviewer quality matrix — 2026-08-19

This experiment follows the assurance-adherence work. It asks whether reliable fresh review produces useful engineering value on varied normal behavioral changes, rather than merely increasing Reviewer invocation count.

## Setup

Three small but distinct tasks were run under two policies:

- released v1.0 baseline;
- split-state candidate (`SIMPLE/STANDARD/DEEP` investigation plus first-class `NONE/REVIEW/RISK` assurance).

Cases:

1. **falsey-config** — align update-time timeout handling with an established create-time contract, including explicit zero while preserving `None` and retries semantics;
2. **request-id** — align update headers with an established request-ID normalization/validation helper while preserving Authorization and absence behavior;
3. **cache-key** — align cache invalidation with the normalized key identity/validation used by put/get while preserving missing-key no-op behavior.

These were not seeded Reviewer traps. Each fixture represented a normal local contract-alignment task with visible tests and a separate hidden evaluator.

All runs used GPT-5.6 Luna through Copilot CLI 1.0.80, identical tool bounds, no premium models, OTel content capture off, and an isolated plugin/fixture per run. The temporary paid PR-trigger workflow was deleted immediately after artifact collection.

## Result summary

| Case | Baseline hidden | Baseline reviewer | Split hidden | Split reviewer | Split review outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| falsey-config | PASS | 0 | PASS | 1 | PASS + optional test/scope notes |
| request-id | PASS | 0 | PASS | 1 | PASS |
| cache-key | PASS | 0 | PASS | 1 | PASS |

Across these three tasks:

- baseline hidden correctness: **3 / 3**;
- split-state hidden correctness: **3 / 3**;
- split Reviewer adherence: **3 / 3**;
- unique verified must-fix findings from Reviewer: **0**;
- Reviewer-driven repairs: **0**;
- material false-positive repairs: **0**.

The Reviewer was mostly disciplined. On falsey-config it suggested optional additional invalid-timeout coverage and noted unchanged retries validation; Main did not expand scope. On the other two tasks it returned clean PASS judgments.

## Per-case details

### falsey-config

Baseline:

- `Mode: SIMPLE — direct Luna`;
- Reviewer 0;
- hidden PASS;
- input 66,568;
- event duration about 13.3 s.

Split-state:

- `Mode: SIMPLE — direct Luna | Assurance: REVIEW`;
- Reviewer 1;
- hidden PASS;
- total input 88,705;
- Reviewer/Council input 9,229;
- event duration about 51.6 s.

Both implemented the same semantic fix: `if timeout is not None` and focused zero/absence regression coverage. The Reviewer found no defect. Its optional test suggestions did not justify additional production change.

### request-id

Baseline:

- `Mode: SIMPLE — direct Luna`;
- Reviewer 0;
- hidden PASS;
- input 330,885;
- event duration about 60.3 s.

Split-state:

- declared `Mode: STANDARD — focused repository inspection | Assurance: REVIEW`;
- Reviewer 1;
- hidden PASS;
- total input 165,410;
- Reviewer/Council input 3,743;
- event duration about 42.7 s.

Both correctly replaced the truthiness path with `if request_id is not None` plus the shared normalizer and added validation regressions.

Important routing observation: despite declaring `STANDARD`, the split run invoked **no investigative subagent**. The only subagent was the final Reviewer. This is a useful warning that raising the mode label is not equivalent to actually isolating exploration/context.

### cache-key

Baseline:

- `Mode: SIMPLE — direct Luna`;
- Reviewer 0;
- hidden PASS;
- input 67,537;
- event duration about 13.8 s.

Split-state:

- `Mode: SIMPLE — direct Luna | Assurance: REVIEW`;
- Reviewer 1;
- hidden PASS;
- total input 95,447;
- Reviewer/Council input 3,674;
- event duration about 26.3 s.

Both correctly routed invalidation through `_normalize_key`, preserved `pop(..., None)`, and added normalized-identity/invalid-key tests. Reviewer returned PASS.

## Interpretation

This matrix gives **no evidence yet that a fresh Reviewer should run after every normal non-trivial mutation**. The baseline was already correct on all three varied tasks, while review added latency and tokens and produced no unique must-fix finding.

It also does **not** show that Reviewer is useless. The split-state policy made independent assurance reliable without causing unwanted repairs, and its Reviewer precision was materially better than the earlier forced-review sample that produced a factually wrong must-fix claim.

The appropriate current conclusion is therefore:

> Reliable review is now technically achievable, but its **expected-value threshold** is not established. Invocation adherence and reviewer quality are separate problems.

Cheap Luna tokens lower the cost of an extra pass; they do not remove latency, false-positive pressure, or human/rework cost.

## New routing finding

The request-id run exposed an investigation problem independent of assurance:

> A `STANDARD` label can be emitted without a corresponding read-only Council isolation pass.

Therefore v1.1 should not define success as fewer SIMPLE labels or more STANDARD labels. It should measure actual ownership of disposable exploration:

- Main repository reads/searches before mutation;
- Architect invocation when broad scouting is needed;
- Main context/token growth before mutation;
- whether Main rehydrates the broad evidence after Architect returns.

## Next evidence needed

1. **Harder behavioral/cross-file tasks** where baseline correctness is not trivially saturated, to evaluate whether fresh review catches real residual errors and whether Main adjudication avoids false-positive rework.
2. **Broad-scouting isolation experiments** independent of assurance, using tasks whose implementation location must be discovered rather than supplied.
3. **Real authenticated VS Code traces** before release, because CLI experiments validate plugin/model orchestration but not the exact handoff UI or user-selected tool inheritance experience.

The split-state representation remains the leading assurance representation because it has strong adherence with less mental-model churn than a full mode rename, but always-on REVIEW is **not yet a release conclusion**.
