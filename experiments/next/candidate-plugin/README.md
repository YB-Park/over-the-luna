# Over the Luna Next — minimal research candidate

**Status:** EXPERIMENTAL, not a replacement for v1.1.1. This directory
is a complete, isolated **legacy Copilot-format plugin**. The research
branch's repository-root `plugin.json` and shipped `agents/` remain the
unchanged v1.1.1 baseline.

The candidate contains exactly **one visible agent** and no Council,
Reviewer, Premium UI, hooks, MCP servers, scripts, credentials, or API
bridge. It inherits the developer's *actually enabled VS Code tools*
because its frontmatter intentionally **omits `tools`**. This does
**not** constitute sandboxing or prohibit writes: the host's tools and
permission controls are the real boundary.

## Installation: local side-by-side (recommended for this trial)

1. Clone the repository locally and switch to
   `research/next-harness-foundation`; keep the local checkout on this
   branch for the candidate files. Do not switch your production checkout
   or installed v1.1.1 plugin automatically.
2. In your VS Code **User** settings, enable `chat.plugins.enabled` and
   register the **absolute path** to this exact directory:

   ```json
   {
     "chat.pluginLocations": {
       "/ABSOLUTE/PATH/over-the-luna/experiments/next/candidate-plugin": true
     }
   }
   ```

   Integrate this entry with existing user settings rather than
   overwriting the whole file. On Windows, use a valid escaped path or
   forward slashes. Do not commit machine-specific paths.
3. Choose the **Copilot** harness in VS Code, then select
   **Over the Luna Next (Research)** in the agent picker. Check
   `Chat: Open Customizations` / Diagnostics if it is not visible.
   Keep the existing **Over the Luna** v1.1.1 plugin installed, but
   choose only the agent that belongs to the arm being tested.
4. In the model picker choose **GPT-6 Luna** for the first paired
   baseline, **both** in native Agent and this candidate. The candidate
   intentionally has **no `model` frontmatter** so that subsequent
   direct model changes remain possible without rewriting files.
5. Use the same selected tool set, MCP servers, workspace trust and
   approval policy for native and candidate runs. **Do not** change
   permissions just to make a smoke test pass.

Official docs: [local plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins#_use-local-plugins) and
[custom agent model inheritance](https://code.visualstudio.com/docs/agent-customization/custom-agents).

**Do not use the ordinary "Install Plugin From Source" command with the
repository root for this candidate.** That root still intentionally
contains the stable v1.1.1 plugin, not this nested package.

## First use: verify effective behavior, not the model catalogue

- Select Copilot Agent Host + the research agent.
- Ask for a *read-only* explanation of one known, non-sensitive repository
  contract. Check selected model, tool usage, no file changes, and
  whether selected MCP read access behaves as expected.
- Perform **one real authorized code change** in a clean worktree.
  Verify the host approval prompts, changed paths, real tests and diff.
- If a permission expansion, unexpected tool, wrong model, unrequested
  external mutation, or unbounded paid call appears, **stop using the
  candidate** and capture the exact discrepancy. Don't work around it
  with weaker security settings.
- Optional higher-risk case: use the developer's real permission policy
  to test the boundary, never hidden assumptions about `tools: []`.

## Compared with native Copilot Agent

Use [DOGFOOD.md](../DOGFOOD.md) and [SCORECARD.md](../SCORECARD.md).
For real work, prefer isolated equivalently prepared worktrees; a native
change should not leak into the candidate's initial repository state.

Keep Copilot AI Credits and direct OpenAI API USD separate. Prompt cost,
retries, human corrections and elapsed time matter more than raw tokens.

No scripts in this candidate automatically invoke any paid model.
No API keys are stored in the plugin; GitHub Actions
`OPENAI_API_KEY` does **not** automatically enter the user's VS Code host.

## Rollback

Disable the local plugin entry (`false`) or remove its
`chat.pluginLocations` entry, then continue using the original
**Over the Luna** agent or native Copilot Agent. Do not delete v1.1.1
to test this candidate. Research changes remain isolated until supported
by product evidence.
