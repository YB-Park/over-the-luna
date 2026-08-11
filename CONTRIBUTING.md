# Contributing

Contributions are welcome, especially evidence from real VS Code/Copilot usage.

## Principles

Preserve the project's core constraints:

- human-guided, not swarm-by-default
- concise agent prompts
- no hidden premium-model escalation
- preserve the developer's existing VS Code tool selection for execution workers
- keep exploration/review roles structurally narrow
- do not bundle or own user MCP servers, credentials, OAuth, or trust policy
- external side effects are never inferred from a coding task
- routing changes should have a measurable reason
- current VS Code runtime behavior outranks cross-product assumptions; cite current official docs/source for compatibility changes

## Useful contributions

- model-routing experiments
- MCP/extension-tool compatibility reports from real VS Code environments
- better worker output contracts
- compatibility fixes after VS Code changes
- alternative profiles for smaller organization model allow-lists
- telemetry/evaluation recipes that do not collect source, prompts, secrets, or MCP payloads

## Tool-boundary changes

Before changing an agent's `tools` field, classify the role.

**Inherited-tool roles** intentionally OMIT `tools`:

- Over the Luna
- Luna Tool Worker
- Luna Implementer
- MAI Mechanical
- Kimi Deep Worker

This is required by the current VS Code subagent inheritance path. Do not replace omission with `tools: ['*']` or a built-in-only list.

**Strict roles** must keep explicit allow-lists:

- Luna Explorer
- Luna Researcher
- Luna Reviewer
- Sonnet Reviewer
- Opus Critical Reviewer

Do not add `.mcp.json`, plugin `mcpServers`, or per-agent MCP server configuration for convenience. The harness consumes the developer's existing VS Code environment rather than owning integrations.

The coordinator's inherited tool visibility is an explicit tradeoff. Direct Sonnet environment-tool execution is a `HARNESS_VIOLATION`; ambient inheritance is not permission for Sonnet to implement directly.

When reporting an ambient-tool bug, include VS Code version, Copilot version, plugin version, worker/model, MCP or extension source, exact tool name, whether it works in native Agent, Configure Tools state, server/trust state, and exact error.

## Changing an agent

Explain:

1. What failure mode you observed.
2. Why the change belongs in the harness rather than project-specific instructions.
3. Whether it changes prompt size or expected tool calls.
4. What model(s) and tool environment you tested.
5. Whether it changes inheritance, external side effects, or trust boundaries.
6. What improved and what regressed.

Avoid long examples unless they fix demonstrated behavior. Prompt tokens are part of the product.
