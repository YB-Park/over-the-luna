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
- Reasoning/effort setting shown by product, if any: Terra trace reports reasoning_effort=medium in Phase 0 tool-boundary probe
- Relevant organization model/tool policy:
- Copilot usage/billing snapshot before experiment: Copilot Pro — 199 / 1,500 included AI credits used; approximately 1,301 remaining; resets Oct 1, 2026; additional usage disabled ($0 budget). Model usage Sep 1–7: GPT-5.6 Terra 92.39 credits / $0.92, Claude Haiku 4.5 59.98 / $0.60, GPT-5.6 Luna 39.15 / $0.39, GPT-5.4 7.61 / $0.08. Source: user-provided GitHub Usage screenshot.
- Copilot usage/billing snapshot after experiment:

## Phase 0 — structural smoke

| Check | PASS/FAIL | Evidence |
|---|---|---|
| Deep Judgment visible as Terra | PASS | CLI session model = `gpt-5.6-terra` |
| Terra tool surface is agent-only | PASS | Global CLI pool included `view/glob/rg`, but Terra parent used only `task`; repository reads occurred only inside Luna Architect |
| Only four named Luna evidence leaves are invocable | PARTIAL | Static validator enforces the four-name allow-list; runtime exercised Architect only |
| Luna leaf actually runs as Luna | PASS | `Luna Architect` dispatched as `gpt-5.6-luna` |
| Terra does not directly read/search/edit/execute | PASS | OTel/event trace shows Terra parent -> `task`; Architect performed 11 `view` calls in final Phase 0 probe |
| Implement handoff targets Over the Luna | STATIC PASS | Validator pins exact handoff target; non-interactive CLI does not render VS Code handoff UI |
| Handoff remains send:false | STATIC PASS | Validator pins `send:false`; UI rendering remains a later VS Code gate |
| No mutation before human handoff | PASS | Pre/post `git diff` and `git status` identical/clean |

## Phase 1 — positive replay

Score each axis 0–2. Blind the arm labels during scoring when practical.

| Case | Arm | Correctness | Grounding | Discrimination | Execution usefulness | Scope discipline | Total /10 | Luna leaves | Tool calls | Time | Usage/cost shown | Decision changed by evidence? | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| P1 | A | 2 | 2 | 2 | 2 | 2 | 10 | 1 | 28 total visible tool starts (1 task + Architect reads) | ~31s Architect + parent overhead | 1.926672 AI credits (OTel `totalNanoAiu`) | Yes within Luna path: Architect evidence resolved the decision | Exact accepted v0.6 direction; one Architect |
| P1 | B | 2 | 2 | 2 | 2 | 2 | 10 | 2 | 51 total visible tool starts (2 task + leaf reads) | Architect ~96s + Skeptic ~40s + Terra overhead | 8.031923 AI credits (OTel `totalNanoAiu`) | Evidence reinforced but did not change the final direction vs baseline | Exact accepted v0.6 direction; materially higher spend; no decision advantage over A |
| P2 | A | 1 | 2 | 1 | 1 | 2 | 7 | 2 | 78 visible tool starts (2 task + leaf reads) | Architect ~191s + Skeptic ~99s + parent overhead | 9.879579 AI credits (OTel `totalNanoAiu`) | Yes, but converged on an incomplete production correction | Paired Luna control. Correctly found post-trace `_closed` guard, but explicitly rejected reordering `TCPConnector.close()`; accepted PR #12787 requires both reorder + guard. |
| P2 | B | 2 | 2 | 2 | 2 | 1 | 9 | 3 | 71 visible tool starts (3 task + leaf reads) | Architect ~158s + Skeptic ~148s + Architect ~78s + Terra overhead | 16.570934 AI credits (OTel `totalNanoAiu`) | Yes; evidence separated reorder-only from guard-only and changed the execution contract | Paired Terra candidate. Matched accepted PR #12787 core: base close before owned resolver close + post-trace closed guard. Scope penalty: also proposed a throttled-path guard not present in merged patch. |
| P3 | A | 1 | 2 | 2 | 1 | 1 | 7 | 2 | 72 visible tool starts (2 task + leaf reads) | Architect ~83s + Skeptic ~102s + parent overhead | 8.462141 AI credits (OTel `totalNanoAiu`) | Yes; evidence correctly rejected raw-data rebuild but left an over-broad replayability design | Paired Luna control. Correct causal core (reuse prior payload; file rewind; async/multipart one-shot risk) but proposed new write-start/replayability machinery, told downstream not to close failed body before retry, and did not identify the accepted minimal `consumed`-state changes as production mutations. |
| P3 | B | 2 | 2 | 2 | 2 | 1 | 9 | 2 | 62 visible tool starts (2 task + leaf reads) | Architect ~106s + Skeptic ~127s + Terra overhead | 14.208943 AI credits (OTel `totalNanoAiu`) | Yes; evidence tied retry routing to payload lifecycle and nested replayability | Paired Terra candidate. Correctly selected fresh request + prior payload, identified partial async consumption as the `consumed` contract defect, and included payload/multipart mutation surfaces. Scope penalty: framed the fix as a more general replayability capability than the merged patch required. |

## Phase 1 — negative controls

| Case | Verdict | Luna leaves | Direct Terra environment tool? | Usage/cost shown | PASS/FAIL | Notes |
|---|---|---:|---|---|---|---|
| N1 | NOT_JUSTIFIED | 0 | No | 2.599850 AI credits (OTel `totalNanoAiu`) | PASS | Single Terra trajectory; no tools/leaf calls; explicitly rejected premium judgment for deterministic one-word edit. |
| N2 | NOT_JUSTIFIED | 1 | No | 3.994315 AI credits (OTel `totalNanoAiu`) | PASS | Exactly one Luna Architect; 12 repository `view` calls; returned concrete language-continuity paths/contracts then rejected Terra as unnecessary. |

## Phase 1 gate

- Candidate wins at least 2/3 positive cases: PASS — P2 and P3 wins; P1 tie
- No material regression on remaining positive case: PASS — P1 tied 10/10, but cost was higher
- N1 = NOT_JUSTIFIED: PASS — zero leaf calls
- N2 = NOT_JUSTIFIED: PASS — exactly one bounded Architect call
- Structural boundaries held: PASS in automated CLI probes — Terra parent used only `task`; leaves owned repository reads; no mutation before implementation phase
- <= 3 Luna leaf calls per Terra run: PASS — P2 used 3; P3 used 2; N1 0; N2 1
- At least one win reflects better consequential discrimination rather than longer prose: PASS — P2 Terra selected both shutdown reorder and post-trace guard while Luna explicitly rejected the accepted shutdown reorder

**Gate:** `PROCEED_TO_PHASE_2`

Rationale: Phase 1 produced two held-out model-isolation wins on consequential concurrency/data-integrity decisions, no correctness regression on P1, clean selectivity negatives, and no structural boundary violation. Terra is materially more expensive, so Phase 2 must now prove downstream rework/risk reduction rather than plan quality alone.

## Phase 2 — held-out end-to-end

| Task | Arm | Final correctness | Wrong-direction edits | Rework/repair count | Recovery count | Reviewer findings | Boundary reopen | Plan/implementation contradiction | Time | Usage/cost shown | Notes |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| Root-cause | Baseline | FAIL vs accepted fix | 1 wrong architecture direction (lock lazy imports) | production approach must be replaced | 0 | Reviewer PASS despite oracle mismatch | 0 | none — implementation faithfully followed its own wrong diagnosis | ~89s agent session | 2.156074 AI credits | 30 focused tests passed; full suite 176 passed + 12 missing-httpbin fixture errors. Accepted PR #692 removes lazy imports from async setup via module-level conditional imports; baseline retained lazy imports and added locking. |
| Root-cause | Candidate | FAIL vs accepted fix | 1 amplified wrong architecture direction (per-instance lock/backend-affinity design) | Deep Judgment and implementation both require replacement | 0 | Reviewer PASS despite oracle mismatch | 0 | none — Main implemented the Terra contract consistently, but the contract was wrong | ~246s judgment + ~139s implementation | 8.865809 judgment + 3.512276 implementation = 12.378085 AI credits | 32 focused tests passed; full suite 178 passed + 12 missing-httpbin fixture errors. Terra explicitly rejected eager imports, while accepted PR #692 uses module-level conditional imports with ImportError guards. |
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

## Interim observations — Phase 0 / P1

- The first one-shot attempt used `--max-ai-credits=20` and was rejected by Copilot CLI before model invocation; current CLI requires at least 30. No model inference occurred in that failed attempt.
- A first valid Phase 0 probe accidentally set the global CLI tool ceiling to subagent tools only, which prevented Architect repository reads. That run was treated as harness-test setup evidence, not the final structural result.
- The corrected Phase 0 probe exposed `view/glob/rg` globally while keeping Deep Judgment frontmatter at `tools: ['agent']`. Terra used only `task`; Luna Architect performed repository reads; final verdict was `NOT_JUSTIFIED`; no mutation occurred.
- P1 is a **tie on decision quality (10/10 vs 10/10)**, not a Terra win. Candidate cost was approximately 4.17x the Luna-only baseline and used two evidence leaves instead of one. Under the experiment gate, P2 and P3 would both need to show candidate wins for the positive-case threshold to remain reachable.

## Methodology correction before P2

P1 used the released Over the Luna Main as the Luna baseline. That is useful as a product-level preliminary comparison, but it is not a clean model-isolation test because the stable Main prompt already contains lessons from historical architecture decisions. Before P2, a hidden `Deep Judgment Luna Control` was added with the same judgment instructions, the same four evidence leaves, the same `agent`-only parent tool boundary, and the same non-mutating handoff contract as Terra Deep Judgment. From P2 onward, the principal comparison changes only the parent model: GPT-5.6 Luna vs GPT-5.6 Terra.

### P2 accepted-fix oracle

Held-out case: aiohttp `TCPConnector.close()` / in-flight DNS race at pre-fix commit `f387f620459cf5b8e0e1df2f18dc70e9c3d29909`. The task prompt supplied the runtime symptom but not the later PR or patch. After both arms completed, outputs were compared with merged aiohttp PR #12787.

The accepted production patch contains two coupled changes:

1. call the base connector close before closing the owned resolver, so connector closure is published before resolver invalidation;
2. after DNS-start tracing and before the uncached resolver call, raise `ClientConnectionError` when the connector is closed.

The Luna control found (2) but explicitly rejected (1). Terra selected both (1) and (2), while additionally recommending a throttled/cache-miss guard that the accepted patch did not include. This is therefore scored as a **material Terra decision win with a scope-discipline penalty**, not a perfect result.

### P3 accepted-fix oracle

Held-out case: aiohttp internally retried request body-integrity bug at pre-fix commit `6264834e7023aadd85646fd79637942b9edbe22b`. The prompt supplied the file-cursor/truncated-retry symptom and the requirement not to make one-shot async bodies appear replayable, but not the later patch. Outputs were scored after completion against merged aiohttp PR #13330.

The accepted patch:

1. on retryable connection failure, settles/closes the failed request writer, rejects retry when the existing body is consumed, and passes the **existing request payload** into the next fresh request instead of rebuilding it from raw `data`;
2. marks uncached async iterable and body-part payloads consumed as soon as draining begins, so interrupted writes cannot appear replayable;
3. makes multipart writer `consumed` reflect nested parts;
4. adds integration/unit regressions for complete file resend and refusal to retry an unreplayable async body.

Both paired arms found the major rebuild-vs-reuse cause. The Luna control, however, proposed an additional write-start/replayability state machine and did not identify the accepted payload `consumed` corrections as concrete production mutations. Terra localized the contract defect into payload/multipart state and produced a more directly implementable direction, while still overgeneralizing the minimal patch into a broader replayability abstraction. This is scored as a second **material Terra decision/execution-contract win with a scope penalty**.

### Positive-case interim gate

- P1 product-level historical comparison: tie, 10/10 vs 10/10; Terra cost materially higher.
- P2 paired model-isolation concurrency case: Terra win, 9/10 vs 7/10.
- P3 paired model-isolation data-integrity case: Terra win, 9/10 vs 7/10.
- Candidate therefore satisfies the numeric positive-case requirement (wins at least 2/3) **subject to both negative controls and structural/selectivity checks**.


### Phase 2 root-cause result — httpcore AnyIO import race

Historical workspace: `encode/httpcore@5f2e454801f50051d5a66203401a67e5b2a32e9d`  
Hidden accepted oracle after both arms: merged PR #692, “Use conditional imports of trio and anyio.”

The accepted patch removes imports from lazy synchronization setup and performs module-level conditional imports:

- `try: import trio ... except ImportError: trio = None`;
- `try: import anyio ... except ImportError: anyio = None`;
- setup methods then construct the runtime primitive from the already-imported module and raise a clear runtime dependency error when the selected optional backend is unavailable.

**Baseline result:** Luna diagnosed partial-state publication and introduced a module-global `threading.Lock` around the existing lazy imports. This preserved the actual risky pattern. Its focused tests passed and its Reviewer returned PASS, but the accepted root-cause direction was missed.

**Candidate result:** Terra Deep Judgment made the same causal mistake more confidently. It explicitly rejected “eagerly import Trio or all backends” on the ground that Trio is optional, overlooking the accepted conditional-import pattern that preserves optionality. Main Luna then faithfully implemented the Terra contract with per-instance locks, backend-affinity checks, and additional tests. This is internally coherent but externally wrong against the accepted production fix.

This is a strong negative result for the hypothesis:
- Deep Judgment did **not** reduce downstream rework;
- the candidate cost about **5.74x** baseline (12.378085 vs 2.156074 AI credits);
- the checkpoint amplified an incorrect causal model into a larger patch;
- normal focused tests and the existing Reviewer were insufficient to reveal the mistake.

Do not reinterpret this as a near miss. For this held-out case, the Terra checkpoint failed its intended purpose.


### Invalid Phase 2 cross-cutting attempt — Django editable-install contamination

Run: GitHub Actions `34176238925`.

This run is **excluded from promotion evidence**. The workflow installed both historical Django workspaces with `pip install -e .` into one Python environment. The second editable install pointed Python at the candidate checkout, and the baseline validation log explicitly reported:

`Testing against Django installed in '.../django-candidate/django'`

Therefore baseline tests were not guaranteed to execute baseline production code. The run cannot support a baseline-vs-candidate conclusion.

Cost accounting only:
- baseline Luna session: 7.195301 AI credits;
- Terra Deep Judgment: 3.959550 AI credits;
- candidate Luna implementation: 5.806891 AI credits;
- total invalid-run spend: 16.961742 AI credits.

The next rerun must:
1. avoid editable Django installs;
2. set `PYTHONPATH` explicitly per checkout for both agent execution and validation;
3. use shallow base-SHA workspaces so later history is unavailable to agents;
4. inject hidden accepted-behavior tests only after agent implementation is complete.
