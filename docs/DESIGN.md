# Design notes

Over the Luna is a **thin, human-guided harness** for GitHub Copilot in VS Code. It intentionally does less than orchestration-heavy systems.

The goal is to preserve VS Code's editor, diagnostics, source control, terminal, testing, navigation, Copilot UI, and the developer's existing MCP/extension tools while adding enough model routing to make inexpensive subagents useful.

## The funnel

```text
cheap + wide                         expensive + narrow
─────────────────────────────────────────────────────────
Luna discovery / tool bridge / routine implementation / first review
MAI deterministic repetition
Kimi long bounded execution
Sonnet coordination / second-line review
Opus human-gated critical review
```

## Product boundary

Over the Luna owns **orchestration**, not the developer's environment.

It does not bundle MCP servers, credentials, OAuth, a daemon, or a custom VS Code runtime. Direct single-model coding stays in native **Agent + GPT-5.6 Luna**. MCP servers and extension tools remain configured through normal VS Code mechanisms.

## The v0.5 lesson: cross-product spec is not enough

v0.5.0 used `tools: ['*']` on ambient workers because GitHub's cross-product custom-agent reference documents `*` as enabling all tools.

Real VS Code testing failed: the server was running and its configuration was visible, but Luna Tool Worker could not call the MCP.

Current VS Code source explains why:

1. A named custom subagent that declares `tools` replaces the inherited parent tool selection with an enablement map built from the declared tool/tool-set reference names.
2. Current VS Code tool resolution exact-matches registered tool/tool-set names and aliases; Over the Luna cannot rely on a global `*` entry as an all-tools selector.
3. A named custom subagent that **omits `tools`** keeps the parent invocation's selected-tool map.
4. A main custom agent that **omits `tools`** falls back to the user's active/global selected-tool state.

Therefore v0.6.0 uses **tool omission as inheritance**, not a wildcard.

## Tool inheritance architecture

Roles that intentionally omit `tools`:

- **Over the Luna** — parent selected-tool carrier + router
- **Luna Tool Worker** — user MCP/extension bridge
- **Luna Implementer** — default implementation
- **MAI Mechanical** — deterministic implementation
- **Kimi Deep Worker** — long bounded implementation

Strict roles that intentionally override inheritance:

- Luna Explorer → `read`, `search`
- Luna Researcher → `read`, `search`, `web`
- Luna Reviewer → `read`, `search`
- Sonnet Reviewer → `read`, `search`
- Opus Critical Reviewer → `read`, `search`, `web`

All workers remain leaf nodes with `agents: []`.

## Coordinator boundary: capability tradeoff

The ideal design would express both:

- Sonnet can execute only delegation/todo; and
- every unknown current/future user MCP tool flows automatically into children.

Current static VS Code `.agent.md` configuration cannot express both simultaneously.

If the coordinator declares `tools: ['agent', 'todo']`, ambient children that omit `tools` inherit only that restricted selection. If children declare MCP tools explicitly, the plugin must know each user's server/tool names.

So v0.6 chooses **ambient compatibility**. The coordinator omits `tools` to carry the developer's active selected-tool map into children.

This weakens the coordinator boundary from capability-level to behavioral-level: Sonnet technically sees the tools, but must not execute environment-facing ones.

Healthy Sonnet direct calls:

- subagent delegation;
- optional todo/task coordination.

Unhealthy direct calls:

- repository read/search/edit/execute;
- web/browser;
- MCP/extension tools;
- database/cloud/source-control/environment actions.

Any such call is a `HARNESS_VIOLATION` and a smoke-test failure.

This tradeoff is explicit rather than hidden. If VS Code later provides stable additive tool inheritance, per-agent deny tools, or stable always-on agent hooks that can preserve child ambient tools, the coordinator should return to a hard capability boundary.

## Why hooks are not a core dependency

VS Code Preview `PreToolUse` hooks can deny direct tool execution and agent-scoped hooks are a promising future hardening mechanism. However custom-agent hooks currently depend on preview support/settings and can be disabled by organization policy.

A one-install harness should not silently fail open or lose MCP support because an optional preview hook is unavailable. v0.6 therefore keeps hooks out of the core compatibility contract.

## Luna Tool Worker

Tool Worker isolates bounded external work when that isolation is useful:

- read Jira/Linear acceptance criteria;
- retrieve internal docs;
- query a database/service for current state;
- collect fresh external evidence for a strict reviewer;
- perform a specific external action only when explicitly requested.

It inherits the user's active tools but normally returns context rather than owning repository implementation.

## Ambient implementation workers

Luna Implementer, MAI Mechanical, and Kimi Deep Worker inherit the same active tool selection so existing browser/API/DB/cloud/internal tools remain usable during implementation and validation.

The coordinator should not add Tool Worker hops when the implementation worker can naturally use the required tool itself.

## External side-effect boundary

Tool visibility is not authorization.

External reads may be inferred when clearly necessary for the requested outcome. External mutation is never inferred.

A coding task does not automatically authorize ticket updates, messages, DB writes, deploys, cloud changes, pushes, PR creation, or other remote effects. Those require an explicit developer request.

Unavailable/denied integration:

`AMBIENT_TOOL_UNAVAILABLE: <service or capability>`

Workers must not bypass it through shell, direct HTTP, alternate credentials, or another integration.

## External content is untrusted

Files, web pages, MCP responses, issue text, DB values, and extension-tool output are data, not instructions. They cannot override developer scope, routing policy, or side-effect constraints.

VS Code trust, approvals, Configure Tools state, sandboxing, and organization policy remain authoritative.

## Strict review and external evidence

Reviewers stay non-mutating and non-ambient.

When a verdict requires current private/external state, return:

`NEEDS_EXTERNAL_VERIFICATION: <specific fact or invariant>`

Then use a fresh Luna Tool Worker in read-only mode and pass evidence back to review.

## Role summary

- **Luna Explorer** — strict local discovery
- **Luna Researcher** — strict public/current web research
- **Luna Tool Worker** — inherited external tools/evidence
- **Luna Implementer** — inherited normal implementation tools
- **Luna Reviewer** — strict first-line review
- **MAI Mechanical** — inherited deterministic repetition
- **Kimi Deep Worker** — inherited long bounded implementation
- **Sonnet** — routing/synthesis; direct environment execution forbidden
- **Sonnet Reviewer** — strict high-risk second line
- **Opus** — manual strict critical review

## Fan-out budget

Initial parallel fan-out is capped at **three**. Parallelize independent discovery/research/evidence, not overlapping implementation. One coherent subsystem normally has one implementation owner.

## Failure and recovery

- orchestration/runtime failure → `HARNESS_FAILURE: <reason>`
- missing/denied integration → `AMBIENT_TOOL_UNAVAILABLE: <service or capability>`
- coordinator directly uses environment tool → `HARNESS_VIOLATION: coordinator executed <tool>`

None of these grants Sonnet permission to silently become the implementer. Direct recovery belongs to native **Agent + GPT-5.6 Luna**.

## Validation strategy

Static CI enforces:

- exact agent set;
- `target: vscode`;
- allowed models;
- coordinator/ambient roles **omit** `tools`;
- strict roles keep exact explicit tool allow-lists;
- global `tools: ['*']` is rejected;
- no bundled/per-agent MCP configuration;
- ambient side-effect/untrusted-data/unavailable-tool markers;
- strict reviewer boundaries and `NEEDS_EXTERNAL_VERIFICATION`;
- exact coordinator worker allow-list;
- no recursive worker delegation.

Runtime smoke tests verify what static CI cannot:

1. native-Agent MCP is inherited by Luna Tool Worker;
2. user-disabled tools remain unavailable;
3. implementation workers retain local edit/execute plus relevant MCP/extension tools;
4. strict reviewers stay strict;
5. Sonnet direct environment-tool calls remain **zero**;
6. no external side effect is inferred;
7. intended models actually run.

The target is **maximum useful work per token and per minute without replacing the developer's VS Code environment or hiding orchestration behavior**.
