# Design notes — v1.1

Over the Luna is a **thin, human-guided context-isolation harness** for GitHub Copilot in VS Code.

The automatic core uses **GPT-5.6 Luna only**. Claude Sonnet 5 exists outside that automatic core as the backing model for one visible, human-selected **Premium Review**.

## Product invariants

1. **Parallelize thinking; serialize mutation.** Main Luna is the only automatic repository mutation owner.
2. **Main owns the work, not all of the thinking.** Leaf calls must buy independent evidence, context isolation, verification, or materially lower rework/risk.
3. **Investigation and assurance are separate decisions.** Routing uses SIMPLE / STANDARD / DEEP plus NONE / REVIEW / RISK.
4. **Broad unknown semantic discovery belongs in Architect.** Main gets only bounded local orientation before STANDARD becomes mandatory.
5. **A sufficient Architect packet seals discovery.** `MUTATION_TARGETS` is the complete post-handback work set; Main does not replay broad discovery before mutation.
6. **Normal semantic review is artifact-first and bounded.** REVIEW means exactly one named Luna Reviewer trajectory after focused validation; RISK requires at least one post-change named Reviewer.
7. **Premium is one human decision.** Premium Review uses Claude Sonnet 5, is never automatic, and keeps `send: false`.
8. **VS Code owns ambient tools.** Main and Luna Tool Worker omit fixed `tools`; strict leaves keep narrow explicit tool lists.
9. **All leaves are non-recursive.** Council and review agents use `agents: []`.
10. **External side effects are never inferred.** Tool visibility does not authorize remote mutation.

## Routing model

### Investigation

**SIMPLE** is for a known local implementation neighborhood. Main may use direct user-named paths or a very small exact-symbol/literal orientation budget. If that budget is insufficient or an unknown repository contract must be discovered, stop and choose STANDARD.

**STANDARD** delegates the broad evidence pass to Luna Architect. Architect returns:

- `DECISION`
- `EVIDENCE`
- `RELATIONSHIPS`
- `MUTATION_TARGETS`
- `UNRESOLVED`

A sufficient packet causes Main to print `Boundary sealed — work set: ...`. Until mutation begins, Main stays inside that work set and does not perform broad repository rehydration.

**DEEP** is reserved for several independent uncertainties or cross-cutting risks. At most three initial advisory calls are used, with distinct questions.

### Assurance

**NONE** is only for genuinely mechanical, locally bounded work with a direct validation assertion and no semantic invariant to infer.

**REVIEW** is the default for semantic changes. After focused validation, Main captures the current unified diff and invokes **Luna Reviewer exactly once** for the normal trajectory. Main adjudicates findings and may repair/revalidate without recursive review.

**RISK** covers consequential auth/security, concurrency/idempotency, transactions, migrations, persistence/data integrity, rollback, or important public contracts. At least one named post-change Luna Reviewer is mandatory. A second Reviewer is allowed only for one explicitly named residual risk with a distinct rubric.

## Runtime roles

- **Over the Luna / Main Luna** — conversational context, routing, mutation, commands, tests, synthesis, Reviewer adjudication, final report.
- **Luna Planner** — acceptance criteria and constraints; no tools.
- **Luna Architect** — read/search repository evidence and sealed work set.
- **Luna Skeptic** — read/search challenge of one consequential assumption.
- **Luna Researcher** — read/search/web for one current public-docs/API/specification question.
- **Luna Tool Worker** — bounded use of developer-selected MCP/extension tools; no repository mutation ownership.
- **Luna Recovery** — read/search diagnosis after concrete failure evidence.
- **Luna Reviewer** — read/search artifact-first review with bounded dependency closure and one invariant challenge.
- **Premium Review** — visible, human-invoked Claude Sonnet 5 second opinion; read/search only, no delegation.

Only **Over the Luna** and **Premium Review** are intended to be user-visible.

## Tool inheritance

Main intentionally omits both `tools` and `agents` in frontmatter. Omitting `tools` preserves the developer's VS Code-owned selected built-in/MCP/extension environment. Omitting `agents` avoids coupling ambient tool behavior to an explicit Main tool list; the exact seven Council names are sealed in instructions instead.

Luna Tool Worker also omits `tools` so a bounded selected integration can remain VS Code-owned. Planner/Architect/Skeptic/Researcher/Recovery/Reviewer/Premium Review declare explicit narrow tool sets and therefore do not inherit arbitrary mutation-capable integrations.

The plugin does not bundle `.mcp.json`, `mcpServers`, credentials, OAuth, or service-specific configuration.

## Premium boundary

Premium inference never runs automatically. The one visible handoff targets exact custom agent **Premium Review**, pins Claude Sonnet 5 when available, and uses `send: false` so the developer decides whether the premium request is sent.

The handoff and Premium Review agent preserve the user's current natural language. Stable verdict labels and code/path/command literals remain unchanged for machine readability.

If the backing model is unavailable, surface that fact rather than silently claiming the requested premium judgment occurred.

## External side effects

External reads may be inferred when clearly necessary for the requested outcome. External mutation is never inferred. Updating tickets, sending messages, pushing, deploying, creating PRs, changing databases, or modifying cloud resources requires an explicit request for that effect.

## Success criteria

The architecture is healthy when Main keeps implementation continuity, broad disposable discovery is isolated rather than replayed, semantic changes receive bounded artifact-first review, selected developer tools remain available through intended ambient roles, strict leaves stay least-privilege, premium use remains rare and human-selected, and organization/enterprise Copilot boundaries remain intact.
