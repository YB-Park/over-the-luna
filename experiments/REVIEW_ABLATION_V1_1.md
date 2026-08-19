# v1.1 experiment — fresh Luna review ablation

Status: **experiment design only**. This file does not change product routing.

## Question

For a non-trivial completed code change whose implementation path is locally clear, does buying exactly one fresh Luna Reviewer pass improve final correctness enough to justify its token/latency cost?

This deliberately separates two decisions that v1.0 tends to express through one routing label:

1. how much isolated investigation is needed to implement the change;
2. whether the completed artifact deserves independent assurance.

A task can therefore be direct during implementation and still receive a fresh review afterward.

## Primary ablation

Use the same repository revision, task, acceptance criteria, model family, allowed tools, and validation commands for both variants. Start each variant from a clean checkout.

### Variant A — current behavior

- Run the released Over the Luna policy normally.
- Do not externally force a reviewer.
- Record whether the policy chooses a Reviewer on its own.
- Preserve the final diff and validation evidence before any human correction.

### Variant B — one fresh final review

- Run the same implementation task from the same clean base.
- After Main has completed its implementation and focused validation, run exactly one **fresh `Luna Reviewer`** in read-only mode.
- Give the reviewer the user request, acceptance criteria, final diff, and relevant validation evidence; do not give it Main's hidden reasoning/trajectory.
- Use one concrete rubric: requirement satisfaction, regression risk, missing tests/validation, and repository-contract violations.
- Do not add Planner/Skeptic calls merely because this variant contains a Reviewer.

For the first measurement round, do not let the reviewer mutate. Record its findings before deciding whether a repair pass is warranted. This keeps the experiment focused on the value of independent judgment rather than conflating review quality with another implementation attempt.

## Task selection

Start with the existing `direct-nontrivial` corpus archetype:

> Add an already-established validation behavior to one nearby handler, following the local pattern and its tests.

The fixture should have:

- a clear local implementation path, so investigation should not itself require a Council;
- at least one meaningful behavioral acceptance criterion;
- focused tests that can pass even if a plausible secondary regression/requirement is missed;
- no artificial trick designed solely to make the reviewer win.

Repeat with several independent tasks before drawing conclusions. One seeded bug-catching demo is not evidence for a default policy.

## Measurements

Record per variant:

- execution route/mode;
- Main model calls and input/output/cache tokens;
- Council/reviewer calls and input/output/cache tokens;
- wall-clock duration;
- tool calls and mutation ownership;
- initial validation result;
- final diff size;
- reviewer invocation (automatic or forced experiment step);
- reviewer findings classified as:
  - **unique actionable** — changes the patch/tests and is confirmed useful;
  - **duplicate** — Main/tests had already identified it;
  - **false positive/speculative** — not supported after checking;
  - **style-only/non-material**;
- repair required after review;
- final validation result after any accepted repair;
- human intervention;
- edit survival/rework where observable.

## Decision metrics

The main metric is **incremental verified value per added review pass**, not reviewer verbosity.

Evidence in favor of `DIRECT + REVIEW` as a common non-trivial default would look like:

- repeatable unique actionable findings or prevented rework;
- low false-positive burden;
- bounded added latency/token spend relative to the implementation;
- no pressure to add planning ceremony before locally clear work.

Evidence against it would look like:

- almost all findings duplicate focused validation/Main's own checks;
- frequent speculative findings that create unnecessary rework;
- review spend becoming a large fraction of total compute without changing outcomes;
- the extra assurance state making routing less predictable or more bureaucratic.

## Secondary comparison — selective vs always-on review

If Variant B shows value, the next question is **where** to apply it. Do not jump directly to “review every task.” Compare:

- tiny/mechanical: reviewer normally skipped;
- direct/non-trivial: one fresh reviewer candidate;
- isolated/deep tasks: reviewer still independent of the investigation leaves;
- consequential/risk work: distinct rubric(s) only when the risk actually warrants them.

The product goal is a simple developer experience with cheap independent judgment at high-value boundaries, not a target reviewer invocation percentage.

## Premium relation

This experiment is Luna-only. Premium review is a separate incremental-judgment experiment.

A single visible `Premium Review` decision should only be evaluated after the normal Luna assurance baseline is understood; otherwise Sonnet/Opus may appear useful merely because the Luna review layer was missing or inconsistently invoked.
