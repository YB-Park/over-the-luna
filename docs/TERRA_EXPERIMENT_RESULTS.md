# Terra Deep Judgment Experiment Results

Use this file only for recorded observations from `docs/TERRA_EXPERIMENT.md`. Do not fill missing telemetry with estimates.

## Environment

- Date: 2026-09-07
- VS Code version:
- GitHub Copilot extension/version:
- Plugin branch/commit:
- GPT-5.6 Luna availability:
- GPT-5.6 Terra availability:
- Claude Sonnet 5 availability:
- Reasoning/effort setting shown by product, if any:
- Relevant organization model/tool policy:
- Copilot usage/billing snapshot before experiment: Copilot Pro — 199 / 1,500 included AI credits used; approximately 1,301 remaining; resets Oct 1, 2026; additional usage disabled ($0 budget). Model usage Sep 1–7: GPT-5.6 Terra 92.39 credits / $0.92, Claude Haiku 4.5 59.98 / $0.60, GPT-5.6 Luna 39.15 / $0.39, GPT-5.4 7.61 / $0.08. Source: user-provided GitHub Usage screenshot.
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
