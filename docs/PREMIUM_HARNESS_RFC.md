# RFC: Premium Luna Orchestration — Pre-Experiment

Status: **experimental / not a release proposal**  
Branch: `experiment/premium-luna-orchestration`  
Stable baseline: `main@814a069df188d28a564c4b05fbc441c2e3092d3d`

## 1. Question

This experiment does **not** ask whether GPT-5.6 Terra is generally better than GPT-5.6 Luna.

It asks:

> Can a Terra-rooted, Luna-workhorse harness extend reliable task horizon beyond Over the Luna while outperforming raw Terra on cost-efficiency and robustness?

The candidate must earn its place against **both**:
- current Over the Luna, which is already a strong low-cost product;
- raw Terra, which is the obvious premium-model alternative.

A premium harness that is merely more expensive than Over the Luna, or merely a complicated wrapper around raw Terra, fails.

## 2. Product identity

Over the Luna remains a **Luna-first project**.

The premium experiment does not replace the project's center of gravity with Terra. It treats Luna as the abundant compute substrate and buys sparse premium judgment only where that judgment can steer, challenge, or integrate a large amount of Luna work.

Working principle:

> **Use even more Luna. Spend Terra where one judgment can steer a lot of Luna.**

This is an extension of the stable principle:

> **Use more Luna. Pay for judgment only when it earns its place.**

The stable `Over the Luna` agent remains unchanged on this branch except for validator awareness of experimental siblings.

## 3. Evidence behind the experiment

The experiment is motivated by several converging observations:

1. **Our Deep Judgment experiment was mixed, not model-dominance evidence.**
   - ordinary/harness-level P1: Luna and Terra reached the same decision while Terra cost materially more;
   - paired aiohttp concurrency and body-integrity judgments: Terra produced materially better decision contracts;
   - held-out httpcore root-cause E2E: Terra amplified the wrong causal model and cost much more;
   - isolated Django ASGI lifecycle E2E: Terra judgment + Main Luna passed the hidden accepted behavior that Luna-only missed even after review.

2. **Current model economics strongly favor Luna for high-volume tool work.**
   Terra is much more expensive per token, while general coding/tool-use performance is often much closer than the price ratio. Terra's strongest observed separation is in difficult debugging, causal synthesis, and some long-context reasoning.

3. **Recent production and research evidence favors selective orchestration over maximal delegation.**
   GitHub production work on Copilot CLI reports better latency/failure behavior from more selective delegation. GitHub's HydraFusion research preview shows multi-model workflows can improve the quality/cost frontier when the runtime chooses the least-complex workflow expected to satisfy the quality bar.

4. **Long-running agent research warns against over-detailed top-down plans.**
   Strong planners should own mission, acceptance, and consequential decisions, while builders retain implementation judgment from local repository evidence. Extra hierarchy and handoffs must earn their coordination cost.

5. **Wrong beliefs can cascade.**
   The httpcore failure in our own experiment demonstrates that a premium model's coherent but false belief can become more dangerous when downstream implementation treats it as authority.

References:
- GitHub Project HydraFusion: https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/
- GitHub selective delegation: https://github.blog/ai-and-ml/how-we-made-github-copilot-cli-more-selective-about-delegation/
- GitHub cost-efficient coding harness work: https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/
- VS Code subagents: https://code.visualstudio.com/docs/agents/run/subagents
- Anthropic long-running harness design: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Prior local experiment: `experiment/terra-deep-judgment`

## 4. Core architecture

```text
User selects experimental Premium Harness
                    |
                    v
          +----------------------+
          | Terra Executive      |
          | mission / acceptance |
          | global semantic state|
          +----------+-----------+
                     |
              evidence needed?
                     |
              +------+------+
              |             |
              v             v
       Luna Architect   Luna Researcher
              |
        consequential
        unverified belief?
              |
              v
         Luna Skeptic
      cheap falsification
              |
              v
          Terra adjudicates
              |
              v
          Luna Builder
     sole active mutator
              |
              v
          Luna Auditor
       independent check
              |
              v
          Terra adjudicates
       DONE / REPAIR / REPLAN
```

The default path should be shallow:

```text
Terra -> Architect (when needed) -> Builder -> Auditor -> Terra
```

Skeptic/Researcher are conditional, not ceremony.

## 5. Role constitution

### Terra Executive — mission owner, not work owner

Terra owns:
- user mission and acceptance;
- global constraints and invariants;
- explicit distinction between verified facts and hypotheses;
- coarse work decomposition;
- consequential cross-packet decisions;
- final adjudication: done, repair, or replan.

Terra does **not**:
- directly read/search the repository;
- edit files;
- run commands/tests;
- browse tool output repeatedly;
- produce line-level implementation instructions unless an externally fixed contract requires them;
- treat its own hypothesis as authority.

Its tool surface is structurally restricted to subagent invocation.

### Luna Architect — repository evidence

Reuse the stable Luna Architect:
- broad semantic repository evidence;
- relationships/dependencies;
- complete mutation surface when knowable;
- unresolved facts.

### Luna Skeptic — belief falsification

Reuse the stable Luna Skeptic for one narrow consequential assumption. It should discriminate alternatives, not write a second general plan.

### Luna Researcher — current external fact

Reuse only when a public API/spec/platform fact can materially change the engineering decision.

### Luna Builder — sole active mutator

One Builder trajectory owns canonical workspace mutation at a time.

Builder owns:
- local repository reasoning inside the bounded work packet;
- implementation choices consistent with stated invariants;
- edits;
- commands and focused tests;
- repair of ordinary implementation/test failures.

Builder does **not**:
- invoke other agents;
- change mission/acceptance;
- silently override a verified global invariant;
- continue after a contradiction that invalidates the work packet.

Builder returns compact state, not a narrative transcript.

### Luna Auditor — independent post-change check

Auditor is read-only with respect to repository mutation. It may inspect repository state, current diff/status, and run bounded local validation commands. It never edits.

Auditor owns:
- acceptance-critical behavior;
- current diff/change surface;
- one consequential invariant challenge;
- validation gaps;
- verdict: PASS / REPAIR / REPLAN / VERIFY.

The first experiment intentionally does **not** add automatic Sonnet review. Existing human-selected Premium Review remains outside this automatic core.

## 6. Premium invariants

1. **Luna is the compute substrate.**
   Search, repository reading, implementation, tests, and repetitive repair belong to Luna unless an experiment proves otherwise.

2. **Terra owns the mission, not the work.**
   Terra's value must come from leverage over Luna work, not from doing Luna work at a higher token price.

3. **Parallelize evidence; serialize mutation.**
   Read-only evidence may be parallel when questions are independent. Exactly one Luna Builder owns canonical mutation at a time.

4. **High-blast-radius hypotheses cannot authorize mutation.**
   A consequential unverified belief must pass the Critical Belief Gate before Builder receives a work packet.

5. **Delegation must buy leverage.**
   Every subagent call must buy independent evidence, falsification, implementation throughput, verification, or materially lower rework/risk.

6. **No recursive leaves.**
   Architect/Skeptic/Researcher/Builder/Auditor do not invoke agents.

7. **Compress entropy, not evidence.**
   Terra should receive compact decision-sufficient packets with concrete anchors, not raw search/test transcripts.

8. **Builder retains local implementation judgment.**
   Terra specifies outcomes, invariants, constraints, and stop conditions; it should not over-specify line-level implementation.

9. **Audit is independent of implementation.**
   Builder may validate its work, but Builder self-validation never substitutes for Auditor on the premium trajectory.

10. **Premium must expand the Pareto frontier.**
    If the candidate cannot beat Over the Luna on difficult-task capability and raw Terra on cost-efficiency/robustness, remove it.

## 7. Critical Belief Gate

A **critical belief** is an engineering claim whose falsity would materially change:
- causal diagnosis;
- algorithm or state model;
- concurrency/ordering;
- auth/security;
- data integrity/persistence;
- migration/rollback;
- public compatibility;
- multiple downstream mutation targets.

Terra records each consequential belief as one of:

- `VERIFIED` — directly supported by repository/runtime/spec evidence;
- `SUPPORTED_WITH_RESIDUAL` — evidence favors it but a named residual remains;
- `HYPOTHESIS` — plausible but not sufficient to authorize high-blast mutation;
- `USER_ASSUMPTION` — explicitly fixed by the user/product decision rather than inferred.

Before issuing a Builder work packet, **no high-blast belief may remain `HYPOTHESIS`**.

For a high-blast hypothesis, Terra must buy the cheapest discriminating evidence, normally one Luna Skeptic or Architect call. The request must name competing explanations and ask for evidence that could falsify the preferred one.

Blind retries or multiple agents restating the same belief do not satisfy the gate.

## 8. Terra state model

Terra should maintain a compact semantic state:

```text
MISSION
ACCEPTANCE
CONSTRAINTS
VERIFIED_FACTS
CRITICAL_BELIEFS
DECISIONS
CURRENT_WORK
VALIDATION_STATE
RESIDUAL_RISKS
```

Raw repository search logs, long terminal output, and mechanical edit transcripts should stay in Luna contexts unless a concrete excerpt is decision-critical.

## 9. Builder work packet

A Builder packet should contain:

```text
GOAL
ACCEPTANCE
INVARIANTS
VERIFIED_FACTS
WORK_SET
LOCAL_JUDGMENT_ALLOWED
STOP_OR_REPLAN_IF
VALIDATION
```

It should not contain a detailed speculative implementation recipe.

Builder returns:

```text
STATUS
CHANGED_PATHS
VALIDATION
DIFF_SUMMARY
CRITICAL_OBSERVATIONS
CONTRADICTIONS
REPLAN_REQUIRED
```

## 10. Auditor packet

Terra asks Auditor to independently inspect the current workspace against:

```text
ACCEPTANCE
INVARIANTS
CHANGED_PATHS
BUILDER_VALIDATION
ONE_CONSEQUENTIAL_CHALLENGE
```

Auditor may use read/search and bounded execute for:
- `git status`;
- `git diff` scoped to current work;
- focused repository-local validation.

It must not edit, install arbitrary dependencies, use network mutation, or perform external side effects.

This execute boundary is **experimental** and must be runtime-smoked before any product consideration.

## 11. Non-goals for the first experiment

The first experiment will not:
- replace stable Over the Luna;
- add automatic Sonnet/Opus review;
- support arbitrary MCP/extension side effects;
- run parallel competing Builders;
- build a general swarm;
- optimize every Luna/Terra reasoning-effort combination;
- expose model routing choices during a premium run;
- reuse solved cases as promotion evidence.

## 12. Experiment stages

### Phase 0 — structural runtime smoke

Prove in Copilot CLI:
- Terra Executive root actually runs as Terra;
- Terra uses only the subagent tool;
- Architect/Skeptic/Builder/Auditor run as Luna;
- Builder can mutate a disposable workspace;
- Terra itself never directly reads/edits/executes;
- Auditor can inspect/test but does not mutate;
- only one Builder mutation trajectory is active;
- final workspace satisfies a hidden deterministic oracle.

Failure of any boundary stops the experiment.

### Phase 1 — regression laboratory

Previously solved cases are allowed **only as regression/architecture tests**, not promotion evidence.

Use them to test mechanisms:
- ordinary P1-style work should show low premium overhead and shallow routing;
- aiohttp/Django wins should remain achievable;
- httpcore must specifically test whether the Critical Belief Gate blocks the previously amplified wrong causal model.

This stage exists to debug the harness, then freeze it.

### Phase 2 — architecture ablation

On a small fixed task set, compare:
- full candidate;
- without Critical Belief Gate;
- without Auditor;
- raw Terra;
- current Over the Luna.

Remove any component that does not earn measurable value.

### Freeze

After ablation:
- freeze role prompts/contracts;
- freeze budgets;
- freeze scoring;
- do not tune after seeing held-out outcomes.

### Phase 3 — held-out product evaluation

Primary arms:
1. current Over the Luna;
2. raw Terra;
3. premium Terra+Luna harness.

HydraFusion may be added only if its runtime is available in the same environment and the task shape is within its supported scope.

Task strata should emphasize long-horizon value:
- ambiguous multi-file debugging with competing causal models;
- cross-cutting lifecycle/concurrency/data-integrity work;
- coherent feature/change requiring discovery + implementation + validation across several subsystems;
- at least one large-but-straightforward control where premium overhead should not create a quality regression.

Previously studied aiohttp/httpcore/Django cases are excluded from promotion scoring.

## 13. Metrics

Record per arm:
- hidden-oracle/final correctness;
- requirement coverage;
- wrong-direction mutations;
- discarded/replaced patch size;
- repair/replan count;
- critical-belief failures and whether the gate caught them before mutation;
- Auditor actionable findings;
- task completion horizon;
- total wall time;
- total AI credits;
- Terra vs Luna credit share;
- number of Terra turns/checkpoints;
- Luna agent/tool calls;
- duplicate discovery/re-read;
- user interventions;
- unnecessary complexity/maintainability findings.

A prettier plan is not a win.

## 14. Cost discipline

Initial paid runtime uses one-shot workflows that are removed immediately after launch.

Do not lower reasoning quality merely to save credits. Instead:
- keep the architecture shallow;
- cap repeated evidence calls;
- stop failed hypotheses early;
- avoid repeating a run whose result is already decisive;
- expand repetitions only when variance could change the decision.

Reasoning effort should stay fixed within a comparison.

## 15. Promotion criteria

The candidate may advance toward product architecture review only if all are true:

- structural Terra/Luna tool and mutation boundaries hold;
- Critical Belief Gate demonstrably contains at least one consequential wrong-belief cascade in regression or held-out testing;
- held-out difficult-task correctness/completion is materially better than current Over the Luna;
- cost is materially lower than raw Terra for comparable quality, or quality is materially higher for comparable cost;
- Terra is not performing the majority of high-volume repository/tool work;
- Auditor provides independent value without becoming a second implementation agent;
- ordinary or straightforward tasks do not suffer material correctness regression;
- user interaction remains one initial premium-tier choice, not repeated Luna/Terra routing decisions.

## 16. Kill / redesign criteria

Kill or redesign if:
- Terra becomes the dominant search/edit/test worker;
- the system needs frequent Terra round-trips after local steps;
- Critical Belief Gate becomes ceremonial and fails to contain false global beliefs;
- Builder simply follows over-specified Terra recipes;
- Auditor duplicates Builder self-checks without catching consequential defects;
- coordination overhead erases raw-Terra cost advantage;
- the harness cannot beat stable Over the Luna on held-out difficult work;
- success depends on task-specific prompt tuning after seeing answers.

## 17. Open runtime questions

Before serious evaluation:
- Does a Terra parent with only `agent` structurally prevent direct repo/tool work while Luna Builder/Auditor receive their own declared tools in current Copilot CLI/VS Code?
- Can Auditor safely receive `execute` while remaining non-mutating in practice?
- How much artifact detail must flow back to Terra for decision sufficiency without turning Terra into an expensive transcript sink?
- Does one long Luna Builder trajectory outperform multiple coarse Builder packets for the target task horizon?
- Are Builder tool failures/retries visible to Terra in a compact enough return packet to support useful replanning?

These are experimental questions, not assumptions.
