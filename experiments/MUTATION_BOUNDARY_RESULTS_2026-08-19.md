# v1.1 mutation evidence-boundary results — 2026-08-19

This experiment follows `EVIDENCE_BOUNDARY_RESULTS_2026-08-19.md` and tests the evidence boundary on a real mutation rather than a read-only repository map.

The controlled task was identical for both policies: integrate the standalone OTel tool-ownership analyzer into `scripts/analyze_otel.py`, preserve the standalone compatibility contract, expose `tool_ownership` in JSON/Markdown, and add focused nested-leaf/orphan attribution tests.

The fixture was pinned to `fcf0c568ba5bf41f69f6c9594359842c473d8946`. Hidden acceptance tests were created only after Copilot finished, so neither Main nor Reviewer could inspect them.

Both runs used GPT-5.6 Luna only, no premium model, Main as the only mutation owner, one Luna Architect, and one post-change Luna Reviewer.

## Results

| Policy | Main input | Council/reviewer input | Total input | Main repo/tool work | Leaf repo work | Total tools | Visible tests | Hidden contract |
| --- | ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| locality | 369,503 | 56,261 | 425,764 | `view 6`, `glob 2`, `rg 1`, `task 2`, `apply_patch 5`, `bash 9` | `view 7` | 32 | pass — 10 tests | pass |
| full evidence boundary | 347,863 | 105,545 | 453,408 | `view 4`, `glob 3`, `rg 1`, `task 2`, `apply_patch 5`, `bash 11` | `view 37` | 63 | pass — 11 tests | pass |

Both plugin validation runs passed and both hidden ownership contracts passed.

## Correctness and patch quality

The hidden test checked the exact requested compatibility surface:

- global top-level `tools` counts remain unchanged;
- new `tool_ownership.main`, `.council`, and `.by_agent` maps use nearest-agent attribution;
- orphan tool spans count as Main;
- the standalone analyzer preserves `main`, `leaf`, and `by_agent` while reusing the shared implementation;
- Markdown exposes `## Tool ownership`.

Both candidates passed.

The final patches were not equivalent in quality, however.

### Locality patch

The locality run modified the same three files as the boundary run and passed all tests, but it changed the existing primary analyzer fixture so the original `apply_patch` tool moved from the Main root under the Architect span. That made the test exercise leaf ownership, but it also replaced an existing Main-owned mutation-path example instead of preserving it and adding an independent leaf case.

The locality Reviewer returned `PASS`.

### Evidence-boundary patch

The boundary run preserved the existing fixture and added dedicated nested-leaf and orphan/Main regressions. Its Reviewer then found one concrete compatibility issue: `scripts/analyze_tool_ownership.py` only used `from analyze_otel import ...`, which works as a script but fails when imported as `scripts.analyze_tool_ownership` or executed as a package module.

Main accepted that finding and added a package-relative import with script fallback. The final boundary patch therefore retained more pre-existing coverage and closed one compatibility edge that the locality patch did not.

This is a positive quality signal for independent broad evidence + adjudicated review, though one sample is not enough to attribute the difference entirely to the routing policy.

## Context-boundary behavior

The mutation path did not reproduce the perfect read-only closure.

### What improved

After Architect returned, the boundary Main inspected only four concrete files with `view`:

- `scripts/analyze_tool_ownership.py`;
- `scripts/analyze_otel.py`;
- `tests/test_analyze_otel.py`;
- one additional bounded implementation-context view during repair/review handling.

That is consistent with the intended rule that Main may read concrete mutation targets and adjacent implementation context.

Main input was also lower than locality: 347,863 vs 369,503.

### What did not improve enough

The boundary Architect performed **29 `view` calls**, versus only 4 Architect views in the locality run. The evidence packet was comprehensive but too expensive for this mutation.

Main also performed one post-Architect repository-wide `rg` across `.github`, `experiments`, and `README.md`. That search was consumer confirmation rather than mutation-local context and therefore counts as residual broad rehydration under the intended boundary rule.

As a result, total input was about **6.5% higher** for the boundary candidate (453,408 vs 425,764), and total tool calls were nearly doubled (63 vs 32).

The read-only result proved that a tool-closed boundary can eliminate duplicated discovery. This mutation result shows that the current packet prompt can instead **over-scout** when the actual mutation needs only a small subset of the repository contract.

## Evidence-based design position

The evidence-boundary concept survives the mutation correctness gate, but the current implementation is not yet economically ready as a v1.1 product contract.

Two things are now simultaneously supported:

1. **Main should not own broad disposable discovery.** The read-only replications demonstrated that cleanly.
2. **Architect should not exhaustively map every potentially related surface when a mutation needs a bounded contract.** The mutation A/B shows that over-comprehensive packet generation can cost more than the rehydration it prevents.

The target is therefore not a maximal evidence packet. It is a **bounded decision-complete packet**.

## Next candidate — bounded mutation packet

Refine the evidence-boundary policy specifically for mutation work:

### Architect scope

- answer the delegated decision, not the entire repository history;
- identify concrete mutation targets and only contract-critical consumers that constrain those targets;
- stop reading once the mutation decision is supported;
- do not browse experiment history, duplicate docs, or release prose unless they materially change the implementation or acceptance criteria;
- keep `EVIDENCE` compact and decision-relevant;
- put unresolved facts explicitly in `UNRESOLVED` rather than reading indefinitely for completeness.

### Main handback rule

After the packet returns:

- read concrete `MUTATION_TARGETS` and immediately adjacent code/test context;
- do not run repository-wide `rg`/`glob` merely to reconfirm consumer coverage already established by Architect;
- if a genuinely missing broad fact appears, state the specific boundary reopen and delegate a focused follow-up rather than silently rebuilding broad context in Main;
- preserve Main ownership of edits, commands, validation, reviewer adjudication, and final synthesis.

## Success gate for the refinement

Repeat the same mutation fixture and require:

- the hidden contract still passes;
- existing tests are preserved rather than traded away for new coverage;
- Architect remains early;
- post-Architect Main broad search is zero;
- Main reads are mutation-local or explicitly unresolved only;
- Architect scouting is materially smaller than the 29-view run;
- total input is no worse than locality by a material margin, ideally lower;
- Reviewer findings remain adjudicated evidence, not automatic rework.

Until this gate passes, the v1.1 design should keep **epistemic ownership** as the leading principle but not freeze the current packet prompt as the final contract.
