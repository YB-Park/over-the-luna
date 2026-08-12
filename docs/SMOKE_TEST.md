# Over the Luna 1.0 — Runtime Smoke Test

This checklist verifies behavior that static validation cannot prove: Luna-only automatic routing, context-isolation budgeting, Main-Luna mutation ownership, selected-tool inheritance, bounded recovery/review, and human-visible premium escalation.

## Preflight

- Install/update the plugin and confirm **v1.0.0**.
- Reload VS Code.
- Confirm GPT-5.6 Luna is available.
- Confirm Claude Sonnet 5 and Claude Opus 4.8 only if you want to test premium handoffs.
- Confirm all custom agents load without diagnostics errors.
- Keep normal/default tool approval settings for compatibility tests.
- Have one harmless MCP/extension tool that already works in built-in Agent.

## Test 1 — SIMPLE stays direct

Ask for a tiny clear repository change with an obvious nearby pattern.

Expected:

`Mode: SIMPLE — direct Luna`

Check:

- Main Luna performs focused inspection, then edits/validates directly;
- no Planner/Architect/Skeptic/Recovery call occurs;
- no separate Luna Reviewer for a truly tiny mechanically validated task unless explicitly requested;
- no Sonnet/Opus call occurs.

**Fail** if the harness creates a council for every trivial edit.

## Test 2 — Broad scouting is isolated even when the edit is simple

Ask for a mechanically simple change whose correct location or pattern is not obvious without searching across the repository.

Expected example:

`Mode: STANDARD — Luna Architect`

Check:

- Main Luna may do focused initial inspection to establish locality;
- broad search, dependency tracing, or distant pattern comparison is delegated instead of becoming a long Main-Luna scouting trail;
- Architect returns compact file/symbol evidence;
- Main Luna performs the actual edit and validation.

**Fail** if Main Luna performs broad disposable repository scouting itself merely because the eventual edit is simple.

## Test 3 — STANDARD uses only necessary advice

Use a bounded change with one real uncertainty or one clean-context evidence need.

Expected examples:

`Mode: STANDARD — Luna Architect`

or

`Mode: STANDARD — Luna Skeptic`

Check:

- one or at most two advisory calls;
- advisory output is compact;
- Main Luna owns edits/tests;
- each advisory role materially answers an uncertainty, protects Main context, or reduces anchoring risk.

## Test 4 — DEEP council is shallow and independent

Choose a task with ambiguous acceptance criteria plus meaningful repository/risk uncertainty.

Expected example:

`Mode: DEEP — Luna Planner ∥ Luna Architect ∥ Luna Skeptic`

Check:

- at most three initial advisory calls;
- calls address independent questions;
- no council agent delegates another agent;
- Main Luna synthesizes a compact Work Contract;
- Main Luna owns implementation after synthesis.

**Fail** if routing becomes a nested manager chain.

## Test 5 — File count does not force DEEP

Give a mechanical but coherent change spanning several files.

Expected:

- SIMPLE or STANDARD is allowed;
- Main Luna performs mutation directly;
- Architect may still be used if broad scouting would otherwise pollute Main context;
- the harness does not fan out merely because many files are touched.

## Test 6 — Existing MCP/extension tools are preserved

First confirm a harmless read-only MCP/extension tool works in built-in Agent. Then ask Over the Luna for the same bounded fact.

Expected:

- Main Luna may use the tool directly when it naturally belongs in the implementation context; or
- Main Luna may isolate it through Luna Tool Worker when a clean external-context hop is useful;
- no hardcoded server name is required;
- no external state changes unless explicitly requested.

**Hard gate:** built-in Agent works but neither Main Luna nor Luna Tool Worker can use the selected capability = fail.

## Test 7 — Strict council roles stay strict

Inspect expanded calls for Planner, Architect, Skeptic, Recovery, and Reviewer.

Expected:

- Planner: no tools;
- Architect: read/search;
- Skeptic: read/search;
- Recovery: read/search;
- Reviewer: read/search;
- none can edit/execute or use arbitrary MCP tools.

## Test 8 — Recovery is evidence-triggered and bounded

Choose a bounded task that produces a real focused validation failure.

Expected:

1. Main Luna attempts implementation/validation.
2. Recovery is not called before failure evidence exists.
3. Luna Recovery receives the exact failure plus attempted fix/context.
4. Recovery returns a bounded diagnosis/next attempt.
5. Main Luna performs the next mutation.
6. No more than two Recovery calls occur for the same bounded task without surfacing the blocker.

## Test 9 — Normal non-trivial review is independent

Complete a non-trivial but ordinary change whose focused validation passes.

Expected:

- one Luna Reviewer call still occurs;
- Main Luna supplies an explicit rubric;
- reviewer remains read/search only;
- Main Luna handles accepted fixes itself.

**Fail** if Main Luna skips independent review solely because tests passed or it reports high confidence.

## Test 10 — DEEP/high-risk review uses distinct rubrics

Expected:

- at most two Luna Reviewer calls;
- each gets a different rubric, for example correctness vs regression/security/data/concurrency;
- duplicate vague review prompts are a failure;
- Main Luna synthesizes findings.

## Test 11 — Sonnet is recommendation + human handoff only

Use architecture-sensitive, auth/security, concurrency, transaction, migration, data-integrity, or public-contract work where premium judgment is plausibly useful.

Expected:

- automatic core remains Luna-only;
- Luna Reviewer or Main Luna may output `RECOMMEND_SONNET: <specific reason>`;
- Sonnet Reviewer is not automatically invoked;
- the **Review with Sonnet** handoff is visible;
- Sonnet runs only after explicit user selection.

## Test 12 — Opus is manual only

Expected:

- Opus is never an automatic subagent;
- the handoff requires visible user action;
- Opus remains read/search/web only;
- no edit/execute/arbitrary MCP inheritance.

## Test 13 — Automatic model boundary

Across normal runs, inspect expanded model names.

Expected automatic core model:

**GPT-5.6 Luna only.**

Any non-Luna model appearing in automatic council/execution/review calls is a failure.

## Test 14 — Operational balance

For representative real tasks, observe when available:

- wall-clock time;
- Main Luna vs council/recovery/reviewer token or credit use;
- subagent count;
- broad scouting performed by Main vs Architect;
- first-pass correctness;
- validation attempts;
- real findings caught by council/review;
- human interventions;
- premium handoff frequency and whether it changes the outcome.

There is **no target percentage of subagent usage**. The desired outcome is that Main Luna keeps implementation continuity while broad disposable exploration and genuinely independent verification are isolated often enough to earn their overhead.

---

## Release gates

- [ ] Plugin v1.0.0 loads without customization errors.
- [ ] SIMPLE local task uses Main Luna directly with zero default subagents.
- [ ] A simple edit requiring broad repository scouting can promote to STANDARD and use Luna Architect.
- [ ] STANDARD uses no more than two justified advisory calls.
- [ ] DEEP initial council uses no more than three independent calls.
- [ ] All hidden council agents are leaf nodes.
- [ ] Main Luna remains the only automatic repository mutation owner.
- [ ] Main Luna does not monopolize broad read-only exploration when Architect can compress it.
- [ ] Existing selected MCP/extension tools remain usable.
- [ ] Strict council/review roles do not inherit arbitrary ambient tools.
- [ ] Recovery is evidence-triggered and stops after two default calls if unresolved.
- [ ] Normal non-trivial review uses one rubric-driven Luna Reviewer even after successful focused validation.
- [ ] DEEP/high-risk review uses at most two distinct reviewer rubrics.
- [ ] Automatic core model is GPT-5.6 Luna only.
- [ ] Sonnet runs only after a visible human handoff.
- [ ] Opus runs only after a visible human handoff.
- [ ] No external side effect is inferred.
- [ ] Council output remains compact enough that management traffic does not dominate the main context.

## Capture on failure

Record:

- VS Code/Copilot/plugin versions;
- mode line;
- council agents invoked and order/parallelism;
- displayed model for every call;
- direct Main Luna tool calls;
- broad repository scouting performed by Main vs Architect;
- exact MCP/tool and built-in-Agent comparison if relevant;
- validation failure and Recovery inputs/outputs;
- reviewer rubrics;
- any automatic premium-model invocation;
- approximate tokens/credits and wall-clock time when visible.
