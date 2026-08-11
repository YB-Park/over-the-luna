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

The Over the Luna coordinator is fixed to **Claude Sonnet 5** and intentionally has only `agent` and `todo`.

That is a real capability boundary. The coordinator decides which worker should act, passes a bounded task, and synthesizes returned results. It should make zero repository read/edit/execute calls during a healthy harness run.

Fixing the coordinator to Sonnet also keeps child model routing predictable. If the parent itself were allowed to fall back to a much cheaper model, a requested Kimi or Sonnet worker could exceed the parent cost tier and be replaced by the parent model.

The user-facing coordinator is also `disable-model-invocation: true`; it is an entry point, not a worker another agent should silently nest.

## Parent tools are not worker tools

This distinction was the key lesson from v0.2 testing.

A parent coordinator showing edit/terminal tools as unavailable is **expected** when its tool list is intentionally narrow. That observation does not prove the delegated implementation worker lacks those tools.

VS Code custom subagents can provide their own model, tools, and instructions, overriding the defaults inherited from the parent session.

The meaningful runtime test is therefore whether the expanded implementation subagent — Luna Implementer, Kimi Deep Worker, or MAI Mechanical — receives its own declared `edit` and `execute` capabilities.

v0.2.1 temporarily widened the coordinator after these two layers were conflated. v0.3 restores the strict coordinator boundary.

## Failure and recovery

A failed delegation remains visible.

If a subagent cannot start, its required model/tooling is unavailable, or it otherwise cannot perform its task, the coordinator reports:

`HARNESS_FAILURE: <reason>`

It does not silently become the implementation agent.

A **Continue directly with Luna** handoff gives the developer an explicit recovery path. Luna Solo is also `disable-model-invocation: true`, so this transition is user-chosen rather than an automatic hidden fallback.

## Luna roles

- **Explorer** — `read`, `search`; compact repository facts only.
- **Researcher** — `read`, `search`, `web`; current external/documentation facts only.
- **Implementer** — `read`, `search`, `edit`, `execute`, `todo`; default coding owner.
- **Reviewer** — `read`, `search`; independent first-line review without mutation capability.

Separating these roles reduces unnecessary tool choice and keeps exploratory context out of the parent conversation.

## Kimi Deep Worker

Kimi K2.7 Code owns one coherent, long-horizon task with clear boundaries and acceptance criteria. It is an implementation worker, not an orchestrator.

Prefer one Kimi owner for a subsystem-sized multi-file change that needs a sustained thread and repeated validation rather than several overlapping implementers.

## MAI Mechanical

MAI-Code-1-Flash is reserved for work whose design is already decided: DTOs/schemas, mappers, mocks, repeated tests, boilerplate, mechanical renames, obvious lint/type fixes, and pattern replication.

If the work exposes a real architecture/product/API decision, MAI stops with `REROUTE: decision required`.

## Layered review

**Luna Reviewer** is the default because review is frequent and Luna is cheap enough to use routinely.

**Sonnet Reviewer** is second-line judgment for architecture, auth/security, concurrency, persistence/data integrity, migrations, public contracts, or explicit Luna uncertainty.

**Opus Critical Reviewer** is a manual, user-facing handoff for the highest-stakes review. It is marked `disable-model-invocation: true` so it cannot be silently selected as a subagent.

All reviewers are structurally non-mutating: they receive neither `edit` nor `execute`. Implementation workers own test execution and report the validation they performed; reviewers assess those claims against repository evidence.

## Why Opus is a handoff

Premium escalation should be visible and chosen by the developer. There is also a model-routing reason: VS Code falls back to the parent model when a requested subagent model exceeds the parent's cost tier. A handoff avoids pretending an Opus role ran when the runtime actually substituted Sonnet.

## Model selection

For custom subagents, VS Code prioritizes:

1. an explicitly requested subagent model;
2. the custom agent's configured model/list;
3. the parent conversation model.

A requested subagent model cannot exceed the parent model's cost tier; if it does, VS Code falls back to the parent model. Runtime smoke tests therefore record the model displayed on each expanded subagent.

## Tool naming

GitHub documents primary aliases including `execute`, `read`, `edit`, `search`, `agent`, `web`, and `todo`.

Compatible aliases such as `shell` for `execute` are valid, but v0.3 uses primary aliases only. Unknown tool names can be silently ignored, so a narrow documented vocabulary makes configuration drift easier to detect.

## VS Code-only target

Every distributed agent sets `target: vscode` because this project is designed and tested as a VS Code harness. Copilot CLI can still be used as an installation transport, but CLI runtime behavior is not part of the compatibility promise.

## Fan-out budget

Initial parallel fan-out is capped at **three** workers. Parallelism is mainly for independent discovery/research. A coherent implementation normally has one owner.

More agents are not automatically better: each duplicates prompt/tool context, overlapping investigation wastes credits, synthesis cost grows with outputs, and wide swarms reduce human visibility.

## Reasoning-effort limitation

VS Code supports configurable thinking/reasoning effort for supported models, but `.agent.md` does not currently expose a documented per-agent reasoning-effort field. Several roles share Luna, so **Luna Medium** is the recommended global starting point.

## Deliberate exclusions

Over the Luna currently does not provide recursive/nested swarms, background daemons, autonomous issue picking, automatic commits/pushes, hidden premium escalation, MCP servers, lifecycle hooks, a custom VS Code extension, or a second editor UI.

Those features should be added only if measured use shows a real need.

## Validation strategy

### Static CI

`scripts/validate_plugin.py` checks:

- frontmatter parseability;
- `target: vscode`;
- allowed model names and primary tool aliases;
- valid subagent/handoff references;
- manual-only user entry agents;
- Sonnet-only coordinator model;
- router-only coordinator tools and exact worker allow-list;
- implementation-worker read/search/edit/execute access;
- reviewers having neither edit nor execute;
- no recursive worker delegation.

### Runtime smoke test

Static configuration cannot prove how a particular VS Code/Copilot release resolves tools and models. [`SMOKE_TEST.md`](SMOKE_TEST.md) verifies the actual runtime path.

Useful metrics:

1. Luna completion rate.
2. Kimi/Sonnet/Opus escalation rate.
3. Wall-clock time versus Luna Solo.
4. Review defect rate.
5. Agent count per task.
6. Harness failure rate.
7. Sonnet repository-tool calls — expected to be zero in healthy harness runs.
8. Intended model versus displayed subagent model.

The target is **maximum useful work per token and per minute while keeping the developer in control**.
