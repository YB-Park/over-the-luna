# v1.1.1 Surface Economy Experiment

## Question

Can Over the Luna preserve GPT-5.6 Luna reasoning, routing, mutation ownership, validation, and review quality while materially reducing user-visible reading load?

> **Compute is cheap. Human attention is not.**

Visible communication is a separate product budget from internal reasoning.

## Working diagnosis

Observed verbosity can come from three interacting layers:

1. GPT-5.6 Luna generation behavior;
2. the VS Code/Copilot agent loop and user-visible preambles around tool use;
3. Over the Luna v1.1's own reporting contract.

Do not assume Luna alone is the cause. A useful change should compress the product-controlled surface without weakening the v1.1 execution contract.

## External guidance used

- OpenAI GPT-5.6 guidance treats reasoning effort and response verbosity as separate controls and recommends representative evals rather than assuming one setting is universally best.
- OpenAI's current GPT-5.6 prompting guidance recommends leaner prompts, stating each instruction once, and measuring prompt simplification against evals.
- Broad `be concise` instructions can make output too brief; task-specific requirements should identify what a short answer must preserve.
- VS Code exposes model thinking effort independently, so this experiment does not lower reasoning effort merely to reduce visible text.
- LLM judges can favor superficial verbosity, so winner selection must not rely primarily on a prose-quality judge.

## Phase 1 variants

- **control** — exact v1.1.0 Main prompt.
- **naive** — broad `be concise` instruction; intentionally weak baseline.
- **semantic** — preserve decision-relevant information and omit routine process narration.
- **economy** — semantic compression plus progressive disclosure and suppression of routine progress narration.

No variant changes routing, tool ownership, Council membership, Reviewer protocol, or Premium Review.

## Phase 1 cases

- **tiny** — SIMPLE + NONE mechanical edit.
- **broad** — STANDARD + REVIEW with mandatory Architect discovery and exactly one Reviewer.
- **detail** — explicit user request for a detailed read-only explanation; compression must yield to requested detail.

RISK is deferred until a candidate survives screening.

## Measurements

### Hard gates

- fixture hidden contract passes;
- expected route/assurance remains intact where deterministic;
- tiny does not acquire unnecessary Architect/Reviewer calls;
- broad still uses exactly one Architect and one Reviewer;
- no execution contract is relaxed merely to save words.

### Surface metrics

- top-level visible assistant-message count;
- visible character count (more language-robust than English word count);
- final-answer character count;
- visible line count;
- required boundary-marker count.

### Reasoning/compute metrics

- OTel chat input/output tokens;
- OTel reasoning tokens when exposed by the runtime;
- Architect/Reviewer invocation counts.

## Selection rule

A candidate is eligible only if all hard gates pass.

Among eligible candidates, prefer the smallest visible surface that:

- does not materially reduce reasoning work on the broad task;
- still expands when the user explicitly asks for detail;
- keeps failures, actionable findings, unresolved risk, and human decisions visible.

Correctness and trajectory gates come before human preference. For UX, compare anonymized outputs with actual users rather than trusting an LLM judge that may reward verbosity.

## Phase 2

Run the top one or two candidates plus control on:

- the **risk** concurrency/idempotency fixture;
- repeated **broad** runs for stability;
- Korean real-VS-Code tasks;
- one concrete failure -> Recovery trajectory.

If the winner is only a Main communication/reporting adjustment, ship as **v1.1.1**. If the evidence requires a new adaptive communication-budget architecture across Main and leaf contracts, reconsider **v1.2.0**.
