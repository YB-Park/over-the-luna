# v1.1 Gate A — real VS Code Agent Plugin runtime

Status: **manual/runtime gate — REQUIRED before productizing RC2 into released agents**  
Updated: **2026-08-20**

## Why this gate exists

The automated RC2 core passed the controlled Copilot CLI matrix 8/8, but CLI behavior is not sufficient evidence for the real VS Code product contract.

The most important unresolved issue is Main tool/subagent wiring.

Current VS Code custom-agent documentation says:

- the `agents` frontmatter field restricts available subagents;
- when `agents` is specified, the `agent` tool must be included/enabled;
- custom-agent `tools` specifies the tools available to that custom agent;
- VS Code request tools can include built-in, MCP, and extension-contributed tools;
- handoffs with `send: false` keep the next step user initiated.

RC2 intentionally omitted Main `tools` during CLI experiments to avoid replacing the developer's ambient selected MCP/extension tools. Therefore the released Main frontmatter cannot be chosen from CLI results alone.

## Gate question

Choose the wiring that best satisfies both product requirements:

1. Main can reliably invoke only the intended Luna leaves;
2. developer-selected built-in/MCP/extension tools remain usable instead of being unexpectedly replaced by a fixed product list.

## Wiring candidates

### Candidate A — schema-strict leaf allowlist

Start from the RC2 Main body:

`experiments/v1_1_candidate_rc2.agent.md`

Frontmatter characteristics:

- keep `agents: ['Luna Planner', 'Luna Architect', 'Luna Skeptic', 'Luna Researcher', 'Luna Tool Worker', 'Luna Recovery', 'Luna Reviewer']`;
- configure Main tools so the VS Code `agent` / `agent/runSubagent` capability is explicitly enabled;
- include the implementation/read/search/terminal tools required for normal development;
- enable at least one known MCP or extension-contributed tool that is already part of the developer's normal tool selection.

Purpose:

- verify structural leaf allowlisting works;
- determine whether explicit custom-agent tools replace/narrow the developer's ambient tools;
- determine whether arbitrary configured MCP/extension tools can be preserved without hardcoding product-specific integrations.

### Candidate B — ambient-tool preservation

Start from the same RC2 Main body.

Frontmatter characteristics:

- omit Main `tools`;
- omit Main `agents` if necessary to satisfy VS Code custom-agent semantics;
- keep the allowed Luna leaf names as a hard instruction-level contract in the body;
- leave the developer's normal VS Code tool selection enabled, including `agent/runSubagent` and at least one known MCP/extension tool.

Purpose:

- verify ambient tool selection is preserved;
- verify Main can still invoke the intended Luna leaves;
- verify Main does not select unintended built-in/custom agents even though the leaf allowlist is no longer frontmatter-enforced.

## Preconditions

Use a current VS Code build with the Agent Plugin/custom-agent features intended for release.

Before testing:

1. checkout the research branch at the intended Gate A candidate commit;
2. verify `Validate plugin` is green;
3. ensure no `*_once.yml` paid experiment workflow remains;
4. open VS Code Customizations diagnostics and verify there are no parse/load errors;
5. verify the Over the Luna plugin is enabled/discovered;
6. note the VS Code version, GitHub Copilot extension/version or harness build, active account/plan, selected model, and active tool count;
7. select/enable one identifiable MCP or extension-contributed tool that can be safely read-only-tested;
8. keep premium handoffs non-auto-send.

Record these values in the evidence section below.

## Test 1 — plugin/custom-agent discovery

For each wiring candidate:

1. open the Agent Customizations editor / diagnostics;
2. verify `Over the Luna` appears with no frontmatter/tool/agent errors;
3. verify all intended Luna leaves load;
4. verify leaves marked `user-invocable: false` do not appear as normal user-selectable agents but remain available to subagent invocation;
5. verify Main is not available as a subagent because `disable-model-invocation: true` remains set.

PASS requires no customization diagnostics errors and the intended visibility/invocability behavior.

## Test 2 — subagent capability and allowlist

Run a read-only broad-discovery request that should route to Architect.

Acceptance:

- Main emits `Mode: STANDARD — ... | Assurance: NONE/REVIEW` as appropriate;
- a real subagent tool invocation occurs;
- the invoked custom agent is `Luna Architect`;
- Architect's tools are read/search only;
- Architect cannot mutate or recursively delegate;
- Main receives only the handback packet;
- Candidate A: an unlisted agent cannot be selected by the `agents` allowlist;
- Candidate B: despite no structural allowlist, Main follows the instruction-level leaf policy and selects only the intended Luna Architect.

Capture the expanded subagent tool call or Agent Debug trace showing the custom-agent name and leaf tool calls.

## Test 3 — ambient MCP/extension tool preservation

With the same identifiable MCP/extension tool enabled before switching to Over the Luna:

1. start a request where that external read-only tool is clearly relevant and explicitly requested;
2. confirm Main can see/use it under the candidate wiring;
3. confirm enabling Over the Luna did not silently remove the tool from the request/harness;
4. confirm the leaf tool restrictions remain independent — for example Architect/Reviewer must not inherit arbitrary Main mutation/external tools unless their own frontmatter allows them.

PASS requires Main tool preservation **and** leaf least-privilege behavior.

This is the key A/B discriminator.

## Test 4 — four routing boundaries in real VS Code

Use the same semantic archetypes as the automated matrix. Exact repositories/tasks may be local, but preserve the distinction.

### tiny

Expected:

- `SIMPLE + NONE`;
- no Architect;
- no Reviewer;
- bounded direct/narrow orientation;
- no generic glob/inventory/background prose.

### local

Expected:

- `SIMPLE + REVIEW`;
- Architect 0;
- exactly one named Luna Reviewer after a concrete patch + validation;
- Reviewer gets concrete current artifact evidence.

### broad

Expected:

- `STANDARD + REVIEW`;
- Architect exactly once for initial broad semantic discovery;
- Main emits `Boundary sealed — work set: ...`;
- before mutation Main reads only sealed work-set files;
- no broad discovery replay;
- exactly one final named Luna Reviewer.

### risk

Expected:

- Assurance `RISK`;
- investigation may be SIMPLE/STANDARD/DEEP based on locality;
- at least one post-change named Luna Reviewer;
- pre-change Skeptic/Architect does not substitute;
- generic built-in review does not count;
- no second pass unless a distinct residual consequential risk is explicitly named first.

Capture Agent Debug/OTel or expanded tool calls for each.

## Test 5 — handoffs

After a normal Over the Luna response:

1. verify premium handoff button(s) render;
2. select each currently configured handoff without submitting;
3. verify VS Code switches to the exact named target custom agent;
4. verify the prompt is prefilled;
5. verify it does **not** auto-submit when `send: false`;
6. cancel without premium execution if this is only a functional handoff test.

PASS requires the transition to remain an explicit user action.

## Test 6 — actual tool/agent trace shape

For at least one STANDARD + REVIEW mutation:

Record:

- Main model identity;
- Architect model identity;
- Reviewer model identity;
- Main tool calls before Architect;
- Architect read/search calls;
- exact returned work set;
- Main reads after handback and before mutation;
- mutation owner;
- validation commands;
- Reviewer invocation count and read/search calls;
- whether any MCP/extension tool was available/used;
- any unexpected parentage/inheritance behavior.

PASS requires one Main mutation owner and no hidden competing implementation trajectory.

## A/B decision rule

Prefer **Candidate A** if:

- explicit `agents` + `agent` tool works cleanly;
- ambient developer MCP/extension tools can still be preserved without a brittle hardcoded product list;
- leaf restrictions remain intact.

Prefer **Candidate B** if:

- Candidate A materially replaces/narrows ambient developer-selected tools;
- omitting Main tool/agent lists preserves the intended tool environment;
- instruction-level leaf restriction proves reliable in representative sessions and no unintended agent invocation occurs.

If neither satisfies both requirements, **do not productize v1.1 yet**. Investigate a VS Code-supported tool-set/plugin wiring that explicitly composes the subagent tool with the developer tool environment rather than weakening either requirement.

Do not use undocumented wildcard tool behavior as a release dependency without explicit runtime confirmation.

## Evidence template

Copy this block into a dated Gate A result file after running the test.

```text
VS Code version:
Copilot / harness version:
OS:
Account / plan:
Main model:
Plugin commit:

Candidate: A | B
Customization diagnostics: PASS | FAIL
Main tools visible before switching:
Main tools visible under Over the Luna:
Sentinel MCP/extension tool preserved: YES | NO
agent/runSubagent available: YES | NO
Leaf allowlist behavior: PASS | FAIL
Leaf tool restrictions: PASS | FAIL

Tiny: PASS | FAIL
Local: PASS | FAIL
Broad: PASS | FAIL
Risk: PASS | FAIL

Handoff render: PASS | FAIL
Exact-name switch: PASS | FAIL
send:false human gate: PASS | FAIL

Unexpected behavior:
Trace / screenshot references:
Decision:
```

## Gate A PASS condition

Gate A closes only when one wiring candidate has evidence for all of the following:

- clean plugin/custom-agent loading;
- reliable intended subagent invocation;
- developer-selected MCP/extension tool preservation acceptable for the product;
- leaf least privilege;
- real tiny/local/broad/risk routing behavior consistent with RC2;
- sealed broad handback in the actual runtime;
- named final Reviewer behavior;
- handoff rendering/exact switching;
- premium remains explicitly user initiated.

Only then should RC2 be ported into released `agents/`.
