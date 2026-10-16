# P0c — OpenAI direct Sol key + inference gate

User added the repository-level Actions Secret **OPENAI_API_KEY**. This is
an **OpenAI API** credential, not an OpenRouter key or a GitHub Copilot
account token. It must never be copied into this repository or the chat.

Official model documentation: https://developers.openai.com/api/docs/models/gpt-6.1-sol
- API model ID: `gpt-6.1-sol`
- Endpoint: `https://api.openai.com/v1/responses`
- Standard rates: input $2/M tokens and output $10/M tokens.
- Sol supports low/medium/high/xhigh/max reasoning effort, not none.

## Strict gate

The GitHub Actions workflow `.github/workflows/openai-sol-one-shot.yml`
only runs when BOTH conditions hold:
1. A push changes `experiments/next/ONE_SHOT_OPENAI_SOL.md`.
2. The head commit message includes `[run-openai-sol-once]`.

It uses the short-lived job environment to read `secrets.OPENAI_API_KEY`,
first GETs `/v1/models/gpt-6.1-sol` (non-inference), then sends exactly
**one** small Responses API request if the model metadata gate succeeds.
`reasoning.effort=low`, `max_output_tokens=256` including reasoning,
`store=false`, `tools=[]`; no automatic retry and no shell/tool access
for the model. The script does not print raw response bodies, API keys or
request payloads. A tiny standard-rate cost estimate and token totals are
printed; actual API billing must be confirmed in the OpenAI dashboard.

A key can exist but lack project permission, billing balance, sufficient
tier, or access to this model. Treat those cases as **BLOCKED**, not as
evidence of poor model quality. Do NOT repeatedly retry a denied request.

## What the result will and will not prove

PASS means this particular GitHub Actions project credential can reach
**the direct OpenAI Sol API** and complete a bounded prompt. It does NOT
prove Copilot Agent Host supports that provider, that Luna Main can delegate
to OpenAI-hosted Sol, or that Sol improves coding/review quality.

After PASS, the next separate gate is Provider BYOK in a Copilot SDK
session (isolated from the ordinary Luna session), followed by VS Code
Agent Host and mixed-provider delegation. No plugin architecture changes
until these constraints are observed.

## Observed run: 2026-10-16

- [GitHub Actions #38849783651](https://github.com/YB-Park/over-the-luna/actions/runs/38849783651)
- Secret was present and supplied by Actions. The GET
  `/v1/models/gpt-6.1-sol` returned exact metadata, so the token works for
  model metadata access.
- One bounded POST `/v1/responses` returned
  **HTTP 429 `credit_balance_exhausted`** before a successful completion.
- Classification: **BLOCKED — OpenAI API prepaid organization balance**.
  Model inference identity, output, latency, token cost, model entitlement
  beyond metadata are **NOT YET TESTED**.
- No automatic retry. Do not repeat the request until the user funds the
  matching OpenAI API organization and confirms the prepaid balance is ready.
  Billing overview: https://platform.openai.com/settings/organization/billing/overview
- This is separate from the already-working GitHub Copilot Luna account,
  and from OpenRouter. Avoid enabling auto-recharge without deliberate choice.

Status: **BLOCKED by prepaid balance, model metadata PASS; inference NOT RUN SUCCESSFULLY**.


## Funded single retry: 2026-10-16 — PASS

- [GitHub Actions #38850785950](https://github.com/YB-Park/over-the-luna/actions/runs/38850785950): completed successfully, one Responses API inference request, no retries.
- Exact observed model: `gpt-6.1-sol` (not only the requested model).
- Model metadata: `gpt-6.1-sol`, PASS.
- Prompt acceptance: exact `SOL_API_OK`, PASS.
- `reasoning.effort=low`, `max_output_tokens=256`, `tools=[]`, `store=false`.
- Usage: **20 input tokens**, **7 output tokens**.
- Standard non-cached token-rate estimate: **$0.000110**. Actual billed amount should be checked in the OpenAI API dashboard.
- **Decision**: Direct OpenAI Sol credential and inference path **PASS**. This verifies the Actions-secret / OpenAI Responses API path, NOT the Copilot SDK provider bridge, VS Code Agent Host, or mixed Luna/Sol delegation.
- **Next gate**: one isolated, separately authorized Copilot SDK `provider: {type: "openai", wireApi: "responses"}` session; keep its provider credentials isolated from the ordinary GitHub-hosted Luna path.
