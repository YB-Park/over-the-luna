# P0d — Copilot SDK → direct OpenAI Sol BYOK (isolated, one-shot)

**Product decision:** Does the *Copilot SDK*, not just direct OpenAI
Responses API, accept `OPENAI_API_KEY` and create a model session with
`gpt-6.1-sol`?

Control evidence:
- [Direct OpenAI Sol API PASS, 2026-10-16](https://github.com/YB-Park/over-the-luna/actions/runs/38850785950): actual model `gpt-6.1-sol`, exact short response, 20 input + 7 output tokens.
- Official BYOK runtime config: https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md

One opt-in invocation requires a push of
`experiments/next/ONE_SHOT_SDK_BYOK.md` **and** head commit marker
`[run-sdk-sol-once]`. The action is otherwise silent.

The Node SDK session is isolated from the GitHub Copilot Luna session:
`model: "gpt-6.1-sol"`, `reasoningEffort: "low"`,
`provider: { type: "openai", baseUrl: "https://api.openai.com/v1",
apiKey: process.env.OPENAI_API_KEY, wireApi: "responses" }`.
No model tools or repository modifications are authorized.
Only one short prompt, with a 55-second SDK response timeout and a
5-minute job timeout, no retries. **SDK does not provide the direct
Responses API output cap used in P0c here; tiny prompt and one-shot
policy bound ordinary use, but not absolute spend**. OpenAI's project
budget/credit balance remains the meaningful external limit.

PASS proves SDK single-provider BYOK transport and requested short
answer only; a configured model ID is *not independent provider-side
proof*. It does not prove VS Code Copilot Agent Host BYOK compatibility
or Luna-Copilot Main → OpenAI Sol subagent execution.

Status: prepared, not yet run.
