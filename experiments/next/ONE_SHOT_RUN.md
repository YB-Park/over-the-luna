# Intentional one-shot probe — 2026-10-16

This file is a deliberate trigger for **one** Copilot CLI GPT-6 Luna auth probe in the research branch.
The CLI job uses a soft 30 AI Credit response cap (the CLI's current minimum; normally far more than this short prompt needs), a short fixed prompt, tool restrictions and an 8-minute job timeout.
No agent implementation or repository mutation is requested from the model. The token comes from GitHub Actions `GITHUB_TOKEN`; no PAT is stored.
This is a one-time probe, not the start of recurring AI evaluations.

2026-10-16 retry: initial run rejected 2-credit flag before sending a model request; retry with current CLI minimum 30-credit soft limit.

Trigger outcome: inspect the corresponding GitHub Actions run. Do not rerun until the result and account policy are understood.
