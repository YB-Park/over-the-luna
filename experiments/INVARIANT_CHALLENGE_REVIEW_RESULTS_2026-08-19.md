# v1.1 invariant-challenge Reviewer replication — 2026-08-19

This experiment follows `DEPENDENCY_CLOSURE_REVIEW_RESULTS_2026-08-19.md`. The same exact completed patch was reviewed twice by `v1_1_candidate_invariant_reviewer.agent.md`.

The candidate keeps artifact-first evidence and bounded semantic dependency closure, then requires one acceptance-critical invariant challenge before PASS. The challenge must be derived from the changed behavior plus inspected dependencies, not generic adversarial brainstorming.

The known patch-relevant oracle remained unchanged: the completed ownership patch indexes ancestry by `span_id` alone even though spans carry `trace_id`; valid identical span IDs in different traces can therefore corrupt nearest-agent ownership.

## Results

| Repeat | Verdict | Repo tools | Input | Output | Cross-trace issue | Speculative re-export |
| --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | **MUST-FIX** | 4 `view` | 23,427 | 895 | **found** | no |
| 2 | **MUST-FIX** | 3 `view` | 21,298 | 902 | **found** | no |

Both reviews were read-only; the exact pre/post diff remained identical. Visible tests and plugin validation passed before review.

## Repeat 1

The Reviewer inspected:

- `scripts/analyze_otel.py` in two bounded ranges;
- `scripts/analyze_tool_ownership.py`;
- `tests/test_analyze_otel.py`.

It returned:

> Ownership lookup keys only by `span_id`, omitting `trace_id` despite `Span` carrying both. Valid spans from different traces can share span IDs, causing nearest-agent traversal and ownership attribution to use the wrong trace's parent.

It explicitly challenged the unsupported assumption that span IDs are globally unique across all loaded traces.

## Repeat 2

The Reviewer inspected only:

- `scripts/analyze_otel.py` in two bounded ranges;
- `scripts/analyze_tool_ownership.py`.

It independently returned the same defect and the same repair direction: parent lookup should preserve `(trace_id, span_id)` identity through ancestry traversal.

## Comparison with previous Reviewer shapes

On the exact same patch:

| Reviewer shape | Repeats finding cross-trace defect | Typical repo reads | Typical input |
| --- | ---: | ---: | ---: |
| current Reviewer | 0 / 2 | 0 | ~7.6k |
| strict artifact-first | 0 / 2 | 0 | ~7.8k |
| dependency-closure only | 0 / 2 | 3 | ~20.9k |
| **dependency + invariant challenge** | **2 / 2** | **3–4** | **~22.4k** |

The invariant-challenge candidate costs roughly 3× the input of a zero-read PASS review on this small patch, but it converted a repeatable false PASS into a repeatable supported must-fix finding with only local repository reads.

This is the first v1.1 Reviewer experiment where a structural evidence-selection rule repeatably improves defect detection on an unchanged completed artifact.

## Why this worked

The important difference was not simply “more context.” Dependency-closure-only runs had already opened the same central analyzer code and still passed incorrectly.

The successful rule was:

> after reading the acceptance-critical dependency, explicitly falsify one semantic assumption that connects the changed code to the requirement.

Here, the changed aggregation builds a parent lookup while the data model visibly carries both trace and span identity. That naturally creates an identity/partition invariant to challenge. The Reviewer did not need broad repository discovery or a seeded mention of the known failing test.

## Assurance design lead

The leading normal `REVIEW` shape is now:

1. **First-class assurance state is declared early** so Reviewer adherence is reliable.
2. Reviewer receives acceptance criteria + exact final patch + validation evidence first.
3. Reviewer closes only acceptance-critical unchanged dependencies.
4. Before PASS, Reviewer challenges one consequential semantic invariant implied by the changed behavior.
5. Reads remain local and bounded; no broad repository review.
6. Findings are evidence for Main to adjudicate.
7. **Normal REVIEW buys exactly one Reviewer invocation for the task trajectory.**
8. Accepted repairs are performed and revalidated by Main, but do not automatically buy another Reviewer.
9. A second independent review requires explicit `RISK` escalation with a distinct rubric.

This combines the strongest evidence from the assurance-adherence, reviewer-quality, artifact-first, dependency-closure, and review-loop experiments without inheriting the four-review trajectory explosion.

## Remaining caution

This result is still one completed patch archetype with two replications. The invariant-challenge rule must not become a generic “invent an edge case” instruction; it should stay constrained to the changed artifact and acceptance-critical dependencies.

The next useful gate is therefore an **integrated candidate** that combines this Reviewer with the leading investigation boundary and enforces exactly one normal Reviewer even when a finding causes a repair.

Success should be judged on the whole trajectory: correctness, review precision, Main/Architect epistemic ownership, one-review adherence, revalidation after repair, and total cost.
