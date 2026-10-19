# P18 — preflight live Copilot Host model catalog, no inference

P17 #39189500097 submitted one real public Host turn, which returned
`chat/error` **before** `task` started, but raw errors were intentionally
never exported and so the root cause remains unknown.

The AHP `AgentInfo.models` list is the authoritative backend-advertised
catalog (per VS Code `channels-root/state.ts`). Copilot's
`_listModels` calls SDK `models.list` with a GitHub token; a missing
model ID may cause the Host to reject `chat/turnStarted`.
P17 selected `gpt-6-luna` without checking this precondition.
This is a **hypothesis, not the established cause**.

P18 boots the official Host in the same kind of public GitHub Actions
runner with the job-scoped GitHub permission, but **only initializes
AHP and reads the root model catalog**. It performs no session creation,
chat turn, model request, plugin mutation, provider switch or BYOK.
It publishes only aggregated model counts, whether the exact requested
Luna model is advertised and enabled, whether Auto is present, whether
disabled models exist, and a count of protected resources.
There are no model listings, tokens, error messages, account details,
host endpoints or private files in public output.

Gating rule: even if Luna is advertised, it is not proof that the
GitHub Actions token can execute a turn. If Luna is not advertised,
do **not** blindly resubmit P17 with a different model. Distinguish
backend/model availability from credential or local agent initialization.

Relevant upstream:
- https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/common/state/protocol/channels-root/state.ts
- https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/copilot/copilotAgent.ts

One-shot trigger: docs/P18_MODEL_CATALOG_SENTINEL.md with commit marker
`[p18-model-catalog-once]`. Keep main/RC1/PR unmerged.
## Actual P18 result — 2026-10-19

[Workflow #39197886981](https://github.com/YB-Park/over-the-luna/actions/runs/39197886981)
**SUCCESS** on a real localhost-only VS Code Host:
`ahpInitialized: true`, `copilotAdvertised: true`,
`copilotModelCount: 0`, `lunaExactAdvertised: false`,
`autoModelAdvertised: false`, `protectedResourceCount: 2`.
No session created, no plugin published and **zero model turns**.

The same CI runner type and official job-scoped GitHub Copilot
permission were used, but one cannot assert that the precise
P17 `chat/error` originated from a model mismatch: that P17
error type was not recorded. Do not blindly select Auto when the
catalog also lacks Auto. Do not relay private user tokens.
New code now checks advertised Luna before sending any turn.
