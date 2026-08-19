# v1.1 durable handoff

Last reconstructed/updated: **2026-08-19**  
Primary research branch: `research/v1.1-runtime-baseline`  
Primary PR: **#13 — Research v1.1 runtime behavior and experiment harness**

This file is the operational handoff. If a session dies, start here instead of reconstructing the entire branch history.

## Current status in one paragraph

The automated GPT-5.6 Luna core has a **leading v1.1 design candidate**. Investigation keeps `SIMPLE / STANDARD / DEEP`; assurance is a separate early `NONE / REVIEW / RISK` state. Broad disposable repository discovery is isolated to Luna Architect using an evidence packet and a Main-side tool-closed handback. Main remains the only mutation owner. Normal `REVIEW` uses exactly one artifact-first Reviewer that closes acceptance-critical semantic dependencies and challenges one consequential invariant before PASS. Main adjudicates findings, repairs/revalidates accepted issues, and does not automatically re-review. This shape has replicated on the self-hosted OTel mutation and on an external generated TTL-cache fixture. **Do not merge or version-bump yet**: real VS Code/runtime behavior and premium UX remain open gates.

## Read these first

1. `docs/V1_1_DESIGN_CANDIDATE.md` — current evidence-backed design candidate.
2. `docs/V1_1_RESEARCH.md` — original hypotheses, invariants, evidence layers, release gates.
3. `experiments/INTEGRATED_CANDIDATE_RESULTS_2026-08-19.md` — combined self-hosted replication.
4. `experiments/EXTERNAL_INTEGRATED_CANDIDATE_RESULTS_2026-08-19.md` — external TTL-cache replication.
5. `experiments/INVARIANT_CHALLENGE_REVIEW_RESULTS_2026-08-19.md` — why the current Reviewer shape exists.
6. `experiments/ARCHITECT_PACKET_ABLATION_RESULTS_2026-08-19.md` — why the simpler Architect packet is preferred.

## Candidate files

Use these as the current research implementation of the design:

- Main integrated policy: `experiments/v1_1_candidate_integrated.agent.md`
- Architect packet: `experiments/v1_1_candidate_architect_packet.agent.md`
- Reviewer: `experiments/v1_1_candidate_invariant_reviewer.agent.md`

Do **not** promote these into `agents/` blindly. Productization comes after runtime gates.

## Decisions with strong automated evidence

### Keep

- `SIMPLE / STANDARD / DEEP` as investigation vocabulary.
- Separate first-class `NONE / REVIEW / RISK` assurance state.
- Main Luna as sole mutation owner.
- Architect for broad disposable repository scouting when locality is not already known.
- Architect evidence packet:
  - `DECISION`
  - `EVIDENCE`
  - `RELATIONSHIPS`
  - `MUTATION_TARGETS`
  - `UNRESOLVED`
- Main-side tool-closed handback; do not replay broad evidence after Architect.
- Normal REVIEW = exactly one fresh Reviewer invocation for the whole task trajectory.
- Reviewer starts from exact artifact + validation, closes only acceptance-critical dependencies, then challenges one consequential invariant.
- Main adjudicates Reviewer findings and revalidates accepted repairs without automatic re-review.
- Automatic core remains GPT-5.6 Luna only.
- Premium remains human-selected.

### Do not resurrect without new evidence

- lowering SIMPLE merely to get more Council calls;
- treating STANDARD/Architect invocation as proof of context isolation;
- letting Main re-read the whole repository after Architect returns;
- “all non-trivial mutation => recursively review until Reviewer PASS”;
- late-only assurance gates that are easy for Main to skip;
- strict zero-read artifact review;
- dependency reads without an explicit invariant/falsification step;
- the more elaborate bounded Architect prompt as a default — direct A/B did not show a stable advantage;
- hidden/automatic premium inference.

## Important experiment outcomes

### Context isolation

`SCOUTING_ISOLATION_MATRIX` showed that baseline/locality policies could still duplicate broad repository work even when Architect was called.

`EVIDENCE_BOUNDARY_RESULTS` demonstrated replicated read-only closure: full evidence-boundary runs left Main with only the Architect `task` call and zero repository read/search calls after handback.

### Reviewer evidence selection

The same exact completed OTel ownership patch was reviewed under several policies:

- current Reviewer: cross-trace defect found 0/2;
- strict artifact-first: 0/2;
- dependency closure only: 0/2;
- dependency + invariant challenge: **2/2**.

The successful finding was that `span_id` is trace-local and parent lookup must preserve `(trace_id, span_id)` identity.

### One-review trajectory

Earlier bounded mutation work produced **four Reviewer invocations** and ~887k input tokens. The integrated candidate explicitly caps normal REVIEW at one invocation.

Integrated self-hosted repetitions:

- Reviewer 1/1 each;
- same cross-trace MUST-FIX found both times;
- Main repaired/revalidated;
- no second Reviewer;
- strengthened hidden contract passed both times.

### External replication

Generated TTL-cache fixture, two repetitions:

- route `SIMPLE + REVIEW` both times;
- no Architect, which is correct for the local task;
- exactly one Reviewer each;
- one Reviewer PASS;
- one Reviewer found a real MRU test-contamination gap and Main strengthened the test;
- exact uploaded patches pass the corrected/strengthened hidden behavior oracle while the untouched baseline fails it.

The GitHub workflow's original hidden step had a `PYTHONPATH`/script-location harness mistake; this is documented in the external result file. Do not interpret those workflow `hidden-tests.exit=1` values as candidate failures.

## Current branch hygiene

One-shot paid experiment workflows are temporary by design and must be deleted after artifact collection.

At the time this handoff was written, the latest external one-shot workflow had been removed. The repository should have only the intentionally manual paid research workflows already covered by runtime-contract tests.

Before doing anything else after a future interruption:

1. check PR #13 head and `Validate plugin`;
2. list `.github/workflows` for any `*_once.yml` paid experiment residue;
3. if an experiment run is still active, collect its artifacts before deleting its workflow;
4. do not start a duplicate paid probe if a relevant run already exists.

## Exact next work

### Gate A — real VS Code runtime/manual integration

Use the actual VS Code Agent Plugin runtime, not Copilot CLI, to validate:

1. plugin loads with the candidate agent contracts;
2. `SIMPLE / STANDARD / DEEP` + assurance state are followed in representative interactive sessions;
3. Architect handback produces the expected context-local behavior in Agent Debug/OTel;
4. selected MCP/extension tools are inherited/preserved as intended when Main has no explicit `tools` field;
5. leaf tool restrictions remain intact;
6. handoff buttons render and switch agents with exact custom-agent names;
7. premium handoffs remain `send: false` / human initiated.

CLI probes are not sufficient proof for these UI/tool-inheritance semantics.

### Gate B — premium UX decision

Once the functional handoff baseline is confirmed in VS Code, decide the product question:

> Should v1.1 expose one human premium-review decision or keep separate Sonnet/Opus choices?

Evaluate:

- plan/model availability;
- incremental judgment vs Luna Reviewer;
- latency/cost;
- false positives / unique actionable findings;
- number of user decisions;
- whether a single `Premium Review` affordance can hide unnecessary model-routing complexity while preserving explicit human spend authorization.

Do not change premium handoffs to auto-send.

### Gate C — productization

Only after A/B:

- port the accepted Main/Architect/Reviewer contracts from `experiments/` into real `agents/`;
- update runtime-contract tests;
- update README / README.ko / DESIGN / SMOKE_TEST / CONTRIBUTING as required;
- decide what research/experiment infrastructure remains in the repository;
- update changelog/version to `1.1.0` only when the runtime design is actually accepted;
- then create the release PR/merge plan.

## Branches

- `research/v1.1-runtime-baseline` — **primary active research line**. Use this unless a new deliberate branch is created.
- `research/v1.1-assurance-candidate` — older assurance experiment line; useful evidence, not the current integrated candidate.
- `research/v1.1-bounded-assurance` — historical branch slot; do not assume it contains newer work than the active research line.

## Safety / cost notes

- Paid Copilot workflows must remain manual-only in normal repository state.
- Temporary PR-triggered one-shot workflows intentionally violate that invariant only long enough to launch a controlled experiment and must then be removed.
- `--max-ai-credits=30` is the CLI minimum supported hard ceiling used by these probes, not a target spend.
- OTel content capture should remain disabled unless a specific experiment explicitly requires otherwise.

## Definition of “ready to implement v1.1 product changes”

Do not begin versioned productization merely because the automated candidate looks good.

The threshold is:

- automated integrated candidate evidence is stable — **currently yes**;
- real VS Code behavior agrees with the intended contracts — **pending**;
- premium UX/manual gate decision is explicit — **pending**;
- no known experiment harness artifact is being mistaken for product behavior — **currently documented**.

When those pending items close, convert the candidate into the v1.1 release contract and only then change the real product agents/version.
