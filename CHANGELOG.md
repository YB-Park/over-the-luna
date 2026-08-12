# Changelog

All notable changes to **Over the Luna** are documented here.

The project follows [Semantic Versioning](https://semver.org/).

## v0.8.0 — 2026-08-12

Luna Council experiment: remove the always-on premium coordinator and use GPT-5.6 Luna as both the main working agent and the automatic orchestration core.

### Added

- Added **Luna Planner** for tool-free acceptance criteria and work-contract decomposition.
- Added **Luna Architect** for independent read-only repository structure, dependency, pattern, and impact evidence.
- Added **Luna Skeptic** for evidence-backed assumption challenges and edge-case falsification.
- Added **Luna Recovery** for failure-anchored diagnosis after concrete validation/implementation failures.
- Added explicit `SIMPLE`, `STANDARD`, and `DEEP` compute budgets.
- Added compact-output contracts for every council/evidence/review leaf.
- Added manual **Review with Sonnet** and **Critical review with Opus** handoffs from Main Luna.

### Changed

- **Over the Luna now runs on GPT-5.6 Luna** and performs repository implementation directly instead of acting as a Sonnet-only router.
- Automatic routing is now **Luna-only**. Sonnet and Opus are outside the automatic subagent allow-list.
- Main Luna owns repository edits, commands, tests, validation loops, and final synthesis.
- Council workers are a shallow star topology: all are `agents: []`; nested management chains are not part of the core design.
- STANDARD uses at most two advisory calls; DEEP uses at most three initial independent advisory calls.
- Recovery is evidence-triggered and defaults to at most two Recovery calls per bounded task.
- Normal review uses one rubric-driven Luna Reviewer; DEEP/high-risk review can use at most two independent reviewers with distinct rubrics.
- Luna Researcher, Tool Worker, and Reviewer now pin GPT-5.6 Luna with no automatic non-Luna fallback.
- Sonnet Reviewer is now user-visible, manual-only, non-mutating, and may only suggest a manual Opus handoff.
- Opus Critical Reviewer now pins Opus directly with no Sonnet fallback.
- Selected-tool inheritance remains unchanged for Main Luna and Luna Tool Worker so user MCP/extension tools stay available.

### Removed

- Removed **Luna Implementer** because Main Luna now owns execution directly.
- Removed **Luna Explorer**; its repository-shape role is absorbed by Luna Architect.
- Removed **Kimi Deep Worker** from the v0.8 Luna-only experiment.
- Removed MAI/Haiku/Kimi fallback paths from the automatic core.

### Why

v0.8 tests a different use of Luna's low token cost: spend extra Luna inference on **independent planning, evidence, skepticism, recovery, and verification**, while avoiding duplicated implementation contexts and an always-on premium coordinator.

The design rule is:

**Parallelize thinking; serialize mutation.**

Premium model judgment remains available, but only through visible human-selected handoffs.

## v0.7.0 — 2026-08-11

Luna-first routing simplification after re-evaluating whether MAI and Kimi dedicated routes still justified their complexity and cost.

### Removed

- Removed the dedicated **MAI Mechanical** agent and its coordinator route.
- Reduced the distributed architecture from 10 agents to **9 agents**.

### Changed

- **Luna Implementer** now owns ordinary features, deterministic repetition, boilerplate/test replication, mechanical edits, and coherent multi-file implementation by default.
- **MAI-Code-1-Flash** remains only as Luna Implementer's availability fallback. This preserves resilience without maintaining a redundant routing role.
- **Kimi Deep Worker** is now **escalation-only**. Sonnet may invoke it only when the developer explicitly requests Kimi or Luna Implementer returns `ESCALATE_KIMI: <specific reason>`.
- Multi-file scope, task length, repetition, unfamiliarity, or expected validation cycles are no longer sufficient reasons to select Kimi initially.
- Luna Implementer now defines a concrete Kimi escalation contract for non-converging validation/fix loops or implementation-continuity problems.
- Kimi Deep Worker now targets **Kimi K2.7 Code** directly instead of carrying a Luna fallback list, keeping the escalation route semantically distinct.
- Static validation now forbids reintroducing MAI Mechanical, requires Luna primary + MAI fallback on Luna Implementer, and enforces the Kimi escalation contract.
- Smoke tests now verify that mechanical and multi-file work start with Luna, while Kimi remains available through explicit/natural escalation.

### Why

Over the Luna should not manufacture jobs for every model in the organization's catalog. A specialist routing branch must demonstrate a measurable advantage over Luna in correctness, wall-clock time, total tokens/credits, context continuity, or capability isolation.

The current Luna cost/capability profile makes the dedicated MAI mechanical route especially hard to justify, while the original Kimi long-task specialization remains a hypothesis rather than a proven default advantage. v0.7 therefore keeps model diversity only where it has a clear purpose: **Kimi as observable escalation, MAI as availability fallback, Sonnet/Opus as judgment layers.**

## v0.6.0 — 2026-08-11

VS Code runtime compatibility correction after the v0.5 MCP hard gate failed in a real environment.

### Fixed

- Removed `tools: ['*']` from Luna Tool Worker, Luna Implementer, MAI Mechanical, and Kimi Deep Worker. Current VS Code named-custom-subagent runtime resolves explicit tool lists against registered tool/tool-set names and did not provide the global wildcard behavior v0.5 assumed.
- Removed the explicit `tools` list from **Over the Luna** as well. Current VS Code uses the active selected-tool state when a main custom agent omits `tools`, and named custom subagents that also omit `tools` inherit the parent invocation's selected-tool map.
- Arbitrary user MCP/extension compatibility now follows that native inheritance path instead of relying on a cross-product `*` assumption.
- Static validation now rejects global `tools: ['*']`, requires coordinator/ambient roles to omit `tools`, and keeps strict roles on exact explicit allow-lists.

### Changed

- The Sonnet coordinator is no longer capability-limited to `agent + todo` at frontmatter level. It technically sees the active selected-tool surface so that unknown user MCP/extension tools can flow into ambient children.
- Router-only Sonnet is now an explicit behavioral contract: healthy runs allow only delegation and optional todo/task coordination directly from Sonnet. Any direct repository/web/MCP/extension/environment call is a `HARNESS_VIOLATION`.
- Strict roles remain capability-limited: Explorer, Researcher, Luna Reviewer, Sonnet Reviewer, and Opus Critical Reviewer keep their explicit tool lists.
- MCP docs and smoke tests now distinguish server-running/config-discovered state from actual subagent tool selection.
- Added release gates for user-disabled tool preservation and zero direct Sonnet environment-tool calls.

### Why

The real failure was informative: **Luna Tool Worker was routed correctly and could see that MCP configuration existed, but could not call the MCP even though the server was running.**

A source-level review of current VS Code showed that v0.5 conflated GitHub's cross-product custom-agent tool semantics with the VS Code implementation. The native VS Code inheritance path is based on omitting `tools`, not a generic `*` entry.

There is also a real current platform tradeoff: static `.agent.md` configuration cannot simultaneously hard-limit the parent to `agent + todo` and automatically pass every unknown current/future user MCP tool to children. v0.6 chooses user tool compatibility and makes the coordinator limitation observable/tested rather than pretending both guarantees exist.

Preview agent-scoped hooks could harden this further, but they are not a core dependency because preview hook support/settings can be disabled by the user or organization.

## v0.5.0 — 2026-08-11

Attempted ambient-tool compatibility release. **Superseded by v0.6.0 before close-beta distribution.**

### Added

- Added **Luna Tool Worker** as a hidden Luna-first bridge for user-configured MCP/extension context, external verification, and explicitly requested external actions.
- Added `docs/MCP.md`, MCP runtime smoke tests, `AMBIENT_TOOL_UNAVAILABLE`, external-side-effect rules, prompt-injection handling, and `NEEDS_EXTERNAL_VERIFICATION` review behavior.

### Incorrect assumption corrected in v0.6

v0.5 configured ambient workers with `tools: ['*']` based on the cross-product GitHub custom-agent reference. A real VS Code test showed that the MCP remained unavailable inside the named custom subagent. v0.6 replaces that mechanism with actual VS Code selected-tool inheritance.

## v0.4.0 — 2026-08-11

Close-beta simplification: the plugin owns only behavior unique to the harness.

- Removed the user-facing **Luna Solo** wrapper; direct Luna coding uses native Agent + model picker.
- Harness failures point to native **Agent + GPT-5.6 Luna** for manual direct recovery.
- Updated validation to prevent reintroducing the redundant direct-mode wrapper.

## v0.3.0 — 2026-08-11

Pre-production hardening against the then-current VS Code/GitHub custom-agent and subagent behavior.

- Restored Sonnet as a router/synthesizer after v0.2.1's broad direct-execution fallback.
- Fixed coordinator model to Claude Sonnet 5.
- Added `disable-model-invocation: true` to user-facing entry/handoff agents.
- Made review agents non-mutating.
- Added `target: vscode` to all agents.
- Added visible `HARNESS_FAILURE` behavior.
- Added static validator, GitHub Actions, and runtime smoke tests.

## v0.2.1 — 2026-08-11

Interim hotfix made during live investigation.

- Temporarily restored broad repository tools to Sonnet after parent editor tools appeared disabled.
- Later superseded when parent and named-subagent tool surfaces were distinguished more carefully.

## v0.2.0 — 2026-08-11

First routing-focused revision based on live VS Code testing.

- Small implementation → Luna Implementer.
- Deterministic repetition → MAI Mechanical.
- Long coherent bounded work → Kimi Deep Worker.
- Default independent review → Luna Reviewer.
- High-risk second-line review → Sonnet Reviewer.
- Added visible one-line route reporting.

## v0.1.0 — 2026-08-11

Initial public test release.

- Agent Plugin packaging.
- Luna/MAI/Kimi worker set.
- Sonnet coordinator.
- Human-gated Opus critical review.
- Conservative fan-out and human-in-the-loop routing.
