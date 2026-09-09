# Astra Independent Premium Harness Audit

## 1. EXECUTIVE VERDICT

**STOP_AND_REDESIGN**

**Confidence: MEDIUM.** Stop paid screening of this frozen candidate; retain the broader premium-product hypothesis as unproven. Do not promote it, silently repair its prompts, or erase H1. This is an engineering investment decision, not a statistical finding that mixed-model orchestration cannot work.

The decisive finding is stronger than the handoff's summary suggests: **the H1 limitation reached Terra explicitly, twice, and Terra still accepted the patch.** Builder reported that unsupported receive flags, including SSL-like sockets, retained the old readiness behavior. Auditor repeated that limitation while returning PASS. The executive had a decision-relevant warning; the control loop failed to turn it into a discriminating check or an unresolved acceptance item. More context alone is therefore an inadequate explanation or remedy. See the original [H1 execution log, job 102380885415](https://github.com/YB-Park/over-the-luna/actions/runs/34325241072/job/102380885415), particularly 07:50:43–07:52:43 UTC on 2026-09-09.

Three considerations determine the recommendation:

1. **The premium role has no demonstrated marginal benefit on unseen work.** H1 costs 2.58 times OTL and takes 2.13 times as long, with the same failed acceptance case. The successful Django case is development regression evidence. The documented record does not contain the RFC's controlled component ablation establishing that Terra and Auditor earn their roles.
2. **The frozen control contract has an assurance gap.** Its critical-belief gate scrutinizes Terra-originated constraints, while an acceptance-critical Builder-originated assumption can survive implementation, independent review, and final adjudication. Builder autonomy is sensible; restricting high-risk belief management to the originator is not.
3. **The remaining screen cannot settle the stated long-horizon claim.** H2 is another subtle bug, H3 is one coherent feature, and H4 is a small control. These can discover wins, but they do not measure sustained mission state, resumption, or integration over a calibrated task horizon. There is no declared user-task distribution or numerical quality/cost tradeoff to convert those wins into a product decision.

There is a respectable case for finishing a cheap, already specified screen. This audit rejects neither its possible information nor the possibility of H2/H3 wins. It recommends resolving the assurance mechanism and intended product distribution before spending on more outcomes that would still leave those questions open. The recommendation would weaken substantially if a finite H2–H4 screen already had an explicit decision threshold and a product scope limited to comparable one-shot repository tasks.

Audit reference date: **2026-09-09 UTC**. Repository reviewed: `YB-Park/over-the-luna`, audit-branch starting head `8bf018cfa3a608241b800c3f4610bc2f41bd2364`; experiment source `2968f86f19cfc29100e67e18623858c4e967fa35`; frozen candidate `0083f3d81e7339f3b22e3efaa852562d7daa07e5`; stable comparator `814a069df188d28a564c4b05fbc441c2e3092d3d`. No candidate, result ledger, or workflow is changed by this report. No Copilot experiment, AI rerun, or oracle execution was performed for this audit.

## 2. STRONGEST CASE FOR THE CURRENT DESIGN

The economic premise is credible. Expensive judgment can be amortized over substantial cheaper execution when the hard decisions are infrequent, visible, and consequential. A mission owner can protect requirements across several work packets while a continuous Builder retains local implementation knowledge. A second context can test a completed artifact without inheriting every commitment made during construction. One mutation owner avoids patch races, and non-recursive leaves constrain coordination topology. These are useful properties independent of the Luna brand.

The best target distribution has four characteristics: expensive mistakes occur at identifiable integration boundaries; most repository labor is within Luna's competence; acceptance can be made executable; and requirements fit in a compact, evidence-grounded state. Examples include a coherent feature spanning configuration, API, storage, and migration behavior, or a long change whose individual components are easy but whose compatibility requirements are easily forgotten. Here Terra need not outcode Luna locally; preventing one globally inconsistent work packet could repay many executive turns.

The regression history contains real favorable signals. Removing the dedicated causal Probe cut R1-v3 cost to about half of R1-v2 and avoided lock proliferation. R2 passed the recovered accepted Django tests. Those results justify preserving a research hypothesis, although tuning and repeated exposure prevent using them as independent promotion evidence. The [regression results](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/PREMIUM_HARNESS_RESULTS.md) appropriately acknowledge both limitations.

External evidence does not support killing the whole idea. GitHub's HydraFusion demonstrates a plausible mixed-model frontier under selected offline policies; SWE-Edit shows that carefully chosen context boundaries can improve repository-task economics. Their mechanisms differ from this candidate: neither establishes that every premium task should have a permanently tool-blind Terra supervisor followed by a same-model Builder/Auditor pair. See sources S1 and S8 below.

## 3. STRONGEST CASE AGAINST THE CURRENT DESIGN

### The executive may be buying the wrong kind of intelligence

The architecture pays Terra to formulate a task before repository evidence exists and adjudicate after Luna has selected, implemented, and defended a causal model. On tasks where the hard intelligence is inside repeated code–hypothesis–execution cycles, this places the stronger model outside the relevant loop. Calling Terra the mission owner does not establish that mission management is the bottleneck.

The shallow default can become an expensive wrapper around an ordinary Luna implementation. There is no parallel implementation throughput to amortize the serial Builder/Auditor path. On locally bounded tasks that OTL already solves, mandatory premium initiation and audit are pure overhead unless they prevent enough rework. On hard local debugging tasks, withholding integrated strong-model diagnosis may preserve Luna's failure mode. On tasks beyond both models' competence, more certification creates confidence without capability.

### Independent context is not independent error

Builder and Auditor share the same model, repository cues, task wording, and successful tests. Auditor also receives Builder's interpretation. Their errors may be strongly correlated. Terra is a different model tier, but it usually reasons over those same selected assertions. An agent count of three is not three independent observations of correctness.

H1 makes the distinction concrete: Auditor added a real hiredis push-preservation check, but did not falsify the unsupported-flags fallback. A useful check can coexist with a false PASS. R1-v2 likewise shows that an actionable repair can strengthen the wrong intervention class; counting findings or test executions is not a causal measure of assurance value.

### The product commitment precedes the evidence

“Luna does all repository labor” is a resource-allocation constraint, not a result. A strict ban on even bounded premium access to decisive local evidence can sacrifice quality to maintain an identity. Conversely, turning Terra into a continuous worker would undermine the current cost premise. The right boundary must be earned empirically rather than selected to preserve either slogan.

The [RFC](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/PREMIUM_HARNESS_RFC.md) correctly demands comparison with raw Terra, but mixes several goals: task horizon, difficult-task correctness, robustness, cost, and ordinary-task usability. Without weights or hard acceptance thresholds, almost any mixed result can be narrated as progress. Cost reduction relative to a passing expensive arm is not cost efficiency at comparable quality when the cheaper arm fails.

## 4. H1 FORENSIC INTERPRETATION

### What was actually verified

The original paid run used **Copilot CLI 1.0.83**, in order B → C → A. Inspection of its structured log confirms 66, 104, and 59 tool starts respectively and the three credit totals below. The final zero-AI evaluator run separately confirms the four outcomes. These are not inferred from a green Actions badge.

| Arm | Corrected oracle | Credits | Wall time | Observed trajectory |
|---|---:|---:|---:|---|
| A — OTL | 3/4; task FAIL | 5.694290 | 167 s | Luna Main → Architect → Main → Reviewer → repair |
| B — raw Terra | 4/4; task PASS | 71.013030 | 222 s | Terra; no subagents |
| C — Premium | 3/4; task FAIL | 14.671259 | 355 s | Terra → Builder → Terra → Auditor → Terra |
| Accepted Redis head | 4/4 reference PASS | No new AI calls | Not a competing agent run | Post-run reference validation |

Sources: [original execution](https://github.com/YB-Park/over-the-luna/actions/runs/34325241072/job/102380885415), [final evaluator](https://github.com/YB-Park/over-the-luna/actions/runs/34352923102/job/102470343867), and [held-out ledger](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/PREMIUM_HELDOUT_RESULTS.md). The four tests are acceptance cases within **one task**, not four independent task samples.

### The defect and the missed decision

For a kernel socket with no pending data, peer closure can still appear readable. A normal socket peek returns empty bytes and identifies EOF. Python SSL sockets reject nonzero receive flags; the Premium patch catches `ValueError`/`NotImplementedError` and returns `True`. That restores the very readiness-only ambiguity the task asks it to resolve. Python's supported interface makes the limitation foreseeable, rather than an arbitrary hidden helper-name requirement. See S17.

| Time, UTC on 2026-09-09 | Observed evidence | Audit interpretation |
|---|---|---|
| 07:46:58 | Terra delegates local diagnosis; stop conditions include reliance on unsupported socket assumptions | The initial contract contained a relevant concern |
| 07:50:43 | Builder reports completion, successful tests, and fallback to prior readiness behavior for SSL-like flag rejection | The critical exception survived summarization |
| 07:50:49 | Terra's audit packet repeats unsupported-flags behavior and asks about relevant socket/parser states | Terra had another opportunity to demand a counterexample |
| 07:51:09–07:52:13 | Auditor inspects SSL/runtime information and searches SSL/unsupported coverage; also tests a real pending push | It did not simply skip platform semantics entirely |
| 07:52:40 | Auditor returns PASS and explicitly describes readiness-only fallback | A known validation gap was treated as acceptable compatibility |
| 07:52:42 | Terra declares implementation complete | Acceptance reconciliation failed at the final boundary |

The likely shared error is equating preservation of previous behavior with fulfillment of the new liveness requirement. Another contributory ambiguity is equating consumption of socket bytes with destruction of a logical push message. The Premium patch comment treats a normal read as consuming a notification. Raw Terra instead calls the existing `read_from_socket(..., raise_on_timeout=False)` after readiness, retaining received bytes in hiredis' persistent buffer for later response processing.

That raw-Terra implementation satisfies the corrected behavioral oracle. However, the original wording about not consuming pending data can be read literally as forbidding any socket read. Under that reading, raw Terra's solution would conflict with the wording despite preserving logical data. The evaluator's interpretation—preserve future push processing, rather than require kernel-buffer immobility—is reasonable for the reported product bug, but must be documented as a semantic interpretation, not presented as an unambiguous literal contract.

**MSG_PEEK is not itself disproven.** The accepted implementation also uses it, combined with additional closure handling. The failure is the incomplete fallback/state partition. Merely banning peek after H1 would overfit to the winning arm's implementation. The accepted [hiredis implementation at 55d41593](https://github.com/redis/redis-py/blob/55d41593d3795080cdfc090ed56c19d9ab4ea3b1/redis/_parsers/hiredis.py) checks buffered SSL data and uses poll closure flags when receive flags are rejected; it also explicitly limits behavior when poll is unavailable.

### Competing causal explanations

| Explanation | Evidence assessment |
|---|---|
| Assurance/adjudication blind spot | Strongest direct support: the limitation was visible, reviewed, and accepted |
| Context compression lost the decisive fact | Contradicted for this particular fact; other omitted local evidence remains possible |
| Split architecture prevents integrated reasoning | Plausible: raw Terra kept diagnosis, code inspection, mutation, and validation together; no controlled intervention isolates this cause |
| Local continuity was destroyed inside Builder | Not supported: Builder had one continuous 224.076-second trajectory with 72 tool calls |
| Root routing chose too much hierarchy | H1 used the shallow intended path; it cannot be blamed on an unnecessary Architect or retired Probe |
| Too little computation | Weak: Builder used 1,618,071 reported cumulative tokens; Auditor 305,089, 30 tools, and 111.117 seconds |
| Ordinary stochastic trajectory variation | Still possible: one sampled patch does not estimate how often another trajectory would avoid the defect |
| Evaluator manufactured a false failure | Initial evaluators were defective; the corrected real-socket test and accepted-head check materially strengthen the final failure, with remaining scope limits below |

Premium's leaves account for about **335 of 355 seconds**. Roughly 94% of elapsed time was the two serial leaf durations, so optimizing a few Terra narration tokens would not explain away the latency gap. C generated about 1.92 million cumulative leaf tokens, **not** a demonstrated 1.92-million-token simultaneous context window. Cache reuse, repeated input, and output must be separated before diagnosing context pressure.

### What the final oracle does not establish

The corrected fourth case wraps a real kernel socket and rejects flagged receives. It is **SSL-like, not a TLS integration test**: no TLS handshake, encrypted records, close-notify, or genuine decrypted-buffer interaction is exercised. It constructs `_HiredisParser` with `__new__` and a mocked reader. The oracle is independent of the *new accepted helper*, but is still coupled to the existing parser API and selected internals.

The first three cases exercise EOF and pending pushes, including a real hiredis path. The suite does not establish all platform semantics, real Redis pool recovery under TLS, fragmented/multiple pushes, repeated liveness checks, half-close behavior on every backend, or asynchronous equivalence. Thus B has a valid **4/4 on this oracle**, not certified universal correctness. Conversely, A/C's concrete failure must not be excused because B has untested residual risks.

In H1, C ties A on observed correctness and loses on cost/time; it loses to B on correctness/time while costing less. This does not prove population-level domination, Terra-model superiority independent of its harness, or that no premium design can extend task horizon.

## 5. ARCHITECTURE REVIEW

### Control-system assessment

The workspace and runtime are the changing system; Builder performs interventions; repository reads and tests provide observations; Terra selects work packets and adjudicates; Auditor supplies a second measurement. This is a useful analogy, not a claim that an LLM harness satisfies formal control-theory guarantees.

| Component | Useful property | Failure mode in the frozen contract | Assessment |
|---|---|---|---|
| Terra | Preserves mission, acceptance, and global decisions | Receives selected assertions without guaranteed independently checkable support; can accept an acknowledged exception | Sparse supervision is credible only when its decisions change outcomes |
| Builder | Owns local causal continuity and serial mutation | A broad goal can encompass the entire hard problem; weakly bounded exploration and repetitive validation stay inside one opaque work interval | Keep local autonomy; do not confuse it with demonstrated executive value |
| Auditor | Reads the actual diff and can execute checks | Same-model correlation, implementation-shaped tests, one selected challenge, ambiguous completeness of PASS | A second context is evidence collection, not certification |
| Architect | Isolates broad discovery | Stable “complete sealed work set” schema does not match Premium's `WORK_SET`/local-discovery semantics exactly | No proof of hard sealing or avoided rereads in Premium |
| State transfer | Compact facts and contradictions can reduce irrelevant context | No required workspace revision, per-criterion evidence map, or durable machine-checked state transition | Labels alone cannot establish evidence sufficiency |
| Phase boundaries | Avoids a premium round-trip after each command | Builder can complete a long, wrong interval without reporting a global contradiction | Event-based boundaries are preferable to arbitrary periodic supervision |
| Failure containment | Single mutator, non-recursive leaves, repair guidance | Plain shell can mutate; no transactional accepted-patch promotion or rollback guarantee | Structural smoke covers behavior in that run, not capability-proof containment |

The specific control defect is an **unobserved-or-unenforced acceptance condition**, not simply excessive hierarchy. The root's gate prevents a Terra hypothesis becoming a constraint, but does not require the same scrutiny when Builder supplies an uncertain compatibility claim. Nor does `SUPPORTED_WITH_RESIDUAL` impose an operational limit on what may be declared complete. A label without a binding acceptance consequence is weak containment.

The H1 executive also asked Auditor for high-confidence findings only. That is understandable for avoiding speculative noise, but a consequential unverified condition may deserve VERIFY even before a high-confidence bug is proved. The frozen Auditor instruction to challenge exactly one assumption can concentrate effort, yet its global PASS can overstate the coverage of that narrow challenge.

### Supervision frequency and representation

Continuous Terra supervision would likely replay context and charge premium prices for Luna's local work. Supervision only at the start and final PASS is too weak when a critical exception arises in between. The best redesign hypothesis is sparse, **event-triggered** intervention: before an irreversible or cross-packet commitment, after evidence contradicts an acceptance item, and before declaring completion with a known fallback. This is a proposal for a new candidate, not an instruction to alter the freeze.

The useful transferred artifact would be a compact acceptance-to-evidence relation: criterion, changed symbol, supported states, excluded states, test identity/result, workspace version, remaining hypothesis, and consequence if wrong. Executable counterexamples are more valuable than long transcripts. H1 could have been exposed by one row connecting “closed supported socket reconnects” to “SSL flagged recv rejected → readiness only.” More prose about the successful ordinary socket would not help.

A durable representation matters especially for the intended VS Code product. Its current subagent documentation says invocations are stateless and the main agent cannot follow up with the same subagent. Fresh Builder repair packets may lose rationale unless the workspace or handoff preserves it. The CLI smoke does not establish identical continuation semantics in VS Code. See S4.

### Cost dynamics and plausible winning regions

Let `p_j` be complete-task success probability, `c_j` all-in credits, `t_j` elapsed time, and `L` the user's loss from an unresolved or wrong task. One illustrative decision loss is:

`J_j = c_j + lambda * t_j + L * (1 - p_j)`

For C to beat A, its success gain must compensate for extra credits and time: `L * (p_C - p_A) > (c_C - c_A) + lambda * (t_C - t_A)`. This is a sensitivity framework; this audit does not invent the user's `L`, `lambda`, or population probabilities. A mixed model can be cheaper than B and still be the worse choice when an undetected defect is costly.

| Task distribution | Expected position of the frozen design, as an inference |
|---|---|
| Many easy local changes; OTL near ceiling | Usually pays unavoidable coordination overhead with little quality headroom |
| Hard local diagnosis dominated by interactive evidence | Vulnerable to missing the integrated premium reasoning trajectory |
| Several cheap, separable work packets with costly integration mistakes | Most credible winning region, if Terra demonstrably catches cross-packet errors |
| Long, tightly coupled tasks with weak tests | High risk: sparse summaries can conceal accumulating mistakes and confident certification |
| Mostly unsolvable tasks for both tiers | Additional cost without dependable capability; escalation is not automatically useful |

The recorded H1 premium cost advantage over B is real, but it does not buy B's observed success. More Luna is rational only while its marginal work improves a decision, validation coverage, or completed outcome. The [frozen Builder](https://github.com/YB-Park/over-the-luna/blob/0083f3d81e7339f3b22e3efaa852562d7daa07e5/agents/luna-builder.agent.md) has no numeric local search/test cap, and [Auditor](https://github.com/YB-Park/over-the-luna/blob/0083f3d81e7339f3b22e3efaa852562d7daa07e5/agents/luna-auditor.agent.md) only says bounded. Prompt thrift did not prevent substantial repeated checks.

## 6. EXPERIMENT DESIGN REVIEW

### Arm fairness and construct validity

**A/B/C are appropriate product comparators.** B is correctly defined as the default Copilot CLI coding harness with Terra selected, retaining its native behavior. Disabling B's built-in delegation to make it resemble C would answer a different question. H1 happens to contain no B subagents. “Raw” means no OTL custom agent, not a bare model API.

The experiment is **not a clean causal ablation of hierarchy**. The custom prompts, role boundaries, effort allocation, review policy, and search discipline all differ. The H1 trace records root effort as `medium`, while Terra explicitly requests `reasoning_effort: high` for both Premium leaves. Fixed root/default effort therefore did not produce equal per-role effort. This is valid evidence about the sampled product behavior if endogenous delegation settings are part of the product, but not evidence of matched-effort architecture superiority. Do not retrospectively normalize it by silently changing leaf effort.

CLI version 1.0.83 is recorded for H1, but the workflow installs unpinned `@github/copilot`; different task runs could obtain different default prompts or routing behavior. Model aliases likewise do not prove immutable backend weights. The platform gap also matters: A is a VS Code-native product evaluated under a restricted CLI tool pool; C's `target: vscode` contracts are runtime-smoked in CLI. The comparison has useful local validity and incomplete VS Code external validity.

The RFC promised a component-ablation stage before freeze. The reviewed results/history show architecture iteration on R1 and R2, but no documented matched full/no-Auditor/no-premium-owner comparison establishing component value. Changes in diagnosis ownership, prompts, and reviewer behavior between regression versions are confounded. This is an evidence gap, not proof that an undocumented experiment never occurred.

### Oracle validity and correction discipline

Replacing a helper-name-dependent test with a behavior test was warranted. Discarding a fake socket that made the accepted head fail was also warranted. Reconstructing exact frozen patches with zero new AI calls preserves the candidate freeze. These corrections improve H1; they do not retroactively make its evaluator preregistered or blind.

The final [oracle source](https://github.com/YB-Park/over-the-luna/blob/9cc97d2f61a5ea5c798a04c8ea4274f788687170/.github/workflows/premium_h1_final_oracle_once.yml) captures pytest exit codes directly and fails the workflow when the accepted reference fails. It intentionally permits failing candidate arms while the evaluation job succeeds. A green evaluation job is therefore not a passing product result. Collection errors, no tests collected, missing dependencies, and assertion failures need separate machine-readable classifications.

The oracle was revised with arm outcomes already at least partly available. Apply the same test to every frozen patch, preserve prior versions and reasons, and label the final score as a **post-run corrected oracle**. An accepted-head positive control alone is insufficient: an always-passing or overly narrow test could pass it too. A negative historical-base control and contract-violating mutants would help establish sensitivity. Their results are not shown in the final run. Any additional checks must be supplemental evaluator validation, with original scores retained and no AI rerun.

The final suite replaces neither a complete compatibility matrix nor a real-user requirement review. In particular, accepted upstream implementation shape is secondary evidence. R1's conditional-import symmetry should not be promoted from historical reference shape to universal correctness unless the task contract independently requires it. The regression ledger's partial-result caveat is appropriate.

### Isolation and artifact risks found in the workflow

The historical [H1 workflow](https://github.com/YB-Park/over-the-luna/blob/fdfdfdf3523764c79e9fc3fb4c56d5b2e750b905/.github/workflows/premium_h1_once.yml) provides shallow target repositories, but also checks out the **evaluation repository with `fetch-depth: 0`**. It materializes sibling arm workspaces, plugins, logs, and patches under one runner. Agents receive general `bash` and `--allow-all-tools`; no filesystem or network isolation is defined there. The evaluator checkout/history contains future-reference information and task metadata outside the target repository.

This is a real exposure route, not demonstrated cheating. A targeted inspection of recorded shell commands found no explicit future-history fetch, external HTTP lookup, or cross-arm shell read. That does not certify all subprocess behavior or prove an OS boundary existed. The report therefore treats contamination as **unexcluded**, not as an observed explanation of B's win.

Additional concrete risks:

- `git diff` does not capture untracked files, staged-only changes, or commits made during execution. Saving `git status` names does not preserve their bytes. H3 explicitly invites new tests/docs, so complete workspace capture matters more there. Capture HEAD, tracked changes, untracked bytes, and deletions without injecting accepted production code.
- With the runner's default error handling and `pipefail`, a failing Copilot command can exit before the following status/diff capture. `if: always()` on later upload cannot recover artifacts that were never written. Timeout, credit-cap, crash, and unavailable-model outcomes require reliable partial-artifact capture.
- Dependencies are mutable (`hiredis>=3.2.0`, unpinned pytest packages, and runner image). Recovery used a smaller dependency set and emitted coverage-filter warnings. A reproducible environment and import-path attestation are needed before comparing subtle platform behavior across runs.
- The local Redis service was unavailable, causing broader fixture failures in agent validation. Environment failure is not a model correctness failure, but resulting test gaps still limit the completion claim.
- Deleting a workflow file after launch prevents casual retriggers; it neither stops the launched job nor erases its history. It is not a billing limit or a contamination barrier.

### Task selection and repetition

The set deliberately spans ambiguity, lifecycle, feature coherence, and a control. That is useful screening diversity. It remains **four selected tasks from two Python repositories**, with two tasks sharing each repository. Repository correlation, solved-PR selection, Python bias, and evaluator familiarity all limit generalization. H4 is a tiny local key-shape fix, not the RFC's large-but-straightforward control. None has an independently calibrated human-duration baseline, repeated mission changes, or resume/compaction requirement. File count and aggregate tokens are not task horizon.

Recent historical issues reduce some contamination risk, especially relative to the documented February 2026 model knowledge cutoff, but a cutoff is not an audit of all training or post-training data. Public PRs, issue descriptions, mutable model aliases, and shared evaluator context keep memorization and selection bias possible. H1 is now development knowledge. H2–H4 identities and expected behaviors are already known to this audit; if redesign uses them, they should not later be advertised as untouched promotion holdouts.

The deterministic-patch argument for not repeating H1 is **decision-pragmatic but statistically incorrect if generalized**. Reapplying the same patch will reproduce the same failure; sampling the agent again might produce a different patch. This audit recommends no rerun because it would not repair the identified control mechanism, not because model variance has been disproved.

Three or five repeats per selected task cannot establish strong reliability. Even 5/5 independent successes have a two-sided exact 95% binomial lower bound of only about 0.48; 3/3 gives about 0.29. These bounds are illustrations, not valid population estimates for four hand-selected, correlated tasks. Repeating only favorable or ambiguous cases also changes the sampled denominator. Keep screening and repeat cohorts distinct; report every attempt and cost; never replace pass@1 with best-of-N after observing results.

The present terms “narrowly,” “material,” and “ordinary variance” leave stopping discretionary. A future evaluation needs an explicit estimand, acceptance losses, non-inferiority margin against B, minimum uplift against A, and maximum spend before sampling. Optional stopping can be handled by a declared sequential procedure or treated as descriptive screening; ordinary fixed-sample confidence claims should not be bolted on afterward.

### Cost controls and value of information

The official Copilot conversion is **one AI credit = $0.01**, not one dollar. Thus H1 raw Terra's 71.013 credits is approximately **$0.710 of metered usage**, and all three arms total **91.379 credits**, approximately **$0.914**. “Extreme cost” is a relative statement here. Included allowances, marginal billing, and developer time are different budgets. See S16.

A deliberately crude H1-cost extrapolation for three remaining triplets is about **274 credits**, or **$2.74**; it is not a forecast because task shapes differ. Their nine 100-credit ceilings allow up to **900 nominal credits** before any repeats, excluding possible in-flight overshoot. The September 7 allowance snapshot is not a current balance. This audit does not assume the remaining balance or authorize its use.

That small monetary cost is the strongest objection to stopping. The reason to stop is not an unaffordable invoice. It is low decision value relative to evaluator work, contamination of future tasks, and the need for a changed assurance mechanism anyway. H2 can demonstrate another local success; H3 can demonstrate cross-file completeness; H4 can measure overhead. None alone would justify shipping a supervisor that accepts an explicitly reported acceptance exception.

If the experiment runner chooses to finish despite this recommendation, preserve the entire original H1–H4 screen and unchanged candidate. Strong C-only H2 **and** H3 wins with coherent trace evidence would challenge this audit; all-arm passes on H3/H4 would not. Do not skip H1, count only easy wins, or use a favorable partial screen as promotion.

## 7. LATEST EXTERNAL EVIDENCE

Sources below were checked as of 2026-09-09. Dates are publication/revision dates when available; an access date is explicitly used for undated documentation. Vendor results and preprints are not independent replication of this candidate. Versioned paper metadata takes precedence over a regenerated HTML page's incidental date. No external benchmark number is used as a predicted Luna/Terra effect size.

| ID | Source, organization/authors, date, direct URL | Evidence type | Exact implication and limitation |
|---|---|---|---|
| S1 | **Project HydraFusion: Frontier quality via multi-model orchestration** — GitHub Staff, **2026-09-04**. [Source](https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/) | Vendor controlled offline benchmark; research preview | Selects single, cascade, or critique; critique uses another model family. Reports 67% lower estimated cost and +4.9 percentage points on TerminalBench 2.1 against Opus 5, but DeepSWE is −1.5 points at 36% lower cost. Best tuned policies and development reuse limit independence. Supports adaptive composition, not mandatory hierarchy. Preview is best suited to first-turn, single-prompt work; it does not establish long-session superiority. |
| S2 | **How we made GitHub Copilot CLI more selective about delegation** — Pingping Lin and Yu Hu, GitHub/Microsoft, **2026-06-12**. [Source](https://github.blog/ai-and-ml/how-we-made-github-copilot-cli-more-selective-about-delegation/) | Production A/B plus offline evaluation | Reports 23% fewer tool failures/session and 5% lower P95 wait without quality regression. Delegation should buy independent work or useful context isolation. H1's serial mandatory roles face a real opportunity cost; these aggregate production effects do not specify the right custom-agent boundary. |
| S3 | **How we make AI coding more cost efficient without sacrificing task quality** — Erik Kristensen and Napalys Klicius, GitHub, **2026-09-02**. [Source](https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/) | Production engineering; controlled online validation of selected changes | Optimizes complete-task work and useful context, not shortest responses. Supports measuring rereads, recovery, cache behavior, and outcome cost. It argues against both a transcript-heavy Terra and excessively compressed evidence that creates more work. |
| S4 | **Use subagents in Visual Studio Code** — Microsoft/VS Code, page updated **2026-09-02**. [Source](https://code.visualstudio.com/docs/agents/run/subagents) | Official runtime documentation | Describes isolated contexts returning summaries and stateless invocations. A CLI structural pass does not certify durable Builder continuity or identical tool behavior in VS Code. Runtime-specific state transfer needs evidence. Documentation examples are not benchmark proof of quality gains. |
| S5 | **Harness design for long-running application development** — Prithvi Rajasekaran, Anthropic Labs, **2026-03-24**. [Source](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Engineering case studies; not a matched-budget population trial | High-level plans, generator/evaluator contracts, and active application testing helped. One example compares 20 minutes/$9 with six hours/$200 and expanded scope. Evaluator skepticism required tuning; stronger models made prior harness pieces unnecessary. Supports bounded contracts and behavioral QA, not a claim that this mixed-tier harness is cheaper or already calibrated. |
| S6 | **TeamBench: Evaluating Agent Coordination under Enforced Role Separation** — Yubin Kim et al., MIT/Google and collaborators, **2026-05-08**, v1. [Paper](https://arxiv.org/html/2605.07073v1) | Benchmark and controlled role ablations | Verifiers approve about 49% of grader-failing submissions in the reported role-mixing analysis; removing verification improves partial score in an ablation. The verified subset lowers the false-accept estimate to about 39%, illustrating grader sensitivity. OS separation and role value are distinct. Task construction deliberately makes coordination necessary, unlike ordinary shared-repository coding; do not transfer the rate to Luna. |
| S7 | **Towards a Science of Scaling Agent Systems** — Yubin Kim et al., **2025-12-09**, revised **2026-04-08**, v3. [Paper](https://arxiv.org/html/2512.08296v3) | Controlled mechanism/benchmark study | Latest revision covers 260 configurations and six benchmarks, beyond the older 180-configuration blog summary. Architecture alignment and capability saturation matter; tool-heavy and sequential work can lose from coordination. Cross-validated fit is modest and cross-domain absolute prediction is limited. Its approximate thresholds are not a universal routing rule for Terra/Luna. |
| S8 | **SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent** — Yikai Zhang et al., Microsoft/academic collaborators, **2026-04-28**, revised **2026-05-26**, v2. [Paper](https://arxiv.org/html/2604.26102v2) | Repository benchmark and interface/model ablations | Reports +2.1 points resolved and −17.9% inference cost from Viewer/Editor decomposition. This isolates code-access/edit interfaces while retaining main reasoning. It supports context separation conditionally; it does not validate delegating the entire local causal problem away from the premium model. |
| S9 | **Scrouting: Cost-Aware Routing of Coding Agents by Scouting the Repository First** — Ishaan Bhola, Adithyan Krishnan, Mukunda NS, SuperAGI, **2026-08-05**, v1. [Paper](https://arxiv.org/html/2608.04804v1) | Repository benchmark plus calibration/ablation | On 266 Python tasks, the reported cheap-fixer-plus-handoff ablation ties the routed system. This is a direct warning against attributing system gains to the expensive routing component. Claims are checked before handoff; the headline involves only three repositories, fixer contamination is unknown, and handoff contrasts are not statistically significant. Useful mechanism evidence, not a reusable price ratio. |
| S10 | **CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents** — Qijia He et al., UW/NYU/ByteDance and collaborators, **2026-07-21**, v1. [Paper](https://arxiv.org/html/2607.19338v1) | Controlled recovery-routing benchmark | Uses execution feedback to choose reflection, replanning, or escalation. Cheap recovery and escalation have different solve sets. Its cost guarantee is marginal and assumes exchangeability; benchmarks include function/competitive coding rather than this full repository workflow. Supports selective phase-boundary decisions, not a guarantee that expensive judgment is always necessary after failure. |
| S11 | **From Spark to Fire: Modeling and Mitigating Error Cascades in LLM-Based Multi-Agent Collaboration** — Yizhe Xie et al., City University of Macau/Minzu University, **2026-03-04**, revised **2026-05-11**, v2. [Paper](https://arxiv.org/html/2603.04474v2) | Controlled cascade/attack and mitigation study | Models message dependencies, amplification, and consensus inertia. Supports preserving claim provenance and distinguishing repeated assertions from independent evidence. Seeded error propagation is not an estimate of naturally occurring H1-like failures, and this audit does not recommend adding its governance layer wholesale. |
| S12 | **Why Do Multi-Agent LLM Systems Fail?** — Mert Cemri et al., UC Berkeley/Intesa Sanpaolo, **2025-03-17**, revised **2025-10-26**, v3. [Paper](https://arxiv.org/html/2503.13657v3) | Trace-based empirical taxonomy | Latest version describes 1,600+ traces, seven frameworks, and 14 failure modes covering design, alignment, and verification. Useful for classifying ignored evidence and premature approval. Older model families and observational labels do not establish the marginal effect of Terra or Auditor here. |
| S13 | **Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents** — Chenyu Zhao et al., **2026-05-09**, revised **2026-06-05**, v2. [Paper](https://arxiv.org/abs/2605.08717v2) | Controlled recovery benchmark; enterprise prototype | PROBE grounds bounded recovery in actual failed-run telemetry. Diagnosis and successful recovery remain different outcomes. It supports using a concrete contradiction to trigger intervention. It does not support the retired pre-mutation Causal Probe merely because their names resemble one another. |
| S14 | **AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation** — Priyam Sahoo et al., **2026-05-13**, revised **2026-06-02**, v3. [Paper](https://arxiv.org/abs/2605.12925v3) | Trajectory benchmark/observational process analysis | Passing outcomes can hide unstable or wasteful trajectories. Supports inspecting rework and missing validation alongside hidden behavior. Its process references are built from passing trajectories; process similarity must not become a requirement to reproduce the accepted patch or overturn a valid behavioral success. |
| S15 | **Scaling Test-time Compute for LLM Agents** — King Zhu et al., M-A-P/OPPO and collaborators, **2025-06-15**, v1. [Paper](https://arxiv.org/html/2506.12928v1) | Controlled test-time-compute benchmark | Timing of reflection, verification, and diversified rollouts matters. Supports testing the marginal value of added inference; does not show that repeated same-model audit buys useful diversity or that one fixed topology is optimal. Use the arXiv submission date rather than the incidental later HTML date. |
| S16 | **Models and pricing for GitHub Copilot** — GitHub, undated live documentation, accessed **2026-09-09**. [Source](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) | Official billing/runtime reference | Converts token use to $0.01 AI credits, includes cache writes, and specifies different long-context thresholds: Luna >200K, Terra >272K input tokens. This differs from the API model-page threshold and prevents substituting API pricing for Copilot accounting. Cumulative token totals cannot identify which requests crossed a threshold. |
| S17 | **ssl — TLS/SSL wrapper for socket objects**, Python **3.12.14** — Python Software Foundation/contributors; undated versioned documentation, accessed **2026-09-09**. [Source](https://docs.python.org/3.12/library/ssl.html) | Official technical specification/documentation | Nonzero receive flags are unsupported and TLS buffering can differ from kernel readiness. The H1 fallback is a meaningful supported-socket concern. A wrapper that rejects flags validates that branch but cannot certify full TLS lifecycle semantics. |
| S18 | **GPT-5.6 Luna / GPT-5.6 Terra model pages** — OpenAI; undated live documentation, accessed **2026-09-09**. [Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), [Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra) | Official model documentation; not a comparative experiment | Documents Luna's cost-sensitive role, Terra's intelligence/cost positioning, supported reasoning efforts, 1.05M context windows, and February 16, 2026 cutoff. Does not establish that Terra's advantage is specifically mission management, quantify this task distribution, or prove absence of post-training contamination. |
| S19 | **Evaluation best practices** — OpenAI; undated live documentation, accessed **2026-09-09**. [Source](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Official methodological guidance/opinion | Emphasizes nondeterminism, task-specific distributions, logged evidence, and human calibration. Supports a versioned evaluator and separation of product outcomes from component behavior. These principles do not require adopting the hosted Evals service or changing the frozen harness. |
| S20 | **Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading** — Zongxia Li et al., **2026-07-09**, revised **2026-07-13**, v2. [Paper](https://arxiv.org/abs/2607.08964v2) | Long-horizon benchmark | Defines 46 tasks with intermediate graded subtasks and reports long, iterative runs. Shows a concrete way to separate progress from complete success. Does not imply this benchmark is an economical next experiment; its different workloads and grading thresholds should not be imported as the product's definition of success. |

Taken together, the literature supports **selective, evidence-driven allocation and component ablation**. It does not support “always add hierarchy,” but also does not support “never split a trajectory.” HydraFusion is a relevant competitive alternative for a future product review, not an arm to add opportunistically to this freeze. Its preview's tuning history and limited long-session scope should receive the same skepticism as this repository's regression history.

## 8. WHAT WOULD CHANGE MY MIND

The verdict is revisable; the following observations would have genuine decision value. These are counterfactual update criteria, not authorization to run experiments or new retrospective scoring rules.

| Observation | Update |
|---|---|
| Existing, previously omitted controlled evidence shows Terra repeatedly catches acceptance-critical errors that Luna Builder/Auditor miss, at bounded incremental cost | Reconsider stopping; resolves the largest missing component-value claim |
| A valid, already produced trace shows the H1 exception never reached the executive | Withdraw the “visible evidence ignored” mechanism; the inspected log currently shows the opposite |
| Independent supported-platform testing invalidates the fourth oracle's acceptance relevance, rather than merely disliking its outcome | Downgrade H1's negative correctness evidence; preserve its other results and overhead |
| If unchanged H2/H3 are completed by a separately authorized runner: C fully passes both where A fails, approximately matches B at materially lower complete-task cost, and Terra makes identifiable integration corrections | Materially favor a narrow feature/lifecycle premium niche; still no broad reliability or horizon certification |
| C only ties A on H2/H3, or its PASS again accepts a declared critical gap | Stronger stop signal; further same-candidate repetition has little value |
| All arms pass H4 | Little capability update; use only correctness-regression and overhead evidence |
| A future genuinely fresh evaluation shows a reproducible quality/cost point better than both A and B on the declared workload mix, including latency and false-acceptance constraints | Favor the premium hypothesis and the tested new design |
| Several materially different, competently evaluated premium designs fail to beat simple baselines, and representative task outcomes show no exploitable cheap/expensive complementarity | Consider killing the product hypothesis; current evidence does not meet that bar |

The product owner must decide what counts as “material” before another confirmatory phase. A numerical threshold chosen now and applied to H1 would be post hoc. In particular, a single C-only pass cannot establish reliability, and an eloquent Terra explanation is not evidence that the explanation caused the pass.

## 9. FREEZE-SAFE RECOMMENDATIONS

These recommendations concern evaluator/process work only. They are not implemented by this audit, and none permits new paid runs under the current request.

| Proposed action | Freeze classification and conditions |
|---|---|
| Preserve original H1 log, all arm patches, statuses, commands, evaluator versions, and hashes | Safe archival work; no candidate-visible feedback |
| Reconcile credits, root/leaf effort, cache dimensions, test collection, and per-role tool/time counts from existing artifacts | Safe analysis; retain raw values and mark missing fields |
| Correct false-green handling or distinguish assertion failure from collection/infrastructure failure | Safe evaluator correction; no candidate changes or AI reruns |
| Repair a helper-specific oracle or impossible fake socket | Safe only when acceptance meaning is preserved, correction rationale is recorded, and the same version is applied to all frozen patches |
| Validate an oracle against accepted behavior, the original base, and contract-breaking mutants | Safe supplemental evaluator validation; distinguish these checks from the original score and never feed them to the candidate |
| Preserve complete workspace state, including new files, deleted files, index state, and HEAD | Safe capture/process improvement; avoid changing the candidate's visible work or tool responses |
| Preflight dependencies, services, and accepted-test collection outside model-visible workspaces | Safe infrastructure repair if it restores the declared environment; record version changes and do not pool incompatible environments silently |
| Enforce the protocol's existing no-future/no-external boundary using isolated arm filesystems and network restrictions | Candidate prompts may remain frozen, but this changes realized runtime exposure; declare an evaluator/environment revision and keep H1 tagged with its original environment. If legitimate tool behavior changes, treat it as a new comparison condition |
| Record a decision to stop this phase and reserve unopened tasks | Safe governance; no need to edit frozen agent contracts |

**Not freeze-safe:** strengthening Terra's acceptance gate, changing the Auditor rubric or model, passing a new runtime evidence schema, adding SSL examples, changing Builder search budgets, altering effort allocation, allowing Terra direct tools, adding/removing mandatory agents, or adding a recovery route. An external shim that changes what a candidate sees or when it is interrupted is a candidate change even if the Markdown files are byte-identical. These require declaring REDESIGN, a new candidate identity, and a new freeze.

Changing task wording, adding a stricter success requirement, changing arm order, or replacing the task set is an evaluation-design change, not an “oracle fix.” It must be versioned and cannot silently inherit the original comparison claim. The primary runner owns any future result-ledger updates; this audit supplies recommendations only.

## 10. REDESIGN IDEAS — DO NOT IMPLEMENT

1. **Acceptance evidence before executive approval.** Make every consequential exception explicit against a criterion, with its test/counterexample and residual status. Apply critical-belief handling regardless of whether Terra, Builder, Architect, or Auditor originated the claim. The first mechanism to investigate is correct action on visible evidence, not a larger transcript.

2. **Preserve one local implementation trajectory; buy premium evidence at specific uncertainty boundaries.** Consider a Luna-owned default trajectory with a bounded Terra adjudication or diagnostic episode when an acceptance-critical contradiction appears. An alternative is a Terra owner with narrowly scoped evidence access and cheaper mechanical work. These are distinct hypotheses; avoid implementing both at once or reinstating a causal manager chain.

3. **Make assurance orthogonal and measurable.** Compare the added audit with no added audit, a behavior-focused verifier, and a bounded different-model critic under comparable total budgets on development data. Measure critical defects caught, false PASS, false REPAIR, and introduced regressions. A different model is not automatically independent; changed evidence and adversarial state coverage must matter.

4. **Use durable, revision-linked work state for actual horizon.** Track accepted criteria, dependencies, evidence, unresolved states, and workspace identity across packets/resumption. Avoid asking Architect to certify a permanently complete unknown work set. Reopening a boundary should have a named cause and preserve local reasoning needed for repair.

5. **Make expensive topology optional within a single premium product choice.** Single, critique, and escalation paths may serve different task distributions without asking the user to choose models repeatedly. Keep model-identity preferences subordinate to measured complete-task outcomes. If a simpler cheap model plus verified handoff performs equally well, remove Terra from that path.

These are research directions, not a replacement candidate. H1 must become a retained development regression for any design informed by this audit. The next promotion holdout must be fresh relative to that design process.

## 11. NEXT ACTION

1. **Stop the current frozen paid screening and declare REDESIGN for the next candidate.** Keep H1's corrected failure and all existing snapshots intact; do not run H2–H4 merely to complete a table.
2. **Close the zero-AI evidence/accounting record and specify the product decision.** Preserve artifacts, classify evaluator/environment limitations, and define the intended workload distribution, complete-task quality bar, latency tolerance, and spend tradeoff before changing agents.
3. **Only after those decisions, evaluate the smallest justified redesign under a new freeze and fresh holdout.** Component value and a real task-horizon measure must precede a promotion claim. If no narrow viable region can be articulated, stop premium development rather than adding more orchestration.

## 12. EVIDENCE QUALITY / UNCERTAINTY

### Strength of the findings

| Finding | Confidence | Reason |
|---|---|---|
| H1 final evaluator records B/reference 4/4 and A/C 3/4 | HIGH | Direct exit codes and pytest results inspected |
| Premium's SSL-like limitation reached Terra and Auditor | HIGH | Explicit Builder handback, audit input, and Auditor output in the original log |
| Failure was caused specifically by architecture rather than sampled model behavior | LOW–MEDIUM | Mechanism is plausible; no randomized architecture ablation isolates it |
| Current prompts/validator match the candidate freeze at the audit head | HIGH | Repository comparison shows only handoff/protocol/results additions since freeze |
| H1 had no contamination | UNESTABLISHED | No explicit relevant shell access found in targeted inspection, but no structural isolation proof |
| Premium has no useful product niche | LOW | Only one held-out task, no representative distribution |
| Stop and redesign is the best next investment | MEDIUM | Strong control-loop concern and weak horizon measurement; inexpensive remaining screening is a legitimate competing choice |

The audit read the handoff fully and the 13 required files in its specified order. Additional review covered relevant history on this branch, the H1 workflow and corrected evaluator source, original structured execution events, final evaluator logs, and accepted Redis parser code. It did not re-execute any candidate or tests, independently reconcile a billing invoice, inspect provider training data, or perform an exhaustive semantic audit of every terminal-output byte. Public research is mostly vendor-reported or preprint evidence with different models and workloads. No paper establishes the precise Luna/Terra arrangement's frontier.

The static validator checks manifests, model/tool declarations, names, and contract markers. It cannot prove that a shell is non-mutating, that evidence is correct, that a belief is genuinely verified, or that a PASS is justified. The only current workflow at the audit starting head is ordinary plugin validation with `contents: read`; the report does not add an experiment workflow. No broader runtime assurance is inferred from static validation.

### Repository evidence index

All project-document links below are pinned to the reviewed audit starting head rather than a moving branch. Runtime logs are immutable run/job references subject to GitHub retention. The report itself is the sole committed audit deliverable.

| Evidence | Location |
|---|---|
| Handoff and authorized scope | [ASTRA_WORK_HANDOFF.md](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/ASTRA_WORK_HANDOFF.md) |
| Stable product | [README.md](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/README.md), [DESIGN.md](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/DESIGN.md), [CONTRIBUTING.md](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/CONTRIBUTING.md) |
| Product hypothesis and regression record | [RFC](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/PREMIUM_HARNESS_RFC.md), [regression results](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/PREMIUM_HARNESS_RESULTS.md) |
| Frozen protocol and reported H1 | [protocol](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/PREMIUM_HELDOUT_PROTOCOL.md), [held-out results](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/docs/PREMIUM_HELDOUT_RESULTS.md) |
| Agent contracts | [OTL](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/agents/over-the-luna.agent.md), [Premium](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/agents/premium-harness.agent.md), [Builder](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/agents/luna-builder.agent.md), [Auditor](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/agents/luna-auditor.agent.md), [Architect](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/agents/luna-architect.agent.md) |
| Static validation and current workflow | [validator](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/scripts/validate_plugin.py), [validate.yml](https://github.com/YB-Park/over-the-luna/blob/8bf018cfa3a608241b800c3f4610bc2f41bd2364/.github/workflows/validate.yml) |
| Original H1 environment and execution | [workflow at fdfdfdf3](https://github.com/YB-Park/over-the-luna/blob/fdfdfdf3523764c79e9fc3fb4c56d5b2e750b905/.github/workflows/premium_h1_once.yml), [run 34325241072 / job 102380885415](https://github.com/YB-Park/over-the-luna/actions/runs/34325241072/job/102380885415) |
| Final evaluator and independent log check | [source at 9cc97d2f](https://github.com/YB-Park/over-the-luna/blob/9cc97d2f61a5ea5c798a04c8ea4274f788687170/.github/workflows/premium_h1_final_oracle_once.yml), [run 34352923102 / job 102470343867](https://github.com/YB-Park/over-the-luna/actions/runs/34352923102/job/102470343867) |
| Accepted H1 reference | [Redis hiredis.py at 55d41593](https://github.com/redis/redis-py/blob/55d41593d3795080cdfc090ed56c19d9ab4ea3b1/redis/_parsers/hiredis.py) |

The final evaluator logged these SHA-256 hashes for the input diffs; this audit uses them as provenance receipts from that run, not as newly recomputed checksums:

| Arm | Diff SHA-256 |
|---|---|
| A | `b8f000e8c7fd1bf8c75dc172045ce4e9e9d53820c78d03869f16c5b84204f09a` |
| B | `2eff2af6929f8cda0824a8447f5f35445785cc15aa3bff4dcbceab233f4c38b6` |
| C | `1b42a46f097f8d3decc4d5166349fac4b9a06993701a63888eabc67f58847bcf` |

The strongest remaining objection to this verdict is that H2/H3 might cheaply identify the very integration niche the design targets. The strongest reason the verdict survives that objection is that H1 already exposed failure to act on an explicit, acceptance-critical limitation, while the pending screen has no calibrated rule for deciding whether occasional wins compensate. That supports stopping **this freeze** without claiming the premium hypothesis is dead.
