# v1.1 durable handoff

Last updated: **2026-08-20**  
Primary research branch: `research/v1.1-runtime-baseline`  
Primary research PR: **#13 — Research v1.1 runtime behavior and experiment harness**  
Leading VS Code Gate PR: **#15 — ambient-tools RC**  
Fallback VS Code Gate PR: **#16 — schema-strict RC**

This is the operational recovery document. If a session dies, start here instead of reconstructing the experiment history.

## Current status in one paragraph

The automated GPT-5.6 Luna core is **pre-production RC2** and is no longer the main uncertainty: tiny/local/broad/risk boundaries passed **8/8** visible validation + hidden behavior + routing/ownership gates. Premium UX is also narrowed: v1.1 exposes **one human-selected `Premium Review` backed by Sonnet 5 with `send:false`**; the old Sonnet/Opus menu is rejected, and Opus 4.8 was not selectable in the current Copilot environment. The remaining release blocker is **real VS Code Gate A**: select the Main frontmatter wiring and verify actual `agent/runSubagent`, policy-permitted developer MCP/extension tool inheritance, exact custom-agent handoff rendering, and leaf restrictions. The leading candidate is ambient Main (`tools` omitted, `agents` omitted, exact Council sealed in instructions); schema-strict is prepared as fallback. **Do not merge to `main` or bump to 1.1.0 until real VS Code Gate A passes.**

## Read these first

1. `experiments/PREPRODUCTION_RC2_RESULTS_2026-08-20.md` — final automated-core 8/8 evidence and failure history.
2. `experiments/VSCODE_GATE_A_AUTOMATED_RESULTS_2026-08-20.md` — latest Main-wiring evidence, decoy attacks, wildcard rejection, MCP policy barrier.
3. `docs/V1_1_DESIGN_CANDIDATE.md` — evidence-backed architecture.
4. `experiments/PREMIUM_JUDGMENT_RESULTS_2026-08-20.md` — single-premium evidence.
5. `experiments/INVARIANT_CHALLENGE_REVIEW_RESULTS_2026-08-19.md` — why Reviewer challenges one invariant.
6. `experiments/ARCHITECT_PACKET_ABLATION_RESULTS_2026-08-19.md` — why the compact Architect packet is preferred.
7. PR #15 branch `docs/V1_1_VSCODE_GATE.md` — exact manual authenticated VS Code checklist.

## Canonical automated-core contracts

- Main RC2 policy: `experiments/v1_1_candidate_rc2.agent.md`
- Architect: `experiments/v1_1_candidate_architect_packet_v3.agent.md`
- Reviewer: `experiments/v1_1_candidate_reviewer_rc.agent.md`
- Premium: `experiments/v1_1_candidate_premium_review.agent.md`

Release-gate infrastructure includes:

- `experiments/v1_1_release_gate_fixture.py`
- `experiments/v1_1_release_gate_evaluator_v6.py`
- `experiments/v1_1_release_gate_evaluator_rc2.py`
- `tests/test_v1_1_candidate_contract.py`
- `tests/test_v1_1_rc_contract.py`
- `tests/test_v1_1_release_gate_evaluator.py`
- `tests/test_v1_1_rc_release_gate.py`

Do not copy RC2 Main frontmatter blindly into release `agents/`; Gate A is specifically deciding Main runtime wiring.

## Automated-core release result

Final RC2 matrix run: **32323722543**  
Launch commit: `b2b3de4b58a60e4fe62a19f18898f7844c63efaa`

| Boundary | Product shape | Result |
| --- | --- | --- |
| tiny | `SIMPLE + NONE`, Architect 0, Reviewer 0 | 2/2 PASS |
| local | `SIMPLE + REVIEW`, Architect 0, Reviewer 1 | 2/2 PASS |
| broad | `STANDARD + REVIEW`, Architect 1, sealed work set, Reviewer 1 | 2/2 PASS |
| risk | `RISK`, post-change named Reviewer >=1 | 2/2 PASS |

All eight hidden behavioral oracles passed. Automatic premium count was zero in all eight runs.

Earlier hidden-PASS trajectories were intentionally rejected for product-discipline failures including unnecessary tiny review, generic root inventory, README/tooling over-scouting, post-Architect rehydration, recursive normal review, skipped RISK final review, and built-in `code-review` substitution. RC2 is the first candidate to close all four boundaries together.

## Product decisions with strong evidence

### Keep

- `SIMPLE / STANDARD / DEEP` investigation.
- Separate `NONE / REVIEW / RISK` assurance.
- Main as the only mutation owner.
- Bounded no-glob SIMPLE orientation.
- Unknown broad semantic discovery -> Architect before Main consumes it.
- Architect packet: `DECISION / EVIDENCE / RELATIONSHIPS / MUTATION_TARGETS / UNRESOLVED`.
- `MUTATION_TARGETS` as the complete post-handback implementation/test/helper work set.
- Explicit `Boundary sealed — work set: ...` state transition.
- No Main broad rehydration after sufficient Architect handback.
- NONE only for genuinely mechanical work.
- Normal REVIEW = exactly one named Luna Reviewer inference for the trajectory.
- Concrete current unified diff + validation evidence before Reviewer.
- Reviewer bounded dependency closure + one consequential invariant challenge.
- Main repair/revalidation without recursive normal review.
- RISK gets at least one named post-change Reviewer.
- Automatic core remains GPT-5.6 Luna only.
- **Premium = one visible human decision, `Premium Review`, Sonnet 5 candidate, `send:false`.**
- Unavailable integrations/models are surfaced rather than silently bypassed/substituted.

### Do not resurrect without new evidence

- lowering SIMPLE merely to increase Council calls;
- treating every locator as semantic discovery;
- broad Main scouting to decide whether Architect is useful;
- root inventory / wildcard-only discovery for local work;
- background README/docs browsing for confidence;
- treating Architect invocation alone as proof of isolation;
- Main replaying broad discovery after Architect;
- strict zero-read Reviewer;
- dependency reads without invariant falsification;
- Reviewer-until-PASS loops;
- normal Reviewer artifact/VERIFY retry;
- pre-change RISK leaves as a substitute for final artifact review;
- generic/built-in `code-review` as the product Reviewer;
- hidden automatic premium inference;
- separate routine Sonnet/Opus premium menu;
- `tools: ['*', 'agent']` as a portable VS Code compromise.

## Premium decision — Gate B is effectively closed

Controlled premium evaluation used the same bounded rubric on known-defect and known-correct artifacts.

- Sonnet 5: known defect -> BLOCK; known-correct artifact -> PASS.
- The known defect was already caught by the improved Luna Reviewer, so premium remains optional rather than routine.
- Opus 4.8 frontmatter selection silently fell back to Sonnet in the observed CLI environment.
- Explicit `--model=claude-opus-4.8` was unavailable and made zero Opus model calls.

Product candidate:

- one `Premium Review` custom agent;
- Sonnet 5 backing candidate;
- `send:false` human spend boundary;
- no automatic premium calls;
- no second premium escalation/menu;
- surface backing-model unavailability instead of pretending the requested model ran.

Actual handoff rendering/switching is still part of real VS Code Gate A, but the product UX decision itself is no longer open-ended.

## Gate A automated wiring result

### Leading: ambient Main

Branch: `rc/v1.1-vscode-gate-ambient`  
Draft PR: **#15**

Main frontmatter intentionally omits both `tools` and `agents`.

Reason:

- preserves the v1.0 contract that VS Code owns developer-selected built-in/MCP/extension tools;
- avoids hard-coding arbitrary developer MCP/extension names;
- Main instruction body strictly permits delegation only to the seven exact Over the Luna leaves.

Automated adversarial evidence:

- attractive unrelated decoy agents diverted broad discovery **0 / 6 scored runs**;
- every scored broad discovery used intended Luna Architect;
- clean read-only handback produced zero Main repo rehydration;
- one clean run had a rejected `task` call missing `description`, but it produced no `invoke_agent`; immediate retry executed exactly one Architect. Track as runtime call-shape noise, not recursive reasoning.

PR #15 has green static/runtime validation and keeps manifest version `1.0.0`.

### Fallback: schema-strict Main

Branch: `rc/v1.1-vscode-gate-schema`  
Draft PR: **#16**

Main explicitly lists built-in tools including `agent` and exact Council `agents`.

Benefit: structural Council allow-list.

Risk: explicit Main tool list may not preserve arbitrary developer-selected MCP/extension tools zero-config. This would regress the v1.0 MCP ownership contract unless actual VS Code proves sufficient tool-picker behavior.

PR #16 has green static/runtime validation and keeps manifest version `1.0.0`.

### Rejected: wildcard-schema compromise

`tools: ['*', 'agent']` was tested as an attempt to combine explicit Council structure with ambient tool breadth.

Copilot CLI 0.0.420 emitted `Invalid tool '*'`. Do not ship or re-test this as a default wiring unless VS Code itself later documents and demonstrates different Agent Plugin semantics.

## Exact ambient MCP surrogate — inconclusive because outer policy blocked the server

Run: **32327584441**, Copilot CLI **1.0.80**, 2 repetitions.

The actual PR #15 branch was checked out. A harmless local stdio MCP `v11gate` was supplied through supported `--additional-mcp-config` and exposed an `echo` marker.

Both sessions reported before agent tool use:

`1 MCP server was blocked by policy: 'v11gate'`

`session.mcp_servers_loaded` did not contain `v11gate`. Therefore expected marker 0/2 is **not evidence that ambient Main/Tool Worker lost MCP through frontmatter**; the server was removed by an outer Copilot policy first.

Behavior after the policy block was correct:

- bounded task routed `SIMPLE + NONE`;
- exactly one Luna Tool Worker per run;
- no repository reads/mutation/Reviewer/premium;
- unavailable MCP reported explicitly;
- no shell/HTTP bypass.

GitHub's current CLI/admin documentation confirms that session MCP config and custom-agent tool configuration are still subject to organization/enterprise/managed MCP allow/deny policy, including local servers. Do not spend more paid CLI runs on this fixture until the policy permits it.

**Real VS Code must test a developer-selected MCP/extension tool that is actually permitted by the active Copilot policy.**

## Paid-probe SOP / branch hygiene

One-shot paid PR-triggered workflows can retrigger while they remain in the PR diff. Durable SOP:

1. create one-shot workflow;
2. confirm intended run is queued/in-progress at a fixed launch SHA;
3. **immediately delete the one-shot workflow**;
4. collect artifacts later from the already-launched run;
5. never leave `*_once.yml` in normal branch state.

Persistent paid research workflows remain manual-only. Static tests check for residue.

After interruption:

1. check PR #13 head and latest `Validate plugin`;
2. verify no `*_once.yml` residue;
3. inspect whether a relevant paid run already exists before launching another;
4. read `PREPRODUCTION_RC2_RESULTS_2026-08-20.md` and `VSCODE_GATE_A_AUTOMATED_RESULTS_2026-08-20.md` before changing policy thresholds/wiring.

## Exact next work — real VS Code Gate A

Use **PR #15 / `rc/v1.1-vscode-gate-ambient` first**. Its `docs/V1_1_VSCODE_GATE.md` contains the full checklist.

Must observe in authenticated VS Code Agent Plugin runtime:

1. plugin loads without customization diagnostics errors;
2. ambient Main actually exposes/uses `agent/runSubagent`;
3. a **policy-permitted developer-selected MCP/extension tool** remains usable without Over the Luna-specific frontmatter config;
4. unknown broad discovery selects exact `Luna Architect`, not another installed custom agent;
5. leaf restrictions remain effective;
6. sufficient read-only Architect handback causes no Main repository replay;
7. tiny/local/broad/risk routing/assurance shapes survive real runtime;
8. exact-name `Premium Review` handoff renders/switches correctly;
9. Premium remains `send:false` / human initiated and model substitution is not silently misrepresented.

If ambient fails item 2 or 4 materially, test PR #16 schema-strict fallback. If ambient fails item 3 **while the selected integration is known policy-permitted**, treat that as real evidence against ambient rather than confusing it with the Actions policy block above.

## After Gate A passes — Gate C productization

Then, and only then:

- freeze selected Main wiring as the release contract;
- port/finalize actual `agents/` on a versioned release branch;
- update runtime-contract tests;
- update README / README.ko / DESIGN / SMOKE_TEST / CONTRIBUTING / MCP guidance;
- run packaged-plugin clean-install smoke tests;
- decide which research infrastructure remains;
- bump changelog/version to `1.1.0`;
- prepare release integration into `main`.

## Current branch/state

- automated Luna core: **PRE-PRODUCTION RC2 — 8/8 stable**;
- premium UX: **single Premium Review decision selected; real UI verification pending**;
- ambient Gate A RC (#15): **prepared, validation green, leading for real VS Code**;
- schema fallback (#16): **prepared, validation green**;
- wildcard candidate: **rejected**;
- headless selected-MCP inheritance: **unresolved due outer MCP policy block**;
- real VS Code runtime: **pending and now the decisive blocker**;
- released `main`: **still v1.0.0**;
- PR #13: remain draft/research-only until Gate A closes.

## Definition of ready for v1.1 release editing

- automated RC2 evidence stable — **yes**;
- premium UX/manual spend decision explicit — **yes**;
- real VS Code Main tool/subagent wiring selected and verified — **pending**;
- actual policy-permitted selected-tool inheritance verified — **pending**;
- actual Premium Review handoff behavior verified — **pending**.

When those final runtime items close, productization/versioning can begin immediately; no additional routing architecture research should be needed unless the runtime falsifies a contract.
