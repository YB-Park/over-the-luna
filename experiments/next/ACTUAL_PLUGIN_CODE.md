# P4: actual plugin selected vs SDK default — product tooling fix

**Prior gap:** We had compared a copied Next system-message body vs
unmodified SDK, but not the actual registered plugin. [P3 actual
plugin gate](ACTUAL_PLUGIN_GATE.md) is now PASS: plugin registry, discovered
qualified agent identity, explicit selection, real Luna model usage and
file read. P4 builds on that gate.

**Product-relevant task:** [official SDK plugin directories](https://github.com/github/copilot-sdk/blob/main/docs/features/plugin-directories.md)
may load **agents/*.md**. Our research candidate's current
`scripts/validate_candidate.py` checks `*.agent.md` only, which
misses an additional `agents/reviewer.md`. It also does not detect a
`skills/unexpected/SKILL.md` bundle, contradicting the
single Main/no skills product decision.

Two conditions differ:
- **actual_next_plugin**: SDK loads this exact checked-in plugin
  directory, verifies registry and selects `over-the-luna-next:` agent
  with `session.rpc.agent.select` before any inference.
- **sdk_default**: pluginDirectories empty and no selected agent.

Same `gpt-6-luna` low effort, original source/test files copied into
separate public temp fixtures, identical bounded read/edit/search tool set,
same user task and independent `actual_plugin_code_grader.py` outside
model workspace. Grader has **no Copilot token** in its environment and
checks both model-written tests and hidden mutations.

Quality criteria: existing candidate remains valid; a plain
`agents/reviewer.md`, dotted extra agent and bundled `skills/**/SKILL.md`
are rejected; previous tool/model/MCP and manifest cases remain rejected;
at least 8 authored focused tests actually PASS. Change scope is exactly
`scripts/validate_candidate.py` and `tests/test_validate_candidate.py`.
The grader independently covers 12 conditions and archives both patches.

The study runs only on an explicit one-shot sentinel push and consumes
at most **two** Copilot-backed Luna model sessions. Pin CLI/SDK versions,
allow no shell or Git mutations, no BYOK/OpenAI, no corporate files or
local output transfer. Infra/selection failure is **not** model quality.
Two passes produce **no proof** of a Next quality edge; a single
difference is suggestive only, not a product ranking.

Status: STAGED, not yet run.
