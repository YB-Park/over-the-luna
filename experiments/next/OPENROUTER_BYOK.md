# OpenRouter Sol BYOK feasibility (2026-10-16)

Status: **DOCUMENTATION CONFIRMED / NO OPENROUTER CALL RUN / MIXED HOST DELEGATION UNVERIFIED**.

## Why this research exists

GPT-6.1 Sol was **absent** from the 17 models returned by our short-lived
GitHub Actions Copilot SDK account catalogue, even though GPT-6 Luna,
Haiku 5.5 and Sonnet 5.5 were listed. Lack of presence in that catalogue
does **not** imply the OpenRouter API lacks the Sol model.

Goal: retain GitHub Copilot Luna for the economical baseline while
investigating OpenRouter-funded Sol as a targeted strong-model option.
Do not switch all tasks to a paid API or ship a private-key-specific
plugin design.

## Confirmed facts

1. OpenRouter lists `openai/gpt-6.1-sol` and publishes input/output token
   rates of $2/$10 per million in its normal tier. See:
   https://openrouter.ai/openai/gpt-6.1-sol
2. OpenRouter is pay-as-you-go, not an additional Copilot seat. Standard
   credit purchases have a 5.5% platform fee. See:
   https://openrouter.ai/pricing
3. Copilot CLI officially supports BYOK through
   `COPILOT_PROVIDER_BASE_URL`, `COPILOT_PROVIDER_API_KEY`,
   `COPILOT_PROVIDER_TYPE=openai` and `COPILOT_MODEL`. Its
   `providers.json` can also define a provider/model registry, which
   takes precedence over legacy variables. See:
   https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-cli
4. Copilot SDK `createSession({model, provider})` accepts an
   OpenAI-compatible endpoint and explicit model ID. BYOK usage belongs
   to the provider, rather than Copilot premium requests:
   https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md
5. VS Code supports **Custom Endpoint** models. BYOK model use inside
   Copilot Agent Host is experimental and requires enabling
   `chat.agentHost.byokModels.enabled`; exact behavior may change:
   https://code.visualstudio.com/docs/agent-customization/language-models

## Proposed local/Actions environment (not executed)

- Base URL: `https://openrouter.ai/api/v1`
- Provider type: `openai`
- Explicit model ID: `openai/gpt-6.1-sol`
- Secret: `OPENROUTER_API_KEY` stored in GitHub **Actions Secrets** for
  Actions usage, or VS Code's provider credential store for local use.
  Never commit, display, or share a raw key.
- In Actions, pass the secret via `COPILOT_PROVIDER_API_KEY`, and keep
  provider settings scoped to a **separate** process/job. Do not put BYOK
  provider settings on ordinary Copilot Luna baseline jobs.
- The Copilot CLI's `--max-ai-credits` is **not** an OpenRouter spending
  cap; use OpenRouter per-key spending limits and a low prepaid balance.
- Capture the *actual* OpenRouter request usage/cost and resolved model;
  do not confuse external provider charges with Copilot AI Credits.

## Small next gates (explicitly opt-in only)

- **B0**: Check the OpenRouter key's restricted budget and confirm the
  model is available via its public model endpoint. No inference.
- **B1**: One tiny provider-routed Sol prompt via separate CLI/SDK job,
  no shell/write tools, only after a user supplies their own key through
  GitHub Secrets and authorizes the experiment. Prove stream/tool
  compatibility and effective model identity; stop on an API error.
- **B2**: Select the same custom Sol model via VS Code Custom Endpoint,
  enable experimental Agent Host BYOK, and verify observed model/effort,
  tools, permission boundaries with a harmless session.
- **B3**: Check whether **GitHub-hosted Luna Main -> OpenRouter Sol
  subagent** works in a *single Copilot Agent Host session*. Do not
  assume support from CLI or SDK per-session BYOK, and do not work around
  the host by silently creating an additional execution engine.
- **B4**: Only after B3, run one decision-relevant coding/review task and
  compare against Luna-only with genuine total provider cost.

## Decision

**OpenRouter is a viable alternative funding/provider route**, but
**mixed-provider delegation in our shipped plugin is NOT YET PROVEN**.
Do not migrate the plugin or incur recurring charges for a hypothetical
advantage. Keep Luna-first and maintain the original research stop rules.
