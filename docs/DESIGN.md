# Design notes — v0.8 Luna Council

Over the Luna is a **thin, human-guided context-isolation harness** for GitHub Copilot in VS Code.

v0.8 changes the core question from "which model should own this task?" to:

> **Where does an independent fresh Luna context buy enough evidence or adversarial thinking to justify another call?**

The automatic core is GPT-5.6 Luna only. Sonnet and Opus exist only as visible human-selected review handoffs.

## Design principles

### 1. Parallelize thinking; serialize mutation

Repository mutation has one owner: **Main Luna**.

Council agents do not compete on implementation. They contribute independent planning, repository evidence, skepticism, research, recovery diagnosis, or review.

This keeps a coherent mutable state while still allowing extra test-time compute.

### 2. Main Luna owns the work, not all of the thinking

Main Luna being the mutation owner does **not** mean every investigation and judgment should happen in Main Luna's context.

Main should keep:

- the mutable implementation trajectory;
- edits and commands;
- focused validation and fix loops;
- final synthesis and user-facing state.

Council roles should absorb read-only work when isolation has a clear benefit:

- broad repository scouting whose intermediate details do not need to remain in the implementation context;
- independent challenges that reduce anchoring;
- external/research evidence that would otherwise expand the main context;
- independent post-change verification.

A task can therefore justify a STANDARD route even when the eventual code edit is simple. **Uncertainty, context pollution, and anchoring risk are all routing signals.**

### 3. Star topology, not management chains

Good:

```text
Planner ─┐
Architect ├── Main Luna ── implementation
Skeptic ─┘
```

Bad:

```text
Main → Manager → Planner → Architect → Worker
```

All hidden agents are leaf nodes with `agents: []`. Nested delegation is intentionally not required.

### 4. Spend tokens inside isolated contexts; return compressed evidence

A council agent may inspect deeply, but its return contract is short. The main context should receive only decision-changing facts, constraints, risks, or diagnosis.

This reduces repeated context transfer and prevents the management plane from becoming the dominant workload.

The operating rule is:

> **Think widely inside the leaf; speak narrowly back to Main Luna.**

### 5. Scale compute by uncertainty and context value, not file count

Main Luna chooses a complexity budget:

- **SIMPLE** — zero subagents by default when the implementation path is local and obvious after focused inspection.
- **STANDARD** — one or at most two advisory calls when a real uncertainty exists **or** a clean-context evidence pass avoids broad scouting in Main.
- **DEEP** — at most three initial advisory calls, preferably independent and parallel.

A 10-file mechanical change can still be SIMPLE/STANDARD. A 2-file auth state-machine change can be DEEP. A simple one-line change can still be STANDARD if locating the correct pattern requires broad repository exploration.

Main Luna gets a small locality budget: inspect enough nearby context to find the likely implementation area. If that inspection turns into broad search, dependency tracing, or distant pattern comparison, use Luna Architect rather than continuously expanding the main context.

### 6. Evidence-triggered iteration

Do not repeat councils because "more thinking might help."

Use **Luna Recovery** only after concrete failure evidence exists. Recovery receives the attempted path and exact failure, then returns one bounded diagnosis/next attempt.

Maximum default recovery budget is two calls for the same bounded task.

### 7. Rubric-driven verification

One generic reviewer is not automatically safer than none, but self-review is not independent review either.

Tiny, obvious, mechanically validated changes may finish without a separate reviewer.

For normal **non-trivial** work, one Luna Reviewer gets one explicit rubric. A successful test run or Main Luna's confidence is not by itself a reason to skip the independent review.

For DEEP/high-risk work, Main Luna can run two independent reviewer instances in parallel, but each must own a distinct lens such as:

- acceptance/correctness;
- regression/compatibility;
- security/auth;
- concurrency/ordering;
- persistence/data integrity;
- migration/rollback.

### 8. Premium judgment is a human-visible decision

Automatic core agents never include Sonnet or Opus.

Main Luna can emit:

`RECOMMEND_SONNET: <specific reason>`

or:

`RECOMMEND_OPUS: <specific reason>`

The developer then chooses a visible handoff. Handoffs use `send: false`.

This also avoids relying on a Luna parent to invoke a higher-cost-tier subagent.

## Role map

### Main Luna

The main agent is simultaneously:

- the user's conversational context owner;
- complexity/context-value classifier;
- council selector;
- Work Contract synthesizer;
- repository implementer;
- test/validation owner;
- final reporter.

This removes the v0.7 `Sonnet → Luna Implementer → Sonnet` implementation context hop without turning Main Luna into the only reasoning context.

### Luna Planner

No tools. Converts the user's request into acceptance, constraints, work units, human decisions, and unknowns.

It deliberately does **not** know repository facts, so it cannot confuse guessed architecture with requirements.

### Luna Architect

Read/search only. Grounds the work in actual repository structure, patterns, dependency paths, tests, and blast radius.

Architect is the preferred pressure-release valve when repository exploration would otherwise fill Main Luna with intermediate search context.

### Luna Skeptic

Read/search only. Tries to falsify the current direction using concrete counterexamples or repository evidence.

Use it when an assumption is consequential enough that confidently following the wrong path would be expensive, not simply because a task sounds complex.

### Luna Researcher

Read/search/web only. Handles one current public-docs/API/specification question.

### Luna Tool Worker

Omits `tools` to inherit the developer's selected VS Code tools. Isolates one bounded MCP/extension-tool question or explicit external action.

### Luna Recovery

Read/search only. Exists only after failure evidence. It is a diagnosis layer, not a second implementer.

### Luna Reviewer

Read/search only. Reviews against a specific rubric. Can request external evidence with `NEEDS_EXTERNAL_VERIFICATION` and can recommend a Sonnet handoff with `RECOMMEND_SONNET`.

### Sonnet Reviewer / Opus Critical Reviewer

Visible, `disable-model-invocation: true`, non-mutating premium review profiles. They are outside the automatic Luna core.

## MCP inheritance

Main Luna and Luna Tool Worker intentionally omit `tools` so current VS Code selected-tool inheritance preserves user-configured MCP and extension tools.

Strict council/review roles explicitly declare narrow tool lists and therefore do not inherit arbitrary ambient integrations.

No `.mcp.json`, plugin `mcpServers`, credentials, or service names are bundled.

## Why no Luna Implementer subagent?

In v0.7, the parent coordinator delegated normal implementation into a fresh Luna Implementer context. That gave clean separation but also introduced another cold-start repository understanding step and another result transfer back to the parent.

v0.8 makes Main Luna the implementation owner so ordinary work stays in one execution trajectory. Extra Luna calls are reserved for independent evidence or verification rather than duplicating implementation context.

v0.8.1 clarifies that **direct implementation ownership is not a mandate for direct broad exploration**. Read-only investigation should still be isolated when doing so protects context quality.

## Why no Kimi / MAI / Haiku core roles?

v0.8 is an explicit Luna-only experiment. Model diversity is not being optimized in the automatic path.

The question being tested is whether Luna's cost profile makes **more structured test-time compute** economical enough to preserve or improve reliability without a continuously active premium coordinator.

Model diversity remains available through manual Sonnet and Opus review.

## Thinking effort

Do not encode undocumented per-agent reasoning-effort fields. Current VS Code custom-agent frontmatter does not provide a stable per-agent thinking-effort contract.

The harness controls work through observable mechanisms instead:

- task complexity/context-value modes;
- maximum initial council fan-out;
- compact output contracts;
- one mutation owner;
- broad-investigation isolation;
- evidence-triggered recovery;
- reviewer count/rubric;
- explicit stop conditions.

## Experiment success criteria

v0.8 is promising if, compared with v0.7 on comparable real tasks:

- premium-model token share drops materially;
- Main Luna + council total cost remains low;
- wall-clock time is acceptable despite extra advisory calls;
- first-pass correctness or recovery quality does not regress materially;
- broad exploration is often compressed out of Main Luna when appropriate;
- council calls frequently change a decision or catch a real issue;
- non-trivial work receives genuinely independent review;
- user-visible Sonnet/Opus handoffs are rare and justified.

A council role should be removed if it mostly returns predictable restatements that Main Luna could have produced without an isolated context.
