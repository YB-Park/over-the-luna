# Astra Independent Premium v2 Design Audit

## 1. EXECUTIVE VERDICT

**REVISE_BEFORE_IMPLEMENTATION**

**Confidence: HIGH.** This is confidence that the present specification needs revision, not high confidence that Premium will fail. Do not implement the full adaptive L/T/M proposal yet. Retain a narrow, falsifiable premium hypothesis and test the smallest control-and-escalation mechanism only after the design gaps below are resolved.

V2 correctly abandons a tool-blind executive and mandatory Auditor. It does not yet establish how its replacement makes better decisions. It combines three unvalidated policies—execution routing, assurance routing, and acceptance classification—inside the same Terra context. That context can choose the work, define what counts as blocking, select the evidence, mark it verified, and approve itself. A structured ledger can make that failure legible without preventing it.

The main blockers are:

1. **Acceptance enforcement has no defined trust boundary.** The RFC acknowledges prompt-level enforcement, but elsewhere says blocking uncertainty cannot silently pass. Those are different claims. Existing hooks make a small deterministic reconciliation mechanism plausible; they do not prove criterion completeness, test relevance, or unforgeable completion.
2. **L/T/M is a policy space, not an executable routing policy.** “Needs an integrated local loop” often becomes knowable only after paying for that loop. Switching also changes the workspace, context, cache, and remaining budget. Four exposed development cases cannot identify an unconstrained switching policy plus optional verification.
3. **Runtime feasibility is underspecified.** The current VS Code documentation retains the parent cost-tier restriction, but also distinguishes Local and Copilot harnesses, stateless subagents, client-specific hooks, and different tool controls. “VS Code/Copilot” is not one tested runtime. Dynamic lane names do not dynamically revoke tools.
4. **The proposed product gate can reward selective failure.** Cost conditioned on both arms passing omits precisely the tasks where Premium fails and Terra succeeds. Two capability wins, ambiguous denominators, and medians without a declared mixture cannot establish the intended frontier.
5. **The holdout seed is manipulable.** A designer-controlled freeze SHA is reproducible, not unpredictable. Commit metadata can change the sample without changing the candidate's behavior. Pool curation and exclusions can dominate the seed anyway.

**MINIMAL CANDIDATE YOU WOULD TEST FIRST:** a Terra-rooted, Luna-first, one-way cascade with one continuous Luna Builder attempt, at most one Terra takeover, no Lane M, no Verifier, and a bounded, runtime-observed completion receipt. Terra starts as the paid entry point because of the currently documented platform restriction—not because premium intake is inherently valuable. Sections 5, 6, and 9 specify this candidate and how to kill it. Nothing in this report authorizes implementation or spending.

Audit date: **2026-09-09 UTC**. Reviewed branch head: `464a05fc16d35ba4154197cdb6581dc69674ef3d`; proposed RFC commit: `97cc22962e3bf810b76bf8d5ef4c9fe509a542c5`; prior audit: `79f3c4d34beb1383fa55fae180c999aa23770d64`. Repository citations refer to those snapshots. The [v2 RFC](https://github.com/YB-Park/over-the-luna/blob/97cc22962e3bf810b76bf8d5ef4c9fe509a542c5/docs/PREMIUM_V2_PRE_IMPLEMENTATION_RFC.md) is the object of review, not the authority for these conclusions.

## 2. WHAT V2 GETS RIGHT

The narrower claim is materially better. One substantial repository mission is a plausible unit of evaluation; multi-day resumption is explicitly excluded. The [updated disposition](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/PREMIUM_HELDOUT_RESULTS.md) preserves H1 and stops v1 instead of tuning through the holdout. Previously exposed tasks are correctly relegated to development.

V2 also identifies the right H1 lesson: the SSL-like limitation reached Terra and Auditor, so fixing context compression alone is insufficient. Making residual handling independent of its origin closes a real conceptual loophole. Letting Terra inspect and intervene locally removes an unnecessary capability prohibition. Neither implies that Terra will use evidence well; both make a useful intervention possible.

Optional assurance, a single active mutation owner, and event boundaries are defensible defaults. Removing the global Verifier PASS reduces one misleading authority signal. The separate-runner evaluator directly addresses known exposure routes. Proposed numerical gates are preferable to an unrestricted narrative about impressive wins, even though their current construction needs repair.

The strongest economic case remains conditional: many tasks contain cheap work, while a smaller subset contains expensive-to-miss errors that a stronger model can actually resolve. A simple product can hide model allocation without hiding completion status or spend. Recent routing and handoff research supports that possibility, but not any particular L/T/M policy. The strongest favorable evidence includes live routing experiments in TwinRouterBench and direction-dependent benefits in The Handoff Tax; both require more qualification than a headline cost reduction [S9](https://arxiv.org/html/2605.18859v1), [S12](https://arxiv.org/html/2608.24358v1).

## 3. WHAT V2 STILL GETS WRONG

### It replaces one control problem with several interacting ones

The router must infer uncertainty location, intervention value, recoverability, and cost. The assurance selector must infer whether another context can discover a missed defect. The ledger owner must infer acceptance completeness and whether evidence justifies each status. All three can share the original wrong interpretation. Labeling the decisions separately does not make their errors independent.

The RFC's claim that Lane T's existence is “required by H1” is too strong. H1 establishes a useful successful integrated Terra trajectory and a failed split trajectory. It does not isolate direct tools, model capability, prompt differences, effort, or sampling as the cause. Lane T deserves a controlled comparison; its superiority is not already established. The [prior audit](https://github.com/YB-Park/over-the-luna/blob/79f3c4d34beb1383fa55fae180c999aa23770d64/docs/ASTRA_PREMIUM_AUDIT.md) explicitly kept that causal uncertainty open.

The revision also risks optimizing a proxy: fewer false claims can be achieved by reporting every difficult task BLOCKED. That may improve calibration while delivering no additional completed work. Conversely, turning every uncertain detail into a blocking row can consume the entire mission budget. Completion, false completion, abstention, and needless escalation must be measured separately.

### The experiment is being asked to identify too much

Three lanes, four assurance levels, several switch directions, mutable ownership, evidence schemas, and repair rules create many candidate policies. Testing “full v2 versus no Verifier” does not disentangle them. An optional Verifier that happens not to run yields a vacuous ablation. A forced-L arm changes both selection and the possibility of rescue. There is no proposed forced-M comparison that establishes mixed mission value.

The known development record is especially narrow: H1 is heavily exposed; httpcore supplied repeated causal lessons; Django supplied a positive lifecycle example. Their [regression results](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/PREMIUM_HARNESS_RESULTS.md) are useful failure fixtures, not a routing calibration population. A design that learns “socket problem → Terra” or “Django lifecycle → M” would pass those cases while missing the intended mechanism.

Finally, an always-Terra root may be a reasonable compatibility choice but remains a tax on every easy request. The root's identity is not itself a cost metric: a tiny Terra intake could be cheap. Equally, one “small” executive call can be large after a long user history, repository instructions, and tool schemas are included. Measure actual entry and finalization cost, not just root tool count.

## 4. ADAPTIVE ROUTING REVIEW

### L, T, and M are distinguishable only with operational definitions

| Lane | What actually distinguishes it | Observable evidence that could justify it | Main failure and feasibility limit |
|---|---|---|---|
| L | One uninterrupted Luna mutation trajectory; Terra handles intake/finalization | Executable contract plus no unresolved consequential contradiction after a bounded attempt | Absence of a reported uncertainty is not evidence that Luna is adequate; Terra still pays fixed overhead |
| T | Terra owns a continuous read–run–edit–validate trajectory | A failed discriminating check, contradictory supported-state evidence, or an unresolved local decision with a concrete consequence | Terra may explore indefinitely; it can also inherit a poisoned partial patch |
| M | At least two coherent work packets, with an inter-packet dependency and a Terra decision affecting later work | A documented invariant crossing packet boundaries and a decision that cannot be settled within one Builder trajectory | Otherwise it is L with extra calls, or v1 renamed; fresh Builder contexts lose local continuity |

Do not define M by file count, elapsed time, or the appearance of a ledger. A single Builder can implement a cross-subsystem feature. M must beat that continuous trajectory. If Terra merely forwards summaries and approves packets, mission ownership has not earned a distinct lane.

Routing is not necessarily as hard as solving: a reproducible test failure can be easy to observe. But the important prediction is **whether another trajectory will fix it at acceptable total cost**, not whether the task looks difficult. Both tiers can fail; a platform outage does not need a stronger model. Prompt-only semantic categories offer no calibrated probabilities for these events.

The event vocabulary also needs a transition rule. Most blocking criteria start UNVERIFIED, so “any BLOCKING criterion becomes UNVERIFIED” cannot indiscriminately trigger premium intervention at intake. Distinguish an initial open obligation from evidence invalidated after a mutation or a newly discovered contradiction. A synchronous Builder's internal event does not reach Terra until the child returns unless a supported runtime event channel delivers it. Require an immediate bounded handback for a global contradiction; do not describe an unobserved child condition as live executive supervision.

SWE-Router makes the information problem explicit, but its learned value function and continuation-or-restart policy are not a free Terra self-assessment [S8](https://arxiv.org/html/2607.00053v1). Agent-as-a-Router uses experience and performance statistics, unlike this cold-start four-case design [S11](https://arxiv.org/html/2606.22902v3). Conversely, Scrouting's cheapest-fixer-plus-handoff ablation ties its routed system: useful evidence preparation can be mistaken for router value [S10](https://arxiv.org/html/2608.04804v1).

### Switching is an intervention, not relabeling

Before a switch, the receiver needs the original contract, exact workspace identity, outstanding criterion IDs, the counterexample and raw outcome, changed paths, running-process state, and a separation between observations and the outgoing model's hypotheses. It must also know whether to continue the partial patch, revert only agent-owned changes to a checkpoint, or restart in a fresh disposable workspace. None permits discarding a user's pre-existing work.

The handoff interface is directional. The Handoff Tax reports that reducing cheap-model trajectory information helps escalation, whereas expensive-model context can help a cheap successor. Its study includes Luna/Sol, not Luna/Terra, and fixed rather than learned switch times [S12](https://arxiv.org/html/2608.24358v1). That argues against the RFC's single generic evidence packet being assumed sufficient for every switch direction. It also argues against automatically discarding all prior reasoning.

Reject post-hoc claims such as “Terra would have solved from this point because raw Terra passed from the base.” A live continuation sees a different state. The Replay Gap gives a controlled demonstration of that error, although its low-success small-model regime limits quantitative transfer [S13](https://arxiv.org/html/2608.08239v1). Full runs can estimate a policy's observed outcome; selective live branches are needed to investigate a particular switch.

### First policy: one decision after useful work

For the minimal candidate, remove pre-task L/T/M prediction. Start with one Luna Builder attempt and a completion check. Permit **one monotone L → T takeover** if a surfaced blocking condition is unresolved after at most one local repair. A deterministic schema/check failure triggers reconciliation; semantic ambiguity still requires judgment. Infrastructure-only failure ends BLOCKED/INFRA rather than automatically buying Terra. After takeover, Terra finishes or stops; there is no T → L or M loop.

This policy deliberately sacrifices some ideal early-T routing to reduce policy complexity. It can waste a Luna prefix on tasks that Terra should own immediately. That is its principal kill condition, not a flaw to hide. Compare it to forced integrated Terra and unchanged raw Terra. Permit no task-name exceptions derived from H1/httpcore/Django.

A learned or external router may eventually outperform this rule. Four exposed cases cannot train it. A deterministic rule is inspectable, not magically accurate; self-reported “low uncertainty” is not an objective signal merely because software branches on it. Hidden routing is acceptable UX only if users can see cost, blockers, and the actual outcome. Fewer model questions do not justify concealment of unresolved product decisions.

## 5. ACCEPTANCE CONTROL REVIEW

### A ledger cannot validate its own meaning

The proposed ledger improves visibility. Its essential adversarial tests are not whether all fields exist, but whether the system can exploit their semantics:

| Attack | How a well-formatted ledger still fails | Required response |
|---|---|---|
| Criterion omission | Never create a row for an acceptance-critical supported state | Preserve user requirements and link derived criteria to source; separately audit coverage |
| Severity laundering | Reclassify a difficult BLOCKING item as NON_BLOCKING | Record changes; no silent downgrade or deletion of a user-fixed requirement |
| Scope laundering | Mark “ordinary sockets” verified while the criterion covers supported sockets | Evidence must name the validated state set and exclusions |
| Evidence laundering | Successful unrelated tests become evidence for a new semantic claim | Runtime result proves execution, not relevance; relevance remains an explicit reviewed judgment |
| Stale evidence | Validate revision R, then change a dependency at R+1 | Invalidate affected claims; conservative full invalidation is acceptable initially |
| Vacuous checks | A test is skipped, never collected, or weakened by the agent | Record collection, assertion outcome, test bytes, and changes to validation assets |
| Fabricated waiver | Terra writes USER_ACCEPTED_RESIDUAL without a user act | Only an authenticated user decision can create that state |
| Shutdown confusion | A timeout or hook escape ends the turn and looks like success | Session termination is separate from verified completion |

H1 can recur with every ledger row present. Terra could classify SSL-like behavior as unsupported and nonblocking, or claim that preserving readiness behavior verifies compatibility. The ledger does not supply the missing judgment. More required fields can also encourage boilerplate that hides the one meaningful exception.

The acceptance authority must be ordered: explicit user requirements first; established repository/public compatibility contracts second; agent-derived assumptions last, visibly marked as assumptions. For an underspecified request, use conservative existing behavior where defensible. A consequential unresolved choice becomes a targeted question in an interactive session or BLOCKED in unattended mode. Do not invent a requirement merely to justify a costly lane.

`USER_ACCEPTED_RESIDUAL` is not ordinary unattended completion. Rename the terminal outcome **PARTIAL_WITH_USER_WAIVER** and exclude it from full hidden-oracle success. Existing explicit authorization can cover the exact residual; general “be autonomous” or “use Premium” does not waive missing functionality. The original requested scope must remain visible in the record.

### Smallest viable control mechanism

Use a compact **criterion register plus execution receipts**, not the entire proposed eleven-field row repeated every turn. Each row needs an ID, sourced criterion, blocking status, current disposition, validated states/exclusions, and a reference to evidence at a workspace revision. Store detailed logs once; transfer changed rows and consequential excerpts. Every outstanding blocking row remains visible even if a soft context budget is exceeded.

The deterministic part should check only what it can establish:

1. Required criterion IDs exist and have not been silently dropped or downgraded.
2. A claimed executable check has a runtime-recorded command/test identity, collected-result classification, and pre/post workspace identity; model prose is not a receipt.
3. Evidence matches the current revision. Initially invalidate all executable claims after semantic mutation; selective dependency invalidation is a later optimization.
4. No unresolved blocking row or contradictory receipt permits the machine outcome COMPLETE. User waivers require a user event and yield a distinct partial outcome.
5. Missing hook, malformed state, timeout, process crash, or exhausted reconciliation produces NO_VERIFIED_COMPLETION. It does not manufacture a receipt from the final prose.

This can enforce consistency of the recorded claim, not completeness or semantic correctness of the criteria. A hash proves identity, not adequacy. The state digest must cover the relevant working tree—including new/deleted files and executable modes—not just HEAD or `git diff`; test definitions and environment identity need their own linkage. Exclude the ledger/log files from the code digest to avoid self-invalidation. A test that modifies relevant code invalidates its own pre-check receipt unless the final state is explicitly revalidated.

### Hooks make this plausible, not automatic

Current VS Code supports `PreToolUse` decisions and blocking `Stop`/`SubagentStop` hooks; stop blocking spends additional model turns [S2](https://code.visualstudio.com/docs/agents/reference/hooks-reference). Plugins can bundle hooks, so a narrow completion check does not inherently require a new orchestration service, although hook packaging is client-specific [S4](https://code.visualstudio.com/docs/agent-customization/agent-plugins). Agent-scoped hooks require an explicit setting, and enterprise policy can disable hooks [S3](https://code.visualstudio.com/docs/agent-customization/hooks), [S6](https://code.visualstudio.com/docs/enterprise/ai-settings). These are installation prerequisites to verify, not settings to bypass.

The CLI reference documents blocking `agentStop`, an eight-consecutive-block escape, and fail-open command-hook timeouts. Root final output cannot be replaced through the subagent-only `modifiedResponse` field [S5](https://docs.github.com/en/copilot/reference/hooks-reference). Thus **a stop hook alone cannot guarantee that users never see a false completion sentence**. It can request correction and record nonacceptance. A product claiming a hard guarantee needs a trusted visible result/patch-acceptance channel outside model prose; otherwise claim only measured reduction in false completion.

For the first experiment, allow at most **one correction continuation**. If still invalid, retain a failed completion receipt and classify the attempt as incomplete in controller accounting. Do not loop until the model fills the fields. A separate process deadline must bound continued execution; do not assume the hook can rewrite a misleading final sentence. Test the missing-hook, timeout, and stop-limit paths with scripted events before any paid model work. The evaluator can enforce acceptance of a result independently, but that does not retroactively make the agent's user-facing claim truthful.

The proposed minimal mechanism targets accidental omission and stale claims. If shell tools can overwrite the checker, receipts, or user-waiver record, it is not tamper-resistant. Protect trusted control assets outside the editable workspace where the runtime supports that separation. If this cannot be established in the chosen VS Code target without a large extension, narrow the product claim; do not quietly turn the project into a security runtime.

## 6. TERRA TOOL / MUTATION-OWNERSHIP REVIEW

### Always Terra root is a compatibility choice

The current VS Code subagent documentation still says a requested child model cannot exceed the parent's cost tier. It also documents stateless invocations rather than follow-up to the same child [S1](https://code.visualstudio.com/docs/agents/run/subagents). This supports a Terra entry point for automatic Luna/Terra composition in that documented path. It does not establish that every Copilot harness has identical restrictions, or that a Luna-root product with explicit user handoff is inherently inferior.

Specify one primary target: **VS Code Local custom-agent execution**, with a pinned tested VS Code/Copilot version and named required settings. Treat Copilot CLI as an evaluation adapter until parity is demonstrated. The current harness documentation distinguishes Local, Copilot Agent Host, and cloud execution; switching targets is a handoff, not proof of an autonomous model-switch API [S7](https://code.visualstudio.com/docs/agents/run/agent-harnesses). No runtime smoke was performed in this audit.

| Design choice | Feasible interpretation | What is not established |
|---|---|---|
| Terra root with direct tools and Luna Builder | Explicit tool surfaces plus serialized calls; direct diagnosis becomes possible | Availability of tools does not ensure bounded use |
| Terra root as router only; integrated Terra child | Static narrower root, separate full-tool worker | Adds another expensive context and handoff; root still must reconcile completion |
| Lane-dependent tools in one agent | Hook-mediated decisions may deny calls based on trusted state | No documented generic lane flag that atomically changes frontmatter permissions |
| Luna parent → premium child | Blocked in the documented higher-cost subagent path | Do not assume a custom-agent name evades model policy |
| Explicit human handoff | Legitimate product alternative with a visible escalation boundary | Violates the RFC's zero internal model-choice UX if required mid-task |
| External policy/controller | Can own calls and state if implemented on a supported API | A separate product/runtime with maintenance and billing costs |

Terra's tool access recovers the opportunity for integrated reasoning; it also makes the cost boundary primarily behavioral. Instructions such as “avoid mechanical loops” are not a resource ceiling. Separate static agents can enforce clearer tool surfaces, but general shell access remains broad. A hook that recognizes edit tools yet permits arbitrary shell cannot establish read-only behavior.

### Mutation transfer must account for processes, not names

An owner flag in model text is insufficient. A Builder can return while a formatter, test subprocess, file watcher, or background shell remains active. Terra and a human editor can then write concurrently. Read-only verification may also mutate generated assets, caches, or fixtures.

Require a serialized transition: stop new writer actions; wait for or terminate agent-owned background writers; capture state; validate the expected workspace identity; then grant the next owner. A changed workspace invalidates the transfer and its evidence. In an experiment, use disposable isolated workspaces and a runner-owned process boundary. In the interactive product, detect user edits and reconcile them rather than reverting them.

Do not initially build per-file locks or concurrent mutation branches. No claim of atomic ownership should be made until active-agent identity and shell descendants can actually be observed in the selected runtime. If they cannot, retain synchronous single-child execution, prohibit background mutation behavior, and report the remaining boundary as measured compliance.

### MINIMAL CANDIDATE YOU WOULD TEST FIRST

| Element | Proposed minimum and reason it might earn cost |
|---|---|
| Root | GPT-5.6 Terra; handles initial contract, one takeover decision, and final reconciliation; justified provisionally by platform eligibility |
| Root tools | Read/search/edit/execute plus the named Builder invocation; no external mutation tools in the experiment; direct mutation used only after ownership transfer |
| Leaf | One GPT-5.6 Luna Builder with read/search/edit/execute, no delegation; owns a continuous local attempt and at most one ordinary repair |
| Mutation owner | Luna during its synchronous attempt, then NONE during quiescence, optionally Terra until termination; never back to Luna |
| Completion | Runtime-linked criterion/check receipts; COMPLETE, BLOCKED, FAILED, and PARTIAL_WITH_USER_WAIVER remain distinct; hidden evaluator remains independent |
| Escalation | One L → T transition on unresolved acceptance-critical evidence after the bounded attempt; infrastructure-only failures stop; no semantic D1/D2 task-label router |
| Handoff | Original contract, current patch, raw discriminating evidence and residuals; outgoing causal claims explicitly unverified; Terra may discard only agent-owned changes using a checkpoint |
| Excluded components | No M, Architect, Verifier, recursive delegation, automatic cross-family review, or repeated up/down switching |
| Kill ablation | Forced L matches outcomes at lower cost, or forced T/raw Terra consistently beats the cascade after charging the Luna prefix; failed completion reconciliation also kills it |

The root's pre-Builder orientation must be bounded in the design: only acceptance clarification and directly supplied anchors, not broad diagnostic scouting. Fix that policy before the first run. A parent that solves the task before delegating has already collapsed to T, regardless of its lane label. Actual effort and root/leaf usage must be logged; the v1 medium-root/high-leaf mismatch must not be concealed.

## 7. VERIFICATION / ASSURANCE REVIEW

**Omit Verifier from the first candidate.** This is a complexity and identifiability decision, not a finding that Luna cannot verify. The earlier Auditor ran a useful pending-push check and still missed the relevant fallback. Renaming it cannot establish incremental defect detection.

A same-model second context can help when it receives a different evidence task: construct a counterexample for one supported state using a fixed artifact, without the implementer's causal defense. It is less useful when it repeats the same passing suite or accepts the same narrowed criterion. Terra inspecting Luna's output is different-model adjudication but also shares the mission framing and selected evidence. Neither is independent merely by role or model label. TeamBench's verifier result is conditional on its task distribution and available verdicts, not a Luna failure-rate estimate [S15](https://arxiv.org/html/2605.07073v1).

The relevant ablation holds the pre-verification patch and criterion register fixed. Compare a bounded Luna evidence collector with the mutation owner spending the **same incremental credit allowance** on the same unresolved criterion. Resolve both outputs through the same completion policy. Score executable critical counterexamples found, false allegations, changes to the final patch, regression introduced by repair, final correctness, and all added credits/time. Merely reporting more findings is not a win.

Use both defective and correct development snapshots. Otherwise an always-reject verifier looks excellent. Counterexamples must reproduce against the frozen input and cease after a legitimate repair; accepted patch shape is not the oracle. Score detection separately from successful repair. A changed final outcome may be caused by extra compute rather than context isolation.

Automatic Sonnet is not justified by the word diversity. A future cross-family arm needs one declared hypothesis—such as catching state/lifecycle counterexamples missed by Luna at equal added spend—and the same false-repair test. Until cheaper verification demonstrates value or a clear correlated failure survives, omit the extra provider integration. Current human-selected Premium Review remains a separate stable product feature.

## 8. PRODUCT DISTRIBUTION AND THRESHOLDS

### Define a narrow market of tasks, not a universal agent

Recommended initial scope: one issue-to-patch mission in a supported repository, with reproducible local dependencies and executable acceptance. Include diagnosis, implementation, tests, and required documentation. Exclude deployment, arbitrary external side effects, multi-day resumption, and autonomous product discovery. Do not claim multi-language or visual-UI reliability from an all-Python backend sample.

D1–D4 are useful sampling strata, not a measured demand distribution. D1 and D2 overlap: a lifecycle bug can involve both local diagnosis and integration. Assign one primary stratum using a written rubric before model outcomes. D3 must mean substantial routine work with repeated changes, not simply an easy task whose model used many tokens. D4 should expose fixed overhead.

For a deliberately premium-heavy pilot, predeclare **D1 37.5%, D2 37.5%, D3 12.5%, D4 12.5%** as the target mixture. These are proposed decision weights, not observed user demand. Sample two tasks per stratum for eight total, then weight results by the declared mixture. If the intended product is mostly ordinary edits, choose a different mixture before sampling; the economics may reverse.

Missing workloads include ambiguous requirements, dependency/environment recovery, testless changes, visual behavior, and user interruption. Initially document them as excluded or evaluate them later. D2 is the most plausible M niche only where packet boundaries and integration feedback actually help; it is not automatically the best commercial niche. Keep long-horizon/resumption claims excluded.

### Repair the gate before choosing numbers

Define full success as all predeclared blocking acceptance behavior satisfied, with no material scope or compatibility violation. BLOCKED and user-waived residuals are not successes. Define false-complete both as a failed task claimed complete and as an explicitly surfaced blocking exception waved through, even if an incomplete oracle misses it. Report counts over **all attempts** and also the conditional error rate among completion claims. This prevents both denominator manipulation and strategic abstention.

The following numbers are **proposed advancement gates for a small engineering pilot**, not confidence-certified population guarantees or permission to ship:

| Dimension | Recommended predeclared gate | Why / treatment of the RFC proposal |
|---|---|---|
| Known-residual control | **0** surfaced blocking exceptions followed by an unqualified COMPLETE, across development and fresh runs | Candidate veto after adjudicating criterion relevance; never excuse one because OTL also failed |
| Hidden false-complete | **0** adjudicated acceptance-critical false-completes in the fresh pilot | Stronger than “no worse than OTL”; one event blocks advancement, not the whole Premium hypothesis forever |
| Capability versus OTL | At least **2 distinct D1/D2 task wins**, across at least **2 repositories**, and **0 OTL-pass/Premium-fail-or-block tasks** in the eight-task screen | Keep the directional two-win gate; do not count repetitions of one task as two wins |
| Capability versus raw Terra | **0 raw-Terra-pass/Premium-fail-or-block tasks** in the pilot | A conservative small-sample guard against hiding failure behind price; larger future studies may use a justified non-inferiority margin |
| Complete-attempt economics | Weighted mean credits **<=75% of raw Terra**, and weighted credits per full success **<=75% of raw Terra** | Include failures, retries, receipts, all leaves, and takeover; neither ratio is defined as a win when its success denominator is zero |
| Both-pass cost ratio | Report paired median Premium/Terra; **60% is a stretch target, not an independent promotion gate** | Removes survivorship as the primary criterion; a paired ratio is not a ratio of unrelated medians |
| Straightforward overhead | All four D3/D4 tasks pass; paired median credit ratio **<=2.0x OTL**, median time ratio **<=1.5x OTL** | Tighter provisional usability target than 2.5x/2.0x; the exact values remain owner preferences |
| Control tail guard | No D3/D4 task exceeds OTL by **5 credits or 60 seconds** | Absolute increments prevent tiny baselines from making a ratio the only story; a genuinely changed requirement needs a new evaluation condition, not an exception for one arm |
| Difficult-task latency | Paired median Premium/Terra time **<=1.5x** on D1/D2; all attempts share a **15-minute** wall ceiling | Credit savings do not excuse unbounded waiting; timeouts remain failures/blocks, not missing data |
| Runaway credits | **100 credits per complete arm attempt**, plus the global research cap in section 12 | Ceiling is protection, not a target or a guarantee against in-flight overshoot |

The RFC's allowance for >100% of raw-Terra spend when Premium achieves “broader scope” should be removed from a fixed-scope comparison. Unrequested scope expansion is not a success premium. If broader scope matters, define it for all arms before execution as another task.

Why not simply accept two wins and low median cost? Consider an illustrative eight-task sample: OTL solves 4, Terra 8, Premium 6. Premium cheaply solves the shared easy tasks, wins two over OTL, and fails two Terra-only tasks. The RFC's both-pass median can look excellent while Premium gives up the expensive capability. The proposed full-attempt accounting and Terra-regression gate expose that tradeoff.

Also compare against **blind traffic mixing** of unchanged OTL and raw Terra, which needs no intelligent router. For mixture probability q, expected cost and success are the corresponding weighted averages of the two baselines. Plot or tabulate the candidate against that line using all task outcomes. A point no better than a random mix has not demonstrated routing value. With this small sample the line is descriptive and noisy, not a significance test.

Use monetary loss only as a sensitivity analysis: `J = credits + lambda * seconds + L_fail * unresolved + L_false * false_complete`. Fix any decision weights before runs; absent actual user preferences, report break-even values instead of inventing a dollar value for a correctness failure. One Copilot credit is $0.01, so five credits is five cents [S20](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing). The likely scarce resource is engineering attention and wait time as much as billed inference.

With zero events in eight independent trials, the one-sided 95% binomial upper bound is approximately **31%**. With twelve it is about **22%**. Roughly **59** independent zero-event trials would be needed to put that bound below 5%. Correlated repository tasks weaken the interpretation further. Therefore zero observed false-completes is a useful veto screen, not a demonstrated low production rate.

## 9. DEVELOPMENT ABLATION PLAN

Do not run this plan during the audit. After a revised RFC is separately authorized, use a staged design with **at most 24 paid development attempts**, subject to the stricter credit cap. The existing H1/httpcore/Django/simple-control fixtures remain development data. Old costs/results can be context, but current paired comparisons require the same current environment; do not combine September-era runs with a later backend as if contemporaneous.

### Stage 0: no model, no credits

Specify and later exercise scripted acceptance-control events: an unresolved supported-state exception, unrelated green test, zero-test collection, post-validation mutation, severity downgrade, missing criterion, fabricated waiver, background writer, absent hook, hook timeout, and successful unchanged patch. These are synthetic development failure classes, not selected future promotion tasks. Verify that failed checks cannot mint a successful receipt and that stopping is bounded. No claim of LLM compliance follows from this stage.

### Stage 1: twelve core attempts

Run the four named development fixtures with three complete products: unchanged OTL, unchanged raw Terra, and the minimal cascade. This is **4 × 3 = 12** attempts. Use identical task scope and evaluator, contemporaneous version/effort accounting, and predetermined balanced arm order. Preserve default comparator behavior: “raw Terra” remains the native default coding harness, not a stripped custom agent.

### Stage 2: four selection/trajectory contrasts

On H1 and Django, add forced-L and forced-T variants of the minimal candidate: **2 × 2 = 4** attempts. Hold the completion mechanism, effort policy, and total limits fixed. Forced T has the same custom acceptance policy as the candidate; raw Terra remains the product baseline, so these two Terra arms are not interchangeable.

This stage asks whether the observed cascade occupies a useful cost/quality point relative to its own fixed paths. If both fixed paths show no useful complementarity, stop routing research. If the cascade loses because it inherits bad work, investigate restart versus continuation only by reallocating the remaining budget; do not add an unlimited matrix. H1 cannot alone establish a general need for T.

### Stage 3: two optional mechanism modules, four attempts each

| Module | Smallest comparison | Decision |
|---|---|---|
| Verifier | On one correct and one defective stored development snapshot, Luna evidence collection versus owner self-check with equal incremental allowance: **4** bounded attempts | Keep only if it exposes an executable critical defect the self-check misses, causes no false repair on the correct case, and fits a **20%** added-cost envelope relative to the parent attempt; otherwise omit |
| Lane M | On two already exposed or explicitly synthetic multi-packet development missions, forced M versus one continuous Builder with the same root/gate: **4** attempts | Keep only for a new full success or at least **20%** lower total cost at equal success, without a correctness regression; trace must identify the useful inter-packet decision |

The M missions must genuinely contain a dependency crossing packets. Django alone does not establish a general integration distribution; if no second suitable exposed/synthetic case exists, **omit M**, rather than shopping for a future promotion task. Designing a synthetic fixture does not make it unseen evidence.

Stages 1–3 total **24** attempts. Do not run optional modules if the core candidate fails or the credit cap binds. A null result on these few fixtures is a reason not to include a component under this budget, not proof the component never helps. No-Verifier is already the core; a “full adaptive” system need not be implemented just to ablate it.

Route logs should distinguish observed policy performance from causal interpretation. A sampled minimum across L/T outcomes is an optimistic hindsight reference, not an oracle probability. One continuation's improvement does not identify the counterfactual it replaced. If native session branching cannot preserve identical context and workspace, use fresh full-run variants and label them as coarser contrasts. Extra self-check/recovery cost belongs in the intervention's total.

## 10. FRESH HOLDOUT / EVALUATOR PLAN

### Sampling without choosing the future tasks

No future promotion task is selected, enumerated, or revealed in this report. H1 and documented H2–H4 remain excluded from pristine promotion evidence.

Replace the freeze-SHA-only sampler with a committed selection protocol and a sealed eligible-pool manifest. Specify repository/date/language eligibility, stratum rubric, resource limits, deduplication by related issue/change, and exclusion rules **before** final candidate selection. Hash the pool, sampling code, candidate, and evaluator separately. A pool that contains only attractive easy-to-grade tasks remains biased even under perfect randomness.

After commitments, combine those hashes with a later, independently generated random value unavailable to the designer at freeze time. Predeclare its source/time or use a blinded curator who supplies the draw afterward. Record the first valid draw; no reseeding through harmless commits. Sample reserves at the same time, and consume them in fixed order only for predeclared environment/acceptance defects.

Prefer a curator who has not tuned the candidate. If a third person is impractical, separate curation from design access, log all eligible/excluded counts and reasons, and disclose that blinding is incomplete. Do not assign difficulty using Premium's outcomes or choose a stratum because a baseline lost. Limit the eight-task pilot to at least four repositories and at most two tasks per repository, with related changes treated as one exposure cluster. If eligibility cannot meet that target, narrow the generalization claim instead of silently relaxing the rule.

Post-cutoff public PRs reduce a particular risk; they do not certify absence of training, post-training, retrieval, or issue-text exposure. OpenAI's SWE-bench analysis documents both contamination and evaluator defects, with its flawed-test percentage referring to a selected difficult subset rather than all tasks [S18](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/). A newly sampled public task is fresh to this design process, not provably fresh to the model.

### Resolve the oracle timing problem

The RFC would first fetch accepted material after the model jobs. That avoids local exposure but postpones discovery of a broken evaluator until credits are spent. A better separation is **trusted curator preflight before execution, sealed material inaccessible to model jobs, scoring after all jobs**. This is an explicit evaluator-policy revision, not a covert exception.

Precommit the behavior oracle after checking it against accepted behavior, the original base, and at least one contract-breaking mutation where meaningful. Review helper-name coupling, contradictory task wording, skipped tests, and irrelevant requirements. Accepted code is a reference, not the required shape. Do not inject accepted production code into candidate workspaces. Keep a blinded, task-focused human compatibility/maintainability rubric secondary to behavior, with disagreements adjudicated symmetrically; METR shows why passing tests alone can miss mergeability [S19](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/).

After results, allow zero-AI evaluator correction only for a demonstrated test/infrastructure defect. Preserve the original and corrected scores, correction reason, and equal application to all frozen artifacts. Changing the acceptance meaning creates a new evaluation condition. Never treat a correction as permission to rerun a model until it passes.

### Isolation must include the process and credentials

Independent runners, no evaluation checkout, and no sibling workspaces are good changes. Removing a git remote is not a network boundary: a shell can reconstruct a public URL. A job can also expose metadata, tokens, artifact access, home-directory customizations, and caches outside the target tree.

The premise that Copilot service access makes shell isolation impractical is now too pessimistic. Current Copilot documentation describes local filesystem/network sandboxing and configurable restrictions [S22](https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes), [S23](https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings). Whether those capabilities work on this exact headless Actions runner remains untested. Verify the chosen implementation with a harmless denied network/file probe and an allowed local test before the paid phase; a settings declaration is not evidence of enforcement.

Proposed evaluator controls:

- Separate the Copilot service transport from model-command egress where supported. Deny shell access to external repository/search endpoints; preinstall pinned dependencies. If that separation cannot be enforced, classify the run as network-exposed and disclose the limitation instead of claiming a clean no-external experiment.
- Give each arm only its historical target and exact plugin artifacts. Keep pool/oracle manifests, other patches, controller state, and workflow credentials outside its readable boundary. Do not expose a credential that can fetch evaluation artifacts. Audit automatically loaded instructions, skills, MCP servers, and user hooks.
- Use a dedicated restricted subprocess or container boundary for general shell. Preserve supported repository instructions from the historical base consistently across arms; record ambient customization rather than unknowingly adding current global instructions.
- Pin dependency lock data, CLI package/version, action commit SHAs, plugin bytes, and target SHA. `ubuntu-24.04` pins an OS family, not an immutable image: record the actual runner image version or use a digest-pinned environment plus host metadata [S24](https://docs.github.com/actions/using-github-hosted-runners/about-github-hosted-runners).
- Capture complete workspace bytes, file modes/symlinks/deletions, index state and HEAD, test artifacts, tool events, root/leaf effort, four token/cache buckets where available, and whole-attempt credits. A tarball without a manifest/digest is not a complete-state proof.
- Run the agent under a shorter process deadline than the job deadline, reserving time for capture. A controller-owned finally/cancellation path should quiesce subprocesses and preserve partial artifacts. `always()` cannot upload bytes never written, and abrupt runner loss can still defeat local capture.
- Run A/B/C in a compact time block with predetermined balanced order or matched scheduling; record service/model metadata and queue time. Report compute wall time and user-observed wait separately. An unavailable model or changed backend is a versioning event, not a silent substitution.

Model-job failures, cap exhaustion, and crashes remain in complete-attempt product accounting. A demonstrably shared setup failure can invalidate a task under a predeclared rule, with its consumed credits retained in research spend. Do not classify a candidate-induced import breakage as infrastructure. The hidden evaluator must be outside the candidate's completion mechanism so candidate-written receipts cannot determine the score.

### Minimum sample and repetition

Eight tasks × three arms gives **24 first-pass attempts**. Preselect one repeat task per stratum by the sealed draw, without inspecting outcomes. Only if the first screen clears its vetoes and the remaining budget is sufficient, run each of those four tasks once more in all three arms: **12 additional attempts**. This is a fixed robustness check, not selective repetition of winners. Report first-pass and repeat cohorts separately; do not call two runs a reliability estimate.

A repeated regression on a winning task blocks advancement; a repeat success does not erase the first failure. Preserve every attempt. Under budget exhaustion, finish the available record and return NO_PROMOTION/INCONCLUSIVE; do not redefine the sample. A larger population claim requires another explicitly funded, fresh evaluation, not a retrospective confidence interval on this pilot.

## 11. STRONGEST ALTERNATIVE ARCHITECTURES

Ranked for this project's next decision, taking present runtime and maintenance constraints seriously:

| Rank | Alternative | Strongest case | Main weakness / decisive comparison |
|---:|---|---|---|
| 1 | Unchanged OTL for efficient work; unchanged raw Terra when the user selects the expensive product | Zero new adaptive machinery; real product baselines; no router calibration debt | User must choose the initial tier; Premium must beat these outcomes or their blind mixture |
| 2 | Minimal one-way cascade from section 6 | Preserves one tier choice, exploits cheap attempts, permits integrated recovery, exposes a small number of failure modes | Prefix waste and anchoring; forced T/raw Terra may dominate |
| 3 | Integrated Terra with one optional read-only Luna explorer or bounded mechanical worker | Keeps the difficult causal trajectory intact while outsourcing a specific expensive operation | May have too little cheap work to meet cost gates; compare against Terra with no leaf |
| 4 | Cheap default with external deterministic escalation/restart on observable failures | Removes always-Terra intake and makes policy inspectable | Requires a supported external controller or visible handoff; cannot bypass the documented cost-tier restriction |
| 5 | Bounded draft → different-family critique → one revision, including available native orchestration | Orthogonal evidence may help where additional solving does not | Reviewer correlation and false repair remain; native preview results do not establish this workload's benefit |

HydraFusion is a relevant build-versus-buy competitor, not proof that the bespoke RFC is worthwhile. Its current native runtime has bounded, isolated workflow mechanisms and tuned offline evidence [S16](https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/). Do not add a new paid HydraFusion arm during this audit or opportunistically midway through a freeze. If its supported scope and actual availability later match the product, reserve a fixed comparison within—not beyond—the research budget.

A Terra router-only root with an integrated Terra child is less attractive initially than rank 2 or 3: it pays two expensive contexts to restore a separation the root could avoid. It becomes interesting only if static tool isolation demonstrably prevents enough waste or mistakes. A learned step router is also premature without a sufficiently broad calibration corpus and a way to reproduce live switched trajectories.

## 12. KILL CRITERIA / RESEARCH BUDGET

Separate **candidate rejection**, **component removal**, and **ending this project's Premium research**. A false completion can veto one candidate without disproving all multi-model systems. Conversely, repeatedly changing names or prompts should not reset the research clock.

Proposed budget for a cost-sensitive individual project: the smaller of **2,000 Copilot credits total** and the amount the owner separately authorizes for this research program. At the current conversion that nominal ceiling is **$20 of metered AI usage**, not a subscription invoice or a claim about remaining allowance [S20](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing). No spending is authorized by this report. Allocate 600 credits to development, 900 to the first fresh screen, 300 to predetermined repeats, and 200 as failure/in-flight reserve. Do not automatically transfer an exhausted bucket to an optional component.

Also cap implementation/evaluator effort at **two focused working days**, excluding this audit, and at most **two materially distinct new candidate designs after v1** under the same total budget. A materially distinct design changes an identified mechanism, not wording alone. The second candidate does not inherit permission to reuse the first candidate's exposed holdout as fresh. If a smaller current allowance makes the plan infeasible, reduce the claim or stop; the September 7 balance is stale.

| Condition | Stop decision |
|---|---|
| Completion mechanism cannot distinguish a valid result from a stale/contradictory record in scripted development checks | Do not spend on coding-agent evaluation until revised; abandon the hard-enforcement claim if the runtime cannot support it |
| A surfaced blocking exception still receives unqualified completion | Reject this candidate; only a specific mechanism change can justify the second design |
| Forced L matches the cascade at lower total cost | Remove Terra from that path; prefer OTL/cheap baseline |
| Forced T/raw Terra dominates the cascade on the difficult development contrasts after full prefix cost | Stop the cascade thesis; do not add M as a rescue narrative |
| M or Verifier fails its bounded marginal-value module | Remove that component; no repeated retuning on the same fixtures |
| At least 80% of eligible pilot tasks use the same effective solver path, with no observed benefit from the exceptions | Treat topology collapse as a redundancy signal; keep the simpler product unless a predeclared niche earns the overhead |
| Two competent, materially different candidates cannot clear the narrow quality/economics screen, or fail to improve on simple baselines/blind mixing | End bespoke Premium product research for this project; retain stable OTL and raw Terra as choices |
| Global credit/time cap reached, or product benefit still cannot be stated beyond “it chooses models for you” | Stop with NO_PROMOTION; do not fund v3/v4 by default |

“Competent” must be defined before outcomes: valid environment/oracle, supported runtime, functioning completion mechanism, and no gross implementation defect. Do not use incompetence as an unlimited exemption for a losing design. At most one genuine infrastructure repair cycle is covered by the reserve. Restarting the broader hypothesis later should require new external capability, a materially different workload, or a new budget decision—not another favorable regression anecdote.

## 13. LATEST EXTERNAL EVIDENCE

Fresh survey checked **2026-09-09**. Dates below are publication/revision dates where available; live documentation uses its displayed update or an explicit access date. This source set deliberately includes evidence for routing, against naive routing, and against overconfident evaluation. No benchmark percentage is a predicted Luna/Terra effect size.

| ID | Source, authors/organization, date, direct URL | Evidence type | Exact implication and limitation |
|---|---|---|---|
| S1 | **Use subagents in Visual Studio Code** — Microsoft/VS Code; updated 2026-09-02. [Documentation](https://code.visualstudio.com/docs/agents/run/subagents) | Official runtime documentation | Documents cost-tier eligibility, custom agent model/tool overrides, and stateless child calls. Supports a provisional Terra parent; does not prove parity across all session targets or account configurations. |
| S2 | **Hooks reference** — Microsoft/VS Code; updated 2026-09-02. [Documentation](https://code.visualstudio.com/docs/agents/reference/hooks-reference) | Official runtime contract | Tool interception and stop blocking support a small reconciliation layer. Blocking continues inference; hook events are not semantic proof that a task is complete. |
| S3 | **Agent hooks in Visual Studio Code (Preview)** and **Custom agents in VS Code** — Microsoft; updated 2026-09-02. [Hooks](https://code.visualstudio.com/docs/agent-customization/hooks), [custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents) | Official preview documentation | Agent-scoped hooks and explicit tool lists are available with configuration. Hook formats/tool argument names differ; no documented L/T/M-driven atomic permission transition is established. |
| S4 | **Agent plugins in VS Code** — Microsoft; updated 2026-09-02. [Documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) | Official packaging documentation | Plugins can ship client-specific hooks, so deterministic checks need not imply a large external service. Packaging support is not proof that this repository's current manifest loads a future hook correctly. |
| S5 | **GitHub Copilot hooks reference** — GitHub; undated live page, accessed 2026-09-09. [Documentation](https://docs.github.com/en/copilot/reference/hooks-reference) | Official CLI/runtime contract | Stop continuation, subagent response rewriting, timeout behavior, and runaway escape materially limit a hard completion guarantee. Test the exact adapter; a hook declaration is insufficient. |
| S6 | **Manage AI settings in enterprise environments** — Microsoft; live documentation, accessed 2026-09-09. [Documentation](https://code.visualstudio.com/docs/enterprise/ai-settings) | Official policy reference | Hooks can be disabled by policy. The product must detect unmet prerequisites and respect policy, not silently claim the same assurance. |
| S7 | **Choose and use an agent harness** and **Use tools with agents** — Microsoft; updated 2026-09-02. [Harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses), [tools](https://code.visualstudio.com/docs/agents/run/tools) | Official runtime documentation | Local/Copilot/cloud surfaces differ; tools and handoff behavior depend on target. A CLI experiment is not automatically a VS Code product validation. |
| S8 | **SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks** — Seongho Son et al.; 2026-06-30, v1. [Paper](https://arxiv.org/html/2607.00053v1) | Theoretical mechanism plus SWE benchmark | Conditions routing on a cheap exploratory trajectory and learns a value head; escalation restarts the strong solver. The Bayes-information result is not a guarantee for an uncalibrated LLM router after charging exploration. |
| S9 | **TwinRouterBench: Fast Static and Live Dynamic Evaluation for Realistic Agentic LLM Routing** — Pei Yang et al.; 2026-05-14, v1. [Paper](https://arxiv.org/html/2605.18859v1) | Static benchmark plus live 100-case SWE evaluation | Its trained router reports 75/100 versus 74/100 for unrouted Opus at lower realized cost. The rule-based variant is much more expensive. Calibration and live execution matter; the small static corpus and public SWE benchmark limit transfer. |
| S10 | **Scrouting: Cost-Aware Routing of Coding Agents by Scouting the Repository First** — Ishaan Bhola, Adithyan Krishnan, Mukunda NS, SuperAGI; 2026-08-05, v1. [Paper](https://arxiv.org/html/2608.04804v1) | Repository benchmark and component analysis | Cheapest fixer with verified handoff ties routing on 266 Python tasks. Strong warning to separate evidence-preparation value from router value; narrow repositories and directional calibration effects limit generalization. |
| S11 | **Agent-as-a-Router: Agentic Model Routing for Coding Tasks** — Pengfei Zhou et al., NUS/Alibaba and collaborators; 2026-06-22, revised 2026-06-26, v3. [Paper](https://arxiv.org/html/2606.22902v3) | Coding benchmark and information/memory ablations | Performance information and execution-grounded experience improve routing. This is evidence against pure cold-start intuition, not against routing. Reported cost lacks observable cache hits; the agentic evaluation uses a shortened 40-step limit. |
| S12 | **The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents** — Roy Ganz, Mor Shpigel Nacson, Adi Kalyanpur, Ron Litman, AWS; 2026-08-25, v1. [Paper](https://arxiv.org/html/2608.24358v1) | Controlled handoff study, 58,000 reported runs | Transfer direction and representation change quality/cost. Includes Luna/Sol, not Terra; fixed switch timing and public SWE-bench constrain inference about an adaptive controller. Do not assume every safe-looking T → L transfer saves money. |
| S13 | **The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World** — Ashritha Gonuguntla, CMU; 2026-08-08, v1; reports COLM workshop acceptance. [Paper](https://arxiv.org/html/2608.08239v1) | Controlled branching mechanism study | Swapping models changes subsequent observations and actions, undermining stitched-log counterfactuals. Small Qwen models, quantization differences, and 0–3% base success make its numerical effects poor frontier-model forecasts. |
| S14 | **TACIT-Switch: Cost-Aware Model Escalation for LLM Agents from Censored Supervision** — Ji'an Lei and Jian Huang, BNU/PolyU; 2026-08-28, revised 2026-09-04, v2. [Paper](https://arxiv.org/html/2608.27911v2) | Statistical mechanism, simulation, interactive benchmarks | Supports investigating a permanent rather than oscillating handoff. Requires learned risk and teacher supervision; paired strong success from the initial state does not certify rescue from a damaged state. DABench's paired improvement interval includes zero; this is not repository-scale Luna/Terra evidence. |
| S15 | **TeamBench: Evaluating Agent Coordination under Enforced Role Separation** — Yubin Kim et al., MIT/Google and collaborators; 2026-05-08, v1. [Paper](https://arxiv.org/html/2605.07073v1) | Controlled role-separation benchmark | Reported 49.4% false acceptance is conditional on valid attestations; treating missing verdicts as fail yields 22.3%, while the audited subset yields 38.7%. Denominators and role value must be measured; no rate transfers to Luna. |
| S16 | **Project HydraFusion: Frontier quality via multi-model orchestration** — GitHub Staff; 2026-09-04. [Engineering report](https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/) | Vendor tuned offline benchmarks; research preview | Single/cascade/critique is a credible native alternative, with bounded execution and isolated review. Best tuned configurations improve estimated economics but do not prove this custom policy or long-session robustness. |
| S17 | **How we made GitHub Copilot CLI more selective about delegation** — Pingping Lin and Yu Hu, GitHub/Microsoft; 2026-06-12. [Engineering report](https://github.blog/ai-and-ml/how-we-made-github-copilot-cli-more-selective-about-delegation/) | Production A/B | Reports 23% fewer tool failures and 5% lower P95 wait without quality regression. Supports requiring added handoffs to earn their cost; it does not identify the best local L/T/M switch rule. |
| S18 | **Why SWE-bench Verified no longer measures frontier coding capabilities** — OpenAI; 2026-02-23. [Analysis](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) | Vendor evaluator/contamination audit | Shows test-definition and exposure risks. The 59.4% flaw figure concerns 138 selected difficult cases, not the full benchmark. Supports curator preflight and cautious public-PR claims. |
| S19 | **Many SWE-bench-Passing PRs Would Not Be Merged into Main** — METR; 2026-03-10. [Study](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) | Maintainer assessment study | Test passing and practical mergeability differ. Evaluated agents are older and did not iterate with maintainers; do not use the reported rejection proportion as a current Premium estimate or replace behavioral tests with subjective style. |
| S20 | **Models and pricing for GitHub Copilot** — GitHub; live documentation, accessed 2026-09-09. [Pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) | Official billing reference | One credit equals $0.01; account for input/output/cache reads/cache writes. Copilot's Luna and Terra long-context thresholds differ. Use actual complete-attempt credits, not API token estimates or stale allowance balances. |
| S21 | **GPT-5.6 Luna / GPT-5.6 Terra model pages** — OpenAI; live documentation, accessed 2026-09-09. [Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), [Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra) | Official model documentation | Documents price positioning, effort support, and February 2026 cutoff. Does not establish local/global uncertainty routing competence or model-memory cleanliness; API rates are not a Copilot invoice. |
| S22 | **About cloud and local sandboxes for GitHub Copilot** — GitHub; live documentation, accessed 2026-09-09. [Documentation](https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes) | Official runtime documentation | Describes OS-backed filesystem/network restrictions. Makes stronger model-command isolation plausible; exact Actions/headless compatibility and credential boundaries still need validation. |
| S23 | **Configuring local sandbox settings** — GitHub; live preview documentation, accessed 2026-09-09. [Documentation](https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings) | Official configuration reference | Network/filesystem controls are configurable and may be enterprise-managed. A selected setting is not proof that all tools share the boundary or that an experiment retained it. |
| S24 | **GitHub-hosted runners** — GitHub; live documentation, accessed 2026-09-09. [Documentation](https://docs.github.com/actions/using-github-hosted-runners/about-github-hosted-runners) | Official infrastructure reference | Hosted image software updates weekly; an OS label alone does not reproduce a run. Record image metadata and pinned dependency artifacts. |
| S25 | **Towards a Science of Scaling Agent Systems** — Yubin Kim et al.; 2025-12-09, revised 2026-04-08, v3. [Paper](https://arxiv.org/html/2512.08296v3) | Controlled multi-agent benchmark/mechanism study | Tests 260 configurations across six benchmarks; value depends on capability and coordination structure. Supports conditional component testing, not a universal threshold or a mandatory mission hierarchy. |
| S26 | **Scaling Test-time Compute for LLM Agents** — King Zhu et al., M-A-P/OPPO and collaborators; 2025-06-15, v1. [Paper](https://arxiv.org/html/2506.12928v1) | Controlled inference-time scaling study | Added computation's strategy and timing matter. Supports equal-incremental-budget assurance comparisons; more review calls are not intrinsically better evidence. |
| S27 | **Harness design for long-running application development** — Prithvi Rajasekaran, Anthropic Labs; 2026-03-24. [Engineering essay](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Vendor engineering case studies | High-level contracts and active evaluator checks can improve applications, but a showcased 20-minute/$9 versus six-hour/$200 comparison is not cost-matched. It cannot justify M's economics. |

One important cross-source conflict should remain visible: The Replay Gap characterizes TwinRouterBench's dynamic track narrowly, while the directly inspected TwinRouterBench paper explicitly describes live end-to-end execution and realized API costs. This audit uses each primary methodology, not the characterization in the other paper. They jointly justify live evaluation; they do not show that TwinRouterBench's published dynamic results are stitched-log artifacts.

The evidence favors **measured selective allocation with explicit state transfer** over both “always delegate” and “never delegate.” It does not supply this project's missing calibration data, enforce its ledger semantics, or settle its product weights.

## 14. REQUIRED RFC CHANGES BEFORE IMPLEMENTATION

| Priority | Required revision | Reviewable acceptance condition |
|---|---|---|
| P0 | Replace unrestricted L/T/M with the minimal one-way candidate, or justify a different equally small hypothesis | Exact initial path, escalation trigger, termination rule, and excluded components are specified; no task-specific exceptions |
| P0 | Separate record consistency, semantic acceptance, and user-facing completion guarantees | Identify which checks are deterministic, which are model judgments, and what happens when hooks are missing or fail |
| P0 | Specify acceptance authority and waiver semantics | Source-linked criteria, no silent deletion/downgrade, explicit partial outcome for waivers, and an unattended BLOCKED path |
| P0 | Name the primary runtime and supported hook/tool contract | VS Code target/version/settings, CLI adapter differences, availability checks, and ownership limitations are explicit |
| P0 | Define ownership transfer and handoff contents | Quiescence, workspace identity, background-process handling, and preservation of user edits are covered |
| P0 | Replace survivor-only economics and ambiguous false-complete denominators | Full-attempt metrics, fixed scope, declared mixture, capability regression guard, and pilot-versus-production distinction |
| P0 | Replace designer-controlled sampling seed and delayed oracle discovery | Pool/protocol commitments, independent post-commit randomness, sealed curator preflight, and logged reserves/exclusions |
| P1 | Stage development ablations and remove optional components until earned | At most 24 attempts with named contrasts and no hidden full-v2 tuning matrix |
| P1 | Include a finite research/program budget | Credit/time/design ceilings, component kills, and no automatic restart after failed promotion |
| P1 | Correct evidentiary overclaims | Lane T is motivated rather than required by H1; native hooks/sandboxing are current possibilities; one smoke run is not a structural guarantee |

These revisions are prerequisites to authorizing an implementation experiment. They do not require perfect production security or a large learned router before any prototype. They require the prototype to test an explicit modest claim rather than promise an invariant it cannot enforce. The RFC and all candidate files remain unchanged by this audit.

## 15. WHAT WOULD CHANGE MY MIND

| New observation | Verdict update |
|---|---|
| A revised specification defines one executable policy and demonstrates the proposed receipt/termination semantics on the exact runtime with zero-model event tests | Move toward approval for the bounded implementation experiment, not promotion |
| Previously unavailable runtime evidence supports cheap-parent premium escalation with preserved state and policy-compliant model selection | Reconsider the Terra-root premise; compare an external/cheap-entry cascade before paying fixed premium intake |
| A controlled known-task comparison shows Terra takeover reliably resolves blocking evidence that forced L misses, while the cascade saves enough versus forced T | Support the minimal cascade; still require fresh product evidence |
| A full L/T/M policy beats fixed paths and the minimal cascade under equal scope, accounting, and fresh evaluation | Reconsider deferring M/adaptive routing; trace-based attribution alone is insufficient |
| The ledger only changes final wording, while full correctness and recovery do not improve | Retain honest reporting if cheap, but reject it as the claimed premium capability mechanism |
| Hook enforcement needs a substantial custom runtime or is unavailable in the intended user's policy | Prefer simpler baselines or an explicitly different product; do not relax the guarantee invisibly |
| New evidence shows low-cost prefix takeover is dominated by clean Terra restart | Drop continuation; charge discarded work and test a restart policy within the same finite budget |
| The declared pilot clears capability, full-attempt economics, and false-complete vetoes with stable repeat results | Advance to limited product review on that scope; do not infer multi-session reliability |

The strongest objection to this verdict is that a small prompt-only prototype could cheaply reveal useful behavior before every runtime detail is resolved. That is reasonable if explicitly framed as a compliance experiment. The reason revision remains necessary is that the RFC currently joins that modest experiment to stronger completion and frontier claims, while its proposed metrics can conceal the very failures those claims concern.

## 16. NEXT ACTION

1. **Revise the RFC's policy and claim boundaries before implementation:** one-way minimum, explicit completion semantics, and one named runtime.
2. **Precommit the staged development plan, full-attempt gates, sealed selection method, and finite budget.** Keep all future holdout identities unselected during design.
3. **Only after separate authorization, implement and test the smallest mechanism.** Omit M and Verifier unless their bounded ablations earn inclusion; retain the option to stop Premium research.

## 17. EVIDENCE QUALITY / UNCERTAINTY

| Conclusion | Confidence | Limit |
|---|---|---|
| RFC routing and completion policies need operational specification | HIGH | Directly visible in the proposal; the RFC itself acknowledges prompt-only enforcement |
| Both-pass cost selection and freeze-SHA randomness are insufficient | HIGH | Logical properties of the proposed metrics/sampler, independent of model performance |
| Current public docs support hooks and retain a cost-tier restriction | HIGH for documentation; MEDIUM for this deployment | No runtime smoke, account policy check, or headless sandbox trial occurred |
| Minimal one-way cascade is the best first paid candidate | MEDIUM | Prefix waste and handoff anchoring may make integrated Terra preferable |
| D2 will justify M, or Verifier will improve assurance | LOW | No controlled evidence on this proposed implementation |
| Proposed numeric gates represent the owner's true utility | LOW | Explicit provisional preferences, not measured demand or reliability targets |
| Premium has no viable niche | NOT ESTABLISHED | This is a design audit, not a new capability experiment |

The prior audit is not an independent replication merely because this is a new report. Its H1 forensic claims were reread, not rerun here; this design audit relies on that pinned analysis and the result ledgers. The current held-out ledger confirms v1 stopped and H2–H4 were not run. No new model trajectory, hidden oracle execution, or paid Copilot call was produced. No future promotion pool was assembled or task set selected.

The handoff and required materials were read in the specified order: prior audit at its own commit, held-out results, regression results, v2 RFC, held-out protocol, original RFC, and stable README/DESIGN/CONTRIBUTING. Relevant root/Builder/Auditor/stable contracts and the current validation workflow were then inspected for feasibility. The branch tree contains no AGENTS.md and only the ordinary validation workflow; this audit adds no experiment workflow.

Research limitations remain substantial. Many 2026 results are recent preprints or vendor reports; costs, model families, task distributions, and runtime interfaces differ. Handoff studies do not evaluate this exact Terra/Luna candidate. Small routing studies can overfit public tasks, and positive results do not cancel control failures. Official documentation establishes available interfaces, not successful operation under this repository's installation. The recommended eight-task pilot can reject conspicuous failures; it cannot certify a production false-complete rate.

Repository evidence anchors:

| Material | Pinned source |
|---|---|
| Authorized v2 scope | [ASTRA_PREMIUM_V2_HANDOFF.md](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/ASTRA_PREMIUM_V2_HANDOFF.md) |
| Prior independent audit | [ASTRA_PREMIUM_AUDIT.md](https://github.com/YB-Park/over-the-luna/blob/79f3c4d34beb1383fa55fae180c999aa23770d64/docs/ASTRA_PREMIUM_AUDIT.md) |
| V2 design proposal | [PREMIUM_V2_PRE_IMPLEMENTATION_RFC.md](https://github.com/YB-Park/over-the-luna/blob/97cc22962e3bf810b76bf8d5ef4c9fe509a542c5/docs/PREMIUM_V2_PRE_IMPLEMENTATION_RFC.md) |
| Experiment outcomes | [held-out results](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/PREMIUM_HELDOUT_RESULTS.md), [regression results](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/PREMIUM_HARNESS_RESULTS.md) |
| Original design/evaluation | [held-out protocol](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/PREMIUM_HELDOUT_PROTOCOL.md), [original RFC](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/PREMIUM_HARNESS_RFC.md) |
| Stable product | [README](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/README.md), [DESIGN](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/docs/DESIGN.md), [CONTRIBUTING](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/CONTRIBUTING.md) |
| Existing contracts | [Premium root](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/agents/premium-harness.agent.md), [Builder](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/agents/luna-builder.agent.md), [Auditor](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/agents/luna-auditor.agent.md), [OTL](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/agents/over-the-luna.agent.md) |
| Current workflow | [validate.yml](https://github.com/YB-Park/over-the-luna/blob/464a05fc16d35ba4154197cdb6581dc69674ef3d/.github/workflows/validate.yml) |

This report is the sole new audit deliverable. No RFC, agent, validator, result ledger, or workflow is changed, and no branch is merged.
