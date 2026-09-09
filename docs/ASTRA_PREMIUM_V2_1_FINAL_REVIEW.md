# Astra Premium v2.1 Final Pre-Implementation Review

## 1. EXECUTIVE VERDICT

**Verdict: `REVISE_V2_1_BEFORE_IMPLEMENTATION`**  
**Confidence: HIGH**

The minimal cascade is now a sufficiently small, falsifiable research hypothesis. The remaining no-go is confined to **two acceptance-controller contract changes**: preserve the authority and content of captured requirements across model-proposed updates, and make authenticated waivers terminally partial rather than eligible for full completion/success. These are corrections to the prior P0-C requirement, not grounds for another architecture cycle.

The revised RFC states the intended authority policy, but its deterministic completion checklist checks surviving IDs rather than preserved obligations. It also introduces `PARTIAL_WITH_USER_WAIVER` without explicitly excluding a valid waived requirement from its `COMPLETE` predicate or full-success accounting. An implementer should not have to resolve these consequential ambiguities while implementing the gate that is supposed to prevent them. Neither finding demands formal proof of semantic correctness.

**Do not replace the Luna-first sequence, add a router, or restore Verifier/M/Architect to address these findings.** Once the two small changes in section 7 are committed, reassess those changes only. The unresolved empirical question is whether a Luna prefix helps enough to pay for itself; that requires the bounded development contrast, not another speculative design.

Review date: **2026-09-09**. Reviewed branch head: `fd39072d66ea82ac3427d8431230967f7d3aa587`; RFC revision identified by the handoff: `9991878aa93e6d3058103ac32a9edea510bcbc32`. The handoff was read in full first, followed by the prior audit, revised RFC, prior RFC for context, and H1 results. References below use this immutable review snapshot unless otherwise indicated: [handoff](https://github.com/YB-Park/over-the-luna/blob/fd39072d66ea82ac3427d8431230967f7d3aa587/docs/ASTRA_PREMIUM_V2_1_HANDOFF.md), [v2.1 RFC](https://github.com/YB-Park/over-the-luna/blob/fd39072d66ea82ac3427d8431230967f7d3aa587/docs/PREMIUM_V2_1_MINIMAL_CASCADE_RFC.md), [prior audit](https://github.com/YB-Park/over-the-luna/blob/bcccc43d2250fc7771fda4e9ed3da76a1ca01401/docs/ASTRA_PREMIUM_V2_DESIGN_AUDIT.md), [prior RFC](https://github.com/YB-Park/over-the-luna/blob/fd39072d66ea82ac3427d8431230967f7d3aa587/docs/PREMIUM_V2_PRE_IMPLEMENTATION_RFC.md).

This review performed document inspection and focused public-runtime verification only. No candidate, hook, controller, or evaluator was implemented; no Copilot invocation or paid experiment occurred; no future promotion task was selected. This report does not authorize implementation, development spending, or promotion.

## 2. P0 BLOCKER MATRIX

`RESOLVED` means sufficiently specified for a small prototype, subject to the RFC's execution prerequisites. It does not mean that a runtime property or product benefit has already been demonstrated.

| Item | Status | Evidence in revised RFC | Final assessment |
|---|---|---|---|
| **P0-A — executable routing** | **RESOLVED** | §§3–6, 13–15 | Initial Luna attempt, at most one self-repair, concrete residual trigger, infrastructure/user-choice exclusions, one-way Terra takeover, and termination are bounded. No predictive L/T/M router remains. Continuation/restart and semantic escalation judgments are measurable policy choices, not extra solver lanes. |
| **P0-B — acceptance trust boundary** | **RESOLVED** | §§9–11, 14 | Record consistency, semantic adequacy, and prose are explicitly separated. Missing/failed hooks cannot confer trusted completion; correction is bounded. This resolves the previous impossible prose guarantee. The specific authority/outcome defects belong to P0-C below. |
| **P0-C — authority and waiver** | **PARTIALLY_RESOLVED** | §§8–11; compare prior audit's acceptance-authority discussion | U/R/A ordering and authenticated user events are sound intentions. The accepted-update contract does not bind surviving IDs to their original authority/content, and the terminal mapping does not exclude a genuine waiver from full success. Two blocking changes in §7. |
| **P0-D — primary runtime** | **RESOLVED** | §§2, 21, 24 | VS Code **Local custom-agent execution** is specific enough for design. Exact installed versions, enabled hooks, effective permissions and adapter evidence belong to the preflight manifest. Static/configuration evidence must not be mislabeled as an observed live model trajectory; see §6. |
| **P0-E — ownership transfer** | **RESOLVED** | §§6–7, 20 | Synchronous return, state capture, observable background-writer termination, digest matching, checkpoint scope and preservation of user edits are covered. The fallback to synchronous single-child compliance honestly limits the claim. No atomicity requirement is added. |
| **P0-F — economics** | **RESOLVED** | §§16–18 | Full-attempt costs plus hard comparator-regression vetoes eliminate the previous survivor-only advancement rule. Controls must pass, and BLOCKED cannot earn success. The full-success mapping must also implement the P0-C waiver correction; this is the same defect, not a third blocker. |
| **P0-G — holdout/oracle timing** | **RESOLVED** | §§19–20 | Independently committed pool/evaluator/sampler, future independent randomness, no reseeding, and sealed oracle preflight remove the specific designer-seed and late-oracle defects. Curator/pool bias and public-data contamination remain limitations. |
| **P0-H — finite scope/budget** | **RESOLVED** | §§14–15, 22–23 | Maximum 16 development attempts, non-borrowing buckets, a remaining-allowance cap and v2.1 counted as design two are finite. Affordability is conditional; an exhausted budget yields STOP/INCONCLUSIVE, not a smaller favorable evidence denominator. |

## 3. MINIMAL CASCADE THESIS

**Worth a small implementation after the two controller clarifications; not yet supported as a product.** Terra root is an entry/runtime choice, not demonstrated reasoning leverage. The primary scientific burden has shifted from identifying a broad router to showing that a compulsory weak-model prefix sometimes avoids expensive work without making recovery worse.

On a hard local diagnosis, Luna can commit the wrong intervention class, reshape tests around it, and deliver an apparently coherent causal story. Terra then inherits both repair work and an anchor. Restoring workspace bytes does not reset Terra's conversation: the root has already seen the handoff. Consequently, logged `restart` means workspace restart unless a fresh context was actually used; it is not evidence of an uncontaminated raw-Terra trajectory. No fresh-context mechanism is required in this first candidate.

RFC §6 correctly refuses to infer takeover success from raw Terra's success at base. Its checkpoint and complete patch/raw-residual transfer make prefix damage diagnosable. Marking causal claims as hypotheses helps expose the risk but cannot neutralize it. Descriptive continuation/restart logs can reveal wasted work and failure patterns; because Terra selects the option after seeing the failure, those logs cannot estimate the causal benefit of restart. Do not add a restart matrix now. Repeated damaged-prefix failures should trigger the existing kill rule unless a bounded policy can be tested within the existing allowance.

The cost hurdle is strict. In an illustrative equal-success model, let `I` be root intake, `L` the complete Luna attempt, `G` reconciliation overhead, `p` the fraction solved without takeover, and `T` the cost of an otherwise equivalent Terra solve. Expected cascade cost is `I + L + G + (1-p)T`; saving requires `I + L + G < pT`. This is a diagnostic inequality, not a prediction: actual takeover cost and success can differ substantially from raw Terra. A cheap prefix is still wasted expenditure when almost every task needs an equally expensive Terra restart.

The existing H1 evidence establishes that integrated Terra found a full solution while the frozen delegated system did not. It does not establish that Luna-first takeover would recover, or that difficult tasks generally require Terra. The acceptance-critical residual reached the former controller and was accepted anyway; the new controller therefore addresses a real observed mechanism. [H1 results and disposition](https://github.com/YB-Park/over-the-luna/blob/fd39072d66ea82ac3427d8431230967f7d3aa587/docs/PREMIUM_HELDOUT_RESULTS.md).

Stage 2's forced-L/forced-T arms are appropriate first contrasts under the same acceptance policy. Forced L matching at lower cost removes the takeover case; forced T dominating after prefix charges removes the Luna-first case. A useful pattern would be cheap Luna completion on one exposed task and a takeover that fixes a failure forced L retains on another, while avoiding forced-T expense where it is unnecessary. One run per contrast is mechanism screening, not reliable estimation of complementarity across a population.

Integrated Terra with a bounded Luna worker is a plausible simpler product alternative in some runtimes, but it is not necessary to interpret this experiment. Raw Terra and forced T already supply the essential expensive-path benchmarks. Adding another worker topology now spends the final design attempt before testing it. Luna-first remains a falsifiable allocation prior; project identity supplies no evidence that it is optimal. The prior audit's prefix/handoff research remains relevant, but no new broad literature survey is needed for this gate.

## 4. ACCEPTANCE CONTROLLER

The compact register, runtime receipts and one reconciliation function are proportionate to the H1 failure. Their purpose is to preserve recorded obligations, authenticate executable results, and withhold trusted completion on inconsistent records. They should not become a theorem prover, semantic classifier service, or workflow platform.

The following are **paper counterexamples to an implementation using only RFC §11's listed checks**, not observed runtime exploits and not claims that §8 intends to permit these actions:

| Counterexample | Why the listed checks are insufficient | Required boundary |
|---|---|---|
| Capture `U1`, required behavior on supported states X and Y. Later retain ID `U1` but change `SOURCE` to A and `BLOCKING` to no; verify every other row with current receipts. | Every required ID is present; no currently blocking row is unresolved; no waiver is fabricated; receipts/digest can all match. Comparing only the final rows cannot discover the authority change. | Compare model-proposed updates against controller-owned captured authority and obligation content. |
| Keep `SOURCE=U` and `BLOCKING=yes`, but rewrite U1's criterion to cover X only and mark it VERIFIED. | An ID/source/blocking check still preserves the row while losing Y. A test passing on X does not reveal the scope mutation. | Preserve the original criterion content and source anchor; narrower claims are annotations and cannot replace the obligation. |
| Preserve required U1, accept an authentic user event waiving it, set `WAIVED_BY_USER`, and verify all other rows. | WAIVED is absent from the OPEN/FAILED/UNRESOLVED rejection list; the waiver is not fabricated. The list does not explicitly prohibit COMPLETE or full-success credit. | An active waiver of required scope maps to PARTIAL_WITH_USER_WAIVER, never full success. |

These holes are mechanically closable after capture. They do **not** require the controller to determine whether initial extraction from natural language was complete, whether a repository contract really applies, or whether a test covers the criterion. Those remain semantic judgments. Preserve the original request and source anchors so such judgments can be audited without representing them as proven.

For repository-derived R criteria, §§8–9 must have one interpretation: Terra may explain and reconcile an erroneous interpretation, but the original blocking entry and supporting source do not disappear. An evidence-backed invalidation can be recorded as a semantic decision; a bare A reclassification or weaker replacement cannot silently retire the obligation. The controller validates the permitted transition and retained history, not the truth of Terra's explanation.

Receipts similarly prove execution, not relevance. A process exiting zero without collected tests cannot earn a test PASS. Test assets may themselves be weakened, so their recorded identity and the separate evaluator remain necessary. Conservative invalidation after workspace mutation is acceptable for this small experiment; do not implement fine-grained semantic dependency tracking.

Trusted state means state the agent's available edit **and execute** tools cannot overwrite. A sibling directory alone does not demonstrate that property. Preflight can probe the actual permissions without a model. If protected state cannot be provided cheaply, classify the mechanism as compliance logging and withhold the trusted-completion claim; do not treat a model-writable JSON file as a deterministic certificate. This is the existing RFC trust condition, not a demand for a new security runtime.

The missing-stop case needs no always-running watchdog to make an honest completion claim: absence of a valid final controller record must be consumed as `NO_VERIFIED_COMPLETION`. A final record is valid only for its matching run and workspace, not the preceding successful session. User-visible prose remains outside that assurance boundary.

## 5. ECONOMICS / EXPERIMENT IDENTIFIABILITY

The 12 Stage 1 attempts compare the actual product to both baselines; the additional four Stage 2 attempts address fixed-path explanations. Keep all prefix work, root intake, self-repair, correction continuations, discarded patches, failed and blocked runs in cost. Do not subtract controller overhead from the product comparison or erase an expensive failed attempt when reporting a repaired successor.

For stratum weights `w_d`, operationalize the RFC metrics as `mean_cost = sum(w_d * mean(cost in d))`, `success_rate = sum(w_d * mean(full_success in d))`, and `credits_per_full_success = mean_cost / success_rate`. Zero full successes makes the last metric infinite/undefined, never zero. Use the same declared weights and attempted task set for each arm. A full success must satisfy the complete original acceptance oracle and have no unresolved control failure or required-scope waiver. An evaluator pass alone cannot erase a surfaced false completion.

Full-attempt accounting is necessary but insufficient by itself. For example, raw Terra could solve two tasks for 200 total credits, while a cascade solves the cheap task for 10 and abandons the hard task for 1. Both mean cost and credits per success favor the cascade. The RFC's **zero raw-Terra-pass/Premium-fail-or-block veto** correctly rejects that outcome. The equivalent OTL regression guard and the two wins across two repositories prevent capability claims based only on selective abstention. Apply these guards to partial/waived outcomes as well, as required by the waiver correction.

The 75% weighted-mean and cost/full-success gates are defensible predeclared advancement hurdles; they have no established market-optimal or statistically significant status. The premium-heavy 3/8, 3/8, 1/8, 1/8 mixture is explicitly an engineering target. The 60% both-pass ratio is appropriately descriptive/stretch. D3/D4 now require all Premium controls to pass, tighter paired overhead limits, and individual absolute limits. A changed evaluation condition is a comparability problem to document and handle symmetrically, not a candidate-specific excuse after an overrun.

Development cannot establish the fresh-pilot numerical claims. Four exposed tasks and single trajectories can reject a mechanism or justify a small next stage, but cannot calibrate demand, estimate a stable takeover probability, or demonstrate general superiority. The later freeze must fix actual sample counts, weighting/repetition rules and invalid-task handling before sampling; those are promotion-protocol details, not missing components of this implementation hypothesis. No such tasks are selected here.

The budget is a ceiling, not evidence that the full matrix fits. At the 400-credit development maximum, 16 attempts allow 25 credits per attempt on average. The old H1 trio alone consumed **91.378579 credits**, with raw Terra using **71.013030**; these historical values show material headroom risk but are not forecasts for v2.1. [Recorded H1 costs](https://github.com/YB-Park/over-the-luna/blob/fd39072d66ea82ac3427d8431230967f7d3aa587/docs/PREMIUM_HELDOUT_RESULTS.md).

Before separately authorized execution, record the actual remaining allowance and fix the cumulative program cap to the minimum in §22. Deduct subsequent development, pilot and recovery spending from that cap; rereading a balance cannot reset it. An absent owner authorization means no launch. The 400/500/100 buckets remain maxima under the potentially lower total, and cannot borrow automatically. Admission must reserve a declared run ceiling and capture margin within the remaining applicable bucket. If only part of the contrast fits, report the limitation and stop; do not claim complementarity from an unfinished Stage 2. The review does not require spending 1,000 credits or all 16 attempts.

Independent future randomness removes freeze-SHA seed manipulation only after the pool, exclusions, reserve order and sampler are committed. A curator can still bias the pool, and public accepted changes may be memorized. Sealed preflight addresses invalid oracle construction without making accepted material available to model jobs. `NETWORK_EXPOSED` accurately discloses a remaining access limitation; it does not establish contamination-free evaluation. These bounded claims are sufficient at this design gate.

## 6. RUNTIME FEASIBILITY

**No exact installed VS Code version needs to be invented or committed before implementation.** The named Local custom-agent target and separate CLI adapter are sufficient. The unresolved pre-implementation documents are the two controller contracts in §7; version/settings manifests and successful probes are prerequisites to subsequent paid execution.

Focused official-document checks on 2026-09-09 support feasibility without demonstrating this candidate. VS Code documents custom subagent model/tool overrides, a parent cost-tier restriction, and stateless child invocations. That supports Terra root with one Luna child and no follow-up Builder invocation. It also means configured model names alone are insufficient evidence that the intended child actually ran. [VS Code subagents](https://code.visualstudio.com/docs/agents/run/subagents).

VS Code documents Stop/SubagentStop, a continuation indicator, and credit-consuming continuations when Stop blocks. A Stop event is not proof that a session is inactive. These support bounded reconciliation but do not prove background-writer quiescence or suppress all completion prose. [VS Code hooks reference](https://code.visualstudio.com/docs/agents/reference/hooks-reference).

Hook diagnostics can show loaded hooks and configuration errors; hooks consume structured event input. Agent-scoped hooks require an enabled setting and remain preview functionality. These provide configuration and protocol checks, not an observed end-to-end model run. [VS Code hook configuration and diagnostics](https://code.visualstudio.com/docs/agent-customization/hooks).

Distinguish the following evidence in the future preflight:

| Check | What zero-AI can establish | What must not be claimed from it |
|---|---|---|
| Host, extension, model configuration and permissions | Exact installed/configured versions, documented cost-tier rule, enabled tools, hook loading, relevant settings | Actual backend model identity, model compliance or successful live delegation |
| Controller and event adapters | Deterministic results for fixture events; correct host-specific input/output shapes; missing/malformed/timeout handling | That an LLM-triggered event occurred on the installed host |
| State protection and ownership | Harmless permission probes; checkpoint/digest capture; synthetic background-writer handling in the chosen sandbox | Atomic isolation or quiescence of writers the runtime cannot observe |
| Full session trace | Nothing about a session that has not run | “Observed Terra→Luna→Terra” based only on configuration or fabricated fixtures |

Read §2's preflight fields as evidence-labeled records, including `NOT_OBSERVED` where necessary. Do not invoke a model to satisfy a nominally zero-AI preflight. If an installed-runtime property cannot be demonstrated without one, retain the RFC's weaker claim or stop; never record a synthetic pass as live validation. Actual model identity, tool use and handoff compliance must be checked in the first separately authorized development attempt and counted within the existing attempt/credit limits. No additional paid smoke campaign is implied.

The exact zero-AI fixtures needed to exercise the RFC's existing gate include criterion deletion/reclassification/content replacement; valid and forged user waivers; stale or wrong-run receipts; skipped/empty collection; malformed or unknown dispositions; current contradictory results; workspace/test-asset mutation; missing/timeout/disabled finalization; one correction followed by continued invalidity; and transfer while an observable writer remains active. Include preservation of pre-existing user edits when restoring the agent-owned checkpoint. These are tests of the promised record/ownership boundary, not hidden semantic acceptance tests.

The minimum plausible implementation remains two agent roles, a compact state store and reconciler, execution-receipt capture, and host-specific lifecycle/tool adapters. Direct Terra repository work before Luna can remain a measured prompt-compliance rule if cheap structural gating is unavailable. Model judgment about relevance, R-contract interpretation and takeover eligibility can likewise remain explicit and logged. Identity/authority preservation, waiver provenance and outcome mapping, receipt freshness, correction count, and absence-of-final-record handling must be deterministic. A CLI result cannot silently certify the Local adapter.

## 7. BLOCKING CHANGES, IF ANY

**Exactly two. Both concern the existing acceptance controller.**

| Change | Smallest required specification amendment | Closure condition |
|---|---|---|
| **B1 — bind obligations across updates** | Specify a controller-owned captured record for each required criterion: ID, original source/anchor, original criterion content and required/blocking status. Models submit annotations or explicit transitions; they cannot overwrite the authority-bearing record. Only an authenticated user revision can narrow explicit U scope. Retain R obligations and record any evidence-backed Terra reconciliation without silent deletion/reclassification. Resolve §§8–9's downgrade language accordingly. | A fixture retaining an ID while changing U→A, blocking→nonblocking, or X-and-Y→X cannot produce COMPLETE. Legitimate evidence/status updates still work. This checks preservation after capture, not semantic completeness of capture. |
| **B2 — make partial outcomes unambiguous** | State that COMPLETE requires every still-required criterion VERIFIED and no active waiver of required scope. If all remaining obligations are verified and at least one required obligation has a valid waiver, emit PARTIAL_WITH_USER_WAIVER. Remaining unresolved failures cannot be masked by a waiver elsewhere. Explicitly exclude the partial outcome from full-success counts and treat it as non-full-success in comparator vetoes. | A genuine user-waiver fixture produces PARTIAL and zero full-success credit, even if executable receipts or the hidden oracle pass. Forged waiver rejects. A waiver on one row does not clear an unrelated OPEN/FAILED row. |

The original user request remains the reference scope in unattended comparisons; those runs have no fabricated interactive waiver path. An actual later user revision may change an interactive mission, but must retain provenance and cannot retroactively change an experiment's scored contract.

These are normative specification changes, not requests for a particular database, cryptographic signature system, extra agent, or semantic proof engine. Existing §14 zero-AI tests should cover their concrete counterexamples. No other architecture change is blocking this review.

## 8. APPROVED MINIMUM IMPLEMENTATION, IF ANY

**None at this gate.** The current verdict is revision before implementation. Section 6 bounds the feasibility assessment; it is not implementation authorization or a list of files to write now.

After B1/B2 closure, the next gate should consider only the already specified Terra root, single Luna leaf, one takeover, small controller and bounded development plan. Approval would still require separate owner approval for paid development, and would not authorize future holdout selection or promotion automatically.

## 9. EARLIEST KILL SIGNALS

| Earliest point | Signal | Decision |
|---|---|---|
| Before paid execution | A zero-AI authority/waiver/stale-state fixture earns trusted COMPLETE | Block paid testing. Correct the small controller; if that requires a substantial new runtime, stop this candidate. |
| First live development trace | Wrong model/tool surface, missing trusted state/finalization evidence, or an unobservable ownership guarantee represented as enforced | Mark runtime/compliance failure and stop further launches until resolved within scope. Do not score it as a product success. |
| Stage 1 | No plausible complete-task quality/cost point versus OTL/raw Terra; or substantial Terra pre-solving on at least two tasks | Apply the RFC's development kill rather than tuning a broad router. |
| Stage 2 | Forced L matches for less, or forced T/raw Terra dominates after full prefix charges | Reject the tested cascade mechanism. Descriptive handoff explanations do not override the contrast. |
| Any transfer | Repeated prefix damage with no viable bounded restart | Stop the candidate; do not hide wasted prefixes or call workspace restoration a clean-context reset. |
| Budget/program boundary | A bucket cannot fund the needed remaining contrast; or competent v2.1 evaluation fails to produce a useful point | Stop/inconclusive for budget exhaustion; end bespoke Premium research by default after a competent second-design failure. No automatic v3/v4. |

The three most likely implementation drifts are: retaining IDs while changing their meaning; treating any zero-exit/valid-waiver/end-of-turn as completion; and allowing Terra to solve before Luna while still labeling the run a compliant cascade. They directly threaten the question this experiment is meant to answer.

## 10. NEXT ACTION

1. Amend only the v2.1 authority/update and terminal-success contracts to close B1 and B2; preserve the minimal topology, budget and stop rules.
2. Recheck those two amendments and their explicit zero-AI acceptance cases. If closed, consider a minimal implementation authorization without reopening architecture brainstorming.
3. Only after that gate, perform implementation/preflight; launch bounded development only with separate owner approval and a recorded affordable run manifest. Do not select promotion holdouts at this stage.

## 11. UNCERTAINTY

**HIGH confidence concerns the two underspecified controller boundaries and the limited scope of the required correction.** The RFC's general U-preservation rule may lead a careful implementer to add B1 already, and the partial-outcome name may suggest B2. This review does not claim that every conforming interpretation necessarily fails. It rejects leaving those interpretation choices open in the exact mechanism intended to prevent silent acceptance laundering.

Confidence in eventual product value is substantially lower. No v2.1 agent/controller has been implemented or observed here; the installed primary runtime, actual remaining credits, model routing, quiescence coverage and controller overhead are unverified. The small exposed-task matrix can yield useful rejection evidence, not population reliability or optimal routing estimates.

The approval threshold should remain proportionate: plausible primitives, precise recorded-state obligations, honest limits, and a finite identifying experiment. It should not demand proof of semantic correctness or a perfect sandbox. The requested corrections meet that threshold without expanding this into a third large design cycle.
