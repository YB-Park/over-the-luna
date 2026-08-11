# Contributing

Contributions are welcome, especially evidence from real VS Code/Copilot usage.

## Principles

Please preserve the project's core constraints:

- human-guided, not swarm-by-default
- concise agent prompts
- no hidden premium-model escalation
- narrow tools per role
- routing changes should have a measurable reason
- GitHub Copilot models and VS Code behavior change quickly, so cite current official docs when changing compatibility claims

## Useful contributions

- model-routing experiments
- better output contracts for workers
- compatibility fixes after VS Code changes
- alternative profiles for organizations with a smaller model allow-list
- telemetry/evaluation recipes that do not collect source code or prompt contents

## Changing an agent

When modifying an agent, explain:

1. What failure mode you observed.
2. Why the change belongs in the harness rather than in project-specific instructions.
3. Whether it increases prompt size or expected tool calls.
4. What model(s) you tested.
5. What improved and what regressed.

Avoid adding long examples unless they fix a demonstrated behavior. Prompt tokens are part of the product.
