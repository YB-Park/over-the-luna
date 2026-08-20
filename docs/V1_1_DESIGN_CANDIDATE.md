# Over the Luna v1.1 design candidate

Status: **automated Luna core = PRE-PRODUCTION RC2; real VS Code + premium UX gates still open**  
Updated: **2026-08-20**

This is the evidence-backed v1.1 design candidate. It is not yet the released product contract.

## v1.0 -> v1.1 objective

v1.1 is not an attempt to maximize Council calls or independent reviews.

The product objective is:

> **Use cheap GPT-5.6 Luna inference only where it buys context isolation or independent evidence, while preserving one Main mutation owner, direct ergonomics for genuinely local work, and explicit human control over premium spend.**

Operationally:

- parallelize thinking; serialize mutation;
- Main Luna owns repository mutation and mutable implementation state;
- tiny mechanical work must remain cheap;
- local semantic work stays direct when locality and the contract are already concrete;
- broad disposable semantic discovery is isolated before it pollutes Main context;
- normal non-trivial mutation gets one bounded fresh Luna Reviewer at the evidence-rich end;
- consequential RISK always gets final artifact assurance;
- premium models never run automatically.

## Canonical automated-core RC2

Use these files for the current automated-core candidate:

- Main: `experiments/v1_1_candidate_rc2.agent.md`
- Architect: `experiments/v1_1_candidate_architect_packet_v3.agent.md`
- Reviewer: `experiments/v1_1_candidate_reviewer_rc.agent.md`

Supporting release-gate infrastructure:

- fixtures/oracles: `experiments/v1_1_release_gate_fixture.py`
- base policy evaluator: `experiments/v1_1_release_gate_evaluator_v6.py`
- RC2 discipline evaluator: `experiments/v1_1_release_gate_evaluator_rc2.py`
- parser/contract tests under `tests/test_v1_1_*`

Detailed final evidence:

- `experiments/PREPRODUCTION_RC2_RESULTS_2026-08-20.md`

## Route representation

Keep the existing investigation vocabulary and separate assurance from it:

- Investigation: `SIMPLE | STANDARD | DEEP`
- Assurance: `NONE | REVIEW | RISK`

The route is printed as:

`Mode: <SIMPLE|STANDARD|DEEP> — <short route> | Assurance: <NONE|REVIEW|RISK>`

Examples:

- `SIMPLE + NONE` — exact mechanical change;
- `SIMPLE + REVIEW` — local semantic mutation;
- `STANDARD + REVIEW` — unknown semantic discovery isolated to Architect;
- `SIMPLE/DEEP + RISK` — consequential assurance independent of investigation depth.

## Bounded local orientation

SIMPLE does not mean Main can explore indefinitely.

Before routing, Main may locate an already-specified local behavior using a small budget:

- direct user-named file reads; or
- at most three narrow exact `rg` locators;
- at most three semantic source/test files before mutation;
- at most one tooling/build metadata file only when validation cannot otherwise be inferred;
- one visible adjacent helper may be followed inside the semantic-file budget;
- no `glob` during SIMPLE orientation;
- no README/docs/changelog/background-prose browsing unless the task targets those files;
- no recursive inventory, `find`, `tree`, `git ls-files`, `git grep`, recursive grep, or wildcard-only discovery.

This budget answers only:

> Where is this already-specified local thing and its immediate contract?

If the budget is insufficient, or correctness requires discovering/tracing an unknown repository contract, pattern, consumer, or dependency, Main stops and chooses STANDARD.

This distinction is a core v1.1 result:

> **bounded locator orientation is not semantic discovery.**

Earlier candidates that treated all location finding as broad discovery over-routed tiny/local work and damaged ergonomics.

## STANDARD — Architect owns unknown semantic discovery

When the task requires broad disposable evidence, Main invokes Luna Architect before consuming that evidence itself.

Architect returns exactly:

- `DECISION`
- `EVIDENCE`
- `RELATIONSHIPS`
- `MUTATION_TARGETS`
- `UNRESOLVED`

`MUTATION_TARGETS` is the complete post-handback work set, not merely files expected to change. It includes:

- implementation files;
- focused tests;
- unchanged acceptance-critical helper/contract definitions Main must inspect locally.

### Sealed handback

After a sufficient packet, Main emits:

`Boundary sealed — work set: <exact concrete paths>`

Then, before mutation:

- first repository action is a concrete read inside the work set;
- all Main reads remain inside the work set;
- no repository inventory/search replay via read, search, shell, or VCS commands;
- focused validation/build commands, `git status`, and current-patch `git diff` remain allowed;
- one genuinely missing broad fact requires an explicit `Boundary reopen: <fact>` and one focused Architect follow-up rather than silent Main rehydration.

The final broad RC2 fixture reproduced this shape 2/2.

## Assurance

### NONE

Use only when the mutation is fully specified, mechanical, mechanically validated, and carries no semantic/control-flow/validation/identity/data-shape/security/concurrency/persistence/public-contract inference.

NONE means no Reviewer call.

The final tiny RC2 fixture reproduced `SIMPLE + NONE`, Architect 0, Reviewer 0, hidden PASS **2/2**.

### REVIEW

Normal non-trivial mutation buys **exactly one named Luna Reviewer task call total**.

Before the call Main:

1. runs focused validation;
2. captures the current unified diff;
3. puts the concrete artifact between `BEGIN_UNIFIED_DIFF` and `END_UNIFIED_DIFF`;
4. preflights that the artifact contains `diff --git`, `@@`, and every changed path;
5. includes acceptance criteria, changed paths, validation outcomes, and one narrow rubric.

Hard normal-review budget:

- no artifact-format retry;
- no retry after `VERIFY`;
- no re-review after accepted repair;
- no substitution with a generic/built-in code-review agent.

If the single Reviewer returns `VERIFY`, Main reports that unresolved fact instead of buying another pass.

The Reviewer itself:

- starts from the concrete artifact;
- closes only acceptance-critical unchanged dependencies;
- challenges one consequential invariant before PASS;
- reads at most four concrete files / eight read-search calls;
- never inspects `.git`/history/background prose;
- returns at most three material findings.

### RISK

RISK covers consequential auth/security, concurrency/idempotency, transaction, migration, persistence/data-integrity, rollback, and important public-contract boundaries.

Pre-change Architect/Skeptic calls may help, but they do not substitute for final assurance.

After the final meaningful patch and validation, at least one **post-change named Luna Reviewer** is mandatory.

Default budget is one. A second pass is allowed only if Main first names one distinct residual consequential risk with a genuinely different rubric that the first Reviewer and tests could not close.

The final risk RC2 fixture passed 2/2 with exactly one post-change named Reviewer in both runs.

## Automated-core release evidence

Final RC2 matrix: **8 / 8 PASS**.

| Boundary | Repetitions | Expected shape | Result |
| --- | ---: | --- | --- |
| tiny | 2 | `SIMPLE + NONE`, no leaves | 2/2 PASS |
| local | 2 | `SIMPLE + REVIEW`, Reviewer 1 | 2/2 PASS |
| broad | 2 | `STANDARD + Architect + REVIEW`, sealed work set | 2/2 PASS |
| risk | 2 | `RISK`, post-change named Reviewer >= 1 | 2/2 PASS |

Every run also passed its hidden behavioral oracle and automatic-premium count was zero.

The significance is not merely 8/8 correctness. Earlier hidden-PASS trajectories were intentionally failed when they violated cost/context discipline, including:

- unnecessary Reviewer on tiny work;
- generic root globs;
- README/tooling over-scouting on local work;
- shell/VCS broad rehydration after Architect;
- repeated normal Reviewer calls;
- RISK that skipped final Reviewer;
- RISK that substituted built-in `code-review`.

RC2 is the first candidate to close all four boundaries together in the controlled CLI matrix.

## Main tool wiring — unresolved real VS Code blocker

The automated CLI core deliberately kept Main's `tools` field omitted so experiments could preserve the ambient tool set and configured MCP/extension tools.

This assumption is **not yet product-safe**.

Current VS Code documentation states that when a custom agent specifies an `agents` allowlist, the `agent` / `agent/runSubagent` capability must be enabled/included. At the same time, explicitly specifying a custom-agent `tools` list defines the tools available to that agent, which can conflict with the v1.1 goal of preserving the developer's selected arbitrary MCP/extension tools.

Therefore productization requires a real VS Code Gate A comparison before changing the released `agents/` files.

Two wiring candidates must be tested interactively:

### Wiring A — schema-strict subagent allowlist

- keep explicit `agents: [...]`;
- explicitly include `agent` in Main's tool configuration;
- confirm what built-in/MCP/extension tools remain available and whether developer selections can still be preserved without hardcoding integrations.

Strength: structural subagent allowlist.

Risk: fixed custom-agent tools may replace/narrow ambient developer-selected tools.

### Wiring B — ambient-tool preservation

- omit Main `tools`;
- remove the frontmatter `agents` allowlist if required by VS Code semantics;
- enforce the allowed Luna leaf names in Main instructions;
- confirm `agent/runSubagent` remains available from the user's tool selection and no unintended agents are selected.

Strength: preserves ambient tool configuration.

Risk: leaf allowlist becomes behavioral rather than frontmatter-enforced.

Do not choose between A/B from CLI behavior alone.

## Premium UX remains a separate product decision

Normal Luna assurance is now stable enough that premium review can be evaluated incrementally instead of compensating for a missing base reviewer.

Open question:

> Keep separate Sonnet/Opus handoffs, or expose one human `Premium Review` decision?

Requirements that are already fixed:

- premium never auto-runs;
- `send: false` remains the baseline;
- developer explicitly authorizes the extra judgment/spend;
- evaluate unique actionable findings, false positives, latency, plan/model availability, and user decision count.

## Productization gate

Do not port RC2 into released `agents/` or bump to `1.1.0` until:

1. **Gate A — real VS Code** closes Main tool/subagent wiring, actual plugin loading, Agent Debug/OTel shape, leaf restrictions, and handoffs;
2. **Gate B — premium UX** makes the one-vs-two premium affordance decision;
3. then port the accepted RC2 contract into product agents, update tests/docs/smoke coverage, and perform the version/changelog/release work.

Current status:

- automated Luna core: **PRE-PRODUCTION RC2 — stable**;
- real VS Code runtime: **PENDING**;
- premium UX: **PENDING**;
- v1.1 release: **NOT READY YET**.
