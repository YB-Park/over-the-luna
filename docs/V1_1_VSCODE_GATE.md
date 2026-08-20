# Over the Luna v1.1 — real VS Code runtime gate

Branch: `rc/v1.1-vscode-gate-ambient`  
Status: **leading integration candidate for manual authenticated VS Code validation; not a release**

This branch deliberately places the evidence-backed v1.1 RC2 contracts in the real `agents/` directory while keeping `plugin.json` at `1.0.0`.

The automated Gate A wiring work now ranks Main frontmatter strategies as:

1. **ambient leading:** Main omits both `tools` and `agents`; VS Code owns selected built-in/MCP/extension tools, while the instruction body permits delegation only to the seven exact Over the Luna Luna leaves;
2. **schema-strict fallback:** explicit built-in `tools` including `agent` plus explicit Council `agents`; stronger structural subagent namespace, but arbitrary developer MCP/extension tools are not zero-config;
3. **wildcard rejected:** `tools: ['*', 'agent']` is rejected by Copilot CLI 0.0.420 as `Invalid tool '*'`, and a registered local MCP marker remained unavailable in 2/2 attempts.

The goal of this branch is therefore narrow: prove or falsify the remaining product claims that CLI/static tests cannot establish in the authenticated VS Code Agent Plugin runtime.

## Evidence already established before manual VS Code testing

- automated RC2 release matrix: tiny/local/broad/risk x2 = **8/8** hidden behavior + routing/ownership gates;
- adversarial ambient decoy selection: intended Luna Architect in **4/4**, attractive unrelated decoys **0/4**, Main post-leaf repository reads 0;
- exact RC2 ambient clean handback: semantic policy **2/2**, decoys 0, Main post-leaf repository reads 0, `Boundary sealed — work set: none`;
- one clean run had an invalid first `task` tool call missing `description`; it failed before any `invoke_agent` inference and the immediate valid retry ran exactly one Architect. Treat this as runtime tool-call reliability noise, not recursive Council reasoning;
- single premium UX: `Premium Review` / Sonnet 5 / `send:false`; Opus 4.8 was unavailable in the current Copilot CLI environment and must not be silently represented as having run.

Detailed wiring evidence lives in `experiments/VSCODE_GATE_A_AUTOMATED_RESULTS_2026-08-20.md`.

## Before testing

- Use this branch, not `main` and not the broad research PR branch.
- Install/load the repository as an Agent Plugin through the normal VS Code / GitHub Copilot development path.
- Use an authenticated Copilot session.
- Keep OTel/debug content capture off unless a specific observation requires content.
- Record VS Code version, GitHub Copilot extension/runtime version, plan/policy context, and whether Autopilot is enabled.
- Configure at least one harmless developer-selected MCP or extension tool before starting the test. Do not add that tool to Over the Luna frontmatter.
- Do not change `plugin.json` to `1.1.0` for this gate.

Expected visible custom agents in this gate layout include:

- `Over the Luna`
- `Luna Architect`
- `Luna Reviewer`
- `Premium Review`

The old normal-menu `Sonnet Reviewer` and `Opus Critical Reviewer` agents are intentionally absent.

## Gate A1 — plugin discovery and exact identity

Verify:

1. plugin loads without customization diagnostics errors;
2. `Over the Luna` resolves to this plugin's agent;
3. the Luna leaves are loaded with exact names;
4. `Premium Review` is loaded with that exact name;
5. no stale Sonnet/Opus two-choice handoff menu appears.

**Pass evidence:** screenshot/notes plus Agent Debug identity if available.

## Gate A2 — ambient subagent capability and Council selection

This is the decisive wiring test.

Main intentionally has neither `tools` nor `agents` in frontmatter. Its instruction contract permits delegation only to:

- `Luna Planner`
- `Luna Architect`
- `Luna Skeptic`
- `Luna Researcher`
- `Luna Tool Worker`
- `Luna Recovery`
- `Luna Reviewer`

Install or leave enabled at least one unrelated model-invocable custom agent if practical, then use a read-only task that requires discovering an unknown repository contract.

Expected:

- `agent/runSubagent` is available despite omitted Main `tools`/`agents`;
- route becomes `STANDARD` before broad Main scouting;
- the selected leaf is exactly `Luna Architect`;
- no unrelated custom agent is selected;
- Architect returns `DECISION / EVIDENCE / RELATIONSHIPS / MUTATION_TARGETS / UNRESOLVED`;
- for a sufficient read-only map, `MUTATION_TARGETS: none`;
- Main prints `Boundary sealed — work set: none` and synthesizes without repository replay.

**Fail if:** `agent/runSubagent` is absent, another custom agent is selected, or Main rehydrates the repository after a sufficient packet.

If this fails materially, switch to the prepared schema-strict fallback rather than adding wildcard `*` wiring.

## Gate A3 — selected built-in / MCP / extension tool inheritance

This is the other decisive wiring test.

Configure at least one harmless read-only MCP or extension tool in VS Code through the developer's normal settings/tool picker. Do not modify Over the Luna frontmatter.

Expected:

- Main sees and can use the developer-selected tool according to VS Code policy;
- no Over the Luna-specific MCP installation/auth/config is required;
- the tool remains VS Code-owned;
- `Luna Tool Worker` can use the selected integration only when Main delegates a bounded external-tool task;
- read-only leaves such as Architect/Reviewer do not inherit mutation-capable ambient integrations because their own frontmatter explicitly restricts tools.

**Fail if:** Main loses the selected tool, the plugin needs a hard-coded MCP name, or a restricted leaf gains unintended side-effect tools.

Do not bypass an unavailable integration through shell, direct HTTP, or alternate credentials merely to make this gate pass.

## Gate A4 — mechanical boundary: SIMPLE + NONE

Use an exact local scalar/default/text/metadata substitution with a direct existing assertion.

Expected:

- `Mode: SIMPLE ... | Assurance: NONE`;
- Architect 0;
- Reviewer 0;
- Main edits and validates;
- final report explicitly says review was skipped because the mechanical threshold was satisfied.

**Fail if:** a tiny change buys Reviewer ceremony.

## Gate A5 — local semantic boundary: SIMPLE + REVIEW

Use a named local behavioral change with a clear implementation neighborhood.

Expected:

- `SIMPLE + REVIEW`;
- no investigative Architect by default;
- Main only mutation owner;
- current unified diff captured after focused validation;
- exactly one named `Luna Reviewer`;
- Reviewer prompt contains `BEGIN_UNIFIED_DIFF`, `END_UNIFIED_DIFF`, concrete `diff --git`, `@@`, and every changed path;
- accepted repair is revalidated by Main without automatic re-review.

## Gate A6 — broad semantic mutation: STANDARD + REVIEW

Use a real task requiring discovery of an unknown repository contract/dependency.

Expected:

1. bounded local orientation only;
2. `STANDARD` before broad Main scouting;
3. one Luna Architect for the broad evidence pass;
4. complete evidence packet and work set;
5. `Boundary sealed — work set: ...` before another Main repository action;
6. Main reads only known work-set/local mutation context until mutation begins;
7. no broad inventory replay;
8. Main owns mutation;
9. final artifact gets exactly one normal Reviewer.

## Gate A7 — consequential RISK boundary

Use a small but real concurrency/idempotency, auth/security, transaction, migration, persistence/data-integrity, rollback, or important public-contract task.

Expected:

- assurance says `RISK`;
- optional pre-change Skeptic/Architect only for a real independent risk question;
- at least one **named post-change Luna Reviewer** with the concrete artifact;
- a second Reviewer only after Main names one distinct consequential residual risk and rubric;
- Main remains sole mutation owner.

## Gate A8 — single Premium Review UI and human spend boundary

Reuse a completed change with a specific consequential residual uncertainty.

Expected:

1. exactly one handoff: `Premium Review`;
2. exact custom-agent target `Premium Review`;
3. prompt prefilled but not automatically sent;
4. `send:false` remains a real user spend boundary, including under Autopilot;
5. backing model is Sonnet 5 when available;
6. if unavailable, model unavailability/fallback is visible enough that the product does not silently claim the requested premium judgment happened.

**Fail if:** premium auto-runs, the old two-model menu reappears, or model substitution is silent.

## Gate A9 — Agent Debug / OTel sanity

For at least one SIMPLE+REVIEW and one STANDARD+REVIEW session, record enough metadata to verify:

- Main vs leaf identities;
- actual `invoke_agent` count, not merely failed task-tool attempts;
- model identity;
- tool ownership;
- Reviewer count;
- route markers;
- no leaf mutation;
- no post-Architect broad rehydration.

The repository analyzer uses trace-qualified `(trace_id, span_id)` ancestry and has a cross-trace regression; prefer it for exported OTel summaries.

## Exit criterion

Gate A passes only when actual VS Code behavior supports all product-critical claims:

- ambient Main loads cleanly;
- `agent/runSubagent` works without hard-coding Main tools;
- exact Council selection is reliable;
- developer-selected MCP/extension tools remain available zero-config;
- mechanical work stays low-ceremony;
- local semantic work receives bounded assurance;
- broad unknown discovery is isolated and sealed;
- RISK receives final independent assurance;
- Main is sole mutation owner;
- leaves remain restricted;
- one Premium Review handoff is exact-name, human initiated, and model behavior is not silently misrepresented.

If ambient fails only the subagent namespace/capability gate, test the schema-strict fallback and explicitly measure the MCP/extension regression before choosing it.

## After Gate A passes

Then, and only then:

1. freeze the selected Main wiring as the v1.1 product contract;
2. update README / README.ko / DESIGN / SMOKE_TEST / CONTRIBUTING and tool-selection guidance;
3. run packaged-plugin clean-install smoke tests;
4. decide which research artifacts remain after release;
5. bump version/changelog to `1.1.0`;
6. prepare the release integration into `main`.
