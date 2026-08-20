# v1.1 VS Code Gate A automated wiring results — 2026-08-20

## Decision

The automated/surrogate evidence now ranks the three Main-frontmatter wiring candidates as:

1. **LEADING — ambient-tools Main:** omit both `tools` and `agents`; preserve VS Code-owned built-in/MCP/extension tool state; enforce the Over the Luna Council as an instruction-level delegation contract.
2. **FALLBACK — schema-strict Main:** explicit built-in `tools` including `agent` plus explicit Council `agents`; structural Council allow-list, but arbitrary developer-selected MCP/extension tools cannot be zero-config unless they are also made available in that explicit tool set.
3. **REJECTED — wildcard-schema Main:** `tools: ['*', 'agent']` plus explicit Council `agents`; Copilot CLI 0.0.420 reports `Invalid tool '*'` for custom-agent frontmatter, and the local MCP tool was unavailable to the candidate in both repetitions.

This is **not yet the real VS Code Gate A pass**. It is the strongest automated evidence for which candidate should be tested first in the VS Code Agent Plugin runtime.

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

## Contaminated RC2 ambient run — excluded from policy scoring

An earlier exact-RC2 ambient experiment appeared to show Main reads after Architect. It is excluded from policy scoring because the experiment itself contaminated the repository state and contradicted the product contract:

1. the one-shot paid workflow existed at the launch SHA, so the repository genuinely violated the very paid-workflow manual-only contract the task asked Architect to inspect;
2. the harness prompt explicitly told Architect to put files Main should read into `MUTATION_TARGETS` despite being a read-only task, overriding Architect's normal `MUTATION_TARGETS: none` rule;
3. one repeat had an incomplete `task` tool call followed by a valid retry.

The run remains useful as harness evidence but not as a falsification of the ambient boundary.

## Wildcard-schema MCP gate — rejected

The candidate inserted:

`tools: ['*', 'agent']`

while retaining the explicit Council `agents` allow-list. A local MCP server `v11gate` exposed a deterministic `echo` tool. The task required the Main/Tool Worker layer to return `WILDCARD_MCP_OK:<value>` before performing normal Architect discovery.

Copilot CLI 0.0.420 emitted the explicit warning:

`Invalid tool '*'.`

The valid-tool list separately included the concrete `v11gate/echo` and `agent/runSubagent` tools, demonstrating that the wildcard itself — not MCP server registration — was the invalid element.

Across both repetitions:

- MCP server registered successfully;
- expected MCP marker returned: **0 / 2**;
- final output reported `AMBIENT_TOOL_UNAVAILABLE` for the v11gate echo tool;
- Architect discovery still ran;
- no mutation or premium inference occurred;
- attempts to recover tool access through Luna Tool Worker produced repeated Tool Worker task attempts rather than the intended direct configured-tool path.

The CLI command also used `--allow-all-tools`, so any successful tool behavior would have been ambiguous anyway: command-line grants could mask an invalid custom-agent frontmatter contract. The explicit invalid-tool warning plus 0/2 MCP marker is enough to reject wildcard frontmatter as a portable v1.1 product solution.

GitHub's custom-agent documentation may describe wildcard tool semantics in other runtimes, but this result shows that Over the Luna cannot assume those semantics are portable to the VS Code/Copilot CLI plugin path.

## Why ambient leads over schema-strict

Schema-strict gives the strongest structural delegation boundary: only the named Council is eligible through `agents`, and VS Code documentation requires the built-in `agent` tool when that field is used.

Its product cost is that an explicit `tools` list is the custom agent's available tool set. Over the Luna cannot know every developer's configured MCP/extension tool name when the plugin is authored. Making users reconfigure the plugin agent tool list would regress the existing zero-config ambient-tool contract.

Ambient wiring keeps that contract. Its cost is that omission of `agents` is not a structural Council allow-list. The automated adversarial evidence currently mitigates — but does not eliminate — that risk:

- attractive decoys diverted broad discovery **0 / 6 clean/scored runs** (4 first-round + 2 exact RC2 clean);
- all scored broad discovery used the intended Luna Architect;
- clean RC2 handback preserved zero Main repository rehydration.

Therefore ambient is the candidate to test first in the real VS Code runtime. Schema-strict remains a prepared fallback if VS Code exposes unacceptable arbitrary-subagent behavior or fails to provide `agent/runSubagent` under ambient wiring.

## Real VS Code Gate A — remaining blockers

The following cannot be proven by the CLI surrogate and remain release blockers:

1. plugin loads with the ambient Main (`tools` omitted, `agents` omitted) without customization diagnostics errors;
2. Main actually exposes/uses the VS Code `agent/runSubagent` capability;
3. a developer-selected built-in/MCP/extension tool remains available to Main with zero Over the Luna-specific configuration;
4. broad unknown semantic discovery selects the intended Luna Architect rather than another installed custom agent;
5. leaf tool boundaries stay read-only/non-recursive;
6. Architect sufficient read-only handback yields no Main repository replay;
7. exact-name `Premium Review` handoff renders and switches correctly;
8. premium remains `send: false` / human initiated;
9. unavailable premium model is surfaced rather than silently substituted.

If 1–9 pass, ambient wiring becomes the product Main contract. If 2 or 4 fails materially, test the schema-strict fallback and explicitly measure the developer-selected MCP/extension-tool regression before choosing it.

## Productization implication

Do not version-bump yet. Prepare the ambient RC integration branch and the schema-strict fallback branch so the real VS Code A/B is a short runtime verification rather than another architecture exercise.
