# v1.1 direct Architect packet ablation — 2026-08-19

This experiment isolates the investigation policy from Main implementation and assurance. It directly invokes Luna Architect on the same mutation-oriented planning problem, with no repository mutation and no Reviewer.

Two Architect prompts were compared twice each against the fixed fixture `fcf0c568ba5bf41f69f6c9594359842c473d8946`:

- **packet** — `v1_1_candidate_architect_packet.agent.md`, the simpler decision/evidence/relationships/mutation-targets/unresolved handback;
- **bounded** — `v1_1_candidate_architect_bounded_packet.agent.md`, which adds explicit item caps and read-stop discipline.

The task asked for the repository evidence Main would need to integrate tool ownership into the main OTel analyzer while preserving global tool totals, the standalone compatibility contract, nested nearest-agent attribution, orphan/Main behavior, Markdown output, and focused regressions.

All runs were read-only, GPT-5.6 Luna only, and zero premium models.

## Results

| Candidate | Repeat | Decision-completeness check | Views | Model calls | Input | Output |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| packet | 1 | PASS | 12 | 5 | 50,883 | 2,019 |
| packet | 2 | PASS | 15 | 5 | 73,305 | 1,735 |
| bounded | 1 | PASS | 9 | 4 | 41,442 | 1,924 |
| bounded | 2 | PASS | 16 | 7 | 106,659 | 2,466 |

Means:

| Candidate | Mean views | Mean input | Mean output |
| --- | ---: | ---: | ---: |
| packet | 13.5 | 62,094 | 1,877 |
| bounded | 12.5 | 74,051 | 2,195 |

Every fixture stayed clean.

## Quality comparison

All four packets identified the same essential implementation contract:

- `scripts/analyze_otel.py` is the canonical place to centralize ownership;
- preserve existing top-level global `tools`;
- add integrated `tool_ownership` with Main/council/per-agent views;
- reuse existing nearest-agent and Main-agent semantics;
- orphan/unresolved ancestry falls back to Main;
- `scripts/analyze_tool_ownership.py` should become a compatibility adapter preserving `main`, `leaf`, and `by_agent`;
- `tests/test_analyze_otel.py` is the primary focused regression surface;
- add a separate Markdown ownership section;
- keep workflow/CLI consumers compatible.

The bounded packets were somewhat more explicit about mutation-target limits and, in one repeat, surfaced the unresolved possibility of external callers importing the standalone helper directly. The plain packets were at least as decision-complete for the requested implementation and often more concise structurally.

No run omitted a required mutation target or core compatibility constraint according to the fixed completeness check.

## Interpretation

The direct ablation does **not** support promoting the more elaborate bounded Architect prompt.

The explicit caps did not produce a stable efficiency win:

- one bounded run was the cheapest of the four;
- the other bounded run was the most expensive of the four;
- mean repository reads were essentially tied;
- mean input/output were higher for bounded in this small sample.

This also explains the apparently dramatic 18.8k → 2.1k Architect-output difference seen in the prior full mutation A/B: that large previous-boundary output was not representative of the direct packet candidate. When isolated, the simpler packet naturally returned roughly 1.7k–2.0k output tokens.

The additional prompt complexity therefore does not currently earn a product-level contract.

## Evidence-based investigation decision

The leading v1.1 investigation shape should be the **simpler evidence-boundary contract**:

1. keep `SIMPLE / STANDARD / DEEP` as investigation vocabulary;
2. establish locality before broad Main scouting;
3. when broad disposable discovery is needed, invoke Luna Architect early;
4. Architect returns `DECISION`, `EVIDENCE`, `RELATIONSHIPS`, `MUTATION_TARGETS`, `UNRESOLVED`;
5. Main treats that packet as the completed broad discovery pass;
6. read-only work with `UNRESOLVED: none` should not rehydrate repository evidence in Main;
7. mutation work may inspect only concrete mutation targets, adjacent implementation/test context, and explicit unresolved facts;
8. if the packet is insufficient, reopen the boundary for one **specific missing fact**, not a silent broad Main search.

This is a strong enough research result to stop optimizing the Architect prompt for now.

The remaining high-value uncertainty is **assurance trajectory economics and precision**.

## Next gate

Test a fresh **artifact-first, single-review** candidate:

- first-class `Assurance: REVIEW` remains declared early so adherence stays reliable;
- one fresh Reviewer receives acceptance criteria, exact completed patch, and validation evidence before browsing;
- unchanged repository reads are permitted only for a concrete candidate finding;
- normal REVIEW has exactly one Reviewer invocation for the task trajectory;
- accepted repairs are revalidated by Main but do not automatically trigger re-review;
- a second independent review requires explicit escalation to `RISK` with a distinct risk rubric.

Compare this against the existing Reviewer on an identical completed patch before recombining it with the investigation candidate.
