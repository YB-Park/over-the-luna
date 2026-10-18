# Over the Luna Next — real Copilot Agent Host delegation gate

**Product decision gate; not a synthetic model benchmark.** No company files, chat transcripts, logs, credentials or model spend details must be exported outside the user's organization. The owner's company VS Code remains their everyday working environment, not a test-data supplier.

## Why a Host gate exists

- [P5 code task](https://github.com/YB-Park/over-the-luna/actions/runs/38869234496) produced valid fixes in both SDK arms. The plugin arm attempted `task` twice but no leaf completed.
- [One-shot causal diagnostic](https://github.com/YB-Park/over-the-luna/actions/runs/38870191856) resolved the exact qualified `over-the-luna-next:next-architect` identity and model, then reported `Standalone server does not support session effect 'custom_agent_prompt'`.
- [VS Code custom-agent docs](https://code.visualstudio.com/docs/agent-customization/custom-agents) state that `user-invocable: false` hides a selectable agent while `disable-model-invocation` controls availability for other agents. [Copilot harness subagent docs](https://code.visualstudio.com/docs/agents/run/subagents) describe a harness-native delegation path, distinct from the **Local** harness's `agent/runSubagent`.
- The [VS Code SDK conversion path](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/copilot/copilotPluginConverters.ts) passes plugin agent prompts/models/non-empty tool lists into SDK. This does not prove effective Host approvals and does not make `agents: []` a guaranteed recursion sandbox.

## Acceptance flow: Main → Architect → Main

For this narrow read-only check, Main requests one Architect observation, Architect returns the packet, and Main assesses it. Reviewer is excluded until a real diff exists.

## Optional single check, only with PUBLIC repository content

This is a **single optional read-only check**, not an expectation of repeated local trials. When the owner already has a public copy of `YB-Park/over-the-luna` in VS Code, select the **Copilot** Agent Host (not Local) and **Over the Luna Next** from the RC2 research plugin. Use the currently selected Luna model; don't alter company permission, MCP, provider or account settings.

Paste this one request in a fresh session; do **not** send any sensitive corporate context:

> This is a read-only check of the public over-the-luna repository. Use the **named Next Architect** subagent once to examine the real relationship between `scripts/validate_release.py`, `scripts/package_release.py` and their release ZIP allowlist. Ask it to return **DECISION, EVIDENCE, RELATIONSHIPS, WORK_SET, UNCERTAINTIES** with exact public file paths/symbols. As Main, report the returned Architect packet separately from your own assessment. Do not modify files, use other subagents, deploy, push, or access other workspaces. If the delegation tool reports `custom_agent_prompt`, permission or name errors, quote the category only and report `INCONCLUSIVE` rather than claiming Architect was used.

### Local-only pass criteria

PASS (Host path only): the named **Next Architect** was actually invoked and completed; Main cites the *returned* source-specific packet, not merely a prompt mentioning the role. FAIL: observed task failure or blocked policy. INCONCLUSIVE: no trustworthy role completion evidence. Note that even PASS would not prove effective read-only permissions or different-model independence.

**DO NOT EXPORT** company code, complete transcripts, file diffs, approval logs, screenshots containing internal material, BYOK metadata, or model secrets. If the user chooses to share a result externally, the safest optional feedback is only **`HOST_ARCHITECT_PASS`**, **`HOST_ARCHITECT_BLOCKED`**, or **`HOST_ARCHITECT_UNKNOWN`**. It is okay to share nothing.

Reviewer is intentionally NOT part of this quick check: a meaningful Reviewer needs a *real* before/after diff and test outcomes. Verify that naturally on a future approved public task, not by inventing a patch merely to satisfy a gate.

## Release implications and stop rule

A successful standalone SDK registry plus a failed standalone `custom_agent_prompt` call is **not proof of a broken VS Code Host**. Conversely, a picker-visible RC2 role does not establish completed delegation. Keep RC2 opt-in and PR draft until actual Host-native collaboration is observed. No re-running the same paid GitHub Actions probe, no unapproved provider relay, and no corporate artifact transfer. If company policy blocks a reliable Host gate, classify `INCONCLUSIVE`; preserve stable v1.1.1.
