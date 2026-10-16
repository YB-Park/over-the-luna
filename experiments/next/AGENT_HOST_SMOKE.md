# P0b: VS Code Copilot Agent Host smoke — manual runtime observation

This is a **small product compatibility test, not a performance benchmark**. The GitHub Actions CLI smoke verified that the short-lived Actions token can make a Copilot request. It did not run VS Code Agent Host or load the plugin.

## What to verify in actual VS Code

1. Record VS Code version, Copilot extension/Agent Host build, GitHub Copilot plan if known, plugin commit or version. Select **Copilot**, not Claude, as the Agent Host.
2. Confirm a known installed Over the Luna agent is visible and actually selectable. Check whether the selected model is **GPT-6 Luna** when using the generated model-only candidate; do not confuse the unchanged main v1.1.1 (GPT-5.6 Luna) with the candidate.
3. Run one harmless bounded **read-only** request. Record whether the Host shows the actual model, model selection warning, effort setting and the name of any delegated agent. No file edits/pushes/external actions are needed.
4. For an existing harmless user-permitted selected MCP tool, check whether it remains reachable without embedding credentials in the plugin. Check that strictly read-only leaves cannot call mutation tools; do not loosen organization policy to make a test pass.
5. Record the observed outcome below and stop if the runtime rejects the model or tools. No repeated trial-and-error calling to discover billing behavior.

## Evidence to capture, without credentials

| Field | Observation |
| --- | --- |
| VS Code / Copilot Agent Host version | NOT RUN |
| Active plugin version / agent name | NOT RUN |
| Requested model vs observed model | NOT RUN |
| Requested reasoning effort vs observed effort | NOT RUN |
| Subagent model/identity observed | NOT RUN |
| Selected harmless MCP read tool behavior | NOT RUN |
| Permission / external-effect boundary | NOT RUN |
| Cost/credits displayed, or UNKNOWN | UNKNOWN |
| Environment verdict | NOT RUN |

## Release gate

Do not equate a GitHub Actions CLI success with VS Code Agent Host compatibility.
Do not redesign the agent topology or remove Premium Review until live functionality is observed and the alternative provides value.

Evidence links: [CLI auth pass](https://github.com/YB-Park/over-the-luna/actions/runs/38836438484) · [SDK model listing](https://github.com/YB-Park/over-the-luna/actions/runs/38836601586).
