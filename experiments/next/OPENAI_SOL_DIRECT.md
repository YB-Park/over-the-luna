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

Status: NOT RUN.
