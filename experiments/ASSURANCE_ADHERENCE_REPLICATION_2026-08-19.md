# v1.1 assurance-state adherence replication — 2026-08-19

This experiment asks a narrow question: does the way assurance is represented in Main's routing contract affect whether a fresh Luna Reviewer actually runs after the same clear, non-trivial local mutation?

It does **not** test whether review always improves correctness. Reviewer precision is a separate release gate.

## Common fixture

All candidates received the same small Python repository and task: make `preview_order` use the same established customer-ID normalization/validation behavior as `create_order`, add focused regression tests, preserve return shape and quantity semantics, and run relevant tests.

Each run used:

- Copilot CLI 1.0.80;
- GPT-5.6 Luna;
- the checked-out plugin with one experimental Main policy substituted in an isolated runner copy;
- the same tool allowlist and hard AI-credit ceiling;
- an independent hidden evaluation after the run;
- no premium model;
- OTel content capture disabled.

A temporary PR-triggered paid workflow was used only to collect the matrix through the connected experiment harness and was deleted immediately after artifact collection. The research branch's persistent paid workflows remain manual-only.

## Policies

### Full two-axis candidate

Investigation vocabulary changes to `DIRECT | ISOLATE | DEEP`, with assurance declared independently as `NONE | REVIEW | RISK`.

Typical initial route:

`Route: DIRECT + REVIEW`

### Minimal late-gate candidate

Keeps `SIMPLE | STANDARD | DEEP`; says those modes govern investigation only; adds a strong late rule requiring review for non-trivial mutation. Assurance is **not** declared in the initial route.

Typical initial route:

`Mode: SIMPLE — direct Luna`

### Split-state candidate

Keeps `SIMPLE | STANDARD | DEEP` for investigation but declares assurance as a first-class state at the same initial decision.

Typical initial route:

`Mode: SIMPLE — direct Luna | Assurance: REVIEW`

## Adherence result

Including each candidate's first live A/B sample plus two additional identical-task repetitions:

| Policy | Reviewer adherence | Hidden evaluation | Interpretation |
| --- | ---: | ---: | --- |
| Full two-axis | **3 / 3** | 3 / 3 PASS | first-class assurance consistently executed |
| Minimal late-gate | **1 / 3** | 3 / 3 PASS | late textual requirement was often suppressed by SIMPLE trajectory |
| Split-state | **3 / 3** | 3 / 3 PASS | familiar mode names + early assurance commitment consistently executed |

The minimal candidate is therefore not incapable of reviewing: one replication did call the Reviewer. The problem is reliability, not absolute functionality.

## Replication details

### Full candidate repetitions

Both additional runs declared `DIRECT + REVIEW`, performed one Main-owned patch, ran focused tests, then invoked one fresh `Luna Reviewer`.

- repetition 1: Reviewer 1, hidden PASS, total input 91,151, Reviewer/Council input 7,926, event duration about 28.6 s;
- repetition 2: Reviewer 1, hidden PASS, total input 89,582, Reviewer/Council input 5,979, event duration about 28.5 s.

One Reviewer correctly passed the code but added `VERIFY` because test-execution evidence was not available in its evidence packet, even though Main had run the tests. This is not a code defect; it is evidence that reviewer evidence packaging should explicitly carry validation results rather than relying on conversational availability.

### Minimal candidate repetitions

- repetition 1: Reviewer **0**, hidden PASS, input 80,291, duration about 15.8 s;
- repetition 2: Reviewer **1**, hidden PASS, input 86,435, Reviewer/Council input 5,749, duration about 29.1 s.

Both began with `Mode: SIMPLE — direct Luna`. The second happened to honor the late gate; the first did not.

### Split-state repetitions

Both additional runs declared `Mode: SIMPLE — direct Luna | Assurance: REVIEW` and invoked one fresh Reviewer after focused validation.

- repetition 1: Reviewer 1, hidden PASS, input 115,462, Reviewer/Council input 5,766, duration about 29.4 s;
- repetition 2: Reviewer 1, hidden PASS, input 86,122, Reviewer/Council input 5,591, duration about 29.2 s.

The second Reviewer passed the requested behavior but mentioned unchanged quantity type-validation as residual/should-fix risk. The task explicitly required preserving quantity semantics, so Main correctly did not expand scope. This supports keeping Reviewer findings advisory and requiring Main adjudication rather than treating review text as authoritative repair instructions.

## Interpretation

Across this small controlled sample, the important distinction is not the word `DIRECT` versus `SIMPLE`.

The stronger hypothesis is:

> **Assurance adherence improves when the expected independent check is represented as a first-class state at the initial route decision, rather than as a later rule that must override an already-established `SIMPLE — direct` trajectory.**

This is consistent with released-v1.0 observations where non-trivial mutation received no automatic Reviewer despite a later prompt section requiring one.

The split-state candidate currently dominates the full vocabulary rename on product simplicity: it achieved the same 3/3 adherence in this experiment while preserving the existing investigation vocabulary.

That is still only a design lead, not a release decision.

## Release implications not yet earned

Do **not** ship `Assurance: REVIEW` as a default merely because invocation adherence improved.

Before a v1.1 decision, evidence is still needed for:

1. **Reviewer precision across diverse non-trivial tasks** — unique actionable findings, false positives, duplicates, unnecessary rework, and PASS quality.
2. **Latency/cost trade-off** — cheap tokens do not make an extra ~10–15 seconds irrelevant to product quality.
3. **Broad-scouting reclassification** — Probe 002 showed Main can remain SIMPLE while consuming broad disposable repository context; assurance does not solve that investigation problem.
4. **Real VS Code behavior** — CLI routing evidence does not replace authenticated VS Code checks for handoff UI and selected-tool inheritance.

The next candidate experiments should therefore use the split-state policy as the leading assurance representation while independently testing reviewer quality and context-isolation routing.
