# Design notes

Over the Luna is a **thin, human-guided context-isolation harness** for GitHub Copilot in VS Code.

The automatic core uses GPT-5.6 Luna only. Claude Sonnet 5 and Claude Opus 4.8 exist outside that automatic core as visible, user-selected review handoffs.

The central design question is:

> **Where does a fresh Luna context buy enough independent evidence, context isolation, or adversarial thinking to justify another call?**

## Goals

- Keep one coherent mutable implementation trajectory.
- Spend cheap Luna inference on independent evidence when it can improve quality or protect context.
- Keep context hops short and outputs compact.
- Make premium-model use visible and human-selected.
- Preserve the developer's existing VS Code tool ecosystem instead of replacing it.

## Non-goals

- Parallel agents competing to edit the same repository state.
- Deep manager hierarchies or recursive delegation chains.
- Hidden premium escalation.
- Bundled MCP servers, credentials, trust policy, or a second editor UI.
- Maximizing agent count for its own sake.

## Core principles

### 1. Parallelize thinking; serialize mutation

Repository mutation has one owner: **Main Luna**.

Council agents do not compete on implementation. They contribute independent planning, repository evidence, skepticism, research, recovery diagnosis, or review.

### 2. Main Luna owns the work, not all of the thinking

Main Luna keeps:

- the mutable implementation trajectory;
- edits and commands;
- focused validation and fix loops;
- final synthesis and user-facing state.

Council roles absorb read-only work when isolation has a clear benefit:

- broad repository scouting whose intermediate details do not need to remain in the implementation context;
- independent challenges that reduce anchoring;
- public/private external evidence that would otherwise expand the main context;
- failure diagnosis after concrete evidence exists;
- independent post-change verification.

A task can justify a STANDARD route even when the eventual edit is simple. **Uncertainty, context pollution, and anchoring risk are all routing signals.**

### 3. Star topology, not management chains

Good:

```text
Planner ─┐
Architect ├── Main Luna ── implementation
Skeptic ─┘
```

Avoid:

```text
Main → Manager → Planner → Architect → Worker
```

All hidden council/review agents are leaf nodes with `agents: []`.

### 4. Think widely inside the leaf; speak narrowly back

A council agent may inspect deeply, but its result should contain only decision-changing facts, constraints, risks, or diagnosis.

This prevents management traffic from becoming the dominant workload and keeps Main Luna's context focused on the mutable implementation state.

### 5. Scale compute by uncertainty and context value, not file count

Main Luna chooses a bounded mode:

- **SIMPLE** — zero subagents by default when the path is clear and local after focused inspection.
- **STANDARD** — one or at most two advisory calls when a real uncertainty exists or isolation prevents unnecessary context growth.
- **DEEP** — at most three initial advisory calls for several independent questions or meaningful cross-cutting risk.

A multi-file mechanical change can still be SIMPLE. A two-file concurrency change can be DEEP. A one-line edit can still be STANDARD when finding the correct pattern requires broad repository exploration.

Main Luna gets a small locality budget. If focused inspection turns into broad search, dependency tracing, or distant pattern comparison, prefer Luna Architect rather than continuously expanding the main context.

### 6. Evidence-triggered iteration

Do not repeat councils because more thinking might help.

Use **Luna Recovery** only after concrete failure evidence exists. Recovery receives the attempted path and exact failure, then returns one bounded diagnosis and next attempt.

Maximum default recovery budget: two Recovery calls for the same bounded task.

### 7. Rubric-driven verification

Tiny, obvious, mechanically validated changes may finish without a separate reviewer.

For normal **non-trivial** work, one Luna Reviewer receives one explicit rubric. Passing tests or Main Luna confidence is not by itself a reason to skip independent review.

For DEEP/high-risk work, Main Luna may run two independent reviewers in parallel only when their rubrics are distinct, for example:

- acceptance/correctness;
- regression/compatibility;
- security/auth;
- concurrency/ordering;
- persistence/data integrity;
- migration/rollback.

### 8. Premium judgment is a human-visible decision

Automatic core agents never include Sonnet or Opus.

Main Luna or Luna Reviewer can emit:

`RECOMMEND_SONNET: <specific reason>`

or:

`RECOMMEND_OPUS: <specific reason>`

The developer then chooses a visible handoff. Premium handoffs use `send: false`.

## Runtime roles

### Main Luna

Main Luna is simultaneously:

- the user's conversational context owner;
- locality/uncertainty/risk classifier;
- council selector;
- Work Contract synthesizer;
- repository implementer;
- test/validation owner;
- final reporter.

It owns implementation directly so normal work stays in one mutable execution trajectory.

### Luna Planner

No tools. Converts one bounded request into acceptance criteria, constraints, work units, human decisions, and unknowns. It deliberately does not inspect repository facts.

### Luna Architect

Read/search only. Grounds the work in repository structure, dependency paths, existing patterns, tests, and blast radius. It is the preferred pressure-release valve when broad scouting would otherwise fill Main Luna with disposable search context.

### Luna Skeptic

Read/search only. Tries to falsify consequential assumptions using concrete counterexamples or repository evidence.

### Luna Researcher

Read/search/web only. Handles one current public-docs/API/specification question.

### Luna Tool Worker

Omits `tools` to inherit the developer's selected VS Code tools. Isolates one bounded MCP/extension-tool question or explicit external action.

### Luna Recovery

Read/search only. Exists only after failure evidence and provides diagnosis, not a second implementation trajectory.

### Luna Reviewer

Read/search only. Reviews against a specific rubric. It can request external evidence with `NEEDS_EXTERNAL_VERIFICATION` and recommend a manual Sonnet handoff with `RECOMMEND_SONNET`.

### Sonnet Reviewer / Opus Critical Reviewer

Visible, `disable-model-invocation: true`, non-mutating premium review profiles outside the automatic Luna core.

## Tool inheritance

Main Luna and Luna Tool Worker intentionally omit `tools` so the current VS Code selected-tool environment can flow through the native inheritance path.

Strict council/review roles explicitly declare narrow tool lists and therefore do not inherit arbitrary ambient integrations.

The plugin does not bundle `.mcp.json`, `mcpServers`, credentials, or service-specific configuration.

## External side effects

Tool visibility is not authorization.

External reads may be inferred when clearly necessary for the requested outcome. External mutation is never inferred. Updating tickets, sending messages, pushing, deploying, creating PRs, changing databases, or modifying cloud resources requires an explicit request for that effect.

## Thinking effort

Do not encode undocumented per-agent reasoning-effort fields. The harness controls work through observable mechanisms instead:

- task mode and context-isolation triggers;
- maximum initial council fan-out;
- compact output contracts;
- one mutation owner;
- evidence-triggered recovery;
- reviewer count/rubric;
- explicit stop conditions;
- human premium gates.

## Operational success criteria

The architecture is healthy when:

- Main Luna preserves implementation continuity without monopolizing broad read-only exploration;
- council calls frequently change a decision, compress useful evidence, diagnose a real failure, or catch a real issue;
- council outputs stay compact enough that management traffic does not dominate Main context;
- non-trivial work gets genuinely independent review;
- recovery loops remain bounded;
- premium handoffs are rare, specific, and human-selected;
- existing user-selected MCP/extension tools remain usable through the intended roles.

A council role should be removed or merged if it mostly returns predictable restatements that Main Luna could have produced just as efficiently in the same context.
