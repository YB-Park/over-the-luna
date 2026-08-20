# v1.1 automated-core release gate matrix — 2026-08-20

This record closes the next automated productization gate after the integrated/self-hosted and external TTL-cache replications.

The goal was deliberately **not** to maximize Luna/Council usage. The v1.0 → v1.1 product question remains:

> Where does another cheap isolated Luna inference pass buy context isolation, independent evidence, verification, or lower expected rework — while Main remains the one mutation owner and premium judgment remains an explicit human decision?

The matrix therefore tests the **boundaries between doing less and doing more**, not only final correctness.

## Gate archetypes

| Archetype | Expected route | Expected automatic leaves | Product property under test |
| --- | --- | --- | --- |
| tiny mechanical value + exact assertion | `SIMPLE + NONE` | none | do not bureaucratize trivial work |
| local behavioral/validation contract | `SIMPLE + REVIEW` | Reviewer exactly 1 | direct implementation can still receive assurance |
| broad unknown repository contract | `STANDARD + REVIEW` | Architect 1 + Reviewer 1 | isolate broad disposable discovery, then review artifact |
| consequential idempotency/concurrency boundary | `* + RISK` | Reviewer 1–2 | explicit risk state + independent post-change assurance |

All cases additionally require:

- hidden acceptance oracle PASS;
- visible tests PASS;
- Main as the only mutation owner;
- zero automatic Sonnet/Opus calls;
- bounded Reviewer reads;
- a concrete completed patch artifact for Reviewer;
- no Main broad-discovery replay after a sealed Architect handback.

## Round 1 — useful failures

The first matrix was intentionally strict and exposed three product-shaping defects.

### Tiny over-review

The constant/default substitution case produced `SIMPLE + REVIEW` and invoked Reviewer once despite being fully specified, mechanically validated work. Reviewer then spent ~21.9k input tokens and 13 repository views.

Correctness passed, but the product policy failed. This is exactly the v1.1 anti-goal: cheap inference must not become ceremony simply because it is cheap.

Resulting refinement: `NONE` now has an explicit all-conditions threshold. A constant/default/text/metadata substitution with an exact direct assertion is the canonical `SIMPLE + NONE` case when no semantic invariant changes.

### Broad handback shell replay

The broad account-identity task correctly used Architect but Main later used shell repository discovery (`find .`) after handback.

Resulting refinement: the sealed boundary applies across tools, not merely `view/glob/rg`. Recursive `find`, `tree`, `git ls-files`, `git grep`, recursive grep/rg, directory inventory and equivalents are explicitly forbidden after handback except for a stated narrow boundary reopen.

### Artifact / VCS reconstruction pressure

Reviewer trajectories could attempt to reconstruct patch context from repository/VCS state when Main did not provide sufficiently concrete artifact evidence.

Resulting refinement: Main must collect and pass the current completed patch; the stronger RC contract uses a verbatim unified diff with literal artifact markers. Reviewer is forbidden from reconstructing a missing patch from `.git`, refs, index, object database, logs, or history.

## Round 2

After the refinements:

- **tiny:** full gate PASS — `SIMPLE + NONE`, Reviewer 0, hidden PASS;
- **local:** full gate PASS — `SIMPLE + REVIEW`, Reviewer 1, hidden PASS;
- **risk:** full gate PASS — `RISK`, mandatory post-change Reviewer, hidden concurrency/idempotency PASS;
- **broad:** functional/routing behavior and hidden oracle passed, but the initial policy evaluator reported two failures.

The broad failures were separated rather than hand-waved:

1. **evaluator false negative:** Reviewer actually received a concrete hunk artifact, while the evaluator coupled validity to specific heading / `diff --git` formatting;
2. **real Architect hygiene failure:** Architect explicitly opened fixture `.git` metadata during broad discovery.

The evaluator was made format-aware rather than heading-aware, while still requiring a concrete patch. Architect was hardened to treat VCS internals as out of scope unless version-control metadata is explicitly the delegated subject.

## Round 3 — broad replication

The hardened broad candidate was run twice from the same generated account-summary fixture with the policy gate enforced as CI.

Both repetitions passed all layers:

| Metric | Repeat 1 | Repeat 2 |
| --- | ---: | ---: |
| Route | `STANDARD + REVIEW` | `STANDARD + REVIEW` |
| Architect | 1 | 1 |
| Reviewer | 1 | 1 |
| Premium automatic calls | 0 | 0 |
| Visible tests | PASS | PASS |
| Hidden account-identity oracle | PASS | PASS |
| Policy gate | **PASS** | **PASS** |
| Total model calls | 9 | 12 |
| Total tool calls | 35 | 30 |
| Total input | 122,129 | 166,939 |
| Total output | 4,428 | 5,101 |
| Main input | 101,400 | 150,213 |
| Council/reviewer input | 20,729 | 16,726 |

Both final implementations reused the established `normalize_account_id` contract, canonicalized equivalent identifiers, preserved first-canonical-appearance order, and rejected invalid identifiers through the existing repository rule.

Reviewer returned PASS in both repetitions after bounded artifact/dependency/invariant inspection.

## Automated-core gate status

The representative matrix now supports the intended discontinuities:

- **tiny mechanical work:** `SIMPLE + NONE` — no automatic review ceremony;
- **local semantic work:** `SIMPLE + REVIEW` — direct Main implementation with one independent assurance pass;
- **broad unknown contract discovery:** `STANDARD + REVIEW` — Architect owns broad evidence, Main owns local mutation, Reviewer owns one artifact assurance pass;
- **consequential concurrency/idempotency work:** explicit `RISK` with mandatory post-change independent assurance.

This is stronger evidence than a single average token metric because it demonstrates that the candidate can both **spend** and **decline to spend** isolated inference at the intended boundaries.

## Research-infrastructure correction discovered during the gate

While hardening the gate, the branch's own OTel analyzer was found to still index ancestry by `span_id` alone even though earlier Reviewer experiments had already demonstrated that span IDs are trace-local.

The validated repair was promoted into the research infrastructure:

- ancestry / nearest-agent lookup now preserves `(trace_id, span_id)` identity;
- tool ownership uses the same trace-qualified identity;
- standalone and package execution of the ownership analyzer are both supported;
- a cross-trace regression reuses identical span IDs in two traces and asserts independent agent/token/tool ownership.

This matters because the experimental instrumentation must not silently misattribute Main/Council behavior on a rare cross-trace collision.

## What this closes

For the automated GPT-5.6 Luna core, the evidence is now strong enough to treat the current RC contracts as a **pre-production product candidate**, not merely a promising routing experiment.

The gate does **not** prove VS Code UI/runtime semantics, selected MCP/extension-tool inheritance, or the best premium UX. Those remain independent release gates.

## Remaining gates

1. **Real VS Code / Agent Plugin runtime**
   - plugin discovery/loading;
   - actual Agent Debug/OTel subagent shape;
   - selected MCP/extension-tool inheritance when Main intentionally omits a fixed `tools` list;
   - leaf restrictions;
   - exact-name handoff rendering/switching;
   - premium handoffs remain human initiated.
2. **Premium UX / incremental judgment**
   - compare one visible premium decision against the current Sonnet/Opus menu;
   - measure unique actionable findings beyond Luna Reviewer, false positives, latency/cost, and availability;
   - never make premium inference automatic.
3. **Productization** after those gates
   - port accepted RC contracts into real `agents/`;
   - update runtime/static tests, README/README.ko, DESIGN, SMOKE_TEST, CONTRIBUTING;
   - intentionally retain/remove research infrastructure;
   - bump version/changelog to `1.1.0` only after runtime/product gates close.
