# v1.1 integrated candidate replication — 2026-08-19

This experiment recombines the strongest investigation and assurance findings after testing them independently.

Integrated candidate:

- Main policy: `v1_1_candidate_integrated.agent.md`;
- Architect: the simpler `v1_1_candidate_architect_packet.agent.md`;
- Reviewer: `v1_1_candidate_invariant_reviewer.agent.md`.

The fixture and mutation task were the same OTel tool-ownership integration used in earlier mutation experiments. The final hidden contract was strengthened to include the previously discovered cross-trace span-ID collision case.

The candidate was run twice from the same fixed fixture revision. Both runs used GPT-5.6 Luna only and zero premium models.

## Candidate contract under test

### Investigation

- keep `SIMPLE / STANDARD / DEEP`;
- establish locality before broad Main scouting;
- broad disposable repository discovery belongs to Luna Architect;
- Architect returns `DECISION / EVIDENCE / RELATIONSHIPS / MUTATION_TARGETS / UNRESOLVED`;
- after handback, Main does not replay broad discovery and reads only mutation-local context or explicit unresolved facts.

### Assurance

- `NONE / REVIEW / RISK` is a separate first-class state declared early;
- normal non-trivial mutation uses `REVIEW`;
- Reviewer receives the completed artifact and validation evidence, closes acceptance-critical semantic dependencies, and challenges one consequential invariant before PASS;
- **normal REVIEW has a hard budget of exactly one Reviewer invocation for the entire task trajectory**;
- if Main accepts a finding, Main repairs and revalidates but does not automatically buy another Reviewer;
- a second review requires explicit `RISK` escalation with a genuinely different rubric.

## Results

| Metric | Repeat 1 | Repeat 2 |
| --- | ---: | ---: |
| Route | STANDARD + REVIEW | STANDARD + REVIEW |
| Architect invocations | 1 | 1 |
| Reviewer invocations | **1** | **1** |
| Hidden final ownership contract | **PASS** | **PASS** |
| Visible tests | 11 pass | 11 pass |
| Plugin validation | pass | pass |
| Main mutation owner | yes | yes |
| Total model calls | 15 | 19 |
| Total tool calls | 52 | 58 |
| Total input | 456,220 | 608,280 |
| Total output | 11,959 | 12,720 |
| Main input | 313,221 | 434,890 |
| Council/reviewer input | 142,999 | 173,390 |
| Architect views | 23 | 33 |
| Reviewer views | 8 | 3 |
| Main views | 3 | 4 |
| Main mutations | 5 `apply_patch` | 6 `apply_patch` |

Both worktrees ended with only the intended three changed files:

- `scripts/analyze_otel.py`;
- `scripts/analyze_tool_ownership.py`;
- `tests/test_analyze_otel.py`.

## Assurance behavior — replicated success

Both runs independently produced the same important Reviewer finding:

> ownership ancestry was keyed only by `span_id`, while the OTel data model also carries `trace_id`; span IDs are trace-local, so identical IDs across traces can resolve the wrong parent/agent.

The Reviewer derived this from the completed patch plus bounded dependency/invariant inspection. The user prompt did not mention the cross-trace oracle.

In both repeats:

1. Main completed the initial implementation and validation;
2. exactly one fresh Reviewer ran;
3. Reviewer returned a supported MUST-FIX for cross-trace identity;
4. Main accepted the finding;
5. Main repaired parent lookup to preserve trace identity;
6. Main added cross-trace regression coverage;
7. Main reran validation;
8. **Reviewer invocation count remained 1**.

This is the behavior the earlier four-review trajectory failed to achieve economically.

The final hidden workflow oracle — which was not available to Main/Reviewer during implementation — passed in both runs.

## Final patch quality

Both final patches preserved:

- global top-level `tools` counts;
- integrated `tool_ownership.main / council / by_agent`;
- nearest-agent ownership;
- orphan/Main fallback;
- Markdown `## Tool ownership`;
- standalone `main / leaf / by_agent` compatibility;
- trace-qualified ancestry lookup;
- nested-leaf, orphan/Main, and cross-trace regression coverage.

Both runs also made the standalone adapter robust to package/module execution (`python -m scripts.analyze_tool_ownership`) while retaining direct-script behavior.

## Investigation behavior — boundary works, scouting breadth is still variable

The important Main-side boundary held.

After Architect handback, Main repository reads were mutation-local:

- repeat 1: 3 Main `view` calls;
- repeat 2: 4 Main `view` calls.

No Main repository-wide rediscovery loop occurred. Main owned mutation, commands, validation, and Reviewer adjudication; Architect owned the broad read-only pass.

However, the Architect itself remained variable and sometimes over-comprehensive:

- repeat 1: 23 `view` calls;
- repeat 2: 33 `view` calls.

It inspected several experiment/documentation surfaces beyond the minimum code/test/consumer contract needed for the mutation. This is consistent with the earlier direct Architect ablation: the simple evidence packet is decision-complete, but the exact breadth of one model run is stochastic.

The result therefore supports the **epistemic-ownership boundary** more strongly than any fixed target for Architect read count.

## Cost interpretation

The integrated candidate used 456k and 608k total input tokens.

For context on the same mutation family:

- locality A/B run: ~426k input, but the later cross-trace defect was not part of its final assurance result;
- earlier full evidence-boundary run: ~453k input, hidden basic contract pass, but cross-trace correctness was not repeatably caught;
- bounded-packet integrated run: ~887k input because normal review recursively expanded to **four** Reviewer invocations;
- this candidate: ~456k / ~608k, **one** Reviewer, repeatable cross-trace repair, strengthened hidden contract pass.

The integrated candidate is not the cheapest trajectory observed, but it is the first replicated trajectory in this series that combines:

- real broad-context ownership;
- reliable one-review adherence;
- a repeatably useful Reviewer finding;
- Main adjudication and repair;
- hard prevention of recursive review spend;
- final hidden correctness on the discovered invariant.

## Evidence-based v1.1 core direction

The automated Luna core now has a strong research candidate:

### Investigation

**Keep `SIMPLE / STANDARD / DEEP`. Do not optimize for mode percentages.**

Use Architect when broad disposable discovery has positive context-isolation value. Treat its evidence packet as the completed broad discovery pass; Main should not rehydrate that context.

### Assurance

**Separate assurance from investigation.**

Use early `NONE / REVIEW / RISK` state so direct implementation does not suppress later independent assurance.

For normal `REVIEW`, buy exactly one artifact-first Reviewer that:

- closes acceptance-critical unchanged dependencies;
- challenges one consequential semantic invariant;
- stays local/bounded;
- returns evidence for Main to adjudicate.

Accepted repairs are revalidated by Main without automatic re-review.

### Mutation ownership

**Main remains the sole repository mutation owner.**

This invariant survived every successful experiment and should not be reopened without much stronger contrary evidence.

## What is not decided by this result

This is still a research candidate, not a v1.1 release contract.

Remaining gates include:

- at least one integrated replication outside this repository/self-hosted analyzer family, to check Reviewer precision and investigation behavior on less familiar code;
- real VS Code runtime/manual integration for UI semantics and selected-tool inheritance;
- premium UX/model decision: one premium affordance vs current Sonnet/Opus choices;
- release documentation/versioning only after those gates.

The next automated gate should therefore use an external/generated fixture rather than further tuning this repository-specific mutation.
