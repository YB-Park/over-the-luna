# P21 — Is Copilot ignoring Over the Luna agents?

**Status:** host-specific diagnostic, not a new paid benchmark.
This guide distinguishes three independent states: agent definition
was discovered; agent instructions actually reached the active model;
a named subagent tool was offered, invoked and completed successfully.
None may be substituted for the others.

## What we verified

- Current VS Code separates the **Copilot harness** (Agent Host/Copilot SDK)
  from the **Local harness** (VS Code extension host). Model names and UI
  location do not determine the harness.
- Protected stable `main` v1.1.1's
  `agents/over-the-luna.agent.md` explicitly requests
  `agent/runSubagent`, which current VS Code documentation places under
  **Local**, not the Copilot harness. This is a **real compatibility
  hypothesis**, not proof that the user's sessions did or did not run in
  Local at the time.
- Next RC2 avoids blindly using Local's `agent/runSubagent`. Native
  P16 public CI verified plugin discovery in the actual Copilot Host
  (**8/8 roles**), but P17 did not complete a named call, and P18's
  isolated Actions account advertised no models. This does **not**
  establish the end-user's authenticated runtime behavior.
- VS Code shows subagent chats in the **Agents window**; the standard
  Sessions hierarchy may not expose them as separate chats. Missing
  UI badges alone cannot establish non-delegation.

## Safe single-session diagnostic (no source edits)

1. Open a **new** session and explicitly choose **Copilot** or
   **Local** from Session Target; record which you chose. Select
   **Over the Luna Next** in the agent picker. Open
   Agent Customizations → Agents and inspect its source path. Ensure
   there is no other installed same-name agent taking precedence.
   If Next is unavailable, stop and use the view's Diagnostics to
   determine whether the plugin is installed/loaded.
2. In an approved public/test repository, use the exact bounded prompt:

   > **Delegation diagnostic, not a coding task.** Use the named
   > **Next Architect** subagent *exactly once* to read
   > `scripts/validate_release.py` and `scripts/package_release.py`,
   > and return `DECISION / EVIDENCE / RELATIONSHIPS / WORK_SET /
   > UNCERTAINTIES`. Do not edit files, use another model/provider,
   > invoke premium roles, or pretend a leaf ran. If native named
   > delegation is unavailable, say `NAMED_DELEGATION_UNAVAILABLE`
   > and the actual reason.

3. Before the test, for **Copilot** sessions enable
   `chat.agentHost.agentDebugLog.enabled`. After the test open
   **Developer: Open Agent Debug Logs** → the selected session →
   **Agent Flow Chart**. For **Local**, use Local's subagent display
   and its separate log setting
   `github.copilot.chat.agentDebugLog.fileLogging.enabled`.
4. Open **Developer: Show Chat Debug View** for that request. Privately
   inspect the **System prompt** for Next's body, and the **Tool
   definitions** for the current harness's native delegation tool.
   Right-click Chat → **Diagnostics** to see loaded/missing/errors in
   discovered customizations. Do not infer visibility from the agent
   picker alone.

## Interpret exactly

| Observed | Diagnosis | Next action |
| --- | --- | --- |
| Next prompt missing or wrong source/version | Customization selection/discovery issue | Fix selected harness and loaded plugin first |
| Next prompt present, native delegation tool absent | Tool availability/policy mismatch | Verify current harness/tool policy; do not edit source blindly |
| Prompt and tool present, no tool invocation | Main/model chose DIRECT or disregarded explicit instruction | Compare with one direct forced leaf request; inspect request/response |
| Tool invoked but failed | Real runtime, auth, model or permissions failure | Record sanitized category; not a quality failure |
| Tool completed, named leaf returned path evidence | **True handback candidate** | Verify actual leaf identity and independent returned evidence |
| Only on-screen subagent indicator absent | Possible UI presentation issue | Confirm through Agent Flow Chart and tool lifecycle |

**Safety:** Debug views can contain workspace paths, raw source, chat
messages, tool payloads and credentials. Do not paste raw logs,
screenshots of secrets, internal code, organization URLs or tokens into
a public PR or chat. Share only `Copilot/Local`, agent source
(Next/stable/other), `PROMPT_PRESENT?`, `NATIVE_TOOL_PRESENT?`,
`LEAF_TOOL_STARTED?`, `LEAF_TOOL_COMPLETED?`, and an allowlisted
error category. Keep stable `main` and release RC1 untouched.

References:
- https://code.visualstudio.com/docs/agents/run/agent-harnesses
- https://code.visualstudio.com/docs/agents/run/subagents
- https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view
- https://code.visualstudio.com/docs/agent-customization/custom-agents
