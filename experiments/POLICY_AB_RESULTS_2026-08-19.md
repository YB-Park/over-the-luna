# v1.1 policy A/B — first live result

This records a controlled live Copilot comparison between the released v1.0 routing contract and the experimental `DIRECT/ISOLATE/DEEP + NONE/REVIEW/RISK` candidate. It is evidence, not a release decision.

## Setup

Both variants started from byte-identical small Python repositories and received the same normal user task:

- make `preview_order` use the same established customer-ID validation/normalization as `create_order`;
- add focused regression tests;
- preserve return shape and quantity semantics;
- run relevant tests;
- do not use premium review.

Runtime:

- GitHub Actions;
- Copilot CLI 1.0.80;
- GPT-5.6 Luna;
- checked-out Over the Luna plugin loaded with `--plugin-dir`;
- same allowed tools and hard AI-credit ceiling for both variants;
- OTel content capture disabled;
- separate clean fixture and plugin copy per variant;
- hidden post-run evaluation outside the agent-visible repository tests.

The candidate changed only Main routing/assurance instructions. Main remained the only mutation owner and used the same `Luna Reviewer` leaf implementation as v1.0.

## Released-policy baseline

Observed route:

`Mode: SIMPLE — direct Luna`

- Agent invocations: 1
- Reviewer invocations: 0
- Model calls: 7
- Tool calls: 10
- OTel input/output tokens: 98,932 / 957
- Main input/output tokens: 98,932 / 957
- First mutation tool: `apply_patch`
- Visible repository tests: PASS
- Hidden evaluation: PASS

The completed patch was correct but received no automatic independent review despite being a behavioral mutation with new tests.

## Direct-assurance candidate

Observed route in the final response:

`DIRECT + REVIEW`

- Agent invocations: 2
- Subagents: 1 (`Luna Reviewer`)
- Reviewer invocations: 1
- Model calls: 8
- Tool calls: 13
- OTel input/output tokens: 103,367 / 1,724
- Main input/output tokens: 99,503 / 1,259
- Reviewer input/output tokens: 3,864 / 465
- First mutation tool: `apply_patch`
- Visible repository tests: PASS
- Hidden evaluation: PASS
- Reviewer verdict: PASS

The Reviewer inspected the final state and confirmed that `preview_order` reused `_normalize_customer_id`, preserved return/quantity semantics, and had focused coverage. It did not mutate the repository.

## Patch equivalence

The baseline and candidate produced the same implementation/test diff:

- one call to `_normalize_customer_id` added to `preview_order`;
- tests added for normalization, blank ID, and non-string ID;
- no unrelated changes.

So in this sample the assurance candidate did **not** alter implementation trajectory or cause review-driven rework.

## Incremental cost

Compared with the released policy:

- total input tokens: 98,932 → 103,367 (**+4.5%**);
- additional reviewer input/output: 3,864 / 465;
- Main input remained essentially flat (98,932 → 99,503);
- model calls: 7 → 8;
- one fresh read-only Reviewer was added.

The large percentage increase in total output tokens is not itself a useful cost signal here because absolute output volumes are small and the candidate final report explicitly includes the review result. Input/reviewer tokens and wall-clock should remain the primary overhead measures for subsequent samples.

## What this sample supports

It supports three narrow claims:

1. A clear local task can remain a single-Main implementation while a late fresh Reviewer is invoked reliably.
2. The independent pass can be added with modest incremental input-token overhead in at least one real Copilot run.
3. Separating assurance from implementation complexity does not inherently require competing mutation owners or pre-implementation planning ceremony.

## What this sample does **not** prove

- It does not prove that an always-on Reviewer improves correctness. Both variants were already correct.
- It does not prove that the full new routing vocabulary is needed; a smaller change to the existing SIMPLE/STANDARD/DEEP contract may achieve the same adherence.
- It does not establish reviewer precision on difficult patches. Earlier forced-review samples included one materially incorrect finding, so false-positive pressure remains a release concern.
- It does not justify a target Reviewer invocation rate.

## Next comparison

Compare this full two-axis candidate against a **minimal late-review candidate** that keeps `SIMPLE / STANDARD / DEEP` intact but makes two changes explicit:

1. the complexity mode governs investigation only, not the whole trajectory;
2. a late assurance gate requires one fresh Reviewer for non-trivial completed mutation regardless of initial mode.

If the minimal candidate achieves the same Reviewer adherence and similar quality/cost, prefer the smaller product/mental-model change. Independently test broad-scoping reclassification; do not use Reviewer policy as a substitute for Architect/context-isolation routing.
