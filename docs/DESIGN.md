# Design notes

Over the Luna is a **thin harness**. It intentionally does less than orchestration-heavy systems such as OpenCode/OmO.

The goal is to preserve the strengths of VS Code — editor integration, diagnostics, source control, terminal, testing, navigation, and the Copilot UI — while adding just enough model routing to make cheap subagents useful.

## The funnel

The architecture is a funnel:

```text
cheap + wide                         expensive + narrow
─────────────────────────────────────────────────────────
Luna discovery
Luna routine implementation
MAI deterministic repetition
Kimi long bounded execution
Sonnet coordination/review
Opus critical review
```

GPT-5.6 Luna is the center of gravity because it is fast, inexpensive, and capable enough to make subagent fan-out economically reasonable. The harness does **not** assume Luna is the best model at every task.

## Why the coordinator is Sonnet 5

A coordinator makes high-leverage decisions: whether to delegate, what context to gather, how to divide work, and whether a result is good enough.

A cheap coordinator that creates unnecessary work can cost more than a better coordinator. Sonnet 5 is used here as a routing and synthesis model, not as the default code generator.

The coordinator prompt is kept short and has a hard initial fan-out budget.

## Why Luna has three worker roles

All three use the same model but intentionally expose different tools and output contracts.

- **Explorer**: local codebase facts only. No edits, no terminal.
- **Researcher**: external/current documentation plus repository context. No edits.
- **Implementer**: edits and focused validation.

Separating them reduces tool choice, isolates noisy context, and makes returned results smaller.

## Why Kimi is bounded

Kimi K2.7 Code is used when the task is large enough that a single worker should stay with it for a while, but the task still has clear boundaries and acceptance criteria.

The coordinator should prefer Kimi for a coherent subsystem-sized task, not for open-ended orchestration.

## Why MAI is mechanical

MAI-Code-1-Flash is reserved for tasks where design is already decided:

- DTOs and schemas
- mappers
- repetitive tests
- mechanical renames
- boilerplate
- obvious type/lint corrections

If a mechanical task reveals an architectural decision, the agent is instructed to stop and reroute rather than invent a design.

## Why Opus is manual

There are two reasons.

First, VS Code currently prevents subagents from requesting a model above the parent model's cost tier.

Second, and more important, automatic premium escalation works against this project's human-in-the-loop philosophy.

Opus is a **handoff**. The user can see that a premium, critical review is about to happen and decides whether it is worth doing.

## Fan-out budget

The coordinator starts with at most **three** parallel subagents.

More is not necessarily better:

- each subagent duplicates some prompt/tool context
- overlapping research wastes credits
- synthesis gets harder as outputs grow
- broad swarms reduce human visibility

If a task truly benefits from a wider map/reduce strategy, the user can explicitly ask for it.

## Reasoning-effort limitation

VS Code supports configurable reasoning for models including GPT-5.6 Luna, Claude Sonnet 5, and Claude Opus 4.8.

At the time this project was created, `.agent.md` frontmatter can select a model but does not expose a documented per-agent reasoning-effort field. VS Code remembers Thinking Effort per model, so all Luna roles effectively share that setting.

For that reason, **Luna Medium** is the recommended global starting point.

## Model cost-tier limitation

A subagent's requested model cannot exceed the parent conversation's model cost tier. If it does, VS Code falls back to the parent model.

This is why the Opus role is not in the coordinator's subagent allow-list.

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

Those can be added later if they solve a measured problem.

## Evaluation

If you test this harness, useful metrics are:

1. **Luna completion rate** — tasks completed without rerouting.
2. **Escalation rate** — how often Kimi, Sonnet review, or Opus review is necessary.
3. **Wall-clock time** — harness speed versus a direct agent.
4. **Review defect rate** — serious issues found after Luna/Kimi implementation.
5. **Agent count per task** — a simple signal for orchestration bloat.

The ideal outcome is not "maximum subagents." It is **maximum useful work per token and per minute while keeping the developer in control**.
