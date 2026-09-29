# GPT-6 Luna model-only qualification

This experiment asks one narrow question before any architecture redesign:

> Holding the Over the Luna v1.1.1 harness constant, how does GPT-6 Luna behave relative to GPT-5.6 Luna?

It is deliberately not a migration script and does not assume either model wins.

## Experimental rules

1. **Change one variable first.** The control and candidate plugin variants differ only in the automatic Luna model frontmatter (`GPT-5.6 Luna` vs `GPT-6 Luna`). Prompts, routing, tools, Premium Review, and budgets remain unchanged.
2. **Hidden correctness beats self-report.** Candidate summaries and Reviewer verdicts are evidence, not ground truth. Each fixture has an external hidden gate.
3. **Matched cases and repetitions.** Both models receive the same fixture, task text, tool surface, and credit cap. Important cases are repeated.
4. **Hard violations are first-class.** Mutation-ownership violations, wrong routing, broad replay after a sealed boundary, missing required review, false tool denial, or unauthorized side effects are recorded separately from correctness.
5. **No architecture tuning during model qualification.** SIMPLE/STANDARD/DEEP thresholds, Reviewer budgets, and agent topology are not changed until the model-only comparison is complete.
6. **Blind qualitative review.** When human patch-quality review is useful, aggregate artifacts should hide the model identity until judgments are recorded.
7. **No paid calls on push.** The branch preflight performs only static/self tests. Copilot model calls are manual-only in the later paid runner.

## Initial case families

- `mechanical_none`: exact scalar/default change with a direct assertion; expected route `SIMPLE + NONE`.
- `local_review`: named local behavioral change; expected route `SIMPLE + REVIEW`.
- `broad_contract`: requires discovering an unknown repository contract; expected route `STANDARD + REVIEW` and a sealed Architect work set.
- `reviewer_trap`: a local semantic change with an acceptance-critical edge case that tests artifact-first review.
- `risk_idempotency`: persistence/idempotency semantics; expected assurance `RISK`.

The first paid runtime screen should be intentionally small. Its purpose is to prove that both model variants can execute Main, Architect, mutation, validation, and Reviewer paths before buying repetitions.

## Primary measurements

The primary outcome is **accepted correct change**, not token price alone. Each run should capture:

- hidden correctness gate;
- route/assurance contract;
- Architect and Reviewer counts;
- sealed-boundary replay indicators;
- mutation ownership / unexpected file changes;
- candidate exit and incomplete/truncated runs;
- elapsed time and first-output latency;
- AI-credit / token telemetry available from the Copilot runtime;
- resulting patch and final user-visible output.

Architecture experiments belong to a later phase only after the model-only result is understood.
