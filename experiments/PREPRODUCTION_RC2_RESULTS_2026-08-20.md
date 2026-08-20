# v1.1 automated-core RC2 pre-production matrix — 2026-08-20

## Verdict

The automated GPT-5.6 Luna core now has a **pre-production release candidate** for the v1.1 routing/assurance contract.

The final RC2 matrix ran the same four release-boundary fixtures twice each (**8 independent trajectories**) and required all of the following simultaneously:

- visible validation passes;
- a separate hidden behavioral oracle passes;
- the expected investigation/assurance route is emitted;
- Main remains the only mutation owner;
- premium inference is never invoked automatically;
- tiny/local orientation remains bounded and non-inventory-like;
- broad semantic discovery is isolated to Architect with a sealed Main work set;
- normal REVIEW uses one named Luna Reviewer;
- RISK receives at least one post-change named Luna Reviewer;
- Reviewer evidence contains a concrete current unified-diff artifact;
- Reviewer/local read budgets and VCS-metadata prohibitions are respected.

**Final result: 8 / 8 PASS.**

This closes the automated CLI core gate. It does **not** close the real VS Code runtime/tool-inheritance/handoff gate or the premium UX decision.

## Canonical RC2 files

- Main: `experiments/v1_1_candidate_rc2.agent.md`
- Architect: `experiments/v1_1_candidate_architect_packet_v3.agent.md`
- Reviewer: `experiments/v1_1_candidate_reviewer_rc.agent.md`
- Fixture/oracles: `experiments/v1_1_release_gate_fixture.py`
- Base evaluator: `experiments/v1_1_release_gate_evaluator_v6.py`
- RC2 discipline evaluator: `experiments/v1_1_release_gate_evaluator_rc2.py`

Launch workflow run: **32323722543** at commit `b2b3de4b58a60e4fe62a19f18898f7844c63efaa`.

The one-shot paid workflow was deleted immediately after launch confirmation. Branch cleanup/static-contract commit `426e6c48076b6d15966ceacba3c1b9f2561ea03d` validated green afterward.

## Final matrix

| Case | Rep | Route | Architect | Reviewer | Hidden | Policy | Input tokens | Council/reviewer input |
| --- | ---: | --- | ---: | ---: | --- | --- | ---: | ---: |
| tiny | 1 | `SIMPLE + NONE` | 0 | 0 | PASS | PASS | 80,183 | 0 |
| tiny | 2 | `SIMPLE + NONE` | 0 | 0 | PASS | PASS | 92,587 | 0 |
| local | 1 | `SIMPLE + REVIEW` | 0 | 1 | PASS | PASS | 187,273 | 8,262 |
| local | 2 | `SIMPLE + REVIEW` | 0 | 1 | PASS | PASS | 223,071 | 8,893 |
| broad | 1 | `STANDARD + REVIEW` | 1 | 1 | PASS | PASS | 154,254 | 21,238 |
| broad | 2 | `STANDARD + REVIEW` | 1 | 1 | PASS | PASS | 186,305 | 45,673 |
| risk | 1 | `SIMPLE + RISK` | 0 | 1 | PASS | PASS | 192,048 | 6,961 |
| risk | 2 | `DEEP + RISK` | 0 | 1 | PASS | PASS | 241,496 | 8,947 |

Across the eight runs, total input was 1,357,217 tokens; Council/reviewer input was 99,974. The important product property is not the aggregate spend but its shape:

- tiny/mechanical work bought **zero** leaf compute;
- local semantic work bought only the final Reviewer;
- broad unknown semantic discovery bought Architect + Reviewer;
- RISK always bought the final named Reviewer, with one run additionally buying a pre-change Skeptic because it chose DEEP.

No run invoked Sonnet or Opus automatically.

## Per-boundary interpretation

### tiny — `SIMPLE + NONE`, 2 / 2

Task: change a fully specified default scalar from 50 to 64 and update the exact regression assertion.

Both runs:

- remained SIMPLE;
- invoked no Architect;
- invoked no Reviewer;
- passed visible and hidden behavior;
- passed the local-orientation discipline gate.

Average input was ~86k and Council/reviewer input was exactly zero.

This is important because earlier candidates made tiny work bureaucratic: Round 1 incorrectly selected REVIEW and bought a 13-view Reviewer. RC2 demonstrates that the final contract can preserve independent assurance where valuable without taxing genuinely mechanical work.

### local — `SIMPLE + REVIEW`, 2 / 2

Task: align named `update_headers` behavior with named `create_headers` and their visible request-ID normalizer.

Both runs:

- stayed SIMPLE;
- used no Architect;
- invoked exactly one named Luna Reviewer;
- passed blank/normalization/absence hidden behavior;
- passed the no-glob/no-background-prose local-orientation gate;
- supplied concrete artifact evidence to Reviewer.

This is the intended direct semantic path: locality and the contract are already named/adjacent, so another investigative leaf would add ceremony rather than context isolation.

### broad — `STANDARD + REVIEW`, 2 / 2

Task: discover and reuse an unknown established account-ID contract for exported aggregation behavior.

Both runs:

- selected STANDARD;
- invoked Architect exactly once;
- produced the same sealed work set of six concrete paths;
- kept pre-mutation Main reads inside that work set;
- replayed no broad discovery after handback;
- invoked exactly one named Luna Reviewer;
- passed canonical grouping/order/invalid-ID hidden behavior.

This is the v1.0 -> v1.1 context-isolation objective in its product form: the need for unknown semantic discovery routes to Architect, while Main resumes only with a concrete implementation work set.

### risk — `RISK`, 2 / 2

Task: make idempotent charging linearizable for concurrent same-key retries while keeping failure retryable and distinct keys independent.

Both runs:

- declared RISK;
- passed the concurrency/failure hidden oracle;
- invoked exactly one post-change named Luna Reviewer;
- did not substitute built-in `code-review` for the product Reviewer;
- did not recursively re-review.

One run remained SIMPLE + RISK; one selected DEEP + RISK and added a pre-change Luna Skeptic. Both are acceptable because investigation and assurance are separate states. The invariant is that consequential work receives final artifact assurance regardless of whether pre-change investigation is direct or deep.

## Why RC2 exists: failures we refused to wave through

The final 8/8 result is only meaningful because earlier correctness-PASS trajectories were deliberately failed when they violated the product goal.

### Round 1

- tiny: hidden PASS, but `SIMPLE + REVIEW` and an unnecessary 13-view Reviewer;
- broad: hidden PASS, but Main replayed repository inventory with shell `find` after Architect;
- Reviewer could attempt `.git` reconstruction when Main did not provide a concrete patch artifact.

### v3 / v4 refinements

Making semantic-discovery isolation stronger initially over-routed tiny/local work to STANDARD. That exposed an important distinction:

> **bounded mechanical/local locator orientation is not the same thing as broad semantic discovery.**

Subsequent candidates restored direct local work but exposed narrower discipline problems:

- generic root `glob '*'` during tiny/local orientation;
- README/background-prose reads and excessive tooling metadata for local work;
- normal REVIEW buying a second Reviewer after the first pass returned artifact VERIFY;
- RISK using pre-change Skeptic/Architect but skipping final Reviewer;
- RISK substituting a built-in `code-review` agent instead of the named Luna Reviewer.

### First RC matrix

The first explicit RC passed **5 / 8**, with three genuine contract failures despite hidden correctness:

1. tiny used generic `glob '*'`;
2. local consumed README/background material and excess tooling metadata;
3. broad bought a second Reviewer after an artifact-format VERIFY.

Those were not relaxed away. RC2 changed the executable contract:

- SIMPLE orientation uses direct reads / narrow exact `rg`; **no glob**;
- README/docs/background prose are forbidden unless the task targets them;
- tooling metadata is read only when validation cannot otherwise be inferred, max one;
- Main preflights the concrete review artifact before the single Reviewer call;
- normal REVIEW is a hard **one task-call** budget: no artifact retry, no VERIFY retry, no re-review after repair;
- Reviewer tolerates cosmetic transport whitespace when the concrete diff is otherwise present;
- RISK requires at least one post-change **named Luna Reviewer**; generic/built-in review does not count.

The same four fixtures × two repetitions then passed 8/8.

## Automated-core contract earned by the evidence

The evidence now supports the following as the leading automated v1.1 contract:

1. `SIMPLE / STANDARD / DEEP` remains investigation vocabulary.
2. `NONE / REVIEW / RISK` is a separate first-class assurance state.
3. Main is the sole mutation owner.
4. SIMPLE gets a small bounded orientation budget for already-specified local behavior.
5. Unknown semantic discovery beyond that budget is isolated to Architect.
6. Architect returns evidence plus a complete post-handback work set.
7. Main seals the handback and does not replay broad discovery before mutation.
8. NONE protects genuinely mechanical work from review ceremony.
9. Normal REVIEW buys exactly one named Luna Reviewer with concrete current artifact evidence.
10. RISK always gets at least one post-change named Luna Reviewer; pre-change leaves do not substitute.
11. Reviewer findings are evidence for Main adjudication; accepted repair does not recursively purchase another normal review.
12. Premium inference remains explicitly human initiated.

## What this still does not prove

### Real VS Code / Agent Plugin behavior remains open

CLI evidence does not prove the exact interactive VS Code semantics for:

- Main `tools` omission and preservation of developer-selected built-in/MCP/extension tools;
- whether the `agent/runSubagent` tool remains enabled when the Main agent restricts `agents`;
- actual Agent Debug/OTel parentage and tool inheritance;
- handoff button rendering and exact-name agent switching;
- premium handoffs remaining human initiated in the real UI.

These are release blockers, not optional polish.

### Premium UX remains open

The automated core intentionally does not choose between:

- separate Sonnet/Opus buttons; or
- one simplified human `Premium Review` affordance.

That decision needs real plan/model availability and incremental-judgment evidence after the normal Luna assurance layer is established.

## Productization status

**Automated Luna core: PRE-PRODUCTION RC — evidence stable.**

**v1.1 release: NOT READY YET.**

Do not version-bump or merge the research PR solely because RC2 is 8/8. Next close the real VS Code Gate A, then the premium UX Gate B, then port the accepted contracts into real `agents/` and perform versioned productization.
