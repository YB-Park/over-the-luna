# v1.1 VS Code Gate A automated wiring results — 2026-08-20

## Decision

The automated/surrogate evidence now ranks the three Main-frontmatter wiring candidates as:

1. **LEADING FOR REAL VS CODE — ambient-tools Main:** omit both `tools` and `agents`; preserve the v1.0 contract that VS Code owns developer-selected built-in/MCP/extension tool state; enforce the Over the Luna Council as an instruction-level delegation contract. Automated Council-selection and sealed-handback evidence is strong. **Actual selected-MCP inheritance remains unresolved because the headless CLI MCP fixture was blocked by outer Copilot policy before agent tool availability could be tested.**
2. **FALLBACK — schema-strict Main:** explicit built-in `tools` including `agent` plus explicit Council `agents`; structural Council allow-list, but arbitrary developer-selected MCP/extension tools cannot be assumed zero-config unless they are also available in that explicit tool set.
3. **REJECTED — wildcard-schema Main:** `tools: ['*', 'agent']` plus explicit Council `agents`; Copilot CLI 0.0.420 reports `Invalid tool '*'` for custom-agent frontmatter, so wildcard portability cannot be assumed on the VS Code/Copilot CLI plugin path.

This is **not yet the real VS Code Gate A pass**. It is the strongest automated evidence for which candidate should be tested first in the authenticated VS Code Agent Plugin runtime.

## Product constraint carried from v1.0

`docs/MCP.md` deliberately makes VS Code own MCP/extension configuration and authorization. Main and Tool Worker historically omit `tools` so the developer's selected runtime tools are not replaced by a product hard-coded list. Over the Luna must not install, authenticate, or bypass an unavailable integration through shell/HTTP.

That is a product compatibility invariant, not merely a convenience preference. Any v1.1 wiring that regresses zero-config developer-selected tool availability needs strong contrary evidence.

## Ambient selection robustness

### Adversarial decoy matrix — 4 repetitions

A Main candidate with `agents` omitted was exposed to three deliberately attractive unrelated model-invocable agents:

- `Fast Repository Scout`;
- `Universal Architect`;
- `Instant Reviewer`.

The read-only task required unknown repository semantic discovery.

After correcting a harness-only plugin-qualified-name evaluator bug, all four artifacts showed:

- `Mode: STANDARD`;
- intended Luna Architect: **1 / run**;
- decoy invocations: **0 / 4 runs**;
- Reviewer: 0;
- mutation: none;
- Main post-leaf repository read/search: **0**;
- all repository `view` calls belonged to Architect.

Detailed first-round evidence is in `AMBIENT_SUBAGENT_DECOY_RESULTS_2026-08-20.md`.

### Exact RC2 clean handback — 2 repetitions

The exact RC2 Main/Architect/Reviewer/Premium candidates were assembled, then Main omitted both `tools` and `agents`. The same decoys were injected. The task was a pure read-only OTel architecture mapping with no implementation expected; Architect therefore had to return `MUTATION_TARGETS: none`, and Main had to synthesize without repository replay.

Both runs were semantically successful:

| Repeat | Mode | Architect inference | Decoys | Main repo reads after leaf | Boundary | Note |
| --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | STANDARD | 1 | 0 | 0 | `work set: none` | first `task` tool attempt was rejected before agent execution because `description` was missing; immediate retry executed exactly one Architect |
| 2 | STANDARD | 1 | 0 | 0 | `work set: none` | clean pass |

Repeat 1's extra `task` count is runtime/tool-call schema noise, not a second leaf inference. The failed tool call produced no `invoke_agent` span.

Therefore the **ambient RC2 semantic policy passed 2/2** on the clean handback gate, while exposing one separate task-tool call reliability issue worth observing in real VS Code.

Across the 4-run decoy matrix plus 2-run exact-RC2 clean gate, attractive unrelated agents diverted the intended broad-discovery leaf **0 / 6 scored runs**.

## Contaminated RC2 ambient run — excluded from policy scoring

An earlier exact-RC2 ambient experiment appeared to show Main reads after Architect. It is excluded from policy scoring because the experiment itself contaminated the repository state and contradicted the product contract:

1. the one-shot paid workflow existed at the launch SHA, so the repository genuinely violated the very paid-workflow manual-only contract the task asked Architect to inspect;
2. the harness prompt explicitly told Architect to put files Main should read into `MUTATION_TARGETS` despite being a read-only task, overriding Architect's normal `MUTATION_TARGETS: none` rule;
3. one repeat had an incomplete `task` tool call followed by a valid retry.

The run remains useful as harness evidence but not as a falsification of the ambient boundary.

## Exact ambient RC + selected MCP attempt — policy-blocked, not a wiring verdict

A final automated surrogate checked the **actual `rc/v1.1-vscode-gate-ambient` branch** with Copilot CLI **1.0.80**. A harmless local stdio MCP server named `v11gate` exposed an `echo` tool returning `AMBIENT_MCP_OK:<value>`. It was added with `--additional-mcp-config`; the session also used `--allow-all-tools` and `--allow-all-mcp-server-instructions` so ordinary per-tool approval would not be the blocker.

Both repetitions were blocked before the model/agent tool surface could test inheritance. The session emitted:

`1 MCP server was blocked by policy: 'v11gate'`

and `session.mcp_servers_loaded` contained no `v11gate` server. Only the built-in GitHub MCP server connected.

Consequently:

- expected MCP marker: **0 / 2**, but **not attributable to Main or Tool Worker frontmatter**;
- `v11gate` tool calls: 0 / 2 because the server never entered the available tool set;
- Main selected `SIMPLE + NONE` for the bounded integration task;
- Main delegated exactly one Luna Tool Worker in each run;
- Tool Worker made zero tool calls and returned `AMBIENT_TOOL_UNAVAILABLE`;
- Main did not inspect repository files, mutate, invoke Reviewer, invoke premium, or bypass the missing integration through shell/HTTP.

This is useful product evidence in two ways:

1. the unavailable-integration boundary behaved correctly;
2. **the experiment cannot adjudicate ambient MCP inheritance** because organization/enterprise/managed MCP policy is outside custom-agent frontmatter and was enforced first.

GitHub's current Copilot CLI documentation confirms that `--additional-mcp-config` is a supported session MCP source and has the highest server-loading priority, while organization/enterprise MCP allowlists and managed `allowedMcpServers` / `deniedMcpServers` can independently block non-default servers, including local servers. Therefore no additional paid CLI rerun is justified until the relevant MCP policy allows the fixture.

The real VS Code gate must use a developer-selected MCP/extension tool that is actually permitted by the active Copilot policy and then observe whether the ambient Main and Tool Worker receive it without Over the Luna-specific frontmatter configuration.

## Wildcard-schema MCP gate — rejected

The candidate inserted:

`tools: ['*', 'agent']`

while retaining the explicit Council `agents` allow-list. A local MCP server `v11gate` exposed a deterministic `echo` tool. The task required the Main/Tool Worker layer to return `WILDCARD_MCP_OK:<value>` before performing normal Architect discovery.

Copilot CLI 0.0.420 emitted the explicit warning:

`Invalid tool '*'.`

The valid-tool list separately included concrete MCP and `agent/runSubagent` tools in that older experiment, demonstrating that the wildcard token itself was invalid in custom-agent frontmatter on that runtime.

Across both repetitions the expected MCP marker was not returned, and the trajectory did not establish a portable wildcard solution. The CLI command also used permissive command-line grants, so even a successful call would have been ambiguous: command-line permissions could mask a broken product frontmatter contract.

The explicit invalid-tool warning is enough to reject wildcard frontmatter as a v1.1 product solution. GitHub custom-agent semantics can differ across surfaces; Over the Luna must not assume a wildcard documented for another custom-agent runtime is portable to VS Code/Copilot CLI Agent Plugins.

## Why ambient still leads over schema-strict

Schema-strict gives the strongest structural delegation boundary: only the named Council is eligible through `agents`, and VS Code documentation requires the built-in `agent` tool when that field is used.

Its product cost is that an explicit `tools` list is the custom agent's available tool set. Over the Luna cannot know every developer's configured MCP/extension tool name when the plugin is authored. Making users reconfigure the plugin agent tool list would regress the existing zero-config ambient-tool contract unless real VS Code proves otherwise.

Ambient wiring keeps the v1.0 ownership model. Its cost is that omission of `agents` is not a structural Council allow-list. The automated adversarial evidence currently mitigates — but does not eliminate — that risk:

- attractive decoys diverted broad discovery **0 / 6 scored runs**;
- all scored broad discovery used the intended Luna Architect;
- clean RC2 handback preserved zero Main repository rehydration;
- the exact ambient branch correctly surfaced an outer-policy-blocked integration without unsafe bypass.

Because the selected-MCP experiment was blocked before the agent tool surface, ambient remains the **leading candidate to test first**, not a proven MCP-inheritance winner. Schema-strict remains a prepared fallback if actual VS Code exposes unacceptable arbitrary-subagent behavior or fails to provide `agent/runSubagent` under ambient wiring.

## Prepared integration candidates

- leading ambient branch: `rc/v1.1-vscode-gate-ambient`, draft PR **#15**;
- schema-strict fallback: `rc/v1.1-vscode-gate-schema`, draft PR **#16**.

Both integration candidates keep `plugin.json` at `1.0.0`, use the same evidence-backed Architect/Reviewer contracts, expose one `Premium Review`, remove the old Sonnet/Opus model menu, and have green static/runtime validation on their Gate PRs.

## Real VS Code Gate A — remaining blockers

The following cannot be proven by the headless CLI surrogate and remain release blockers:

1. plugin loads with the ambient Main (`tools` omitted, `agents` omitted) without customization diagnostics errors;
2. Main actually exposes/uses the VS Code `agent/runSubagent` capability;
3. **a policy-permitted developer-selected built-in/MCP/extension tool remains available to Main/Tool Worker with zero Over the Luna-specific configuration**;
4. broad unknown semantic discovery selects the intended Luna Architect rather than another installed custom agent;
5. leaf tool boundaries stay read-only/non-recursive;
6. Architect sufficient read-only handback yields no Main repository replay;
7. exact-name `Premium Review` handoff renders and switches correctly;
8. premium remains `send: false` / human initiated;
9. unavailable premium model is surfaced rather than silently substituted.

If 1–9 pass, ambient wiring becomes the product Main contract. If 2 or 4 fails materially, test the schema-strict fallback and explicitly measure the developer-selected MCP/extension-tool regression before choosing it. If 3 fails while MCP is known to be policy-permitted, that is real evidence against ambient and must not be explained away as the policy barrier seen in Actions.

## Productization implication

Do not version-bump yet. The automated core and both Gate A integration branches are prepared; the remaining product decision now depends on authenticated real VS Code behavior rather than more prompt tuning.
