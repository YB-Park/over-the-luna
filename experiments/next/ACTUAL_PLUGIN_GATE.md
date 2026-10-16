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

## Observed result — 2026-10-16

[GitHub Actions #38860678994](https://github.com/YB-Park/over-the-luna/actions/runs/38860678994) **PASS** with CLI 1.0.88 and SDK 1.0.19.

- Exact plugin `over-the-luna-next` reported loaded/enabled.
- SDK agent list included `over-the-luna-next:over-the-luna-next`,
  display name `Over the Luna Next (Research)`.
- RPC agent.select and agent.getCurrent independently confirmed this
  exact selected agent name.
- Then ONE short `gpt-6-luna` request read a public fixture with
  a genuine read permission event and returned the correct marker.
- No writes, shell, external API credentials or corporate data.

**Conclusion:** Actual checked-in plugin package and Main agent can be
loaded, explicitly selected and executed in **pinned Copilot SDK**.
This is stronger than copying the instruction body as a system-message
append. It still does **not** verify the installed VS Code Agent Host
tool/MCP contract or task quality.

Current status: **PASS SDK ACTUAL PLUGIN LOAD + SELECT + PUBLIC READ**.
