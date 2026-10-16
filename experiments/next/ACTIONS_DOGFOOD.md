# P2 - GitHub Actions replaces local corporate dogfood

**Reason for change:** the user works inside a corporate environment and
cannot easily export VS Code chat results, diffs, code or logs. **Do not
ask them to transfer internal files or repeatedly run local experiments.**
The prior [local two-worktree guide](DOGFOOD_TASK_01.md) is now an optional
reference, not a required user task.

## What this measures

Two **separate Copilot SDK sessions** on GitHub Actions, not two VS Code
Agent Host executions:

1. `sdk_default`: unmodified SDK default system prompt and agent.
2. `next_instructions`: the **exact checked-in body** of the one-agent
   [Next candidate](candidate-plugin/agents/over-the-luna-next.agent.md)
   appended to the SDK's own base system message.

Both use the same `gpt-6-luna`, reasoning effort `low`, fixed
`view/read_file/edit_file/apply_patch/grep/glob` allowlist and matching
filesystem permission handler. No shell, web, Git write or subagents.
**This comparison tests the incremental value of the real Next instructions
under matched SDK conditions.** It does **NOT** reproduce the entire
VS Code native Agent vs installed Next plugin, including all Host
configuration, MCP, tool approvals and agent-picker semantics.

Official SDK docs support
[system-message append](https://github.com/github/copilot-sdk/blob/main/nodejs/README.md)
and per-session tool selection. A full plugin directory can separately
be loaded using
[pluginDirectories](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/plugin-directories),
but this experiment is intentionally controlled on instructions only.
No independently verified Host quality claim is allowed.

## Real task

Use the first useful production-research improvement proposed in
[DOGFOOD_TASK_01.md](DOGFOOD_TASK_01.md): implement an optional
`--root PATH` on `scripts/validate_candidate.py` and Python stdlib
unittest coverage for unsafe candidate mutations. Unlike the earlier
flawed benchmark, the external `action_pair_grader.py` independently
runs the authored tests, explicitly exercises the positive case and
seven negative mutations, and checks source/test edit scope.
The models cannot access the grader through their tools because it is
outside their temporary workspaces and no shell tools are available.
The grading subprocess inherits **no GITHUB_TOKEN, OPENAI_API_KEY or
Copilot credentials**.

Original candidate and validation scripts are copied into two isolated
temporary directories from the same Git SHA. Only the public-repo
`scripts/validate_candidate.py` and `tests/test_validate_candidate.py`
may be changed. All actual modified files are retained in a short-lived
artifact along with outcome, grader, version, actual model usage, token
metrics, latency, permission and tool metadata. Neither model can
push, create PRs, or modify the checkout.

## Spend and repeat control

Workflow `.github/workflows/actions-dogfood-once.yml` runs only when:

- the pushed change includes `ONE_SHOT_ACTIONS_DOGFOOD.md`, AND
- that head commit message contains `[run-actions-dogfood-once]`.

At most **two** GPT-6 Luna SDK sessions; one fixed prompt per arm;
105-second response timeout per arm; 11-minute job budget; no retries.
Copilot usage is separately metered in credits; no OpenAI API BYOK
credential is used. This is not an absolute dollar charge cap.

Node packages are pinned to `@github/copilot@1.0.88` and
`@github/copilot-sdk@1.0.19` so later runs don't silently compare
different library updates; do not repeat this run without a justified
decision. The result artifact is preserved for 30 days, not committed
as unreviewed product code.

## Interpretive discipline

- Successful workflow with `quality=false` means the **study ran**,
  not that the model completed the requirements.
- One pair is **a case study**, not statistical proof.
- If the SDK-only Next instructions do not help, that is evidence
  against extra prompt complexity, but does not prove the installed
  VS Code plugin lacks value.
- If they help, the next step is a cautious candidate design decision,
  not automatic publication or addition of new agents.
- Corporate Host behavior remains **user-reported smoke only**:
  selectable and first read-only task showed no anomalies.

**Status:** prepared; no paid request sent by this document.
