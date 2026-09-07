# Terra Deep Judgment Experiment Results

Use this file only for recorded observations from `docs/TERRA_EXPERIMENT.md`. Do not fill missing telemetry with estimates.

## Environment

- Date:
- VS Code version:
- GitHub Copilot extension/version:
- Plugin branch/commit:
- GPT-5.6 Luna availability:
- GPT-5.6 Terra availability:
- Claude Sonnet 5 availability:
- Reasoning/effort setting shown by product, if any:
- Relevant organization model/tool policy:
- Copilot usage/billing snapshot before experiment:
- Copilot usage/billing snapshot after experiment:

## Phase 0 — structural smoke

| Check | PASS/FAIL | Evidence |
|---|---|---|
| Deep Judgment visible as Terra | | |
| Terra tool surface is agent-only | | |
| Only four named Luna evidence leaves are invocable | | |
| Luna leaf actually runs as Luna | | |
| Terra does not directly read/search/edit/execute | | |
| Implement handoff targets Over the Luna | | |
| Handoff remains send:false | | |
| No mutation before human handoff | | |

## Phase 1 — positive replay

Score each axis 0–2. Blind the arm labels during scoring when practical.

| Case | Arm | Correctness | Grounding | Discrimination | Execution usefulness | Scope discipline | Total /10 | Luna leaves | Tool calls | Time | Usage/cost shown | Decision changed by evidence? | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| P1 | A | | | | | | | | | | | | |
| P1 | B | | | | | | | | | | | | |
| P2 | A | | | | | | | | | | | | |
| P2 | B | | | | | | | | | | | | |
| P3 | A | | | | | | | | | | | | |
| P3 | B | | | | | | | | | | | | |

## Phase 1 — negative controls

| Case | Verdict | Luna leaves | Direct Terra environment tool? | Usage/cost shown | PASS/FAIL | Notes |
|---|---|---:|---|---|---|---|
| N1 | | | | | | |
| N2 | | | | | | |

## Phase 1 gate

- Candidate wins at least 2/3 positive cases: 
- No material regression on remaining positive case:
- N1 = NOT_JUSTIFIED:
- N2 = NOT_JUSTIFIED:
- Structural boundaries held:
- <= 3 Luna leaf calls per Terra run:
- At least one win reflects better consequential discrimination rather than longer prose:

**Gate:** `PROCEED_TO_PHASE_2` / `STOP`

Rationale:

## Phase 2 — held-out end-to-end

| Task | Arm | Final correctness | Wrong-direction edits | Rework/repair count | Recovery count | Reviewer findings | Boundary reopen | Plan/implementation contradiction | Time | Usage/cost shown | Notes |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| Root-cause | Baseline | | | | | | | | | | |
| Root-cause | Candidate | | | | | | | | | | |
| Cross-cutting risk | Baseline | | | | | | | | | | |
| Cross-cutting risk | Candidate | | | | | | | | | | |

## Final decision

Choose one:

- `PROMOTE_FOR_ARCHITECTURE_REVIEW`
- `KEEP_EXPERIMENTAL_AND_COLLECT_MORE_HELD_OUT_EVIDENCE`
- `REDESIGN`
- `KILL`

Decision:

Evidence that would reverse this decision:
