# Design notes

Over the Luna is a **thin, human-guided harness** for GitHub Copilot in VS Code.

The goal is not to use every available model. The goal is to preserve VS Code's native environment, separate useful contexts/capabilities, and route to the **cheapest reliable path** with visible escalation.

## v0.7 principle: model diversity must earn its cost

Luna is the default implementation model because current use shows it is cheap enough and capable enough to cover ordinary coding, deterministic repetition, and coherent multi-file work.

A dedicated worker exists only when it adds a measurable advantage in at least one dimension:

- correctness or success rate;
- wall-clock time;
- total tokens/credits;
- context continuity;
- capability isolation;
- independent review value.

A model being available in the organization's Copilot catalog is not sufficient reason to create a routing branch for it.

This leads to two simplifications in v0.7:

1. **MAI Mechanical is removed.** Mechanical work routes to Luna Implementer. MAI-Code-1-Flash remains only as Luna Implementer's availability fallback.
2. **Kimi Deep Worker becomes escalation-only.** Multi-file or long work starts with Luna. Kimi is invoked only after a concrete `ESCALATE_KIMI` signal or an explicit developer request.

## Current funnel

```text
wide/default                                         narrow/escalated
────────────────────────────────────────────────────────────────────
Luna discovery / tool bridge / implementation / first review
                                │
                                └─ implementation non-convergence → Kimi
Sonnet coordination / high-risk second-line review
Opus human-gated critical review
```

## Why multiple Luna roles still matter

A harness does not need different models at every stage to provide value.

The Luna roles have different context and capability boundaries:

- **Luna Explorer** — strict local read/search discovery;
- **Luna Researcher** — strict public/current web research;
- **Luna Tool Worker** — inherited user MCP/extension tools for bounded external work;
- **Luna Implementer** — inherited implementation/tool surface and one coherent coding thread;
- **Luna Reviewer** — strict independent read-only review.

Using the same inexpensive model in separate stateless subagent invocations still provides useful separation between discovery, implementation, external evidence, and independent review.

## Luna Implementer ownership

Luna Implementer owns by default:

- ordinary fixes/features;
- deterministic repetition;
- unit-test pattern replication;
- DTO/schema/mapper/mock/boilerplate work;
- mechanical renames and obvious lint/type fixes;
- coherent multi-file implementation;
- repeated validation/fix cycles while progress is converging.

Task size, repetition, unfamiliarity, or file count alone are not escalation signals.

If the blocker is an unresolved product/architecture/security/API decision, Luna returns the decision to the parent; another implementation model is not a substitute for human judgment.

## Kimi escalation

Kimi is a bounded continuation model, not an initial task classifier.

Luna may return:

`ESCALATE_KIMI: <specific reason>`

only when a concrete implementation-continuity problem exists, such as:

- necessary coupled cross-file state is no longer being held reliably;
- repeated validation/fix cycles are demonstrably not converging;
- the same bounded implementation would benefit from handing its thread to another implementation owner.

Sonnet passes Kimi the original acceptance criteria, current implementation state, changed areas, failed validation, and minimal continuation context. Kimi should not restart broad discovery or widen the task.

The developer can also explicitly request Kimi for a bounded task.

## MAI as fallback, not role

MAI-Code-1-Flash remains in Luna Implementer's model preference list after Luna.

That is a **resilience decision**, not a specialization claim. If Luna is unavailable or the runtime chooses the configured fallback, the implementation role can still operate. There is no separate MAI routing branch, prompt surface, or worker lifecycle to maintain.

## Product boundary

Over the Luna owns orchestration, not the developer's environment.

It does not bundle MCP servers, credentials, OAuth, a daemon, or a custom VS Code runtime. Direct single-model coding stays in native **Agent + GPT-5.6 Luna**. MCP servers and extension tools remain configured through normal VS Code mechanisms.

## Selected-tool inheritance

v0.6 established the current runtime-compatible inheritance model and v0.7 keeps it unchanged.

Roles that intentionally omit `tools`:

- Over the Luna
- Luna Tool Worker
- Luna Implementer
- Kimi Deep Worker

Strict roles that intentionally override inheritance:

- Luna Explorer → `read`, `search`
- Luna Researcher → `read`, `search`, `web`
- Luna Reviewer → `read`, `search`
- Sonnet Reviewer → `read`, `search`
- Opus Critical Reviewer → `read`, `search`, `web`

All workers remain leaf nodes with `agents: []`.

## Coordinator boundary

Current static VS Code `.agent.md` cannot simultaneously hard-limit Sonnet to delegation/todo and automatically pass every unknown user MCP into children.

So the coordinator omits `tools` as a selected-tool carrier, while router-only behavior is an explicit contract.

Healthy Sonnet direct calls:

- subagent delegation;
- optional todo/task coordination.

Any direct repository/web/MCP/extension/environment call is:

`HARNESS_VIOLATION: coordinator executed <tool>`

Strict exploration/review boundaries remain capability-level restrictions.

## External side-effect boundary

Tool visibility is not authorization.

External reads may be inferred when clearly necessary for the requested outcome. External mutation is never inferred. Ticket updates, messages, DB writes, deploys, pushes, PR creation, cloud changes, and similar effects require an explicit developer request.

Unavailable/denied integration:

`AMBIENT_TOOL_UNAVAILABLE: <service or capability>`

Workers must not bypass it through shell, direct HTTP, alternate credentials, or another integration.

## External evidence and review

Reviewers stay non-mutating and non-ambient.

When a verdict requires current private/external state:

`NEEDS_EXTERNAL_VERIFICATION: <specific fact or invariant>`

The coordinator invokes a fresh Luna Tool Worker in read-only mode and passes evidence back to review.

## Fan-out budget

Initial parallel fan-out is capped at **three**. Parallelize independent discovery/research/evidence, not overlapping implementation. One coherent subsystem normally has one implementation owner.

## Failure and recovery

- orchestration/runtime failure → `HARNESS_FAILURE: <reason>`
- missing/denied integration → `AMBIENT_TOOL_UNAVAILABLE: <service or capability>`
- coordinator directly uses environment tool → `HARNESS_VIOLATION: coordinator executed <tool>`

None of these grants Sonnet permission to silently become the implementer. Direct recovery belongs to native **Agent + GPT-5.6 Luna**.

## Validation strategy

Static CI enforces:

- exact 9-agent architecture;
- no Luna Solo or MAI Mechanical worker;
- Luna Implementer with Luna primary + MAI availability fallback;
- Kimi as K2.7-only escalation worker;
- `ESCALATE_KIMI` contract in Luna and coordinator;
- coordinator/ambient roles omit `tools`;
- strict roles keep exact explicit allow-lists;
- no global `tools: ['*']` assumption;
- no bundled/per-agent MCP configuration;
- strict reviewer boundaries and `NEEDS_EXTERNAL_VERIFICATION`;
- no recursive worker delegation.

Runtime smoke tests verify:

1. existing MCP tools reach Luna Tool Worker;
2. user-disabled tools stay disabled;
3. Luna handles ordinary, mechanical, and multi-file implementation first;
4. Kimi is **not** selected merely because a task is long/multi-file;
5. explicit Kimi escalation can run and remains bounded;
6. strict reviewers stay strict;
7. Sonnet direct environment-tool calls remain zero;
8. no external side effect is inferred.

The target is **maximum useful work per token and per minute, with the fewest routing branches that can justify themselves**.
