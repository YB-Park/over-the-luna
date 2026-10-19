# P14 — authentic VS Code Agent Host AHP zero-inference gate

**Purpose:** Move beyond P5 standalone SDK, which registered plugin roles
but did not complete named subagents because the standalone server
rejected the custom_agent_prompt session effect.

P14 boots the official Linux CLI via code agent host on an isolated
GitHub Actions machine, discovers its authenticated localhost endpoint
and negotiates AHP initialize. It observes whether the root channel
advertises Copilot. No chat turns, model messages, provider credentials
or copilot-requests: write permission. No corporate content is involved.

Sources:
- https://code.visualstudio.com/docs/agents/concepts/agent-host
- https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/LOCAL_ENDPOINT.md
- https://microsoft.github.io/agent-host-protocol/guide/getting-started.html
- https://code.visualstudio.com/docs/supporting/faq

**Evidence levels:** successful AHP connection is a real Host transport
check, NOT proof of RC2 plugin load, named Architect or Reviewer
completion, model identity, effective permissions or cost advantage.
CLI bootstrap failure or absent provider means INCONCLUSIVE or BLOCKED;
don't silently revert to SDK for the Council inference claim.

Security: no endpoint token, socket address, raw session, login keys,
model prompts or organization logs in GitHub artifact or stdout.
Bind localhost only. Never use GitHub tunnel, company data or BYOK.
The no-model probe may be followed by an authentic paid Host task
ONLY after adapter authentication and named plugin discovery work.

One-time workflow trigger: create docs/P14_HOST_AHP_SENTINEL.md with
commit marker [p14-host-probe-once]. No automatic repetitions, merge or release.
