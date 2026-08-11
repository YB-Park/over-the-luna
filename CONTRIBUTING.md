# Contributing

Contributions are welcome, especially evidence from real VS Code/Copilot usage.

## Principles

Please preserve the project's core constraints:

- human-guided, not swarm-by-default
- concise agent prompts
- no hidden premium-model escalation
- **strict roles stay narrow; designated execution roles preserve ambient user tools**
- do not bundle or take ownership of user MCP servers, credentials, or trust policy
- arbitrary MCP/extension compatibility is an architecture contract for ambient-capable workers
- external side effects are never inferred from a coding task
- routing changes should have a measurable reason
- GitHub Copilot models and VS Code behavior change quickly, so cite current official docs when changing compatibility claims

## Useful contributions

- model-routing experiments
- MCP/extension-tool compatibility reports from real VS Code environments
- better output contracts for workers
- compatibility fixes after VS Code changes
- alternative profiles for organizations with a smaller model allow-list
- telemetry/evaluation recipes that do not collect source code, prompts, secrets, or MCP payloads

## Ambient-tool changes

Before changing `tools` on an agent, classify the role:

- **strict role**: coordinator, explorer, public researcher, reviewer → keep the exact narrow tool boundary
- **ambient role**: Luna Tool Worker, Luna Implementer, MAI Mechanical, Kimi Deep Worker → keep exactly `tools: ['*']`

Do not replace the wildcard with a list of built-in tools or a few known MCP server names. That silently breaks users whose MCP/extension tools have different names.

Do not add `.mcp.json`, `mcpServers`, or per-agent MCP server configuration to make a local setup convenient. This project intentionally consumes the developer's existing VS Code tool environment rather than owning it.

When reporting an ambient-tool bug, include VS Code version, Copilot version, plugin version, worker/model, MCP or extension source, exact tool name, whether it works in native Agent mode, permission level, and the exact error.

## Changing an agent

When modifying an agent, explain:

1. What failure mode you observed.
2. Why the change belongs in the harness rather than in project-specific instructions.
3. Whether it increases prompt size or expected tool calls.
4. What model(s) and tool environment you tested.
5. Whether it changes external side-effect or trust boundaries.
6. What improved and what regressed.

Avoid adding long examples unless they fix a demonstrated behavior. Prompt tokens are part of the product.
