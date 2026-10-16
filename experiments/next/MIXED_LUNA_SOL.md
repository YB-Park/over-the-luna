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

Status: NOT RUN.
