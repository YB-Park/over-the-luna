# P15 — authenticate Copilot provider identity and create a native AHP session

P14 proved actual VS Code AHP 1.0.0 initialize with 2 advertised providers
but its first root projection incorrectly expected the id copilot.
The source-defined ID is copilotcli:
https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/common/agent.ts

P15 reuses the **real code agent host** (not the standalone SDK), then
creates a disposable AHP Copilot session in this public repository through
createSession(provider=copilotcli). It sends NO chat/turnStarted action,
and the workflow has only contents:read permission. No paid model request.

Outcomes: COPILOT SESSION READY means Host session initialization happened,
not plugin-loaded RC2 Main or named Architect completion. Missing credentials
or unavailable SDK should report blocked/inconclusive without circumventing
organization permissions or adding BYOK. The session is disposed after the
probe; output is a metadata-only summary without bearer tokens, agent
transcripts, model prompts, paths, account identifiers or internal code.

Provenance: AHP createSession parameters are defined by
https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/common/state/protocol/channels-session/commands.ts
and AHP lifecycle by https://microsoft.github.io/agent-host-protocol/guide/getting-started.html

One-shot trigger: docs/P15_HOST_SESSION_SENTINEL.md with commit message
[p15-host-session-once]. Do not retry a blocked provider by running the
previous unsupported standalone SDK plugin-agent test. No merge/release.

## P15 verified initialization boundary (2026-10-19)

First [no-token P15 run](https://github.com/YB-Park/over-the-luna/actions/runs/39187067070) negotiated AHP 1.0.0, observed `copilotcli`, had `createSession` accepted and a real session subscribed, but **did not observe Ready** in the observation window (SESSION_NOT_READY). This is not a named-agent success or model failure. Source shows the Copilot agent uses SDK credentials, potentially inherited from approved runtime context. The next **zero-turn** run passes the job-scoped GitHub Actions `GITHUB_TOKEN` and `copilot-requests: write` only to the official local VS Code Host process and captures an allowlisted lifecycle scalar and error code. No role calls or chat turns; no external BYOK or corporate code.
