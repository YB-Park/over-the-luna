# P0e — Actual Luna Main → Sol subagent, same SDK session

**Question:** Can the *same* GitHub Copilot SDK session run a GitHub-billed
GPT-6 Luna parent and a distinct OpenAI API-billed Sol 6.1 custom subagent?

SDK source contract: [Node SessionConfigBase](https://github.com/github/copilot-sdk/blob/main/nodejs/src/types.ts)
now has **experimental** additive `providers` / `models`, unlike legacy
single `provider`. A selected external model uses a qualified name such as
`openai-sol/gpt-6.1-sol` inside `customAgents[].model`.

This is different from two separately working sessions. The experiment must
observe `subagent.started` and `subagent.completed` along with the child's
selected model, and the parent incorporating its response, before claiming
success. **Copilot Agent Host and the installed plugin are not run here.**

## Safety/validity constraints

- One commit-marker-gated Actions invocation only:
  `ONE_SHOT_MIXED.md` and `[run-mixed-luna-sol-once]`.
- Luna parent uses Actions `GITHUB_TOKEN`; Sol provider uses
  `secrets.OPENAI_API_KEY`. Neither appears in logs or committed files.
- Read-only numeric task; tools limited to `task`, and every other tool
  permission is rejected; child has zero tools.
- One parent prompt, max 90 sec response timeout, one try, job timeout 5 min.
- External provider model output cap 1000 tokens; verify OpenAI billing
  dashboard for actual charges, not the SDK estimate.
- Do not infer child execution solely from a plausible answer;
  lifecycle and selected child model are required.

A pass is evidence of **SDK-level mixed-provider delegation**, not automatic
proof of full VS Code Copilot Agent Host compatibility.

## Observed result — 2026-10-16: PASS

[GitHub Actions run #38851373848](https://github.com/YB-Park/over-the-luna/actions/runs/38851373848)
completed successfully.

- The SAME Copilot SDK session started under `gpt-6-luna`, with an additive
  OpenAI Responses API provider named `openai-sol`.
- Recorded usage sequence: **`gpt-6-luna` → `gpt-6.1-sol` → `gpt-6-luna`**.
- `subagent.started`: `sol-check`, selected model
  **`openai-sol/gpt-6.1-sol`**.
- `subagent.completed`: same model, once, without failure.
- Main exact acceptance: `LUNA_GOT_SOL_17` — PASS.
- Counters: **1 started / 1 completed / 0 failed / 0 rejected tool calls**.
- No repository mutation or external tool use was requested by either model;
  Sol leaf had `tools: []`.
- Both provider routes were exercised with GitHub Actions `GITHUB_TOKEN` and
  `OPENAI_API_KEY`; no raw credentials appeared in test output.
- Cost totals were **not** captured; Copilot and OpenAI API dashboards are
  billing sources of truth. This was a small correctness-of-routing probe,
  **not** a cost-effectiveness or model-quality experiment.

**Decision:** the SDK's **experimental additive multi-provider API actually
supports Luna Main → OpenAI Sol leaf within one session**. This removes the
need to invent a separate model-bridging engine for SDK-only execution.

**Important remaining question:** Can the SAME provider registry / qualified
model identity be supplied by the existing VS Code **Copilot Agent Host**
plugin format? The SDK result is not proof that VS Code exposes or preserves
the necessary `providers` / `models` fields in plugin loading. DO NOT
ship or advertise live-plugin mixed routing until that is separately observed.

Status: **PASS SDK MIXED DELEGATION / VS CODE PLUGIN UNKNOWN**.
