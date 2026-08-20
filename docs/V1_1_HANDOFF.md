# v1.1 durable handoff

Last updated: **2026-08-20**  
Primary research branch: `research/v1.1-runtime-baseline`  
Primary PR: **#13 — Research v1.1 runtime behavior and experiment harness**

This is the operational handoff. If a session dies, start here instead of reconstructing the experiment history.

## Current status in one paragraph

The automated GPT-5.6 Luna core has reached a **pre-production RC2**. The final controlled matrix ran tiny/local/broad/risk boundaries twice each and passed **8/8** visible validation + hidden behavioral oracle + routing/ownership policy gates. The canonical RC2 preserves `SIMPLE / STANDARD / DEEP` investigation and separate `NONE / REVIEW / RISK` assurance, keeps Main as the sole mutation owner, gives SIMPLE a bounded no-glob local-orientation budget, isolates unknown semantic discovery to Architect with a sealed work set, gives normal REVIEW exactly one named artifact-first Luna Reviewer, and requires RISK to receive at least one post-change named Luna Reviewer. Premium remains human initiated. **Do not merge or version-bump yet:** real VS Code tool/subagent wiring and premium UX are still release blockers.

## Read these first

1. `docs/V1_1_DESIGN_CANDIDATE.md` — current design and open blockers.
2. `experiments/PREPRODUCTION_RC2_RESULTS_2026-08-20.md` — final automated-core 8/8 evidence and failure history.
3. `docs/V1_1_RESEARCH.md` — original hypotheses/invariants/release gates.
4. `experiments/INVARIANT_CHALLENGE_REVIEW_RESULTS_2026-08-19.md` — why Reviewer challenges one invariant.
5. `experiments/ARCHITECT_PACKET_ABLATION_RESULTS_2026-08-19.md` — why the compact Architect packet is preferred.
6. `docs/V1_1_VSCODE_GATE_A.md` — exact next real-runtime A/B procedure.

## Canonical RC2 files

Use these as the current automated-core implementation:

- Main: `experiments/v1_1_candidate_rc2.agent.md`
- Architect: `experiments/v1_1_candidate_architect_packet_v3.agent.md`
- Reviewer: `experiments/v1_1_candidate_reviewer_rc.agent.md`

Release-gate infrastructure:

- `experiments/v1_1_release_gate_fixture.py`
- `experiments/v1_1_release_gate_evaluator_v6.py`
- `experiments/v1_1_release_gate_evaluator_rc2.py`
- `tests/test_v1_1_candidate_contract.py`
- `tests/test_v1_1_rc_contract.py`
- `tests/test_v1_1_release_gate_evaluator.py`
- `tests/test_v1_1_rc_release_gate.py`

Do **not** blindly copy the RC2 Main frontmatter into released `agents/`: its missing `tools` field is now an explicit VS Code Gate A question.

## Automated-core release result

Final RC2 run: **32323722543**  
Launch commit: `b2b3de4b58a60e4fe62a19f18898f7844c63efaa`

| Boundary | Expected product shape | Final result |
| --- | --- | --- |
| tiny | `SIMPLE + NONE`, Architect 0, Reviewer 0 | 2/2 PASS |
| local | `SIMPLE + REVIEW`, Architect 0, Reviewer 1 | 2/2 PASS |
| broad | `STANDARD + REVIEW`, Architect 1, sealed work set, Reviewer 1 | 2/2 PASS |
| risk | `RISK`, post-change named Reviewer >=1 | 2/2 PASS |

All eight hidden behavioral oracles passed. Automatic premium count was zero in all eight runs.

The important point is that earlier hidden-PASS runs were deliberately rejected for product-discipline failures such as unnecessary tiny review, generic root globs, README/tooling over-scouting, post-Architect broad rehydration, repeated normal Reviewers, skipped RISK final review, and built-in `code-review` substitution. RC2 is the first candidate to close all four boundaries together.

## Decisions with strong automated evidence

### Keep

- `SIMPLE / STANDARD / DEEP` investigation vocabulary.
- Separate `NONE / REVIEW / RISK` assurance state.
- Main Luna as sole mutation owner.
- Bounded SIMPLE locator orientation for already-specified local behavior.
- No `glob` or background-prose browsing during SIMPLE orientation.
- Unknown semantic discovery -> Architect before Main consumes broad evidence.
- Architect packet: `DECISION / EVIDENCE / RELATIONSHIPS / MUTATION_TARGETS / UNRESOLVED`.
- `MUTATION_TARGETS` as complete post-handback implementation/test/helper work set.
- Explicit `Boundary sealed — work set: ...` transition.
- No Main broad rehydration after sufficient Architect handback.
- NONE for genuinely mechanical work.
- Normal REVIEW = exactly one named Luna Reviewer task call total.
- Concrete current unified-diff artifact between explicit markers before Reviewer invocation.
- Reviewer bounded dependency closure + one consequential invariant challenge.
- Main adjudication + repair/revalidation without recursive normal review.
- RISK gets at least one post-change named Luna Reviewer; pre-change Skeptic/Architect do not substitute.
- Automatic core remains GPT-5.6 Luna only.
- Premium remains explicitly human selected.

### Do not resurrect without new evidence

- lowering SIMPLE merely to increase Council usage;
- treating every locator/search as semantic discovery;
- broad Main scouting merely to decide whether Architect is useful;
- generic `glob '*'`/root inventory on local tasks;
- README/docs/background exploration for implementation confidence;
- treating Architect invocation alone as proof of isolation;
- allowing Main to replay broad discovery after Architect;
- strict zero-read Reviewer;
- dependency reads without invariant falsification;
- recursive Reviewer-until-PASS loops;
- normal Reviewer artifact/VERIFY retry;
- pre-change RISK leaves as a substitute for final artifact review;
- generic/built-in `code-review` as the product Reviewer;
- hidden automatic premium inference.

## Branch hygiene / paid-probe SOP

One-shot paid PR-triggered workflows caused an important operational problem: GitHub PR `paths` filtering can retrigger an older one-shot workflow while that file remains part of the PR diff.

The durable SOP is now:

1. create a one-shot workflow;
2. confirm the intended run is `queued`/`in_progress` at its fixed launch SHA;
3. **immediately delete the one-shot workflow**;
4. collect artifacts later from the already-launched run;
5. never leave `*_once.yml` in normal branch state.

Static contract tests also check for one-shot residue.

Persistent paid research workflows remain intentionally manual-only.

Before new work after interruption:

1. check PR #13 head and latest `Validate plugin`;
2. list `.github/workflows` and verify no `*_once.yml` residue;
3. inspect whether a relevant paid run already exists before launching another;
4. read `PREPRODUCTION_RC2_RESULTS_2026-08-20.md` before changing routing thresholds.

## Exact next work

### Gate A — real VS Code tool/subagent/runtime A/B

This is now the primary blocker.

Latest VS Code documentation says that if a custom agent specifies `agents`, the `agent` tool must be enabled/included. Our CLI RC2 deliberately omitted Main `tools` to preserve ambient developer-selected built-in/MCP/extension tools. CLI success therefore does not prove the final VS Code wiring.

Test two Main frontmatter strategies in the real VS Code Agent Plugin runtime:

#### A. schema-strict allowlist

- explicit `agents: [...]`;
- explicit `agent`/`agent/runSubagent` capability in Main tools;
- verify actual built-in/MCP/extension availability and whether developer-selected tools are preserved.

#### B. ambient-tool preservation

- omit Main `tools`;
- remove frontmatter `agents` if required;
- keep the allowed leaf names as an instruction-level contract;
- verify `agent/runSubagent` availability and ensure no unintended agent is selected.

For both:

- plugin loads cleanly with no customization diagnostics errors;
- run representative tiny/local/broad/risk sessions;
- verify actual subagent/tool trace and leaf tool restrictions;
- verify configured MCP/extension tools remain usable as intended;
- verify handoff buttons render/switch exact custom-agent names;
- verify premium handoffs remain `send:false` / user initiated.

See `docs/V1_1_VSCODE_GATE_A.md` for the exact checklist.

### Gate B — premium UX

After Gate A establishes the normal Luna layer in the real product runtime, decide:

> one human `Premium Review` affordance vs separate Sonnet/Opus choices.

Measure:

- plan/model availability;
- incremental findings over Luna Reviewer;
- false-positive/rework pressure;
- latency and premium cost;
- user decision count;
- whether one simplified affordance can preserve explicit spend authorization.

Never auto-send premium review.

### Gate C — versioned productization

Only after A/B close:

- port accepted RC2 body/leaf contracts into real `agents/` with the selected VS Code Main tool wiring;
- update runtime-contract tests;
- update README / README.ko / DESIGN / SMOKE_TEST / CONTRIBUTING as required;
- decide which research infrastructure remains;
- bump changelog/version to `1.1.0` only after product runtime acceptance;
- then create the release merge plan.

## Current branch/state

- automated CLI core: **PRE-PRODUCTION RC2 — 8/8 stable**;
- static contract tests: **green**;
- one-shot paid workflow residue: **none expected**;
- real VS Code runtime: **pending**;
- premium UX: **pending**;
- released `main`: still v1.0.0;
- PR #13: should remain draft/research-only until Gate A/B close.

## Definition of “ready to edit released v1.1 agents”

Do not start versioned productization until all are true:

- automated RC2 evidence stable — **yes**;
- real VS Code Main tool/subagent wiring selected and verified — **pending**;
- actual handoff/tool inheritance behavior verified — **pending**;
- premium UX/manual gate decision explicit — **pending**.

When those close, convert RC2 into the release contract and only then change the real product agents/version.
