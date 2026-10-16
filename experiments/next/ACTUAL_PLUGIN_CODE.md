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

Status: P4 COMPLETE; see results below.

## Observed P4 actual plugin work — 2026-10-16: BOTH PASS

[Actions run #38860917956](https://github.com/YB-Park/over-the-luna/actions/runs/38860917956).
The experiment first observed the **actual registered Next plugin**
and selected `over-the-luna-next:over-the-luna-next` using SDK RPC.
The control session verified the plugin was **not loaded/selected**.
Both arms used GPT-6 Luna, low effort, identical allowed tools and
public isolated workspaces.

| Arm | Independent gate | Authored unit tests | Duration | Input tokens | Output tokens | Copilot nano-AIU |
| --- | --- | --- | --- | --- | --- | --- |
| Actual Next plugin | **12/12 PASS** | 8/8 | 15.720 s | 44,734 | 1,212 | 186,801,000 |
| SDK default | **12/12 PASS** | 8/8 | 10.277 s | 23,828 | 878 | 128,648,000 |

Both models edited exactly `scripts/validate_candidate.py` and
`tests/test_validate_candidate.py`, with no forbidden changed paths.
The CI artifact contains exact public patches, permission/tool events,
selection evidence and independent test details (retained 30 days).

**Interpretation:** This single ordered run does **not** establish
a quality advantage for Next: both fixed the actual product bug and
passed identical independent criteria. Unlike the earlier prompt-append
P2 experiment, Next used more tokens, time and reported Copilot nano-AIU
here. The difference is **not a verified USD bill** and is not a general
performance ranking; execution-order/cache variation remains.
This counsels **against claiming a cost-optimized prompt** based on one
successful trial. Do not repeat this exact task to fish for a ranking.

We selected a concise, passing implementation of the legitimate
`agents/*.md` / bundled-skill detection improvement, independent of
whether it came from the control or candidate. It was added to the
research branch and its regression tests are now required in no-credit
CI. Original main and v1.1.1 are preserved.

**What P4 verifies:** Real plugin package discovery/agent selection and
one public coding task in the Copilot SDK under controlled policy.
**What it does NOT verify:** The VS Code Agent Host's exact handling of
permissions/MCP, or any added benefit over native Host Agent.

**Product decision:** Preserve the smallest single-Main candidate
without adding roles or routing complexity. The next information worth
pursuing is a *qualitatively different, decision-changing real task*,
not another tiny negative-mutation fixture or the same model catalogue.

Status: **COMPLETE / BOTH QUALITY PASS / MARGINAL HARNESSED VALUE UNKNOWN**.
