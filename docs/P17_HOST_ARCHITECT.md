# P17 — one bounded genuine VS Code Host Architect delegation trial

**Decision:** P16 [Actions #39189246326](https://github.com/YB-Park/over-the-luna/actions/runs/39189246326)
verified the actual VS Code Host parses and LOADS all eight RC2 roles
through the documented `vscode-agent-host-file` plugin URI.
P15's lingering `creating` with no turn is expected lazy materialization.
This is now the first justified *real Host model request* gate,
not another default SDK-vs-Luna test.

One authenticated Host created on an isolated public Actions runner.
Native AHP session publishes RC2, checks exact eight role names, selects
Over the Luna Next Main, requests explicit GPT-6 Luna (not premium) and
sends one public read-only question about validate_release.py,
package_release.py and the ZIP allowlist. The prompt asks Main to call
named Next Architect once and return a separate file-grounded evidence packet.
Job has a 6 minute cap, no retries, no BYOK, no company data, and no
credential or transcript export. The public checkout is the only workspace.

**Evidence ladder:** Host launched < plugin loaded < turn submitted <
task tool started < arguments identify Next Architect < task completed
successfully < returned public source-specific packet < Main completes.
Partial steps MUST NOT be labeled successful Council handback.
Output contains only booleans, status categories, a requested model label
and sanitized counters; no internal prompts, token secrets, tool outputs,
session IDs, or raw source code. Report Copilot metering only if actually
provided; do not infer a price or broad quality advantage.

Authorization: only GitHub Actions job-scoped official Copilot permission
passed to the Host subprocess; no private OAuth acquisition, login or
provider substitution. If the runtime emits auth/required or cannot
execute a named task, result is BLOCKED or INCONCLUSIVE. Do not rerun
the unsupported standalone SDK custom_agent_prompt attempt.

One shot only: docs/P17_HOST_ARCHITECT_SENTINEL.md and a push marked
[p17-native-architect-once]. No stable main changes or release merge.

## Recorded first paid-eligible native Host turn — 2026-10-19

[Real GitHub Actions #39189500097](https://github.com/YB-Park/over-the-luna/actions/runs/39189500097):

- Official Host and AHP initialized; Copilot \`copilotcli\` advertised;
  real session created and subscribed.
- Corrected host-local RC2 plugin \`loaded\`; **8/8 role names**, including
  Main and Next Architect, verified in the authoritative session state.
- One real AHP \`chat/turnStarted\` submitted with selected Main's native
  agent URI and explicit \`gpt-6-luna\` request, using public files only.
- **\`chat/error\` received**. No \`task\` start, completed task,
  independent returned Architect packet, or normal main turn completion.
- This is **INCONCLUSIVE/BLOCKED**, not native delegation success and
  not evidence of model quality. The event has not been causally
  attributed to auth, model availability, permission or another source.
- No premium calls or extra paid repetitions were conducted. A
  paid-eligible Host turn was submitted but completed model usage and
  billing are not observable in the sanitized artifact.

**Product decision:** Do not add more agents, remove Skeptic/Recovery,
revise all model assignments, or release RC2 based on this. The next
genuine Host verification must observe a completed named leaf and
returned source-backed packet. A coarse \`chat/error\` classifier was
added to the repo after P17 to improve future diagnostics without
reprinting error messages; it was not retroactively available for this
run. Respect signed-in Copilot provider and organization policy.

