# Over the Luna v0.8 — Runtime Smoke Test

This checklist verifies behavior static CI cannot prove: Luna-only routing, complexity budgeting, Main-Luna execution ownership, selected-tool inheritance, recovery/review behavior, and human-visible premium escalation.

## Preflight

- Update/reinstall the plugin and confirm **v0.8.0**.
- Reload VS Code.
- Confirm GPT-5.6 Luna, Claude Sonnet 5, and Claude Opus 4.8 are available if you want to test premium handoffs.
- Confirm all custom agents load without diagnostics errors.
- Keep normal/default tool approval settings for compatibility tests.
- Have one harmless MCP/extension tool that already works in built-in Agent.

## Test 1 — SIMPLE stays direct

Ask for a tiny clear repository change with an obvious existing pattern.

Expected:

`Mode: SIMPLE — direct Luna`

Check:

- Main Luna reads/edits/validates directly;
- no Planner/Architect/Skeptic/Recovery call occurs;
- no separate Luna Reviewer unless the task is non-trivial or you explicitly ask;
- no Sonnet/Opus call occurs.

**Fail** if the harness creates a council for every trivial edit.

## Test 2 — STANDARD uses only necessary advice

Use a bounded change with one real uncertainty, for example a feature where the relevant repository pattern is unclear.

Expected example:

`Mode: STANDARD — Luna Architect`

Check:

- one or at most two advisory calls;
- advisory output is compact;
- Main Luna, not a subagent, owns edits/tests;
- the selected advisory role materially answers the uncertainty.

## Test 3 — DEEP council is shallow and parallel

Choose a task with ambiguous acceptance criteria plus meaningful repository/risk uncertainty.

Expected example:

`Mode: DEEP — Luna Planner ∥ Luna Architect ∥ Luna Skeptic`

Check:

- at most three **initial** advisory calls;
- calls address independent questions;
- no council agent delegates another agent;
- Main Luna synthesizes a compact Work Contract;
- Main Luna owns the implementation after synthesis.

**Fail** if the route becomes Planner → Architect → Skeptic → another manager chain.

## Test 4 — File count does not force DEEP

Give a mechanical but coherent change spanning several files.

Expected:

- SIMPLE or STANDARD is allowed;
- Main Luna performs the work directly;
- the harness does not fan out merely because many files are touched.

## Test 5 — Existing MCP is preserved

First confirm a harmless read-only MCP/extension tool works in built-in Agent.

Then ask Over the Luna for the same bounded fact.

Expected:

- Main Luna may use the tool directly when it is naturally part of the task; or
- Main Luna may isolate it through Luna Tool Worker when a clean external-context hop is useful;
- no hardcoded server name is required;
- no external state changes unless explicitly requested.

**Hard gate:** native Agent works but neither Main Luna nor Luna Tool Worker can use the selected capability = fail.

## Test 6 — Strict council roles stay strict

Inspect expanded calls for Planner, Architect, Skeptic, Recovery, and Reviewer.

Expected:

- Planner: no tools;
- Architect: read/search;
- Skeptic: read/search;
- Recovery: read/search;
- Reviewer: read/search;
- none can edit/execute or use arbitrary MCP tools.

## Test 7 — Evidence-triggered Recovery

Choose a bounded task that produces a real focused validation failure, or use a disposable test case where a first implementation attempt can reasonably fail.

Expected:

1. Main Luna attempts the implementation/validation.
2. Recovery is **not** called before failure evidence exists.
3. Luna Recovery receives the exact failure plus attempted fix/context.
4. Recovery returns a bounded diagnosis/next attempt.
5. Main Luna performs the next mutation.

Check the default stop budget: no more than two Recovery calls for the same bounded task without surfacing the blocker.

## Test 8 — Normal review

Complete a non-trivial but ordinary change.

Expected:

- one Luna Reviewer call;
- Main Luna supplies an explicit rubric;
- reviewer remains read/search only;
- Main Luna handles accepted fixes itself.

## Test 9 — Deep multi-perspective review

Use a high-risk or DEEP task.

Expected:

- at most two Luna Reviewer calls in parallel;
- each gets a different rubric, for example correctness vs regression/security/data/concurrency;
- duplicate vague review prompts are a failure;
- Main Luna synthesizes findings.

## Test 10 — Sonnet is recommendation + human handoff only

Use architecture-sensitive, auth/security, concurrency, transaction, migration, data-integrity, or public-contract work where premium judgment is plausibly useful.

Expected:

- automatic core remains Luna-only;
- Luna Reviewer or Main Luna may output `RECOMMEND_SONNET: <specific reason>`;
- **Sonnet Reviewer is not automatically invoked**;
- the **Review with Sonnet** handoff button is visible;
- Sonnet runs only after you click/select the handoff.

## Test 11 — Opus is manual only

From Main Luna or Sonnet Reviewer, inspect the **Critical review with Opus** handoff.

Expected:

- Opus is never an automatic subagent;
- handoff uses a visible user action;
- Opus remains read/search/web only;
- no edit/execute/arbitrary MCP inheritance.

## Test 12 — No retired model route

Across normal runs, inspect expanded model names.

Expected automatic core models:

**GPT-5.6 Luna only.**

Kimi K2.7 Code, MAI-Code-1-Flash, Haiku, Sonnet, and Opus must not appear in automatic council/execution/review calls.

## Test 13 — Compare v0.8 economics

For comparable real tasks, record when visible:

- wall-clock time;
- Main Luna input/output tokens or credits;
- total council/recovery/reviewer tokens;
- subagent count;
- first-pass correctness;
- validation attempts;
- real findings caught by council/review;
- human interventions;
- whether a premium handoff was offered and whether using it changed the outcome.

Compare against v0.7 and native Agent + Luna on different but comparable tasks to avoid prior-context bias.

---

## Release gates

- [ ] Plugin v0.8.0 loads without customization errors.
- [ ] SIMPLE task uses Main Luna directly with zero default subagents.
- [ ] STANDARD uses no more than two justified advisory calls.
- [ ] DEEP initial council uses no more than three independent calls.
- [ ] All hidden council agents are leaf nodes.
- [ ] Main Luna owns repository mutation.
- [ ] Existing selected MCP/extension tool remains usable.
- [ ] Strict council/review roles do not inherit arbitrary ambient tools.
- [ ] Recovery is evidence-triggered and stops after two default calls if unresolved.
- [ ] Normal non-trivial review uses one rubric-driven Luna Reviewer.
- [ ] DEEP review uses at most two distinct reviewer rubrics.
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
- exact MCP/tool and native-Agent comparison if relevant;
- validation failure and Recovery inputs/outputs;
- reviewer rubrics;
- any automatic premium-model invocation;
- approximate tokens/credits and wall-clock time when visible.
