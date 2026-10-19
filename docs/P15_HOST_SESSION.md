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
