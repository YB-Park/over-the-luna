# Over the Luna v1.1 — schema-strict VS Code Gate A fallback

Branch: `rc/v1.1-vscode-gate-schema`  
Status: **fallback integration candidate; not a release**

Use this branch only if the leading ambient candidate fails a real VS Code product-critical gate around `agent/runSubagent` availability or arbitrary custom-agent selection.

## Wiring

Main explicitly declares:

- built-in tools: `read`, `search`, `edit`, `execute`, `agent`, `todo`, `web`;
- exact Council `agents`: Luna Planner, Architect, Skeptic, Researcher, Tool Worker, Recovery, Reviewer.

This gives a structural subagent allow-list and follows VS Code's documented requirement that a custom agent using `agents` also includes the `agent` tool.

The tradeoff is intentional and must be measured: Main's explicit tool list may not preserve arbitrary developer-selected MCP/extension tools without additional configuration. This is a regression risk against the v1.0 MCP contract, which intentionally lets VS Code own selected integration tools.

Do **not** add `'*'` as a compromise. The automated Gate A wildcard experiment used Copilot CLI 0.0.420, which reported `Invalid tool '*'`; a registered local MCP echo marker was unavailable in 2/2 runs.

## Compare against ambient

Run the same real VS Code checks as `rc/v1.1-vscode-gate-ambient`, especially:

1. plugin discovery/diagnostics;
2. broad unknown discovery selects Luna Architect;
3. developer-selected MCP/extension tool remains usable or becomes unavailable;
4. leaf tool restrictions;
5. Main-only mutation ownership;
6. `SIMPLE + NONE`, `SIMPLE + REVIEW`, `STANDARD + REVIEW`, and `RISK` behavior;
7. one exact-name `Premium Review`, `send:false`;
8. Agent Debug/OTel agent and tool ownership.

A schema-strict win requires more than cleaner agent selection: it must either preserve developer-selected tools sufficiently or demonstrate that the ambient candidate creates an unacceptable orchestration safety/reliability problem that outweighs the compatibility regression.

`plugin.json` remains `1.0.0` throughout this gate. Do not release or merge to `main` from this branch.
