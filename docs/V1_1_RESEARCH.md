# v1.1 research notebook

This document records hypotheses and experiments for the next Over the Luna release.
It is intentionally **not** a specification yet. Runtime behavior should change only after the
hypotheses below survive real VS Code traces and controlled Copilot experiments.

Research baseline: 2026-08-19, released v1.0.0 behavior.

## Problem statement

Real use of v1.0 exposed two gaps between the intended product and observed behavior:

1. `SIMPLE` is selected often enough that the automatic Luna Council can feel less useful than the
   economic premise suggests. The goal is not to force more agent calls; it is to find places where
   another cheap isolated Luna pass has positive expected value.
2. The visible Sonnet/Opus handoff buttons do not currently execute as intended, and the two-choice
   premium UX may be solving the wrong problem even after the runtime bug is fixed.

The research question is therefore broader than "lower the SIMPLE threshold":

> **Where should Over the Luna spend another cheap independent inference pass, and which decisions
> should remain visible to the developer?**

## Invariants that are not currently under challenge

Unless evidence strongly contradicts them:

- **Parallelize thinking; serialize mutation.**
- **Main Luna owns the work, not all of the thinking.**
- Main Luna remains the single mutable implementation owner.
- Council calls stay isolated, bounded, and compact.
- More calls are not automatically better; every extra call must buy evidence, context isolation,
  independent verification, or materially lower rework/risk.
- Premium inference is never an automatic hidden expense.
- The harness stays VS Code / GitHub Copilot native and works inside the available model/tool policy.
- No target Council-call percentage is a success metric.

## Hypothesis A — routing and assurance are different decisions

The current `SIMPLE / STANDARD / DEEP` label mixes at least two questions:

1. How much isolated investigation is useful before/during implementation?
2. How much independent assurance is useful after there is a concrete change to inspect?

That can make `SIMPLE` act as a strong "Main does everything" frame even though the later review
contract asks for a Luna Reviewer on non-trivial work.

A candidate model to test is two-dimensional:

### Investigation / execution ownership

- `DIRECT` — Main can establish locality and implement without broad disposable exploration.
- `ISOLATE` — one or two focused leaf passes protect Main context or test an important assumption.
- `DEEP` — several independent questions justify a bounded council before mutation.

### Assurance

- `NONE` — tiny, obvious, mechanically validated change.
- `REVIEW` — one fresh Luna review against a concrete rubric.
- `RISK` — distinct independent rubrics for genuinely consequential boundaries.

This makes combinations such as `DIRECT + REVIEW` first-class. A clear local change can remain
cheap and coherent during implementation while still buying a fresh independent Luna pass after the
diff and validation evidence exist.

### What would falsify this hypothesis?

- DIRECT + REVIEW produces mostly duplicate/no-op findings and meaningful latency without reducing
  rework or catching requirement/regression mistakes.
- The extra state/routing language makes Main less reliable than the current single-axis policy.
- Reviewer spend becomes a dominant share of total inference without corresponding useful findings.

## Hypothesis B — use cheap compute at evidence-rich boundaries

For clear work, a pre-implementation Planner can repeat what Main already knows. A post-change
Reviewer sees a richer artifact: request + actual diff + tests + repository state.

Candidate default bias to test:

- Do **not** add planning ceremony merely because Luna is inexpensive.
- Prefer another Luna pass when it can inspect a concrete artifact or isolate broad disposable
  evidence.
- Architect remains the primary pressure-release valve for broad repository scouting.
- Reviewer becomes the primary cheap independent-assurance pass for non-trivial completed mutation.
- Recovery remains evidence-triggered rather than speculative.

## Hypothesis C — one premium decision, not a model menu

The user-facing question should probably be:

> **Is a premium independent judgment worth it here?**

not:

> **Should I choose Sonnet or Opus?**

Two premium choices expose model-routing complexity to the developer, create plan-availability
friction, and make the UI look more complex than the core product.

Candidate v1.1 direction to test:

- expose at most one premium-review affordance;
- keep the reason for recommending premium judgment explicit;
- choose the backing model by an evidence-based product policy rather than asking the user to route
  models manually;
- keep the actual premium call human-initiated.

This does **not** yet decide whether the one slot is Sonnet, Opus, or a different interaction such as
a single visible `Premium Review` agent selected from the picker.

Current availability matters to the experiment. As of 2026-08-19, GitHub's supported-model source
lists Claude Sonnet 5 on Copilot Pro, Pro+, Max, Business, and Enterprise; Claude Opus 4.8 is not on
Copilot Pro but is available on Pro+, Max, Business, and Enterprise. A public plugin should not make
an unavailable second button part of the normal cognitive path when it can avoid doing so.

### Premium experiment rubric

Run the same completed patches through candidate premium reviewers with the same read-only evidence
and review rubric. Record:

- unique actionable findings missed by Luna Review;
- false positives / speculative must-fix findings;
- duplication of Luna findings;
- verdict usefulness to the developer;
- latency;
- AI credits / token cost;
- availability on target Copilot plans;
- number of user decisions needed to reach the review.

A premium model earns the single slot only if its incremental judgment is repeatable enough to
justify both cost and product complexity.

## Known v1.0 handoff defect

The current v1.0 frontmatter uses filename-style slugs such as `sonnet-reviewer` and
`opus-critical-reviewer` in `handoffs[].agent`, while the actual custom-agent names are `Sonnet
Reviewer` and `Opus Critical Reviewer`.

Current VS Code handoff execution resolves the target through loaded custom-agent names. It hides the
handoff widget before attempting the switch, so a failed target lookup presents exactly as "button
disappears, nothing else happens."

The research branch therefore adds a regression test that requires every handoff target to resolve
to an actual custom-agent `name`. The test is intentionally red against the v1.0 baseline before the
bug is fixed.

Do not solve this by changing premium handoffs to `send: true`. Current VS Code can automatically
execute auto-send handoffs in Autopilot, which conflicts with the invariant that premium judgment is
a human-selected expense.

## Evidence layers

### 1. Static/runtime-contract tests

Use VS Code behavior as the oracle rather than merely encoding current repository expectations.
Examples:

- handoff target resolves to an actual custom-agent name;
- premium handoffs never auto-send;
- leaf agents remain non-mutating where required;
- selected-tool inheritance contracts stay explicit.

### 2. Real VS Code traces

Use Agent Debug / OTel with content capture disabled by default. Export representative real sessions
and measure:

- route/mode selected;
- Main vs Council/reviewer model calls and token usage;
- subagent count and agent names;
- tool-call count;
- whether non-trivial mutation received independent review;
- whether broad read-only work stayed in Main or was isolated;
- failure/recovery loops;
- wall-clock duration and errors.

Raw `SIMPLE` percentage is descriptive, not a target.

### 3. Controlled Copilot probes

Use a small fixed task corpus to compare the released policy with candidate routing policies.
GitHub Actions/Copilot CLI probes are useful for plugin loading, instruction behavior, routing choices,
and token/call traces. They are **not** accepted as proof of VS Code UI semantics or selected-tool
inheritance.

Paid probes must have a small AI-credit cap and must not run on every repository push.

### 4. VS Code integration / manual runtime checks

Use actual VS Code for:

- handoff rendering and agent switching;
- prompt prefill behavior;
- model switch behavior;
- selected MCP/extension-tool inheritance;
- subagent rendering and debug-flow inspection.

Headless VS Code integration tests may validate discovery/parsing/structural behavior where practical,
but an authenticated interactive Copilot session remains the source of truth for UI-level semantics.

## Evaluation record

For each representative task, capture at least:

- task archetype and acceptance criteria;
- current route and candidate route;
- Main input/output tokens;
- Council/reviewer input/output tokens;
- number and identity of subagents;
- time to first mutation where observable;
- validation attempts;
- reviewer findings: unique / duplicate / false positive;
- recovery calls;
- human intervention;
- premium recommendation and actual premium use;
- final correctness / rework notes.

## Release gates for v1.1

Do not ship a routing redesign merely because it invokes more Luna.

A candidate must demonstrate that, across representative tasks:

- additional calls are concentrated at evidence-rich or context-isolating boundaries;
- Main remains the single coherent mutation owner;
- non-trivial work receives independent assurance more reliably than v1.0 without making trivial work
  bureaucratic;
- broad exploration is isolated when that materially protects Main context;
- reviewer findings are sufficiently actionable to justify their spend;
- recovery remains bounded and evidence-triggered;
- premium review requires one clear human decision at most;
- no premium path can silently auto-run;
- VS Code runtime behavior matches the tested contracts.

Only after these gates have evidence should this notebook be converted into the v1.1 design contract.
