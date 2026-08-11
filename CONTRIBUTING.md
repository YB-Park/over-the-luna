# Contributing

Contributions are welcome, especially evidence from real VS Code/Copilot usage.

## Principles

Preserve the project's core constraints:

- human-guided, not swarm-by-default;
- concise agent prompts;
- Luna-first routing;
- no hidden premium-model escalation;
- preserve the developer's existing VS Code tool selection for execution workers;
- keep exploration/review roles structurally narrow;
- do not bundle or own user MCP servers, credentials, OAuth, or trust policy;
- external side effects are never inferred from a coding task;
- current VS Code runtime behavior outranks cross-product assumptions;
- routing branches must have measurable reasons to exist.

## Specialist-worker burden of proof

Do not add a dedicated model worker just because the organization makes that model available.

A new specialist route should show a repeatable advantage over Luna in at least one of:

- correctness / completion rate;
- wall-clock time;
- total tokens or credits;
- context continuity;
- capability isolation;
- independent review quality.

If the advantage is only availability resilience, prefer a **model fallback inside an existing role** instead of a new worker.

Current policy:

- mechanical/repetitive work → Luna Implementer;
- coherent multi-file work → Luna Implementer first;
- MAI-Code-1-Flash → Luna Implementer availability fallback only;
- Kimi Deep Worker → explicit developer request or `ESCALATE_KIMI` only.

## Tool-boundary changes

**Inherited-tool roles** intentionally omit `tools`:

- Over the Luna
- Luna Tool Worker
- Luna Implementer
- Kimi Deep Worker

Do not replace omission with `tools: ['*']` or a built-in-only list; current VS Code subagent inheritance relies on omission.

**Strict roles** keep explicit allow-lists:

- Luna Explorer
- Luna Researcher
- Luna Reviewer
- Sonnet Reviewer
- Opus Critical Reviewer

Do not add `.mcp.json`, plugin `mcpServers`, or per-agent MCP configuration for convenience. The harness consumes the developer's existing VS Code environment rather than owning integrations.

The coordinator's inherited tool visibility is an explicit tradeoff. Direct Sonnet environment-tool execution is a `HARNESS_VIOLATION`.

## Routing changes

Before changing Luna/Kimi routing, explain:

1. What real failure mode was observed.
2. Why Luna could not reliably own the work.
3. Whether the change improves correctness, time, or token/credit use.
4. What model(s), tasks, and tool environment were tested.
5. Whether the change adds another routing branch or agent call.
6. What evidence would cause the route to be removed again.

`ESCALATE_KIMI` should describe a concrete continuity/non-convergence problem, not task size or file count.

## Ambient-tool bug reports

Include:

- VS Code and Copilot versions;
- plugin version;
- worker/model;
- MCP/extension source and exact tool name;
- whether it works in native Agent;
- Configure Tools state;
- server/trust state;
- exact error.

Avoid long examples unless they fix demonstrated behavior. Prompt tokens are part of the product.
