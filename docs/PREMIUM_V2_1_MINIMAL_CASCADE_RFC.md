# Premium Harness v2.1 — Minimal Cascade RFC

Status: **pre-implementation specification / no paid experiment authorized yet**  
Branch: `research/astra-premium-v2-1-design`  
Parent design audit: `bcccc43d2250fc7771fda4e9ed3da76a1ca01401`  
Prior v2 RFC: `97cc22962e3bf810b76bf8d5ef4c9fe509a542c5`

This revision accepts the central Astra critique: the first v2 proposal tried to identify routing, verification, and acceptance policy at the same time. v2.1 deliberately tests a smaller claim.

---

## 1. Narrow product hypothesis

> A user-selected Premium session can start with one continuous Luna implementation attempt and perform at most one Terra takeover when runtime-visible acceptance-critical evidence remains unresolved, achieving useful quality/cost points between current Over the Luna and raw Terra.

This is **not** a claim that general L/T/M adaptive routing works.

This is **not** a long-horizon or multi-session claim.

This is **not** a claim that the completion controller proves semantic correctness.

The first implementation experiment is only allowed to ask whether this one-way cascade and its completion discipline are worth further research.

---

## 2. Primary product/runtime target

Primary target for architecture feasibility:

> **VS Code Local custom-agent execution**

Before any paid coding-agent run, a zero-AI runtime preflight must record:
- VS Code version;
- GitHub Copilot extension/runtime version;
- plugin/custom-agent support version;
- whether required hooks are enabled and permitted;
- exact supported hook events;
- observed parent/child model-cost restriction;
- tool surfaces actually available;
- whether the controller can keep trusted receipt state outside the editable repository workspace;
- whether synchronous subagent completion and mutation-owner quiescence are observable.

If these requirements cannot be demonstrated on the intended runtime, no hard completion-enforcement claim is allowed.

GitHub Copilot CLI remains an **evaluation adapter**, not assumed runtime-equivalent to VS Code Local. CLI version is pinned separately for experiments.

---

## 3. Minimal candidate topology

There are only two solver phases.

```text
Premium / Terra root
        |
        | bounded intake only
        v
one continuous Luna Builder attempt
        |
        v
completion reconciliation
      /   \
 accepted  unresolved blocking evidence
    |              |
 COMPLETE      one Terra takeover
                   |
                   v
              final reconciliation
```

No Lane M.

No Architect by default.

No Verifier.

No repeated Luna↔Terra switching.

No automatic cross-family reviewer.

### Root model

GPT-5.6 Terra.

Reason: current documented VS Code parent-cost restriction makes a Terra-root entry the cleanest automatic way to permit a later Luna child and Terra takeover inside one Premium choice.

This is a runtime compatibility choice, not evidence that Terra intake itself adds product value.

### Luna leaf

One GPT-5.6 Luna Builder.

The Builder:
- reads/searches/edits/runs;
- owns one continuous local trajectory;
- may perform at most one ordinary self-repair after its own validation failure;
- does not delegate;
- must return unresolved acceptance-critical evidence explicitly.

---

## 4. Bounded Terra intake

Before invoking Luna, Terra may only:

1. preserve the user request and repository-supplied constraints;
2. create the initial criterion register;
3. identify directly supplied anchors such as named files/errors/tests;
4. invoke the Builder.

Terra must not:
- broadly scout the repository;
- run diagnosis commands;
- pre-solve the implementation;
- mutate files.

If Terra performs substantial repository diagnosis before Builder invocation, the attempt is classified **COLLAPSED_TO_TERRA** for component analysis and fails the intended cascade-compliance metric.

The implementation experiment should prefer structural tool gating if the runtime can enforce it cheaply. If not, prompt-only compliance is measured rather than represented as guaranteed.

---

## 5. One-way escalation rule

The first candidate does not predict D1/D2/L/T from task wording.

Luna always gets the first full local attempt.

After Luna returns, the controller reconciles the criterion register and runtime receipts.

### No Terra takeover

Finish without takeover when:
- every blocking criterion is dispositioned `VERIFIED`;
- every executable evidence claim has a current runtime receipt;
- no contradictory runtime result exists;
- no surfaced supported-state exclusion conflicts with a blocking criterion;
- Builder did not report unresolved semantic ambiguity.

### Terra takeover permitted

At most one L → T takeover is permitted when:
- a blocking criterion remains unresolved after Luna's bounded attempt; and
- the unresolved item is repository-local/semantic rather than infrastructure-only; and
- there is concrete evidence to hand Terra: failing test, contradiction, unsupported state, or explicit unresolved decision.

### Do not escalate

Return BLOCKED/FAILED rather than buying Terra when:
- dependencies/service/runtime are unavailable;
- the user must choose product semantics;
- no meaningful local evidence can be obtained;
- the credit/process ceiling is reached.

### After takeover

Terra becomes the sole mutation owner and finishes or stops.

There is no T → L return in v2.1.

The Luna prefix is charged in full even if Terra later discards it.

---

## 6. Continuation versus restart

A takeover sees a changed workspace, so "raw Terra passed from base" is not evidence that takeover will pass.

At transfer, Terra receives:
- original user contract;
- criterion register;
- exact workspace identity;
- complete current patch/worktree state;
- changed paths;
- raw failing/contradictory outputs;
- Builder residuals;
- Builder causal claims explicitly marked as hypotheses unless directly evidenced.

For the experiment, a pre-Builder checkpoint is retained.

Terra may either:
- continue the Luna patch; or
- restore only the agent-owned experiment workspace to the checkpoint and restart.

The choice is logged.

User pre-existing edits must never be discarded by this rule in the interactive product.

Continuation versus restart is descriptive in the first candidate. It becomes a separately testable policy only if takeover failure suggests anchoring damage.

---

## 7. Mutation ownership

State:

```text
LUNA
-> NONE / QUIESCENCE
-> TERRA
-> NONE
```

Exactly one mutation owner.

A transfer is valid only after:
- Luna invocation has returned;
- controller-owned state capture completes;
- observable agent-owned background writers have stopped or been terminated in the experiment sandbox;
- workspace digest matches the captured transfer state.

If the runtime cannot observe or bound writer quiescence, v2.1 may claim only **synchronous single-child compliance**, not atomic mutation isolation.

No per-file locking or parallel mutating branches are introduced.

---

## 8. Acceptance authority

Criterion authority is ordered.

### Tier U — explicit user requirements

Highest authority.

User-fixed required behavior is blocking unless the user explicitly marks it optional.

It cannot be silently removed or downgraded by an agent.

### Tier R — repository compatibility/contracts

Established supported behavior, public API compatibility, tests, documented platform support, invariants, and repository instructions.

These may be discovered during execution.

Once added as blocking, deletion/downgrade must be recorded with a reason and reconciled by Terra.

### Tier A — agent-derived assumptions

Lowest authority.

Assumptions remain visibly assumptions until evidenced.

An assumption cannot create a reason to escalate merely by being described as important.

For underspecified consequential product choices:
- interactive product asks the user;
- unattended evaluation returns BLOCKED rather than inventing semantics.

---

## 9. Compact criterion register

Replace the large v2 ledger with the smallest useful register.

Each criterion contains:

```text
ID
SOURCE: U | R | A
CRITERION
BLOCKING: yes | no
DISPOSITION:
  OPEN
  VERIFIED
  FAILED
  UNRESOLVED
  WAIVED_BY_USER
VALIDATED_STATES
EXCLUDED_STATES
EVIDENCE_REFS
WORKSPACE_REVISION
```

Detailed logs live outside the row.

### Rules

- U criteria cannot be deleted/downgraded by agents.
- Every discovered blocking R criterion remains present until resolved.
- A known unsupported/fallback state relevant to a blocking criterion must appear in `EXCLUDED_STATES` or be resolved.
- Semantic mutation invalidates executable evidence conservatively in v2.1; revalidation is required against the final relevant workspace.
- `WAIVED_BY_USER` requires an authenticated/explicit user event.

---

## 10. Execution receipts

Model prose is not evidence that a check ran.

For executable checks, controller/runtime records a receipt:

```text
RECEIPT_ID
COMMAND_OR_TEST_ID
COLLECTION_STATUS
RESULT_CLASS
EXIT_STATUS
WORKSPACE_BEFORE
WORKSPACE_AFTER
TEST_ASSET_IDENTITY
ENVIRONMENT_IDENTITY
TIMESTAMP
```

Result classes distinguish at minimum:
- PASS;
- ASSERTION_FAIL;
- COLLECTION_FAIL;
- INFRA_FAIL;
- TIMEOUT;
- NOT_RUN.

A PASS receipt proves only that the recorded executable check passed in that state. It does not prove the model's relevance judgment.

Controller state and receipts should be outside the agent-editable target workspace when the primary runtime supports it.

---

## 11. Completion semantics

Separate three things:

1. **record consistency** — machine-checkable;
2. **semantic adequacy** — model/user judgment;
3. **user-visible prose** — not treated as a trusted controller result.

Official controller outcomes:

- `COMPLETE`
- `BLOCKED`
- `FAILED`
- `PARTIAL_WITH_USER_WAIVER`
- `NO_VERIFIED_COMPLETION`

### Deterministic completion reconciliation

The controller may accept `COMPLETE` only if:
- all required criterion IDs remain present;
- no blocking criterion is OPEN/FAILED/UNRESOLVED;
- every executable evidence reference has a valid current receipt;
- no contradictory current receipt exists;
- no fabricated waiver exists;
- final relevant workspace identity matches validation state.

The deterministic layer **does not claim**:
- criteria are complete;
- tests are semantically relevant;
- model judgment is correct.

### Stop-hook behavior

If a stop/finalization hook can block completion:
- allow at most one correction continuation;
- if the state is still invalid, controller outcome is `NO_VERIFIED_COMPLETION`.

If the hook is missing, times out, reaches a platform escape limit, or is disabled:
- never synthesize `COMPLETE`;
- classify the controller outcome separately.

Because model prose may still appear despite hook behavior, v2.1 does **not** claim "the user can never see a false completion sentence." It claims only that the trusted controller does not accept such a result as verified completion.

---

## 12. H1-specific lesson without H1 overfitting

H1 motivates but does not prove integrated Terra superiority.

The general mechanism retained from H1 is only:

> A surfaced supported-state limitation relevant to a blocking acceptance criterion must change completion state.

v2.1 must not encode:
- Redis;
- SSL;
- MSG_PEEK;
- hiredis;
- socket-specific takeover rules.

H1 remains a development regression only.

---

## 13. Verifier and mixed mission are deliberately absent

v2.1 does not include:
- Luna Verifier;
- Luna Auditor;
- Lane M;
- Architect;
- multi-packet Terra supervision.

They may return only after bounded component evidence.

### Future Verifier admission gate

On fixed correct and defective development snapshots, a Verifier must:
- find at least one executable acceptance-critical counterexample missed by equal-budget owner self-check;
- cause no false repair on the correct snapshot;
- stay within 20% added-cost envelope for the parent attempt.

Otherwise it stays removed.

### Future M admission gate

On at least two development missions with genuine cross-packet dependencies, forced M must:
- create a new full success versus one continuous Builder; or
- reduce total cost >=20% at equal full success;
- with no correctness regression.

Otherwise M stays removed.

---

## 14. Development plan before freeze

Maximum **core development matrix: 16 paid attempts**.

Use exposed tasks only as development evidence.

### Stage 0 — zero-AI runtime/controller tests

No model calls.

Must pass:
- criterion cannot silently disappear/downgrade;
- stale receipt invalidates completion;
- skipped/no-collected test is not PASS;
- malformed state cannot COMPLETE;
- missing/timeout stop hook cannot COMPLETE;
- fake user waiver rejected;
- workspace mutation invalidates evidence;
- ownership transfer/quiescence behavior is observed on the actual target runtime or explicitly downgraded as a claim.

Failure blocks paid implementation testing.

### Stage 1 — core product contrast, 12 attempts

Four exposed development tasks:
- H1 Redis;
- httpcore causal regression;
- Django lifecycle;
- one deterministic simple control.

Arms:
1. current OTL;
2. raw Terra;
3. minimal cascade v2.1.

4 tasks × 3 arms = 12 attempts.

Purpose:
- establish whether the cascade has any useful complete-task point;
- measure prefix waste;
- measure controller false completion;
- prevent a regression-only success narrative.

### Stage 2 — routing mechanism contrast, max 4 attempts

Only if Stage 1 does not already kill the cascade.

On H1 and Django:
- forced L;
- forced T under the same v2.1 acceptance/controller policy.

2 tasks × 2 = 4 attempts.

Purpose:
- compare the cascade against its own fixed solver paths;
- determine whether complementarity exists at all.

No Verifier/M matrix is authorized in this development cycle.

---

## 15. Development kill conditions

Stop v2.1 development immediately if any occurs:

- controller accepts COMPLETE while a surfaced blocking exception is unresolved;
- Stage 0 completion reconciliation fails on the supported runtime and cannot be fixed without a substantial new runtime;
- forced L matches cascade outcomes at lower total cost on the mechanism contrasts;
- forced T/raw Terra clearly dominates cascade after charging Luna prefix on the difficult contrasts;
- cascade degenerates into Terra doing substantial repository work before Luna in >=2 development tasks;
- takeover repeatedly inherits a damaged Luna state and no bounded restart policy is viable;
- no development task demonstrates a plausible quality/cost point unavailable from OTL/raw Terra.

A failed v2.1 candidate does not automatically kill Premium research, but it consumes one of the remaining material-design attempts.

---

## 16. Full-attempt accounting

All economics use **all attempts**, not survivor-only both-pass subsets.

For every arm record:
- complete task success/fail/block;
- false-complete status;
- total credits, including failed prefixes and correction turns;
- root/leaf credit split;
- wall/compute time;
- tool calls;
- number and reason of takeover;
- continuation vs restart;
- discarded patch work;
- controller outcome;
- hidden evaluator outcome.

Failures and blocks remain in the denominator.

---

## 17. Fresh pilot scope — only after a new freeze

No promotion holdout is selected during v2.1 design/development.

If development earns a freeze, initial product scope is:

> one issue-to-patch repository mission with reproducible local dependencies and executable acceptance.

Exclude:
- deployment;
- arbitrary external side effects;
- multi-day resumption;
- product discovery;
- visual/UI reliability claims unless separately sampled.

Sampling strata:
- D1 difficult local diagnosis;
- D2 multi-subsystem/invariant work;
- D3 substantial routine work;
- D4 straightforward control.

Pilot mixture:
- D1: 3/8;
- D2: 3/8;
- D3: 1/8;
- D4: 1/8.

These are deliberately premium-heavy engineering weights, not claims about market demand.

At least four repositories; no more than two tasks per repository.

---

## 18. Fresh pilot gates

Pilot gates are advancement gates, not population-level confidence claims.

### Hard vetoes

Across fresh first-pass attempts:
- 0 surfaced blocking exceptions followed by trusted `COMPLETE`;
- 0 hidden acceptance-critical false-completes by Premium;
- 0 raw-Terra-pass / Premium-fail-or-block tasks.

A hard veto stops promotion of this candidate. It does not alone kill all Premium research.

### Capability vs OTL

Require:
- >=2 distinct Premium-pass / OTL-fail-or-block wins in D1/D2;
- across >=2 repositories;
- 0 OTL-pass / Premium-fail-or-block tasks.

### Full-attempt economics vs raw Terra

Weighted by the predeclared D1–D4 mixture:
- Premium mean total credits <=75% of raw Terra;
- Premium credits per full success <=75% of raw Terra.

Also report paired both-pass median ratio; <=60% is a stretch target, not a primary gate.

### Straightforward overhead

Across D3/D4:
- all Premium tasks pass;
- paired median Premium/OTL credits <=2.0x;
- median wall time <=1.5x;
- no individual control exceeds OTL by >5 credits or >60 seconds unless the evaluation condition itself changed.

### Abstention

BLOCKED is not a success.

A candidate cannot improve false-complete by refusing difficult work and still pass capability gates.

---

## 19. Fresh-task selection

The candidate freeze SHA must not determine its own sample.

Before freeze:
- commit eligibility rules;
- commit stratum rubric;
- commit exclusion rules;
- commit sampling code;
- build/seal an eligible-pool manifest without model outcomes;
- hash candidate, evaluator, pool, and sampler independently.

After freeze:
- use an **independent future randomness beacon/value that was unavailable before the commitments**;
- derive the deterministic sample and reserves from the committed artifacts + that value;
- record the first draw and never reseed through commits.

A blinded independent curator is preferable where practical.

Oracle material is curator-preflighted before paid execution but sealed from model jobs:
- passes accepted head;
- meaningfully fails original base/known contract-breaking mutation where applicable;
- avoids helper-shape coupling;
- collection behavior verified.

Scoring occurs only after all arms complete.

---

## 20. Evaluator isolation

Model jobs:
- one independent runner per arm;
- no checkout of evaluation repository;
- no sibling arm workspace;
- historical target only;
- exact frozen plugin only;
- no accepted oracle/reference material;
- no credential capable of reading evaluator artifacts;
- no web/browser/MCP research tools;
- target remote removed;
- network/filesystem restrictions tested where Copilot runtime supports them.

Before paid use, run harmless zero-AI probes showing the claimed sandbox restrictions actually hold.

If model-command network egress cannot be blocked separately from Copilot transport, label the run `NETWORK_EXPOSED`; do not pretend it is cleanly isolated.

Capture on every exit path:
- full workspace archive + manifest/digest;
- file modes, symlinks, deletions, untracked bytes;
- index state and HEAD;
- test outputs;
- tool events;
- runtime/model metadata;
- partial state on timeout/cap failure.

Agent process deadline must leave time for controller-owned capture.

---

## 21. Runtime reproducibility

Pin/record:
- primary VS Code runtime for product smoke;
- Copilot CLI version for evaluation adapter;
- plugin/candidate commit;
- reasoning effort policy;
- target base SHA;
- Python/Node/dependency lock;
- runner environment/image metadata;
- oracle version;
- execution date/model metadata.

Do not silently compare runs across materially different model/runtime versions.

---

## 22. Research budget

This project is intentionally cost-sensitive.

No paid run is authorized merely by this RFC.

At execution time, first read the actual remaining included Copilot allowance. Do not infer it from old screenshots.

Program budget rule:

> **Maximum future Premium research spend = min(1,000 Copilot AI credits, 70% of the then-remaining included allowance, any lower amount explicitly authorized by the owner).**

Additional paid overage remains disallowed unless the owner separately changes that policy.

Budget buckets:
- core v2.1 development: max 400 credits;
- fresh pilot if separately authorized: max 500 credits;
- reserve/recovery: max 100 credits.

An exhausted bucket does not automatically borrow from another.

If the planned comparison cannot fit the available bucket without lowering model quality, reduce scope or stop. Do not lower reasoning quality merely to manufacture affordability.

---

## 23. Program-level kill rule

v1 already consumed one materially distinct Premium design.

v2.1 is the second.

If v2.1 is competently implemented/evaluated and still fails to produce a useful point versus simple OTL/raw-Terra baselines, **end bespoke Premium product research by default**.

Restart later only if:
- runtime capabilities materially change;
- a new external orchestration primitive appears;
- model economics/capabilities materially change;
- or the owner explicitly authorizes a new research budget for a different hypothesis.

Do not fund v3/v4 by renaming topology.

Other kill signals:
- >=80% of eligible fresh tasks collapse to one effective solver path without benefit from exceptions;
- acceptance control adds visible overhead but no reduction in false completion/recovery mistakes;
- product benefit cannot be stated more concretely than "it chooses models for you";
- simple user choice between stable OTL and raw Terra remains superior on the declared workload.

---

## 24. What must be true before implementation authorization

The design may move to a small implementation experiment only if an independent review agrees that:

1. the one-way policy is operational, not descriptive;
2. the completion controller's guarantee is stated narrowly enough;
3. required VS Code hooks/tool behavior can be tested without paid model use;
4. ownership transfer is implementable or honestly downgraded as a claim;
5. development matrix can fit the finite budget;
6. fresh task selection does not depend on designer-controlled randomness;
7. full-attempt economics and false-complete denominators are fixed before results;
8. no omitted component is required to interpret a v2.1 result.

Until then: **no implementation and no paid Copilot experiment.**
