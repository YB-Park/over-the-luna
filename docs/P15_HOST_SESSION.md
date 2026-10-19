# P15 — authenticate Copilot provider identity and create a native AHP session

## Correction: no-turn \`creating\` was a false blocker

The earlier conclusion that a ready state was required before any chat
turn was incorrect. Official VS Code sources document provisional
sessions materialized **on the first send**; idle no-turn sessions may
stay at \`creating\` indefinitely by design. This neither proves nor
disproves whether the injected GitHub job token would authenticate an
actual model turn.

The correct later observations are P16's **8/8 native Host RC2 roles
loaded** and P17's **single actual first-turn \`chat/error\` before
named Architect task**, with unknown root cause. See
[updated Host evidence gate](HOST_DELEGATION_GATE.md).

P14 proved actual VS Code AHP 1.0.0 initialize with 2 advertised providers
but its first root projection incorrectly expected the id copilot.
The source-defined ID is copilotcli:
https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/common/agent.ts

P15 reuses the **real code agent host** (not the standalone SDK), then
creates a disposable AHP Copilot session in this public repository through
createSession(provider=copilotcli). It sends NO chat/turnStarted action,
and no chat inference is permitted. The first workflow had only contents:read permission. No paid model request.

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

## Final P15 result and stop rule

[P15 job-scoped GitHub Copilot token #39187238270](https://github.com/YB-Park/over-the-luna/actions/runs/39187238270)
again confirmed native `copilotcli`, `createSession` acceptance, session
subscription, and initial lifecycle `creating`, but **not `ready`**.
Both P15 runs used zero chat turns, zero model requests, and no company
data. The second granted only the official GitHub Copilot job-scoped
token; it was **not evidence of a signed-in user OAuth session**.

Current VS Code specifies `gitHubCopilotResource` as a GitHub protected
resource with scope metadata `read:user` and `user:email`. The AHP
`authenticate` command is defined for credentials obtained from that
resource's authorization server; no such authorized user credential was
available in the ephemeral runner. We did **not** inject an unverified
credential, change auth policy, or claim authentication was the observed
root cause of the pending session.

**Decision:** No more paid standalone tests, role-ratio grids or blind
Host bootstrap retries. The next product-value gate needs an actual
authorized Host session that reaches `ready`, plus an observed named
Architect handback; only then should we spend on genuine complex Council
collaboration. Superseded status: the no-turn session was PROVISIONAL,
not a proven login failure; P17 later submitted a first turn but received
`chat/error` before any named task started.
