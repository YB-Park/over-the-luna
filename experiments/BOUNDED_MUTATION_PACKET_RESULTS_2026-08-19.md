# v1.1 bounded mutation-packet A/B — 2026-08-19

This experiment follows `MUTATION_BOUNDARY_RESULTS_2026-08-19.md`. It repeats the exact same fixed mutation fixture but compares the previous full evidence-boundary policy with a new bounded mutation-packet policy.

Fixture: `fcf0c568ba5bf41f69f6c9594359842c473d8946`.

Task: integrate tool ownership into `scripts/analyze_otel.py`, preserve the standalone ownership analyzer contract, preserve global tool totals, add Markdown/JSON ownership output, add focused nested-leaf/orphan regressions, and validate the repository.

Both runs used GPT-5.6 Luna only and zero premium models. Hidden ownership tests were created by the workflow after Copilot completed.

## Candidates

### Previous boundary

- Main: `v1_1_candidate_split_packet.agent.md`
- Architect: `v1_1_candidate_architect_packet.agent.md`

This policy establishes early Architect delegation plus a tool-closed Main handback, but asks Architect for a generally complete evidence packet.

### Bounded packet

- Main: `v1_1_candidate_split_bounded_packet.agent.md`
- Architect: `v1_1_candidate_architect_bounded_packet.agent.md`

This version asks Architect to stop once the mutation decision, concrete targets, and contract-critical constraints are established. It also forbids post-handback repository-wide confirmation searches in Main.

## Results

| Metric | Previous boundary | Bounded packet |
| --- | ---: | ---: |
| Hidden ownership contract | pass | pass |
| Repository/plugin validation | pass | pass |
| Visible repository tests | 11 pass | 10 pass |
| Main input | 207,197 | 579,061 |
| Council/reviewer input | 155,774 | 308,210 |
| **Total input** | **362,971** | **887,271** |
| Total output | 36,316 | 16,620 |
| Model calls | 11 | 26 |
| Total tool calls | 31 | 118 |
| Architect views | 11 | 19 |
| Architect input/output | 97,696 / 18,793 | 67,501 / 2,149 |
| Reviewer invocations | **1** | **4** |
| Reviewer views | 7 | 64 |
| Main views | 4 | 5 |

The bounded run's high total cost was **not primarily caused by Architect**. It was dominated by Main repair/revalidation plus repeated Reviewer trajectories.

## Investigation result

### The bounded handback was dramatically more compact

The previous Architect returned 18,793 output tokens in this repeat. The bounded Architect returned 2,149 output tokens while still identifying the correct mutation shape:

- centralize ownership in `scripts/analyze_otel.py`;
- preserve top-level global `tools`;
- retain the standalone `main` / `leaf` / `by_agent` adapter contract;
- mutate `scripts/analyze_otel.py`, `scripts/analyze_tool_ownership.py`, and `tests/test_analyze_otel.py`;
- treat workflow consumers as read-only constraints.

This strongly supports the **decision-complete packet** direction. A context-boundary handback does not need an essay-sized reconstruction of every repository surface.

### But explicit output bounds did not reliably reduce repository reads

The bounded Architect used 19 `view` calls, while the previous-boundary repeat happened to use only 11.

The bounded Architect still inspected several surfaces that were not necessary to choose the mutation targets, including experiment history and duplicate product/contract context. So the new read-discipline language improved packet compression more clearly than it improved scouting breadth.

This is an important falsification: **packet length and repository-read breadth are related but not interchangeable controls.**

### Main-side handback remained acceptably local

After Architect returned, the bounded Main read the concrete analyzer/test implementation neighborhood. Its only later `rg` was scoped to `scripts/analyze_otel.py`, not a repository-wide consumer rediscovery. No `Boundary reopen:` was needed.

The previous-boundary repeat similarly used four mutation-local views plus one local test glob after handback.

So the epistemic-ownership boundary itself survives this replication. The unstable variable moved to Architect completeness and assurance trajectory cost.

## Patch-quality result

Both workflow hidden contracts passed, but the final patches exposed why hidden-test pass rate alone is insufficient.

### Previous-boundary repeat

This run produced a clean 11-test patch and one Reviewer returned no actionable issue. However, inspection against evidence from the prior mutation experiment shows two broader defects remained untested in this particular trajectory:

1. parent lookup was still keyed only by `span_id`, even though span IDs are trace-local and can collide across traces;
2. `scripts/analyze_tool_ownership.py` retained a script-style absolute `from analyze_otel import ...` import, which is unsafe when imported as `scripts.analyze_tool_ownership` / package-style execution.

The workflow's hidden contract did not test either edge. The single Reviewer did not surface them in this repeat.

### Bounded-packet repeat

The bounded run initially introduced real defects, but repeated independent review found several of them:

1. Reviewer 1 found a name-shadowing recursion bug in the standalone adapter; Main fixed it.
2. Reviewer 2 found that ownership parent lookup was not trace-safe; Main changed the index to `(trace_id, span_id)`.
3. Reviewer 3 found the trace-safety fix lacked an actual repeated-ID-across-traces regression; Main added coverage.
4. Reviewer 4 returned PASS after the repairs.

The final bounded patch therefore contains the trace-safe attribution improvement and an explicit cross-trace regression that the previous-boundary repeat missed.

However, it still retained the package-import weakness noted above. Four review passes did **not** guarantee exhaustive correctness.

## Assurance result — the dominant new signal

This A/B accidentally produced a stronger assurance finding than an Architect finding.

The current simplified `Assurance: REVIEW` language allows a natural loop:

> review → accepted repair → "final patch changed" → review again → another repair → review again

In the bounded run that became four Reviewer invocations, 64 Reviewer `view` calls, 21 Main turns, and 887,271 total input tokens.

Several findings were genuinely valuable. The problem is not that review was useless. The problem is that **the review trajectory has no sufficiently explicit economic stopping rule.**

This reinforces the earlier external-fixture conclusion that the unit of assurance cost is not the Reviewer call alone:

> Reviewer → Main adjudication → repair → validation → possible re-review

## Evidence-based position

### Investigation

Keep these principles as the leading v1.1 direction:

- broad disposable discovery has an explicit epistemic owner;
- Architect is invoked before Main consumes broad details;
- Architect returns a decision-complete packet with concrete mutation targets and unresolved facts;
- Main does not replay the broad discovery after handback;
- mutation work reopens only mutation-local implementation/test context.

Do **not** yet freeze the exact bounded Architect prompt. It clearly compresses handback output, but this single repeat did not prove lower read breadth.

### Assurance

The next research priority should be assurance, not another increasingly elaborate Architect prompt.

A `REVIEW` trajectory needs an explicit bounded contract such as:

- exactly one fresh Reviewer for the normal REVIEW state;
- artifact-first evidence: acceptance criteria + exact completed diff + validation evidence before repository browsing;
- Reviewer repository reads only when a concrete candidate finding depends on unchanged context;
- Main adjudicates findings;
- accepted repairs are revalidated by Main but do **not** automatically buy another Reviewer;
- a second independent review is reserved for an explicitly escalated `RISK` state with a genuinely different rubric, not merely because the first review changed the patch.

This is consistent with the earlier assurance-candidate experiments and directly targets the trajectory explosion observed here.

## Next gates

1. Isolate Architect quality from assurance by comparing the previous and bounded Architect directly on the same mutation-oriented **read-only planning** task, with no Main mutation/review trajectory.
2. Then test an **artifact-first single-review** assurance candidate on an identical completed patch so Reviewer browsing, finding quality, and total adjudication cost can be measured without routing noise.
3. Only after those dimensions are separately stable should they be recombined into a v1.1 product candidate.
