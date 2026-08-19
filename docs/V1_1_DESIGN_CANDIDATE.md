# Over the Luna v1.1 — leading design candidate

Status: **research-backed candidate, not yet a release specification**  
Evidence date: 2026-08-19

This document captures the design that currently has the strongest experimental support. It exists so the v1.1 work no longer depends on reconstructing intent from experiment branches and commit history.

Do not treat this as permission to merge the research branch into `main` or bump the plugin version. Real VS Code/runtime and premium-UX gates remain open.

## Product thesis

Over the Luna should spend cheap independent Luna inference where it buys one of two things:

1. **context isolation** — broad disposable evidence should not pollute Main Luna's mutable implementation context;
2. **independent assurance** — a completed non-trivial artifact should receive one fresh, bounded attempt to falsify an acceptance-critical assumption.

The goal is not more agents, more STANDARD routes, or more Reviewer invocations.

> **Optimize duplicated epistemic work and verified engineering value, not agent count.**

The existing core invariants remain:

> **Parallelize thinking; serialize mutation.**

> **Main Luna owns the work, not all of the thinking.**

Main Luna remains the only automatic repository mutation owner.

---

## 1. Two independent decisions

v1.1 should make investigation and assurance separate first-class state.

### Investigation

Keep the existing vocabulary:

- `SIMPLE`
- `STANDARD`
- `DEEP`

These modes answer:

> How much isolated investigation or independent evidence is useful before/during implementation?

Do **not** optimize for a target SIMPLE/STANDARD/DEEP percentage.

### Assurance

Add/retain explicit state:

- `NONE`
- `REVIEW`
- `RISK`

This answers:

> How much independent assurance is justified after there is a concrete artifact and validation evidence?

A task can therefore be:

`Mode: SIMPLE — direct Luna | Assurance: REVIEW`

This separation is important. Experiments repeatedly showed that a SIMPLE implementation route can otherwise suppress a later Reviewer even for non-trivial mutation.

---

## 2. Investigation policy

### SIMPLE

Use SIMPLE when a focused orientation pass establishes the concrete implementation neighborhood and the local pattern is sufficient.

No investigative subagent is required by default.

Do not lower the SIMPLE threshold merely to increase Council usage. External TTL-cache replication correctly stayed SIMPLE while still using REVIEW.

### STANDARD

Use STANDARD when one or two focused leaf passes have real value, especially when broad repository discovery would otherwise fill Main's context with disposable evidence.

Luna Architect is the preferred owner of broad repository scouting.

### DEEP

Use DEEP for multiple independent uncertainties or cross-cutting risk boundaries, not for file count alone. Keep the initial fan-out bounded.

---

## 3. Architect evidence boundary

The important v1.1 change is not “call Architect more often.”

It is **epistemic ownership**.

When broad disposable discovery is justified:

1. Main performs only enough orientation to recognize that the implementation/evidence neighborhood is not local.
2. Main delegates before consuming the broad details itself.
3. Luna Architect owns that broad read-only pass.
4. Architect returns a compact handback packet:
   - `DECISION`
   - `EVIDENCE`
   - `RELATIONSHIPS`
   - `MUTATION_TARGETS`
   - `UNRESOLVED`
5. Main treats a sufficient packet as the completed broad discovery pass.

### Tool-closed handback

For a read-only mapping task with `UNRESOLVED: none`, Main should normally synthesize without reopening repository read/search tools.

For mutation, Main may inspect:

- concrete `MUTATION_TARGETS`;
- immediately adjacent implementation/test context;
- explicitly `UNRESOLVED` facts.

Main should **not** replay repository-wide discovery merely to reconfirm evidence Architect already established.

If a material broad fact is missing, reopen the boundary for that **specific fact** rather than silently rebuilding the broad investigation in Main.

### Why this shape

Scouting experiments falsified these alternatives:

- increasing STANDARD usage by itself;
- counting Architect invocation as successful isolation;
- improving only Architect output format while leaving Main free to rehydrate broad evidence;
- optimizing agent count rather than duplicated context.

The simpler evidence-packet Architect is currently preferred over the more elaborate bounded-packet prompt. Direct A/B replication did not show a stable read/token advantage for the more complex prompt.

---

## 4. Assurance policy

### NONE

Use NONE for:

- read-only work;
- genuinely tiny, obvious, mechanically validated mutations with no meaningful behavioral/compatibility/security/data/concurrency/public-contract consequence.

This should remain cheap and Reviewer-free.

### REVIEW

For expected non-trivial mutation, declare REVIEW **early**, before implementation anchors the task as “direct.”

After there is a meaningful completed patch and focused validation evidence, run **exactly one fresh Luna Reviewer for the entire normal REVIEW trajectory**.

Give Reviewer:

- original request and acceptance criteria;
- exact completed patch/artifact;
- focused/full validation evidence;
- a concrete task-specific rubric.

#### Reviewer evidence selection

Normal Reviewer should be **artifact-first**, not repository-first.

Before PASS it should:

1. identify acceptance-critical unchanged semantic dependencies used by changed behavior;
2. inspect only those bounded local definitions/callers needed to close the dependency;
3. challenge **one consequential semantic invariant** implied by the changed artifact and that dependency closure.

Useful invariant categories include, only when actually relevant:

- identity/key uniqueness;
- scope/partitioning;
- ordering/ancestry;
- sentinel/fallback semantics;
- compatibility boundary.

This is not permission for generic adversarial brainstorming. The challenge must come from the changed artifact plus concrete dependency evidence.

#### One-review trajectory bound

Normal REVIEW has a hard budget of **one Reviewer invocation total**.

If Reviewer reports a supported finding:

1. Main adjudicates it;
2. Main performs any accepted repair;
3. Main reruns the relevant validation;
4. **do not automatically invoke Reviewer again because the patch changed.**

The previous four-review experiment demonstrated that recursive review can dominate trajectory cost even when findings are useful.

### RISK

Reserve RISK for genuinely consequential boundaries such as:

- auth/security;
- concurrency/idempotency;
- transactions;
- migrations;
- persistence/data integrity;
- rollback;
- important public contracts.

RISK may use at most two independent review passes only when they have genuinely different rubrics.

Do not escalate to RISK merely because the normal Reviewer found an issue or Main repaired it.

---

## 5. Reviewer finding standard

Reviewer findings are evidence, not commands.

Main must adjudicate them against the actual code/tests/contracts.

A useful normal Reviewer should prefer:

- concrete must-fix correctness/compatibility violations;
- supported test/validation gaps that could hide an acceptance failure;
- precise `VERIFY` when an acceptance-critical fact cannot be established within the bounded read budget.

Avoid:

- speculative public-consumer claims without evidence;
- style preferences promoted to correctness issues;
- generic “add more tests” advice;
- broad repository inventory for confidence.

---

## 6. Recovery remains evidence-triggered

Luna Recovery is not a general self-reflection pass.

Use it only after concrete failure evidence, such as a focused validation failure or repository behavior contradicting the current plan.

Main remains responsible for the repair.

Do not treat a Reviewer finding by itself as a Recovery trigger; Main first adjudicates whether the finding is supported.

---

## 7. Automatic model boundary

The automatic core remains GPT-5.6 Luna only in this candidate.

No evidence collected in the v1.1 routing/assurance work justifies adding a hidden automatic premium/non-Luna call.

Premium inference remains human-selected.

---

## 8. Premium UX is deliberately unresolved

The v1.0 handoff execution defect has a known cause and a research-branch regression fix: handoff targets must resolve to actual custom-agent names rather than filename-style slugs.

That functional repair does **not** decide the v1.1 product UX.

Still open:

- keep two visible Sonnet/Opus choices;
- expose one `Premium Review` affordance and choose the backing policy internally;
- whether a static handoff is the right interaction at all.

Constraints that remain non-negotiable:

- no premium model auto-runs;
- one explicit human decision at most should be the design target;
- plan/model availability must be considered;
- `send: true` must not accidentally create an automatic premium path.

---

## 9. Evidence summary

### Investigation

Read-only evidence-boundary replications showed that a full packet + Main handback rule could reduce Main repository read/search after Architect to zero.

Packet-only improved behavior but did not fully close Main rehydration.

Direct Architect A/B showed no stable advantage for the more elaborate bounded-packet prompt over the simpler packet contract.

### Assurance

- early first-class assurance state produced reliable Reviewer adherence where late textual gates did not;
- strict artifact-only review missed an acceptance-critical cross-trace identity defect;
- dependency reads alone also missed it;
- dependency closure + explicit invariant challenge found the same defect in **2/2** exact-patch replications with only 3–4 local reads;
- integrated self-hosted runs found and repaired the defect in **2/2** trajectories with exactly one Reviewer each and passed the strengthened hidden contract;
- external TTL-cache runs stayed SIMPLE, used exactly one Reviewer each, and produced correct exact patches on a strengthened hidden oracle; one Reviewer returned PASS and one found a concrete MRU test-contamination gap.

### Cost

The design does not claim minimum token use.

It does claim a better target:

> spend cheap inference where it prevents duplicated broad context or buys a bounded independent falsification attempt, while hard-bounding recursive assurance trajectories.

---

## 10. Remaining release gates

The automated Luna-core evidence is strong enough to call this the **leading design candidate**, but not enough to ship v1.1.

Before converting this document into a release specification:

1. **Real VS Code integration/manual runtime**
   - Agent Plugin discovery/loading;
   - visible mode/assurance behavior in representative sessions;
   - handoff rendering and switching;
   - selected MCP/extension-tool inheritance;
   - actual subagent/debug trace shape.
2. **Premium UX decision**
   - one affordance vs two model choices;
   - backing model/policy and plan availability;
   - explicit human gate remains intact.
3. **Productization pass**
   - update real `agents/` contracts from the research candidate;
   - update README / README.ko / DESIGN / SMOKE_TEST / CONTRIBUTING as required;
   - version/changelog only after runtime gates;
   - remove/retain research artifacts intentionally rather than accidentally shipping experiment infrastructure.

Until those gates close, `main` remains v1.0.0 and PR #13 remains a research PR.
