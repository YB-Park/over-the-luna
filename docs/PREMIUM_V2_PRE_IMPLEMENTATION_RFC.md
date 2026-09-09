# Premium Harness v2 — Pre-Implementation Design RFC

Status: **design only / no implementation authorized**  
Research branch: `research/astra-premium-v2-design`  
Prior frozen candidate: `0083f3d81e7339f3b22e3efaa852562d7daa07e5` — **stopped / redesign**  
Primary evidence head: `experiment/premium-luna-orchestration@b7ce4b88ad090cc26d6d9a377b765fdf9a075e89`  
Independent audit: `research/astra-premium-audit@79f3c4d34beb1383fa55fae180c999aa23770d64`

This document is a **hypothesis proposal**, not a candidate prompt specification. No paid Copilot experiment should be launched from this document alone.

---

## 1. Why v2 exists

The first Premium candidate tested a fixed topology:

```text
Terra mission owner
  -> Luna Builder
  -> Luna Auditor
  -> Terra final adjudication
```

It established useful runtime facts but failed its first held-out product task:

- Over the Luna: 3/4 corrected H1 behavior oracle, 5.694290 credits, 167s;
- Raw Terra: 4/4, 71.013030 credits, 222s;
- frozen Premium: 3/4, 14.671259 credits, 355s.

The most important forensic result is not merely that Premium lost. The Builder explicitly reported the unsupported-flags fallback limitation, Terra repeated that limitation to Auditor, Auditor repeated it while returning PASS, and Terra still declared completion.

Therefore H1 is poor evidence for the explanation:

> "Terra simply lacked enough local context."

For that acceptance-critical branch, the information reached the control plane. The stronger evidence is:

> **A known residual was not operationally bound to completion.**

The independent Astra audit therefore recommended `STOP_AND_REDESIGN` with MEDIUM confidence while preserving the broader Premium hypothesis.

v2 must not become an H1-specific patch. It must address the general product/control problem exposed by H1 while avoiding a new fixed topology whose components have not earned their cost.

---

## 2. Product identity remains Luna-first

The project still starts from a deliberate prior:

> **Luna is abundant, cheap, and unusually capable. Use it whenever premium inference has not demonstrated leverage.**

But Luna-first is a **resource-allocation prior**, not a constitutional prohibition on Terra touching the repository.

The failed v1 architecture taught that enforcing:

> "Terra may never participate directly in the local repository evidence loop"

can remove exactly the integrated strong-model trajectory that raw Terra may sometimes need to buy a correctness edge.

v2 therefore reframes the identity:

> **Default compute to Luna. Spend Terra only where its direct participation or global judgment is expected to change the complete-task outcome.**

This preserves the project's Luna identity without making model identity more important than correctness.

Working slogan:

> **Use Luna by default. Let expensive intelligence enter the exact loop where it can change the result.**

---

## 3. Revised product thesis

The v1 thesis overclaimed "long task horizon" without directly measuring it.

The v2 initial thesis is narrower and testable:

> **Can one Premium product choice adaptively allocate Luna and Terra across a single substantial coding mission so that it beats current Over the Luna on target difficult work and beats simply choosing raw Terra on complete-task cost efficiency, without asking the user to route models?**

Initial product scope:
- one user-selected Premium session / mission;
- repository discovery, implementation, validation, and integration;
- local difficult debugging;
- cross-subsystem feature/change work;
- large-but-routine controls.

Out of scope for the first v2 promotion claim:
- multi-day autonomous resumption;
- durable cloud-agent work across disconnected sessions;
- arbitrary external side effects;
- parallel competing mutation branches.

If later evidence justifies a true long-horizon/resumption claim, it becomes a separate phase.

---

## 4. Core change: adaptive topology, not fixed hierarchy

User experience stays simple:

```text
Over the Luna
or
Premium
```

The user never chooses Luna vs Terra internally.

Inside Premium, the runtime chooses among a **small set of execution lanes**.

### Lane L — Luna execution

Use when:
- the task has a clear executable acceptance contract;
- local implementation/diagnosis is within one coherent Luna trajectory;
- there is no evidence that a stronger integrated local loop is needed;
- cross-subsystem integration risk is low enough to validate directly.

Shape:

```text
Terra intake
   -> Luna Builder
   -> evidence returned
   -> Terra completion gate
```

Optional cheap verification is added only when it can provide orthogonal evidence.

This lane accepts a fixed small Terra intake cost because the user selected Premium, but avoids turning every Premium task into a multi-agent ceremony.

### Lane T — Terra integrated execution

Use when the hard part is **inside the repeated local evidence loop**:
- competing causal explanations materially change intervention class;
- the next hypothesis depends on direct tool/test output;
- subtle platform/runtime semantics dominate;
- delegating diagnosis would strip the expensive model from the decision-critical observation/intervention cycle.

Shape:

```text
Terra
 read/search/test
 diagnose
 mutate
 validate
 complete
```

Terra may use repository tools directly.

This lane is intentionally close to "raw Terra", but still uses the Premium product's acceptance-evidence and cost/control discipline.

Its existence is required by H1: the product may not assume that all premium reasoning can be compressed into a mission-level supervisor.

### Lane M — mixed mission

Use when:
- much of the work is routine enough for Luna;
- correctness depends on acceptance/invariants spanning multiple subsystems or coarse work packets;
- expensive integration mistakes are plausible;
- one local trajectory should not monopolize the entire mission.

Shape:

```text
Terra mission state
   -> Luna work packet
   -> acceptance/evidence update
   -> Terra adjudication only at an event boundary
   -> next Luna packet or Terra-local intervention
   -> completion gate
```

Terra does not return after every command or file.

### Lane switching

Lane selection is **not permanent**.

Examples:
- L -> T when a Luna Builder returns a blocking, unresolved local causal ambiguity.
- L -> M when implementation reveals a cross-subsystem invariant or multiple coherent work packets.
- M -> T for one bounded diagnostic episode whose answer cannot be safely delegated.
- T -> L when the hard local diagnosis is resolved and remaining work is mechanical.

Lane switches are recorded internally but never exposed as a user model-routing question.

---

## 5. Routing by observable state, not task labels

Do not route simply because a task is called:
- "debugging";
- "architecture";
- "large";
- "important";
- "many files".

Those labels were not predictive enough in prior experiments.

v2 routing should ask four questions.

### Q1 — Where is the uncertainty?

- **Local interactive uncertainty**: the important belief changes after each repository/tool observation -> candidate for Lane T.
- **Global integration uncertainty**: local work is mostly straightforward, but several acceptance constraints must survive across work packets -> Lane M.
- **Low consequential uncertainty**: acceptance is concrete and one Luna trajectory can own the work -> Lane L.

### Q2 — What is the blast radius of a wrong belief?

A belief is high-blast when falsity would alter:
- public contract;
- data model/persistence;
- state ownership/lifecycle;
- concurrency/ordering;
- security/auth;
- migration/rollback;
- several independent mutation targets.

High blast radius changes the **evidence/completion requirement**, not automatically the model.

### Q3 — Can the uncertainty be made executable?

If a disputed property can cheaply become a discriminating test/counterexample, buy that evidence before adding more narrative reasoning.

### Q4 — Does premium inference need direct evidence access?

If the answer depends on an iterative read/run/update loop that cannot be represented as a stable decision packet without losing the crucial state, keep Terra inside that loop.

This is the central v2 departure from the tool-blind Terra executive.

---

## 6. Acceptance Evidence Ledger — first-class control state

H1 shows that a residual can be visible yet still get waved through.

v2 therefore treats acceptance as structured state, independent of who originated a claim.

Every acceptance criterion has an entry conceptually equivalent to:

```text
ID
CRITERION
SEVERITY: BLOCKING | NON_BLOCKING
STATUS: VERIFIED | FAILED | UNVERIFIED | USER_ACCEPTED_RESIDUAL
EVIDENCE
COUNTEREXAMPLE_OR_TEST
SUPPORTED_STATES
UNSUPPORTED_STATES
SOURCE
WORKSPACE_REVISION
CONSEQUENCE_IF_WRONG
```

### Origin does not matter

A consequential uncertainty has the same semantics whether discovered by:
- Terra;
- Luna Builder;
- Architect/Explorer;
- Verifier;
- test output;
- user-provided evidence.

The old distinction around "Terra-originated critical belief" is removed.

### Completion invariant

**No BLOCKING criterion may be `UNVERIFIED` or `FAILED` at completion.**

A BLOCKING residual can finish only when:
- the user explicitly accepts the residual; or
- the mission is reported incomplete/blocked.

"Preserves previous behavior", "seems compatible", and "Reviewer PASS" are not evidence states.

### Known fallback rule

If any agent reports a fallback, unsupported platform branch, untested state, or behavior-preserving exception related to a BLOCKING criterion:
- it must be entered in `UNSUPPORTED_STATES` or resolved with evidence;
- it may not disappear inside a prose summary.

### Workspace linkage

Evidence should be tied to the workspace version it validated.

Preferred experiment representation:
- historical base SHA;
- current diff/workspace digest when practical;
- changed path set;
- test/check identity and result.

This does not prove semantic truth, but prevents evidence from silently referring to a superseded patch.

---

## 7. Terra's new role

Terra is neither:
- a permanently tool-blind manager;
- nor an always-on expensive repository worker.

Terra owns:
- the user mission;
- lane selection/switching;
- the Acceptance Evidence Ledger;
- cross-packet invariants;
- consequential unresolved state;
- mutation-owner transitions;
- final completion decision.

Terra may directly:
- read/search repository evidence;
- execute bounded commands/tests;
- edit when Lane T owns mutation.

Terra should not:
- perform mechanical work in Lane L/M merely because tools are available;
- review every local step;
- add hierarchy for confidence theater;
- declare completion while a blocking ledger entry is unresolved.

### Event-triggered Terra intervention

In delegated lanes, Terra returns when an event occurs, not on a timer.

Candidate events:
- Builder reports contradiction against a verified criterion/invariant;
- any BLOCKING criterion becomes UNVERIFIED;
- a new high-blast cross-subsystem decision appears;
- local repair repeats without progress;
- mutation ownership must transfer;
- a work packet completes and affects later packets;
- verifier produces contradictory evidence;
- user/product decision is required.

---

## 8. Mutation ownership

Keep the proven stable invariant:

> **Parallelize evidence; serialize mutation.**

But mutation owner can change by lane.

State:

```text
MUTATION_OWNER = TERRA | LUNA_BUILDER | NONE
```

Rules:
- exactly one active owner;
- Terra may not edit while Luna Builder owns mutation;
- Luna Builder must return before Terra takes ownership;
- owner transition is a recorded phase boundary;
- read-only evidence may be parallel only when questions are independent.

The design should not depend on multiple competing Builders in v2 initial experiments.

---

## 9. Luna roles should buy clear leverage

Do not reintroduce an agent zoo.

Proposed minimum primitives:

### Luna Builder

Owns one coherent delegated implementation trajectory:
- read/search/edit/execute;
- local causal diagnosis;
- focused validation;
- reports ledger-relevant evidence and residuals.

### Luna Explorer / Architect — optional

Use only when broad repository structure/dependency discovery is the bottleneck.

It must not certify causal truth merely because it read broadly.

The stable Architect may or may not be suitable; this remains an implementation question.

### Luna Verifier — optional, evidence collector rather than certifier

v1 Auditor had a dangerous semantic role: it issued a global PASS.

v2 should test a weaker role:

> collect independent acceptance evidence and counterexamples; **do not certify mission completion**.

Possible output per criterion:
- evidence found;
- test/counterexample run;
- contradiction;
- unverified state.

Terra remains the completion owner.

The Verifier is **not mandatory**. It should be invoked only when:
- it can examine an artifact/state independently;
- a cheap counterexample could change completion;
- the evidence is not merely a repeat of Builder self-validation.

A same-model second context is not assumed to be independent correctness.

---

## 10. Assurance policy must be adaptive

Candidate assurance levels:

### SELF
Builder/Terra owner validates directly. No extra verifier.

Use when acceptance is executable and all blocking criteria have direct evidence.

### CHEAP_VERIFY
One Luna Verifier checks one or more acceptance-critical states independently.

Use only when expected evidence value exceeds coordination cost.

### TERRA_VERIFY
Terra directly inspects/runs a bounded discriminating check when:
- a blocking residual remains;
- local semantics are exactly where premium reasoning matters;
- same-model verification is likely to be correlated.

### HUMAN_PREMIUM_REVIEW
Existing human-selected Sonnet review remains outside the automatic core initially.

Do not add automatic cross-family review before Terra/Luna v2 earns its own value.

---

## 11. The verifier must not say global PASS

This is a deliberate design constraint.

Verifier output should look like:

```text
CRITERION_EVIDENCE
CONTRADICTIONS
UNVERIFIED
TESTS
WORKSPACE_REVISION
```

not:

```text
PASS
```

The final completion decision belongs to Terra and must reconcile the ledger mechanically in its reasoning contract:

```text
for every BLOCKING criterion:
    status must be VERIFIED or USER_ACCEPTED_RESIDUAL
otherwise:
    cannot declare complete
```

This is still prompt-level enforcement unless a future deterministic policy layer is added. Compliance must therefore be measured experimentally rather than assumed.

---

## 12. Avoiding the "adaptive router becomes raw Terra" failure

Adaptive topology can collapse into expensive always-Terra behavior.

v2 must measure and constrain this.

Record for every development/evaluation task:
- initial lane;
- each lane switch and trigger;
- Terra direct repository tool calls;
- Luna repository tool calls;
- Terra/Luna credits;
- mutation-owner time;
- whether a lane switch changed the final implementation/evidence;
- post-hoc counterfactual regret from development ablations.

A routing decision has value only when it changes:
- correctness;
- rework;
- accepted evidence;
- or materially lowers cost for the same outcome.

"Terra thought carefully before delegating" is not leverage.

---

## 13. Cost controls are topology controls, not quality reduction

Do not lower reasoning effort merely to make v2 appear cheap.

Instead:
- no mandatory Verifier;
- no mandatory Architect;
- no Terra round-trip after local steps;
- one mutation owner;
- one repair cycle by default before re-evaluating lane;
- no repeated agents answering the same question;
- prefer executable discrimination over duplicate narrative reasoning;
- once local premium diagnosis is resolved, hand mechanical work back to Luna when safe.

Credit ceilings remain runaway protection, not budgets.

---

## 14. Product workload distribution must be declared before promotion evaluation

v1 had no sufficiently explicit workload distribution.

v2 should define the first product target as:

### D1 — difficult local diagnosis
Examples:
- platform/runtime semantic edge;
- competing intervention classes;
- data integrity/concurrency bugs where direct tool evidence changes the next hypothesis.

Desired product behavior:
- Premium should sometimes choose Lane T.
- OTL may be near but below sufficient reliability.
- Raw Terra is the strongest expensive comparator.

### D2 — multi-subsystem integration
Examples:
- coherent feature spanning config/API/storage/lifecycle;
- several cheap implementation packets constrained by global compatibility.

Desired behavior:
- Lane M should amortize Terra judgment over substantial Luna work.

This is the most credible theoretical niche for mixed orchestration.

### D3 — large but routine work
Desired behavior:
- Lane L; Premium should avoid unnecessary Terra tool work and mandatory review.

### D4 — straightforward control
Desired behavior:
- shallow Luna path;
- no correctness regression;
- measure fixed Premium overhead.

The first v2 product claim should **not** include autonomous multi-session resumption unless specifically evaluated later.

---

## 15. Proposed quantitative product gates — draft for attack, not yet final

Astra should challenge these numbers. They are proposed before v2 implementation so the project has something falsifiable.

### Safety / false acceptance

Across fresh promotion holdouts:
- Premium must not produce more acceptance-critical false-complete outcomes than Over the Luna.
- Any trace that explicitly surfaces a BLOCKING unsupported state and still declares complete counts as a **control failure**, even if the hidden oracle happens to pass elsewhere.

### Capability against OTL

On target difficult strata D1 + D2:
- Premium must show at least **two task-level capability wins** where Premium passes and OTL fails/blocks, with no offsetting task where OTL passes and Premium fails.
- With a small sample, this is a product gate rather than a population-significance claim.

### Efficiency against Raw Terra

On tasks where both Premium and Raw Terra satisfy the complete hidden oracle:
- median Premium AI credits should be **<= 60% of raw Terra**;
- no task should require >100% raw-Terra credits unless Premium achieves a clearly broader accepted scope.

### Straightforward overhead

On D3/D4 controls where OTL and Premium both pass:
- median Premium credits should be **<= 2.5x OTL**;
- median Premium wall time should be **<= 2.0x OTL**;
- routing should remain Lane L unless concrete evidence forced escalation.

These thresholds are intentionally strict enough that "Premium is just more elaborate" cannot pass.

Astra should recommend different thresholds if these lack product/economic justification.

---

## 16. Development evidence before a new freeze

Do not jump directly to fresh holdouts.

Use already-exposed/solved tasks **only as development/regression evidence**.

### Required mechanism regressions

- H1 Redis hiredis: v2 must preserve the known acceptance-critical unsupported-state lesson. Do not hardcode the accepted implementation.
- httpcore import race: ensure v2 does not rebuild a pre-mutation causal-manager chain that amplifies a wrong intervention class.
- Django lifecycle: ensure v2 can preserve the cross-cutting lifecycle win without mandatory fixed topology.
- deterministic simple control: verify Premium can select a shallow Luna path.

### Component ablation

Before freeze, isolate marginal value on development tasks:

1. adaptive v2 full;
2. same candidate with Verifier disabled;
3. same candidate forced Lane L where applicable;
4. same candidate forced integrated Terra on selected D1 tasks;
5. raw Terra and current OTL baselines.

Purpose:
- determine whether routing itself has value;
- determine whether Verifier catches defects rather than merely consuming tokens;
- identify when integrated Terra actually beats delegated Luna;
- calibrate lane triggers.

Do not use development cases for promotion.

---

## 17. Freeze discipline for v2

Only freeze after:
- routing lanes are defined;
- component ablation shows at least one non-ceremonial role;
- acceptance ledger compliance works on development regressions;
- evaluator infrastructure is validated;
- product thresholds are final.

Frozen identity must include:
- agent/prompts;
- model assignments;
- reasoning-effort policy;
- tool surfaces;
- lane-switch policy;
- completion gate;
- verifier policy;
- credit ceilings;
- evaluator version.

If any of those change after fresh holdouts begin, declare a new candidate version.

---

## 18. Fresh holdout selection must resist cherry-picking

H1 and previously documented H2/H3/H4 are now **exposed** to the design process and cannot be treated as pristine promotion holdouts for v2.

Before v2 freeze, define a task-selection algorithm; select tasks only **after** freeze.

Proposed scheme:

1. define eligible public repositories and date window;
2. require merged post-cutoff changes with reconstructable base SHA and evaluator-owned tests/oracles;
3. build eligible pools for D1–D4 without inspecting candidate performance;
4. sort candidates deterministically;
5. derive a public deterministic seed from the frozen v2 commit SHA;
6. sample the required count per stratum using that seed;
7. record exclusions with reasons before running models.

Astra should challenge whether this is practically sufficient to reduce curator bias.

---

## 19. Evaluator architecture v2

The H1 evaluator improved after several zero-AI corrections, but the original runtime had avoidable exposure.

New preferred workflow topology:

### Prep job — no model
- create exact target historical workspace tarball;
- remove target git remote after shallow checkout;
- materialize exact frozen plugin artifacts;
- pin CLI/tool dependencies;
- upload immutable inputs.

### One independent runner per arm
- download only its target workspace and relevant plugin;
- do **not** check out the evaluation repository;
- do not expose sibling arm workspaces;
- run one model arm;
- capture:
  - complete workspace tarball;
  - tracked/staged/untracked/deleted state;
  - base HEAD;
  - diff digest;
  - output/OTel;
  - tool/runtime versions;
  - partial artifacts even on agent failure/timeout.

Raw Terra, OTL, and Premium run in separate jobs/runners.

### Evaluator job — after all model jobs
- download arm workspaces;
- only now fetch accepted reference/test material;
- validate oracle against accepted head;
- run identical oracle against all arms;
- distinguish:
  - assertion failure;
  - collection failure;
  - dependency/infrastructure failure;
  - timeout/credit cap;
  - no patch/agent crash.

### Contamination limitation

Copilot still needs network access to its service, so perfect outbound isolation may not be practical.

At minimum:
- no evaluation repository checkout in model jobs;
- no target git remote;
- no sibling arms;
- no accepted material;
- no browser/MCP/web tools;
- record shell commands and unexpected network use where observable.

Do not claim stronger isolation than runtime proves.

---

## 20. Runtime reproducibility

Future evaluation should pin where possible:
- Copilot CLI version;
- Python/Node versions;
- dependency versions;
- runner image (`ubuntu-24.04` rather than moving `ubuntu-latest`);
- plugin commit;
- target base SHA;
- hidden oracle version.

Model service aliases/backend weights may still change. Record execution date/model metadata and treat long-separated runs cautiously.

---

## 21. What v2 must prove before it becomes a product

A useful Premium product is not:

> "Terra was present."

It must prove:

1. **Routing value**
   - internal lane choice improves complete-task outcome/cost relative to simpler fixed alternatives.

2. **Acceptance control**
   - surfaced blocking uncertainty changes system behavior and cannot be silently PASSed.

3. **Luna leverage**
   - substantial work stays on Luna when Terra does not need direct evidence.

4. **Integrated premium competence**
   - when local strong-model continuity matters, the architecture does not prohibit it.

5. **Assurance value**
   - optional verification catches consequential defects or is removed.

6. **Product simplicity**
   - user makes one tier choice, no internal model-routing decisions.

7. **Pareto value**
   - on the declared workload mix, Premium occupies useful points between current OTL and raw Terra.

---

## 22. Primary unresolved questions for Astra

The independent design audit should attack these specifically.

### Architecture
- Is an always-Terra root already too much fixed premium overhead?
- Does giving Terra full repository tools destroy the cost discipline by making adaptive routing collapse toward raw Terra?
- Can an LLM reliably self-route among L/T/M without an external deterministic router?
- Would a cheap Luna router be better, despite Luna parent -> Terra escalation limitations in VS Code?
- Is Lane M actually distinct from the failed v1 fixed hierarchy, or just renamed?
- Should Terra direct tool access be bounded structurally, prompt-wise, or through separate hidden agents?
- Is mutation-owner switching viable in current VS Code/Copilot custom-agent semantics?

### Acceptance control
- Is the Acceptance Evidence Ledger useful control state or prompt bureaucracy?
- Can prompt-level completion gating be trusted after H1, or is a deterministic external policy layer necessary?
- What evidence representation best survives subagent statelessness without becoming expensive transcript replay?
- How should user-accepted residual risk be represented in an unattended coding workflow?

### Verification
- Should initial v2 omit Luna Verifier entirely and first prove routing?
- Can same-model verification ever be orthogonal enough to earn cost?
- Would Terra self-verification after Luna work simply recreate expensive review without independence?
- What component ablation best isolates assurance value?

### Evaluation
- Are D1–D4 the right product distribution?
- Are the proposed numeric gates defensible?
- How many fresh tasks are minimally informative under the user's limited credit budget?
- Is deterministic post-freeze task sampling practical, or is another blinding method better?
- How should stochastic repetition be allocated?
- Can historical public PRs after the model cutoff still suffer memorization/contamination risk sufficient to invalidate the design?

### Product strategy
- Is a single adaptive Premium agent a better product than separate "Luna efficient" and "Terra integrated" user choices?
- Is there a credible niche where adaptive mixed orchestration beats both baselines often enough to justify its complexity?
- At what evidence point should the project kill the Premium hypothesis rather than design v3/v4 indefinitely?

---

## 23. Explicit non-goals before Astra review

Do not yet:
- implement v2 agents;
- modify v1 frozen agents;
- run paid Copilot experiments;
- select fresh promotion holdouts;
- use H2/H3/H4 as if they were unexposed holdouts;
- add automatic Sonnet/Opus review;
- create parallel mutating Builders;
- tune prompts against H1 accepted implementation.

The next action after this RFC is **independent design audit**, not code.
