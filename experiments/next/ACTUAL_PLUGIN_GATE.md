# P3: actual candidate plugin loading and activation — SDK

## Decision-critical gap

The previous P2 experiment compared **a copy of the Next Main's
instructions appended to SDK**, not an actual plugin registration. This
P3 gate uses the actual checked-in candidate `plugin.json` and
`agents/over-the-luna-next.agent.md`, without reimplementing its prompt
inside a separate custom-agent configuration.

Before any billable inference:
1. Register exact candidate directory with `pluginDirectories`.
2. Call `session.rpc.plugins.list()` and require the named enabled plugin.
3. Call `session.rpc.agent.list()`, locate the loaded agent.
4. Call `session.rpc.agent.select()` and `getCurrent()` and require
   an exact selected identity.

**Only if metadata gates pass**, send a single read-only, short
`gpt-6-luna` request against a disposable **public-data** file, require
an actual file-read permission event, observed model usage, and a marker
returned from that file. Deny writes, shell, MCP and subagents.

This test is not a proof of full VS Code Agent Host functionality,
model-availability in the user's corporate environment, or model
quality. The user has already verified the agent appears in their
picker and a local read-only check had no reported anomalies.

**One shot**, commit marker `[run-actual-plugin-gate-once]` and modified
`ONE_SHOT_PLUGIN_GATE.md`. No automatic retries. Version-pinned
Copilot CLI and SDK. Do not report PASS from plugin registry alone.

Current status: NOT RUN.
