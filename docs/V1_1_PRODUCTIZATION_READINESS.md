# Over the Luna v1.1 — productization readiness

Status: **automated-core pre-production candidate; not yet ship-ready**  
Updated: **2026-08-20**  
Primary research branch: `research/v1.1-runtime-baseline`  
Primary research PR: #13

This document answers a narrower question than the research notebook:

> What has enough evidence to become product code, and what still blocks a v1.1 release?

## v1.0 → v1.1 goal, restated

v1.1 is **not** a release whose purpose is to call more agents.

It should make the existing economic premise useful in practice:

- spend cheap isolated GPT-5.6 Luna inference where it protects Main context or buys independent evidence;
- avoid ceremony where the mutation is genuinely mechanical;
- keep **one coherent mutation owner**;
- keep broad disposable discovery out of Main when locality is not known;
- make independent assurance reliable without recursive Reviewer spend;
- keep premium inference visible, human initiated, and justified by incremental judgment rather than model-menu complexity.

The invariant remains:

> **Parallelize thinking; serialize mutation.**

> **Main owns the work, not all of the thinking.**

## Automated-core status — READY FOR RUNTIME PRODUCT GATE

The automated Luna core is no longer blocked on another generic routing experiment.

Representative release-gate coverage now includes:

- `SIMPLE + NONE` for a tiny exact mechanical mutation;
- `SIMPLE + REVIEW` for a local semantic/validation mutation;
- `STANDARD + REVIEW` for broad unknown-contract discovery, including replicated sealed-boundary runs;
- `RISK` for a concurrency/idempotency boundary;
- one mutation owner;
- no automatic premium calls;
- bounded fresh Reviewer assurance;
- hidden behavioral oracles;
- VCS/context-boundary hygiene checks.

Detailed record: `experiments/RELEASE_GATE_MATRIX_RESULTS_2026-08-20.md`.

### Current RC artifacts

Use these as the strongest product candidates, not the older experiment files:

- Main: `experiments/v1_1_candidate_rc.agent.md`
- Architect: `experiments/v1_1_candidate_architect_packet_v3.agent.md`
- Reviewer: `experiments/v1_1_candidate_invariant_reviewer_v2.agent.md`

The repository contains static RC contract tests for the state/routing, sealed work set, verbatim Reviewer artifact, hard review budget, leaf non-recursion/read-only behavior, and human-initiated premium handoffs.

Do **not** copy these into released `agents/` until Gate A below is exercised in the actual VS Code runtime.

## Gate A — real VS Code Agent Plugin runtime — OPEN

CLI evidence is useful but cannot prove UI and selected-tool semantics.

Use an authenticated real VS Code / GitHub Copilot Agent Plugin session to establish all of the following.

### A1. Discovery and selection

- plugin installs/loads without fallback to similarly named global agents;
- `Over the Luna` and leaf agents are discoverable under their exact custom-agent names;
- the RC frontmatter parses and renders as intended.

### A2. Ambient selected-tool inheritance

Main intentionally has no fixed `tools` field.

Verify with representative configured built-in/MCP/extension tools that:

- developer-selected tools remain available to Main according to VS Code policy;
- omission of `tools` does not silently drop selected MCP/extension capabilities;
- Council delegation capability remains available when VS Code supplies `agent/runSubagent`;
- leaf explicit tool lists remain restrictive and do not inherit mutation-capable ambient tools.

This is a release blocker because Copilot CLI cannot prove interactive selected-tool inheritance.

### A3. Real sealed Architect handback

Run at least one broad-contract task in Agent mode and inspect Agent Debug / OTel:

- route is visibly `STANDARD` before broad Main scouting;
- Architect runs once and returns the expected packet/work set;
- Main prints `Boundary sealed — work set: ...` before repository work resumes;
- Main local reads stay inside the sealed work set until mutation;
- no hidden/built-in fallback agent performs mutation;
- Main remains the mutation owner.

### A4. Real assurance handoff

Run a non-trivial local mutation:

- route can remain `SIMPLE` while assurance is `REVIEW`;
- exact current unified diff is passed between the required markers;
- one fresh `Luna Reviewer` runs;
- accepted repair is revalidated without automatically buying a second normal Reviewer.

Run one mechanical mutation and verify `SIMPLE + NONE` produces no Reviewer ceremony.

### A5. Premium handoff UI safety

Verify both the current functional baseline and the eventual chosen UX:

- handoff target resolves by exact custom-agent `name`;
- visible handoff switches to the intended agent;
- prompt prefill is correct;
- `send: false` remains a real human confirmation boundary;
- Autopilot or another mode does not silently execute premium inference.

**Gate A exit criterion:** actual VS Code behavior matches the RC contracts in representative tiny/local/broad/risk sessions, with no tool-inheritance or premium-auto-run contradiction.

## Gate B — premium UX / incremental judgment — OPEN

The v1.0 two-button Sonnet/Opus UI should not survive merely because its handoff bug is fixable.

Product question:

> Does premium review add enough repeatable judgment beyond bounded Luna Reviewer to justify a visible user decision, and if so should that decision expose a model name at all?

### Required evidence

Use identical completed artifacts and identical read-only rubrics across Luna, Sonnet, and Opus where available. Include both:

1. a subtle known-defect artifact that Luna Reviewer has demonstrated it can detect;
2. a correct artifact on which speculative premium findings count against the model/UX.

Record:

- unique actionable defects missed by Luna;
- duplicate findings;
- false positives / speculative blockers;
- useful `VERIFY` outcomes;
- latency;
- token / premium-request cost where observable;
- model availability on intended Copilot plans;
- number of human decisions/clicks required.

### Candidate product outcomes

Evidence may support any of these:

- **one `Premium Review` affordance** with an internal backing-model policy;
- one named premium reviewer if one model clearly earns the slot;
- no default premium handoff, with premium review left to explicit agent-picker use;
- retaining two model choices only if each has a repeatable distinct product role worth the extra decision complexity.

Non-negotiable: premium never auto-runs.

**Gate B exit criterion:** one explicit documented premium UX/policy decision backed by comparative evidence, not taste.

## Gate C — productization — BLOCKED ON A + B

When A and B are closed:

1. port the accepted Main/Architect/Reviewer RC contracts into real `agents/`;
2. implement the chosen premium handoff surface;
3. retain exact-name handoff regression coverage;
4. promote relevant RC/static tests into the released runtime contract;
5. update README and README.ko to describe investigation vs assurance without presenting internal research complexity as user ceremony;
6. update `docs/DESIGN.md`, `docs/SMOKE_TEST.md`, `CONTRIBUTING.md`, and MCP/tool-selection guidance where needed;
7. decide which `experiments/` and paid manual research workflows remain useful after release;
8. run clean install + smoke tests from the packaged plugin artifact;
9. only then bump plugin/changelog/version to `1.1.0` and prepare the release PR/merge.

## Stop conditions

Do not declare v1.1 ship-ready if any of these remain true:

- actual VS Code selected-tool inheritance is unverified;
- handoff UI semantics are inferred from CLI/static parsing only;
- a premium path can run without a visible human decision;
- Main or another hidden worker can compete for repository mutation;
- normal REVIEW can recurse into unbounded Reviewer loops;
- broad discovery can silently rehydrate Main after Architect;
- tiny exact changes routinely purchase Reviewer work;
- experiment instrumentation can misattribute agent ownership.

The last instrumentation risk now has a concrete regression: OTel ancestry/tool ownership preserves `(trace_id, span_id)` rather than assuming globally unique span IDs.

## Current recommendation

Treat the automated core as **ready to be exercised as a release candidate in real VS Code**, not as ready to release.

The highest-value next work is no longer another generic Luna routing probe. It is:

1. close Gate A in actual VS Code;
2. run Gate B premium comparative evidence;
3. productize only the contracts that survive both.
