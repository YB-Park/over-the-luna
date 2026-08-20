# v1.1 evidence-boundary scouting results — 2026-08-19

This experiment follows `SCOUTING_ISOLATION_MATRIX_2026-08-19.md` and tests the next question directly:

> Can a broad Architect pass become a real context boundary, so Main does not reconstruct the same repository evidence after the leaf returns?

The task stayed read-only in every run. All runs used GPT-5.6 Luna only, zero premium requests, `STANDARD — Luna Architect`, and the same `main` repository fixture/task used by the prior scouting matrix.

## Candidates

Three shapes matter:

1. **locality** — the stronger locality checkpoint from the previous experiment, with the released Architect handback;
2. **packet-only** — the same locality Main policy, but Luna Architect returns the structured evidence packet (`DECISION`, `EVIDENCE`, `RELATIONSHIPS`, `MUTATION_TARGETS`, `UNRESOLVED`);
3. **full evidence boundary** — the packet Architect plus a Main policy that treats successful handback as tool-closed for read-only mapping when `UNRESOLVED` is `none`.

The full candidate is represented by `v1_1_candidate_split_packet.agent.md` together with `v1_1_candidate_architect_packet.agent.md`.

## Results

| Policy/run | Main repo tools | Architect repo tools | Main input | Council input | Total input | Model calls | Total tools |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| prior locality matrix | `view 23`, `glob 1`, `rg 3`, `task 1` | `view 28` | 152,714 | 86,128 | 238,842 | 8 | 56 |
| locality replication | `view 15`, `glob 4`, `rg 3`, `task 1` | `view 31` | 143,230 | 126,345 | 269,575 | 7 | 54 |
| packet-only | `view 9`, `glob 2`, `rg 3`, `task 1` | `view 34` | 92,347 | 71,965 | 164,312 | 6 | 49 |
| full boundary repeat 1 | `task 1` | `view 22` | 22,108 | 58,956 | 81,064 | 3 | 23 |
| full boundary repeat 2 | `task 1` | `view 25` | 21,807 | 87,097 | 108,904 | 3 | 26 |

All fixtures remained clean.

## What the ablation shows

### 1. Better Architect output helps, but does not create the boundary by itself

Replacing only the Architect handback reduced Main-side reconstruction materially in one controlled run:

- Main input fell from 143,230 in the same-run locality control to 92,347;
- Main repository work fell from 15 `view` + 4 `glob` + 3 `rg` to 9 `view` + 2 `glob` + 3 `rg`.

That is useful, but it still violates the desired ownership shape. Main continued to reopen repository surfaces after receiving a comprehensive packet.

The packet format is therefore **not sufficient** on its own.

### 2. Explicit Main-side epistemic ownership closed the loop in both replications

With the full evidence-boundary candidate, both independent runs had exactly one Main tool call: the `task` invocation that delegated to Luna Architect.

Main performed:

- **0 `view`**;
- **0 `glob`**;
- **0 `rg`**;
- **0 post-leaf repository reads/searches**.

Architect owned all repository discovery. Main synthesized directly from the returned packet.

This is the first replicated result in the v1.1 work that demonstrates actual context isolation rather than merely a route label or an Architect invocation.

### 3. The token result moved in the intended direction

The earlier locality candidate used 238,842 total input tokens in the original matrix and 269,575 in the same-task replication here.

The full evidence-boundary repeats used 81,064 and 108,904 total input tokens.

This is not a pricing proof and the sample remains small, but it falsifies the concern that isolating the broad pass necessarily adds a second full copy of repository context. When Main accepts the completed evidence packet as the delegated discovery result, duplication can disappear rather than merely move between agents.

### 4. Final-answer quality did not visibly collapse

Both full-boundary runs returned the expected distributed Luna-only contract surface, including:

- Main and Council agent model declarations;
- Main automatic-agent allowlist;
- validator model/allowlist/handoff contracts;
- premium Sonnet/Opus manual gating;
- README / Korean README / DESIGN / CONTRIBUTING / SMOKE_TEST / plugin metadata / changelog surfaces;
- tool-boundary invariants;
- the unresolved product decision about what kind of non-Luna automatic policy would actually be intended.

The two runs differed in detail and line-reference density, but neither required Main to reopen repository files to produce a coherent answer.

## Evidence-based design position

The target behavior should no longer be described as merely “call Architect earlier.”

The stronger concept is:

> **Broad read-only discovery has one epistemic owner. A sufficient Architect evidence packet closes that discovery phase; Main does not replay it.**

This requires **both** sides of the contract:

- Architect must return a decision-complete bounded packet with exact evidence, relationships, mutation targets, and unresolved items;
- Main must treat that packet as the completed broad discovery pass and reopen repository evidence only for explicitly unresolved facts or mutation-local implementation context.

This is a context-boundary rule, not blind trust. Main still owns synthesis, mutation, validation, and adjudication.

## What is now falsified

The accumulated scouting experiments reject these shortcuts:

- lower SIMPLE merely to increase STANDARD usage;
- count Architect invocation as successful isolation;
- improve only the leaf response format and assume Main will naturally stop re-reading;
- optimize agent count rather than duplicated epistemic work.

## Next gate — mutation boundary

The read-only mapping case is now strong enough to move on.

Before promoting the evidence-boundary rule into a v1.1 design contract, test a non-trivial mutation task where broad discovery is genuinely useful but Main must still inspect concrete implementation-local context.

Success criteria:

- Architect is invoked before broad Main scouting;
- Architect returns concrete `MUTATION_TARGETS` and `UNRESOLVED` evidence;
- Main does **not** replay broad discovery after handback;
- Main reads only mutation targets, immediately adjacent implementation context, and explicitly unresolved facts;
- Main remains the only mutation owner;
- focused/full validation passes;
- the final patch remains behaviorally correct;
- the boundary reduces duplicated Main context rather than merely suppressing necessary verification.

Only after that mutation-path gate should this rule be promoted from research candidate to v1.1 product contract.
