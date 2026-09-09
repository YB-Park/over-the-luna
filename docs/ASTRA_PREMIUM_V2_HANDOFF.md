# Astra Work Handoff — Premium Harness v2 Design Audit

Status: **independent pre-implementation design audit**  
Target branch: `research/astra-premium-v2-design`  
Design RFC commit: `97cc22962e3bf810b76bf8d5ef4c9fe509a542c5`  
Prior independent audit: `research/astra-premium-audit@79f3c4d34beb1383fa55fae180c999aa23770d64`

## Mission

The first frozen Premium candidate has been stopped and classified `REDESIGN`.

The broader product hypothesis remains alive:

> Can one user-selected premium coding harness combine cheap GPT-5.6 Luna work with selective GPT-5.6 Terra intelligence so that it is meaningfully stronger than current Over the Luna and more cost-efficient/robust than simply selecting raw Terra?

The primary experiment runner has drafted a **v2 pre-implementation design RFC**.

Your job is not to improve its prose or help it pass.

Your job is:

> **Determine whether the v2 design is coherent, productizable, falsifiable, and worth implementing at all.**

Be adversarial. A useful outcome may be:
- approve for a small implementation experiment;
- require major revision before implementation;
- reject this v2 architecture thesis while preserving another premium thesis;
- or conclude evidence is insufficient.

Do not implement anything.

---

## Read in this order

1. `docs/ASTRA_PREMIUM_AUDIT.md` from commit `79f3c4d34beb1383fa55fae180c999aa23770d64` or its audit branch.
2. `docs/PREMIUM_HELDOUT_RESULTS.md`
3. `docs/PREMIUM_HARNESS_RESULTS.md`
4. `docs/PREMIUM_V2_PRE_IMPLEMENTATION_RFC.md`
5. `docs/PREMIUM_HELDOUT_PROTOCOL.md`
6. `docs/PREMIUM_HARNESS_RFC.md`
7. stable product docs:
   - `README.md`
   - `docs/DESIGN.md`
   - `CONTRIBUTING.md`
8. relevant stable and experimental agent contracts only when needed to test feasibility.

Treat the new v2 RFC as a proposal, not authority.

---

## Context you must preserve

### Project identity

Over the Luna is deliberately Luna-first because Luna's low-cost policy/capability is the project's original reason for existing.

But the previous Astra audit correctly reframed this:

> Luna-first is a product/resource prior, not evidence and not a reason to prohibit better engineering.

The v2 RFC therefore permits Terra to enter the direct repository loop when that expensive participation is expected to change complete-task outcome.

Challenge this balance.

### Why v1 stopped

The first frozen Premium topology was roughly:

```text
Terra mission owner
 -> Luna Builder
 -> Luna Auditor
 -> Terra final decision
```

H1 Redis held-out:
- OTL: 3/4 FAIL, 5.694290 credits, 167s;
- raw Terra: 4/4 PASS, 71.013030 credits, 222s;
- Premium: 3/4 FAIL, 14.671259 credits, 355s.

Most important forensic point:
- Builder explicitly reported an SSL-like fallback limitation;
- Terra received/repeated it;
- Auditor repeated it while returning PASS;
- Terra declared completion.

The redesign is therefore trying to solve **acceptance/adjudication control**, not merely context compression.

Do not let the new RFC overfit H1's implementation details.

### Why v2 is different

The proposal is an **adaptive topology** with three conceptual lanes:

- Lane L: Luna execution;
- Lane T: integrated Terra repository/tool trajectory;
- Lane M: mixed mission — Terra global state + Luna work packets.

The user still chooses only one product tier: Premium.

The design also proposes an **Acceptance Evidence Ledger** where every BLOCKING criterion must be verified regardless of whether uncertainty originated from Terra, Luna, tests, or verification.

A Luna Verifier becomes optional evidence collection and loses authority to declare global PASS.

These are hypotheses to audit, not approved design decisions.

---

## Audit questions

### 1. Does adaptive topology solve the real problem or merely move it into routing?

Attack the central assumption:

> "The system can identify when Luna, integrated Terra, or mixed mission is the cheapest adequate trajectory."

Questions:
- Is reliable self-routing itself as hard as solving the task?
- Does the router need repository evidence before it can choose the lane, creating circular cost?
- Will a Terra root rationalize using its own tools too often?
- Will cost pressure bias it toward Luna exactly when Terra is needed?
- Can lane switching recover from an initially wrong choice without wasting both models?
- Is a hidden adaptive router materially better UX/product design than user-visible Luna/Terra choices?

Compare against credible alternatives:
- always raw Terra;
- current OTL;
- cascade/escalation;
- critique/revision;
- cheap default with premium takeover only after observed failure;
- deterministic non-LLM router;
- external policy based on measurable runtime signals;
- model-family second opinion;
- any current research/production pattern you find.

### 2. Is "always Terra root" itself a bad premise?

Current VS Code cost-tier restrictions make Luna-parent automatic Terra escalation difficult/impossible, which motivates a Terra-rooted Premium.

Challenge whether this technical fact should define the product.

Consider:
- Terra root with direct tools + Luna leaves;
- Terra root acting only as a router;
- a separate integrated Terra child;
- explicit internal handoff;
- user-visible escalation;
- changes in current VS Code/Copilot behavior since prior research;
- whether a future/runtime-specific solution is better than compromising architecture now.

### 3. Audit the L / T / M lane definitions

For each lane:
- is it meaningfully distinct?
- can it be selected from observable state?
- can it be implemented with current VS Code custom agents/Copilot CLI?
- does mutation ownership remain safe?
- what is the minimum information required to switch lanes?
- what failure modes are introduced by switching?

Specifically test whether Lane M is just the failed v1 hierarchy renamed.

### 4. Audit the Acceptance Evidence Ledger

This is the most important proposed control mechanism.

Attack it.

Questions:
- Does structured criterion state actually prevent H1-style false completion?
- Is it prompt bureaucracy that models can still ignore?
- Does it create huge context/maintenance overhead?
- Can evidence become stale after mutations?
- Can an LLM reliably classify BLOCKING vs NON_BLOCKING?
- Who defines acceptance criteria when the user's prompt is underspecified?
- Is `USER_ACCEPTED_RESIDUAL` usable in an unattended coding session?
- Does workspace/diff linkage materially help?
- Would deterministic enforcement be required?
- If deterministic enforcement is required, is that feasible in a VS Code plugin/custom-agent architecture without building a large external runtime?

Propose the smallest mechanism that would actually change system behavior when a visible acceptance-critical uncertainty appears.

### 5. Audit Terra's tool access

v1 made Terra tool-blind. v2 allows direct repository tools.

Questions:
- Does this recover integrated reasoning at the price of destroying cost control?
- Can prompt instructions reliably keep Terra out of mechanical loops?
- Should tool access change by lane?
- Can tool access change dynamically in current runtime?
- Would separate agents with different tool surfaces be cleaner even if they add handoff cost?
- Can mutation ownership transitions be structurally enforced?
- How much of the design is relying on instructions rather than runtime capability?

### 6. Audit optional verification

The RFC weakens Auditor into an optional Luna Verifier that collects evidence but cannot issue global PASS.

Evaluate:
- Is that enough to justify a second context?
- Should v2 initially omit Verifier entirely until routing value is proven?
- Could same-model Verifier still provide useful behavioral counterexamples?
- Would Terra checking Luna output be more useful?
- Would a different model family be more orthogonal?
- How should assurance value be ablated fairly?

Do not recommend automatic Sonnet merely because diversity sounds good. It must have a falsifiable marginal-value hypothesis.

### 7. Audit product workload distribution

The RFC proposes:
- D1 difficult local diagnosis;
- D2 multi-subsystem integration;
- D3 large routine work;
- D4 straightforward control.

Questions:
- Is this a meaningful product distribution?
- Is D2 actually the strongest niche for mixed orchestration?
- Are important user workloads missing?
- Is "one substantial coding mission" sufficiently clear?
- Should long-horizon/resumption remain excluded for v2 initial claims?
- What would a representative test set look like without bankrupting the user?

### 8. Audit proposed product thresholds

The RFC intentionally proposes attackable gates:
- no worse acceptance-critical false-complete rate than OTL;
- at least two D1/D2 capability wins with no OTL-pass/Premium-fail offset;
- <=60% median raw-Terra credits where both pass;
- <=2.5x OTL credits and <=2.0x OTL time on straightforward controls.

Assess:
- Are these economically meaningful?
- Are they too strict/lenient?
- Do small-N task-level gates invite noise?
- What exact thresholds would you recommend **before implementation**?
- How should latency vs credit vs failure loss be handled?
- Should false-complete be a hard veto?

Do not retrofit thresholds to make previous results look good.

### 9. Audit development ablations

RFC proposes using known/exposed tasks only for development:
- H1;
- httpcore;
- Django lifecycle;
- deterministic simple control.

Then compare:
- adaptive v2;
- no Verifier;
- forced Lane L;
- forced integrated Terra on selected D1;
- raw Terra;
- OTL.

Challenge whether this is sufficient to identify component value without exploding cost.

Recommend the **smallest ablation set** that can decide:
- whether routing adds value;
- whether integrated Terra needs to exist;
- whether Verifier earns cost;
- whether Lane M earns cost.

### 10. Audit fresh holdout selection

H1 and the documented H2/H3/H4 are now exposed to the design process and should not be treated as pristine v2 promotion holdouts.

RFC proposes deterministic post-freeze sampling from eligible public PR pools using the freeze SHA as seed.

Assess:
- contamination/model-memory risk;
- curator bias in building the eligible pool;
- whether deterministic sampling actually helps;
- how to stratify without cherry-picking;
- whether a third-party curator or blinded selection process is better;
- minimal task count/repetition plan under limited credits.

### 11. Audit evaluator architecture

The RFC proposes:
- prep job;
- one independent runner per arm;
- no evaluation repo checkout in model jobs;
- no sibling arms;
- complete workspace capture;
- evaluator fetches accepted material only after all model jobs.

Review practical feasibility and remaining leakage:
- Copilot requires network;
- general shell exists;
- model aliases can change;
- dependencies/runtime can drift;
- artifacts can be incomplete on failure.

Recommend concrete, freeze-safe evaluator controls.

### 12. Kill criteria

This project can iterate forever unless it knows when to stop.

Give explicit kill criteria for the **Premium product hypothesis**, not only candidate v2.

Examples to challenge:
- N distinct competent Premium designs fail to create a Pareto improvement;
- routing regret remains high;
- premium topology mostly collapses to raw Terra or OTL;
- acceptance control adds large overhead without reducing false completion;
- user-visible benefit cannot be explained simply.

Recommend a finite research budget or stopping rule appropriate for a cost-sensitive individual project.

---

## Latest evidence requirement

Perform a fresh current-source survey as of the date you run this audit.

Prefer:
- OpenAI official docs/research;
- GitHub Copilot / VS Code official engineering and runtime docs;
- Anthropic engineering only where mechanisms are relevant;
- recent 2025–2026 peer-reviewed work or strong preprints on:
  - model routing;
  - adaptive inference;
  - multi-agent orchestration;
  - software-engineering agents;
  - test-time scaling;
  - evaluator/reviewer correlation;
  - context/state transfer;
  - long-horizon coding;
  - mixture/cascade/critique systems;
  - task selection/evaluation contamination.

For each important source distinguish:
- production A/B;
- controlled benchmark;
- mechanism study;
- vendor report;
- opinion/design essay.

Do not let one vendor benchmark settle the architecture.

---

## Constraints

### Do not implement

Do not create or modify candidate agent files.

Do not edit:
- `docs/PREMIUM_V2_PRE_IMPLEMENTATION_RFC.md`;
- existing experiment results;
- stable product files;
- validator;
- workflows.

### Do not run paid experiments

Do not:
- invoke Copilot models;
- create a workflow with `copilot-requests: write`;
- consume the user's Copilot credits;
- execute H1/H2/H3/H4 model runs.

Your own Work/Astra analysis allowance is fine.

### Do not select promotion holdouts

You may critique or propose a selection method, but do not reveal/select the actual future fresh holdout set in this audit.

### Do not optimize for agreement

The RFC is written by the primary runner and may be wrong.

If the best design is:
- not Terra-rooted;
- not multi-agent;
- not adaptive;
- or not worth building,

say so.

---

## Required primary output

Create exactly one new report:

`docs/ASTRA_PREMIUM_V2_DESIGN_AUDIT.md`

Commit it to:

`research/astra-premium-v2-design`

Do not modify any other existing file.

Use exactly this top-level structure:

# Astra Independent Premium v2 Design Audit

## 1. EXECUTIVE VERDICT

Choose exactly one:
- `APPROVE_FOR_IMPLEMENTATION_EXPERIMENT`
- `REVISE_BEFORE_IMPLEMENTATION`
- `REJECT_V2_ARCHITECTURE_THESIS`
- `INSUFFICIENT_EVIDENCE`

Confidence: LOW / MEDIUM / HIGH.

## 2. WHAT V2 GETS RIGHT

Strongest steelman.

## 3. WHAT V2 STILL GETS WRONG

Strongest red-team case.

## 4. ADAPTIVE ROUTING REVIEW

Analyze L/T/M and alternatives.

## 5. ACCEPTANCE CONTROL REVIEW

Analyze the ledger/completion gate and propose the smallest viable control mechanism.

## 6. TERRA TOOL / MUTATION-OWNERSHIP REVIEW

Feasibility and failure modes.

## 7. VERIFICATION / ASSURANCE REVIEW

Whether Verifier should exist and how to measure it.

## 8. PRODUCT DISTRIBUTION AND THRESHOLDS

Recommend explicit workload scope and numeric gates.

## 9. DEVELOPMENT ABLATION PLAN

Give the smallest informative pre-freeze experiment plan.

## 10. FRESH HOLDOUT / EVALUATOR PLAN

Selection, isolation, reproducibility, repetition.

## 11. STRONGEST ALTERNATIVE ARCHITECTURES

At least three alternatives, ranked.

Include simple baselines, not only multi-agent variants.

## 12. KILL CRITERIA / RESEARCH BUDGET

Give finite stopping conditions.

## 13. LATEST EXTERNAL EVIDENCE

Title, authors/org, date, URL, evidence type, exact implication/limitation.

## 14. REQUIRED RFC CHANGES BEFORE IMPLEMENTATION

If verdict is not approval, list concrete design changes.

Do not implement them.

## 15. WHAT WOULD CHANGE MY MIND

Concrete observations.

## 16. NEXT ACTION

At most three actions.

## 17. EVIDENCE QUALITY / UNCERTAINTY

Critique your own audit.

---

## Special requirement: propose one minimal candidate

Regardless of verdict, include within the relevant sections:

> **MINIMAL CANDIDATE YOU WOULD TEST FIRST**

Describe the smallest architecture you would spend the user's next paid Copilot credits on.

It may reject the RFC's L/T/M design.

The design must specify:
- root model;
- tool access;
- leaf roles;
- mutation owner;
- completion gate;
- routing/escalation rule;
- why each component earns cost;
- what development ablation would kill it.

Do not implement it.

---

## Handoff back

When finished:
1. commit only `docs/ASTRA_PREMIUM_V2_DESIGN_AUDIT.md`;
2. do not merge;
3. report commit SHA;
4. report only the executive verdict + confidence to the user.

The primary runner will read the full report from GitHub and decide whether to revise the RFC or authorize implementation.
