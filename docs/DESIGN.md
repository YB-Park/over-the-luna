# Design notes

Over the Luna is a **thin, human-guided harness** for GitHub Copilot in VS Code. It intentionally does less than orchestration-heavy systems such as OpenCode/OmO.

The goal is to preserve VS Code's editor, diagnostics, source control, terminal, testing, navigation, Copilot UI, **and the developer's existing MCP/extension tool ecosystem** while adding enough model routing to make inexpensive subagents useful.

## The funnel

```text
cheap + wide                         expensive + narrow
─────────────────────────────────────────────────────────
Luna discovery / ambient tools / routine implementation / first review
MAI deterministic repetition
Kimi long bounded execution
Sonnet coordination / second-line review
Opus human-gated critical review
```

GPT-5.6 Luna is the center of gravity because it is fast and inexpensive enough to make selective subagent use practical. The harness does **not** assume Luna is the best model at every task.

## Product boundary

Over the Luna owns **orchestration**, not the developer's environment.

The plugin does not bundle:

- a duplicate direct-coding agent;
- MCP servers;
- MCP credentials or OAuth configuration;
- lifecycle hooks;
- a daemon;
- a custom VS Code extension runtime.

Direct single-model coding stays in VS Code's built-in **Agent** with **GPT-5.6 Luna** selected. MCP servers and extension tools stay configured through normal VS Code user/workspace mechanisms.

## Coordinator boundary

The Over the Luna coordinator is fixed to **Claude Sonnet 5** and intentionally has only `agent` and `todo`.

That is a real capability boundary. The coordinator decides which worker should act, passes a bounded task, and synthesizes returned results. It should make zero direct repository or external-service tool calls during a healthy harness run.

Fixing the coordinator to Sonnet also keeps child model routing predictable. If the parent itself fell back to a cheaper model, a requested Kimi or Sonnet worker could exceed the parent cost tier and be replaced by the parent model.

The user-facing coordinator is `disable-model-invocation: true`; it is an entry point, not a worker another agent should silently nest.

## Parent tools are not worker tools

A parent coordinator showing edit/terminal/MCP tools as unavailable is **expected** when its tool list is intentionally narrow. That observation does not prove a delegated worker lacks those tools.

VS Code custom subagents can provide their own model, tools, and instructions, overriding defaults inherited from the parent session.

The meaningful runtime tests are therefore performed inside the expanded subagent.

## Ambient tools

### Compatibility requirement

A distributed VS Code harness is not useful if selecting it disconnects developers from the MCP servers and extension tools they already use.

GitHub's custom-agent configuration defines `tools: ['*']` as all available tools, including configured MCP tools. VS Code also allows extension-contributed tools in custom agents.

Over the Luna uses explicit `tools: ['*']` on designated **ambient-capable workers**:

- Luna Tool Worker
- Luna Implementer
- MAI Mechanical
- Kimi Deep Worker

The explicit wildcard is intentional. Omitting `tools` has the same broad default, but a visible `*` is easier to audit and validate as a product contract.

### Why strict roles do not inherit ambient tools

Arbitrary MCP compatibility and structural read-only guarantees cannot both be expressed generically when the plugin does not know the user's server/tool names.

There is no generic project-level rule equivalent to "all user MCP tools that happen to be read-only, including future unknown servers." A wildcard can include edit, execute, external write, deploy, messaging, database mutation, and other side-effecting capabilities.

Therefore strict roles keep narrow capability sets:

- Over the Luna — `agent`, `todo`
- Luna Explorer — `read`, `search`
- Luna Researcher — `read`, `search`, `web`
- Luna Reviewer — `read`, `search`
- Sonnet Reviewer — `read`, `search`
- Opus Critical Reviewer — `read`, `search`, `web`

This preserves capability-level safety where it matters most.

### Luna Tool Worker

Luna Tool Worker is the bridge to user-configured MCP and extension tools when external context/action deserves a separate step.

Typical uses:

- read Jira/Linear acceptance criteria before implementation;
- retrieve internal documentation from a company MCP;
- query a database or service for current state;
- collect independent external evidence requested by a strict reviewer;
- perform an explicitly requested external action.

It defaults to read-only external use and normally returns context to an implementation worker rather than editing the repository itself.

### Ambient implementation workers

Luna Implementer, MAI Mechanical, and Kimi Deep Worker also receive the wildcard because external tools may be naturally part of implementation or validation.

Examples:

- Luna uses a Playwright MCP to validate a UI fix;
- Kimi checks a bounded internal API while implementing an integration;
- MAI applies a deterministic change that depends on an existing organization tool.

The coordinator should not insert a Tool Worker hop when the selected implementation worker can use the needed ambient tool directly without adding useful isolation.

## External side-effect boundary

Ambient tool **availability is not authorization** to mutate external systems.

Reading external context may be inferred when it is clearly necessary for the requested outcome. For example, "implement ABC-123" may require reading ticket ABC-123.

External mutation is never inferred. A coding task does not automatically authorize:

- changing ticket status;
- creating/updating remote issues or PRs;
- sending Slack/email/messages;
- writing to databases;
- deploying;
- changing cloud resources;
- pushing repository state;
- performing another remote side effect.

Those actions require an explicit developer request for that side effect.

If an integration is denied or unavailable, ambient workers return:

`AMBIENT_TOOL_UNAVAILABLE: <service or capability>`

They do not bypass the integration through shell, direct HTTP, alternate credentials, or another service.

## External content is untrusted

Files, web pages, MCP responses, extension-tool output, ticket text, database values, and other retrieved content can contain prompt injection.

Ambient workers are instructed to treat retrieved content as **data**, not instructions. External content cannot change the developer's task, parent scope, model-routing policy, or side-effect boundary.

VS Code's own trust, approval, organization policy, and sandboxing remain authoritative. Over the Luna does not attempt to replace those controls.

## External evidence and strict review

Reviewers remain structurally non-mutating and non-ambient.

If a reviewer cannot reach a verdict because correctness depends on current external state, it returns:

`NEEDS_EXTERNAL_VERIFICATION: <specific fact or invariant>`

The coordinator may then run a fresh Luna Tool Worker in read-only mode and pass that evidence to review. This preserves separation between:

1. external evidence collection;
2. repository correctness judgment.

Opus follows the same rule: premium critical review does not gain arbitrary user MCP capabilities merely because it is expensive.

## Failure and recovery

General orchestration/runtime failure:

`HARNESS_FAILURE: <reason>`

Missing/denied ambient integration:

`AMBIENT_TOOL_UNAVAILABLE: <service or capability>`

Neither failure grants Sonnet permission to become the implementation agent or to bypass the user's tool policy.

The developer can recover manually with VS Code's built-in **Agent + GPT-5.6 Luna**, or explicitly choose another integration/path.

## Luna roles

- **Explorer** — strict `read`, `search`; compact repository facts only.
- **Researcher** — strict `read`, `search`, `web`; public current docs/web facts only.
- **Tool Worker** — ambient `*`; external MCP/extension bridge and evidence collection.
- **Implementer** — ambient `*`; default repository coding, validation, and relevant user tools.
- **Reviewer** — strict `read`, `search`; independent first-line review.

Separating these roles keeps strict reasoning roles safe while preserving the developer's actual IDE capabilities where work is performed.

## Kimi Deep Worker

Kimi K2.7 Code owns one coherent, long-horizon task with clear boundaries and acceptance criteria. It is an implementation worker, not an orchestrator.

Kimi receives ambient tools because a coherent subsystem task can legitimately depend on an existing browser, API, DB, cloud, or internal tool. External side effects remain explicit-only.

## MAI Mechanical

MAI-Code-1-Flash is reserved for work whose design is already decided: DTOs/schemas, mappers, mocks, repeated tests, boilerplate, mechanical renames, obvious lint/type fixes, and pattern replication.

MAI receives ambient tools only so deterministic workflows do not lose existing VS Code capabilities. If the work exposes a real architecture/product/API decision, it stops with `REROUTE: decision required`.

## Layered review

**Luna Reviewer** is the default because review is frequent and Luna is cheap enough to use routinely.

**Sonnet Reviewer** is second-line judgment for architecture, auth/security, concurrency, persistence/data integrity, migrations, public contracts, or explicit Luna uncertainty.

**Opus Critical Reviewer** is a manual, user-facing handoff for the highest-stakes review. It is marked `disable-model-invocation: true` so it cannot be silently selected as a subagent.

All reviewers are structurally non-mutating and non-ambient. Implementation workers own test execution; Luna Tool Worker owns arbitrary external evidence collection.

## Why Opus is a handoff

Premium escalation should be visible and chosen by the developer. There is also a model-routing reason: VS Code falls back to the parent model when a requested subagent model exceeds the parent's cost tier. A handoff avoids pretending an Opus role ran when the runtime actually substituted Sonnet.

## Model selection

For custom subagents, VS Code prioritizes:

1. an explicitly requested subagent model;
2. the custom agent's configured model/list;
3. the parent conversation model.

A requested subagent model cannot exceed the parent model's cost tier; if it does, VS Code falls back to the parent model. Runtime smoke tests record the model displayed on each expanded subagent.

## Tool naming and wildcard use

Strict roles use documented primary aliases such as `execute`, `read`, `edit`, `search`, `agent`, `web`, and `todo`.

Ambient roles use **only `*`**. Mixing a built-in allow-list with a few known MCP names would recreate the original compatibility bug for every user whose tool names differ.

The validator enforces both sides of this rule.

## Large tool catalogs

More tools expand the model's decision space, but VS Code supports virtual tools/tool search for large catalogs. Current VS Code uses `github.copilot.chat.virtualTools.threshold` with a default of `128` to activate tools on demand when catalogs exceed the direct-tool limit.

Users should still disable irrelevant MCP servers/tools for a task when practical. Ambient compatibility means tools remain reachable; it does not mean every available service should be called.

## VS Code-only target

Every distributed agent sets `target: vscode` because this project is designed and tested as a VS Code harness. Copilot CLI can still be used as an installation transport, but CLI runtime behavior is not part of the compatibility promise.

## Fan-out budget

Initial parallel fan-out is capped at **three** workers. Parallelism is mainly for independent discovery, public research, or external evidence collection. A coherent implementation normally has one owner.

More agents are not automatically better: each duplicates prompt/tool context, overlapping investigation wastes credits, synthesis cost grows with outputs, and wide swarms reduce human visibility.

## Reasoning-effort limitation

VS Code supports configurable thinking/reasoning effort for supported models, but `.agent.md` does not currently expose a documented per-agent reasoning-effort field. Several roles share Luna, so **Luna Medium** is the recommended global starting point.

## Deliberate exclusions

Over the Luna currently does not provide a duplicate direct-coding agent, recursive/nested swarms, background daemons, autonomous issue picking, automatic external mutations, hidden premium escalation, bundled MCP servers, lifecycle hooks, a custom VS Code extension, or a second editor UI.

Those features should be added only if measured use shows a real need.

## Validation strategy

### Static CI

`scripts/validate_plugin.py` checks:

- exact agent set and frontmatter parseability;
- `target: vscode`;
- allowed model names;
- exact coordinator worker allow-list;
- strict role tool boundaries;
- designated ambient roles declaring exactly `tools: ['*']`;
- no bundled `.mcp.json`, plugin MCP declaration, or per-agent MCP server configuration;
- ambient side-effect / untrusted-data / unavailable-tool policy markers;
- reviewers having neither edit/execute nor wildcard tools;
- reviewer `NEEDS_EXTERNAL_VERIFICATION` behavior;
- no recursive worker delegation;
- no reintroduction of the redundant `Luna Solo` wrapper.

### Runtime smoke test

Static configuration cannot prove how a particular VS Code/Copilot release resolves user MCP/extension tools inside custom subagents. [`SMOKE_TEST.md`](SMOKE_TEST.md) verifies the actual runtime path, including ambient-tool cases.

Useful metrics:

1. Luna completion rate.
2. Kimi/Sonnet/Opus escalation rate.
3. Ambient-tool success rate.
4. Ambient-tool unavailable/failure rate.
5. Unexpected external-side-effect count — target **zero**.
6. Wall-clock time versus native Agent + Luna.
7. Review defect rate.
8. Agent count per task.
9. Harness failure rate.
10. Sonnet direct environment-tool calls — expected **zero** in healthy harness runs.
11. Intended model versus displayed subagent model.

The target is **maximum useful work per token and per minute while preserving the developer's existing IDE capabilities and control**.
