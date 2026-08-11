# Design notes

Over the Luna is a **thin, human-guided harness** for GitHub Copilot in VS Code. It intentionally does less than orchestration-heavy systems such as OpenCode/OmO.

The goal is to preserve VS Code's editor, diagnostics, source control, terminal, testing, navigation, and Copilot UI while adding enough model routing to make inexpensive subagents useful.

## The funnel

```text
cheap + wide                         expensive + narrow
─────────────────────────────────────────────────────────
Luna discovery / routine implementation / first review
MAI deterministic repetition
Kimi long bounded execution
Sonnet coordination / second-line review
Opus human-gated critical review
```

GPT-5.6 Luna is the center of gravity because it is fast and inexpensive enough to make selective subagent use practical. The harness does **not** assume Luna is the best model at every task.

## Coordinator boundary

The **Over the Luna** coordinator is Claude Sonnet 5 and intentionally has only:

- `agent`
- `todo`

That is a real capability boundary, not merely a prompt preference.

The coordinator decides which worker should act, passes a bounded task, and synthesizes the returned result. It should not inspect/edit/execute against the repository itself during a healthy harness run.

This follows VS Code's coordinator/subagent model: a custom subagent can define its own model, tools, and instructions, and those settings override the defaults inherited from the parent conversation.

### Important lesson from v0.2 testing

A parent coordinator showing edit/terminal tools as unavailable is **expected** when its tool list is intentionally narrow. That observation alone does not prove that the delegated implementation worker lacks those tools.

The meaningful runtime test is whether the expanded implementation subagent — Luna Implementer, Kimi Deep Worker, or MAI Mechanical — receives its own declared `edit` and `execute` capabilities.

v0.2.1 temporarily widened the coordinator tools after these two layers were conflated. v0.3 restores the strict coordinator boundary and makes harness failure explicit instead of hiding it behind Sonnet direct execution.

## Failure and recovery

A failed delegation must remain visible.

If the subagent cannot start, its model/tooling is unavailable, or it otherwise cannot perform the delegated repository task, the coordinator reports:

`HARNESS_FAILURE: <reason>`

It must not silently become the implementation agent.

A **Continue directly with Luna** handoff provides a deliberate recovery path. This keeps the developer in control and gives us a measurable harness-failure rate instead of masking failures.

## Why Luna has focused roles

The Luna workers intentionally expose different tool surfaces and output contracts.

- **Explorer**: repository discovery only; `read` + `search`.
- **Researcher**: current external/documentation research; `read` + `search` + `web`.
- **Implementer**: normal coding; `read` + `search` + `edit` + `execute` + `todo`.
- **Reviewer**: independent first-line review; no `edit` tool.

The separation reduces unnecessary tool choices, isolates noisy context, and keeps the parent context smaller.

## Why Kimi is bounded

Kimi K2.7 Code is reserved for a coherent long-horizon task with clear boundaries and acceptance criteria. It is an implementation owner, not another orchestrator.

Prefer one Kimi worker for a subsystem-sized multi-file change that needs a sustained thread and repeated validation rather than several overlapping implementation agents.

## Why MAI is mechanical

MAI-Code-1-Flash is used after design is already decided:

- DTOs and schemas
- mappers
- repetitive tests/mocks
- mechanical renames
- boilerplate
- obvious type/lint corrections
- straightforward pattern replication

If the work reveals a real design decision, MAI stops and returns `REROUTE: decision required` instead of inventing architecture.

## Why review is layered

**Luna Reviewer** is the default because review is frequent and Luna is cheap enough to use routinely.

**Sonnet Reviewer** is second-line judgment for architecture, auth/security, concurrency, persistence/data integrity, migrations, public contracts, or explicit Luna uncertainty.

Reviewers deliberately do not receive the `edit` alias. They may receive `execute` for focused validation; instructions prohibit intentionally mutating source files through terminal commands.

## Why Opus is manual

Opus is a handoff, not a subagent.

This serves two purposes:

1. premium escalation remains visible and chosen by the developer;
2. VS Code will fall back to the parent model when a requested subagent model exceeds the parent model's cost tier, which could otherwise blur whether the intended premium model actually ran.

The handoff preserves conversation context while making the escalation explicit.

## Model fallback behavior

For a custom subagent, VS Code chooses the model in this order:

1. explicit model requested for the subagent;
2. the custom agent's configured model/list;
3. the parent conversation model.

A requested model may not exceed the parent model's cost tier; when it does, VS Code falls back to the parent model. Therefore model identity should be checked in the expanded subagent UI during runtime validation.

## Tool naming policy

GitHub documents primary custom-agent aliases including:

- `execute`
- `read`
- `edit`
- `search`
- `agent`
- `web`
- `todo`

Compatible aliases exist, for example `shell` for `execute`, but v0.3 uses primary aliases only. Unknown tools can be silently ignored by the product, so keeping a narrow documented vocabulary reduces configuration ambiguity.

## VS Code-only target

Every distributed agent uses `target: vscode`.

The project is intentionally designed and tested around VS Code behavior. Leaving `target` unset would make the agent definition applicable to both VS Code and GitHub Copilot contexts, which is broader than the project's current compatibility promise.

## Fan-out budget

Initial parallel fan-out is capped at **three** workers.

Parallelism is mainly for independent discovery/research. A coherent implementation normally gets one owner.

More agents are not automatically better:

- each subagent duplicates some prompt/tool context;
- overlapping investigation wastes credits;
- synthesis cost grows with outputs;
- broad swarms reduce human visibility.

## Reasoning-effort limitation

VS Code supports configurable thinking/reasoning effort for supported models, but `.agent.md` currently does not expose a documented per-agent reasoning-effort field.

Because several roles share Luna, **Luna Medium** is the recommended global starting point. Raise it deliberately for hard direct Luna Solo work rather than maximizing every worker by default.

## What this project does not do

It intentionally does not provide:

- recursive/nested swarms
- background daemons
- autonomous issue picking
- automatic commits/pushes
- hidden premium escalation
- MCP servers
- lifecycle hooks
- a custom VS Code extension
- a second editor UI

These should be added only if a measured problem justifies them.

## Validation strategy

There are two layers.

### Static CI

`scripts/validate_plugin.py` checks the plugin and agent definitions for architectural drift, including:

- frontmatter parseability;
- `target: vscode`;
- allowed models and primary tool aliases;
- valid subagent/handoff references;
- router-only coordinator capability;
- implementation-worker edit/execute access;
- reviewers lacking `edit`;
- no recursive worker delegation.

### Runtime smoke test

Static configuration cannot prove how a particular VS Code/Copilot release resolves tools and models. [`SMOKE_TEST.md`](SMOKE_TEST.md) verifies the actual runtime path.

Important runtime metrics:

1. **Luna completion rate** — ordinary tasks resolved by Luna workers.
2. **Escalation rate** — Kimi/Sonnet/Opus usage.
3. **Wall-clock time** — harness versus direct Luna Solo.
4. **Review defect rate** — serious findings after implementation.
5. **Agent count per task** — orchestration bloat signal.
6. **Harness failure rate** — failed worker invocation/tool/model resolution.
7. **Sonnet repository-tool calls** — should be zero in healthy Over the Luna runs.

The ideal outcome is **maximum useful work per token and per minute while keeping the developer in control**.
