# One-shot OpenAI GPT-6.1 Sol direct API gate

Authorized research-only execution on 2026-10-16.

Goal: verify repository-level `OPENAI_API_KEY` Actions Secret can access `gpt-6.1-sol`, then perform exactly one short, low-reasoning model response with output capped at 256 tokens. There are no model tools, no automatic retries, and no repository mutation by the model. The API key remains in Actions Secrets and is never printed.

This is not proof of Copilot Agent Host mixed-provider support and should not be automatically repeated.
