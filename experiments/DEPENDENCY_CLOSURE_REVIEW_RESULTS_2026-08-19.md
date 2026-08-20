# v1.1 dependency-closure Reviewer replication — 2026-08-19

This experiment follows `ARTIFACT_FIRST_REVIEW_RESULTS_2026-08-19.md`. The same exact completed patch was reviewed twice by `v1_1_candidate_dependency_reviewer.agent.md`.

The candidate keeps the exact patch and visible validation as primary evidence, but adds a mandatory checkpoint: before PASS, inspect unchanged helpers/parsers/import contracts that the changed behavior relies on for acceptance-critical semantics.

The reviewed patch and visible validation were identical to the prior ablation. The known patch-relevant oracle remained the same: repeated `span_id` values in different traces can corrupt ownership because the completed patch indexes parent spans by `span_id` alone.

## Results

| Repeat | Verdict | Repo tools | Input | Output | Dependency marker | Cross-trace issue found? |
| --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | PASS | 3 `view` | 20,845 | 780 | yes | **no** |
| 2 | PASS | 3 `view` | 21,000 | 837 | yes | **no** |

Both reviews were read-only and the pre/post diff was identical. Visible tests and plugin validation passed in both runs.

## What the Reviewer actually inspected

Both repeats opened only:

- `scripts/analyze_otel.py` in two bounded ranges, covering `Span`, span parsing, `nearest_agent`, `is_main_agent`, summary and ownership code;
- `scripts/analyze_tool_ownership.py` once, covering the compatibility adapter.

The final dependency markers named essentially the same semantic closure:

- `Span.operation` / `Span.agent_name` / `Span.tool_name`;
- `load_spans`;
- `nearest_agent`;
- `is_main_agent`;
- the standalone adapter.

So the candidate did what the prompt asked operationally: it inspected the relevant unchanged dependency definitions without broad repository browsing.

## Why it still failed

Reading the correct helper is not equivalent to challenging the helper's assumptions.

The Reviewer saw that ownership builds a parent index and calls `nearest_agent`, but it accepted the representation at face value. It did not ask whether `span_id` is globally unique across the full loaded span set, even though trace identity is also present in the parsed data.

The known failing case requires an **invariant challenge**:

> Is the key used to resolve parent identity unique in the domain over which the new aggregation operates?

The dependency-closure candidate never generated that falsification question, so both runs confidently returned PASS.

## Falsification

This rejects another tempting shortcut:

> “Artifact-first review plus mandatory reads of unchanged semantic dependencies is sufficient.”

It is not. A Reviewer can read exactly the right code and still merely confirm the implementation narrative rather than test the assumptions connecting that code to the acceptance criteria.

## Refined assurance concept — dependency closure + invariant challenge

The next Reviewer candidate should keep the bounded artifact-first dependency closure, then perform **one adversarial semantic-invariant pass** over the changed behavior before PASS.

For each acceptance-critical changed path, ask questions such as:

- **Identity / keying:** what makes lookup or aggregation keys unique in the actual domain? Can two valid records collide?
- **Scope / partitioning:** is state scoped by trace/request/tenant/session/file when the data model carries such a partition key?
- **Ordering / nearest-parent traversal:** can ordering, missing ancestry, or duplicate identifiers change which owner is selected?
- **Sentinel / fallback semantics:** can fallback values collapse distinct unknown states into a real owner or category?
- **Compatibility:** is a changed adapter relying on an incidental symbol exposure or on a documented/internal contract?

Only challenge invariants that are directly implied by the changed artifact and inspected dependency closure. Do not broaden into generic adversarial brainstorming.

For this patch, the presence of both `trace_id` and `span_id` in `Span`, combined with a parent map keyed only by `span_id`, should trigger the identity/partition question naturally.

## Cost interpretation

Dependency closure increased Reviewer input from roughly 7.6–7.8k in the zero-read ablation to about 20.8–21.0k, with only three targeted views. That added cost did not improve defect detection in this case.

Therefore v1.1 should not pay for dependency reads merely as ceremony. The reads need to feed an explicit falsification step.

## Next gate

Repeat the same exact-patch review twice with an **artifact-first dependency + invariant-challenge Reviewer**.

Success requires:

- bounded local reads only;
- explicit dependency marker;
- repeatable detection of the cross-trace identity risk, or a precise `VERIFY` naming the uniqueness/partition assumption;
- no speculative re-export finding without evidence;
- one Reviewer invocation only;
- no mutation.
