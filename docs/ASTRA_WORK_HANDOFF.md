# Astra Work Handoff — Independent Premium Harness Audit

Status: **independent external audit request**  
Target branch: `research/astra-premium-audit`  
Source snapshot: `experiment/premium-luna-orchestration@2968f86f19cfc29100e67e18623858c4e967fa35`  
Frozen candidate snapshot: `0083f3d81e7339f3b22e3efaa852562d7daa07e5`

## Why you are being asked

This repository began as a strongly Luna-first coding harness: use GPT-5.6 Luna broadly because its cost/performance is unusually strong, and buy expensive judgment only when it earns its place.

A new experiment asks whether a **premium product tier** can preserve that Luna-first identity while using a sparse expensive root model to organize larger work:

- Terra root owns mission, acceptance, global coherence, and adjudication.
- Luna owns repository evidence, implementation, tests, and audit.
- User selects only the product tier; the user does not route Luna vs Terra inside the run.

The current candidate is frozen. Your job is **not to help it win**. Your job is to determine whether the product hypothesis, architecture, and evaluation protocol are actually sound.

You are an independent red-team reviewer.

## What to read first

Read these repository files in order:

1. `README.md`
2. `docs/DESIGN.md`
3. `CONTRIBUTING.md`
4. `docs/PREMIUM_HARNESS_RFC.md`
5. `docs/PREMIUM_HARNESS_RESULTS.md`
6. `docs/PREMIUM_HELDOUT_PROTOCOL.md`
7. `docs/PREMIUM_HELDOUT_RESULTS.md`
8. `agents/over-the-luna.agent.md`
9. `agents/premium-harness.agent.md`
10. `agents/luna-builder.agent.md`
11. `agents/luna-auditor.agent.md`
12. `agents/luna-architect.agent.md`
13. `scripts/validate_plugin.py`

Also inspect relevant Git history on this branch only when needed to understand experiment chronology. Do not modify the frozen candidate.

## Current experiment state

### Stable product

Current stable Over the Luna:
- Main Luna owns implementation and commands.
- Short-lived Luna leaves provide isolated evidence/judgment.
- Premium Sonnet review is human-selected only.
- Stable philosophy: `Use more Luna. Pay for judgment only when it earns its place.`

### Earlier Terra Deep Judgment experiment

A separate prior experiment tested a human-selected Terra checkpoint.

Important findings:
- ordinary/harness-level problem: Luna and Terra reached the same correct decision while Terra cost materially more;
- aiohttp concurrency/body-integrity planning cases: Terra made materially better judgments;
- held-out httpcore root-cause E2E: Terra chose and amplified the wrong causal model;
- held-out Django lifecycle E2E: Terra judgment + Luna implementation passed accepted hidden behavior that Luna-only missed.

Product conclusion from that experiment:
- Terra has real strengths;
- those strengths did not produce a safe user-facing `Luna vs Terra` routing rule;
- therefore the experiment pivoted from **model selection** to **premium orchestration**.

### Current Premium hypothesis

> Can a Terra-rooted, Luna-workhorse harness extend reliable task horizon beyond Over the Luna while outperforming raw Terra on cost-efficiency and robustness?

The candidate must justify itself against **both**:
1. current Over the Luna;
2. simply selecting raw Terra in the default Copilot coding harness.

### Frozen Premium architecture

Default shape is intentionally shallow:

```text
Terra mission owner
      |
      v
Luna Builder
local diagnosis + mutation + focused validation
      |
      v
Luna Auditor
independent correctness + simplicity challenge
      |
      v
Terra adjudication
```

Luna Architect is used only when broad repository structure/dependency/work-set discovery is genuinely needed. Luna Researcher is conditional on current external facts.

A dedicated Causal Probe was tried and **removed** because:
- it exceeded its evidence budget;
- it still reinforced the wrong intervention class on the known httpcore regression;
- more agent hierarchy did not earn its coordination cost.

### Regression laboratory

Phase 0 structural smoke:
- Terra root stayed tool-thin;
- one Luna Builder mutated;
- one Luna Auditor independently checked;
- hidden deterministic oracle passed.

Known-case regressions:
- httpcore R1-v1: partial causal improvement but broad Architect pass cost too much;
- httpcore R1-v2: dedicated Causal Probe failed and amplified lock-based design;
- httpcore R1-v3: simplified Builder-owned diagnosis cut cost roughly in half and avoided the lock machinery, but still did not reproduce all accepted historical structural behavior;
- Django lifecycle R2: frozen premium architecture passed the accepted hidden test suite 22/22.

Candidate was then frozen.

## Held-out protocol

Frozen held-out arms:

### A — Current Over the Luna
Stable v1.1 agent, GPT-5.6 Luna.

### B — Raw Terra
Default GitHub Copilot CLI coding-agent harness, GPT-5.6 Terra. No Over the Luna custom agent.

### C — Frozen Premium
Terra root + Luna workhorse/auditor, exact frozen agent snapshot.

Rules:
- identical historical base per arm;
- shallow history;
- no future commits/PRs during model execution;
- accepted tests/material fetched only after all arms finish;
- hidden behavior oracle is primary correctness metric;
- candidate prompts/contracts are frozen;
- evaluator-only oracle fixes are allowed if they do not rerun AI and are validated against accepted behavior.

## First held-out result — H1 Redis-py RESP3/hiredis close behavior

Task:
- distinguish a peer-closed pooled connection from a readable connection containing pending RESP3 push data;
- do not consume/discard pending push merely to test closure.

Final corrected implementation-independent oracle was validated against the accepted Redis head.

Results:

| Arm | Hidden correctness | AI credits | Wall time |
|---|---:|---:|---:|
| Over the Luna | 3/4 FAIL | ~5.69 | 167s |
| Raw Terra | 4/4 PASS | ~71.01 | 222s |
| Frozen Premium | 3/4 FAIL | ~14.67 | 355s |

Key failure:
- Over the Luna and Premium both used a non-destructive `MSG_PEEK` strategy;
- on an SSL-like wrapper where `recv(..., flags)` raises `ValueError`, both treated the socket as readable and missed a real EOF;
- Raw Terra instead read into the persistent hiredis parser buffer after readiness, so EOF raised the existing connection error while pending push data remained available to `read_response()`.

Premium therefore spent about 2.6x OTL and took about 2.1x wall time without improving hidden correctness. Its Auditor still returned PASS.

Raw Terra bought a real correctness edge, but at extreme cost.

This is a **material negative held-out result for the frozen Premium candidate**, not yet a final product verdict.

## Your audit mission

Perform a deep independent review using current public evidence, not just this repository's self-description.

You should:

1. **Challenge the product hypothesis itself.**
   - Is `Terra executive + Luna workhorse` actually a credible Pareto-frontier strategy?
   - Under what task distributions could it win?
   - Under what distributions is it structurally doomed to be slower/more expensive without quality gain?

2. **Review the architecture as a control system.**
   - Is Terra too far from local evidence?
   - Does Luna Builder receive too much autonomy for Terra to add value?
   - Does Luna Auditor duplicate Builder validation rather than provide orthogonal assurance?
   - Is the hierarchy still too deep or already too shallow?
   - Should the expensive model supervise mission state continuously, sparsely, or only at specific phase boundaries?
   - Is a different artifact/state representation needed between Luna and Terra?

3. **Review the H1 failure carefully.**
   - Was Premium's failure caused by the basic orchestration thesis, an assurance blind spot, context compression, task routing, tool boundaries, or ordinary stochastic model behavior?
   - Does H1 suggest Raw Terra has access to a useful integrated tool/reasoning trajectory that the split architecture breaks?
   - Does splitting diagnosis/implementation/audit across models destroy important local continuity?

4. **Review the held-out protocol.**
   - Are A/B/C fair product comparisons?
   - Is Raw Terra defined correctly?
   - Is the hidden-oracle procedure sound?
   - Are task strata sufficient?
   - Are repetition rules statistically defensible under the available budget?
   - Identify contamination, evaluator overfitting, model-memory, selection-bias, and infrastructure risks.
   - Explicitly distinguish **evaluator-only corrections allowed under freeze** from **candidate changes that would require declaring REDESIGN and starting a new freeze**.

5. **Study the latest external evidence.**
   Use current sources, preferring:
   - OpenAI official model/system documentation;
   - GitHub Copilot / VS Code official engineering posts and docs;
   - recent papers on multi-agent orchestration, model routing, long-horizon coding, context engineering, evaluator design, test-time scaling, and multi-model systems;
   - credible production studies.

   Include dates and direct source URLs.

   In particular, compare this design against current work such as:
   - GitHub Project HydraFusion;
   - selective delegation in Copilot CLI;
   - long-running harness work;
   - multi-agent failure/cascade studies;
   - any newer work you find that materially changes the picture.

6. **Decide whether the current frozen evaluation should continue.**
   Do not reflexively recommend more experiments.
   Consider the value of information vs cost.

7. **If you recommend continuing H2–H4 unchanged**, explain what outcomes would materially update your belief.

8. **If you recommend stopping**, distinguish:
   - stop this frozen candidate and redesign;
   - kill the premium product hypothesis entirely;
   - collect more evidence before either.

## Important constraints

### Do not modify the frozen experiment

Do not edit:
- `agents/premium-harness.agent.md`
- `agents/luna-builder.agent.md`
- `agents/luna-auditor.agent.md`
- any other frozen candidate agent/prompt/validator contract.

Do not create a replacement candidate in this audit.

### Do not run paid Copilot experiments

Do **not**:
- create/run any GitHub Action using `copilot-requests: write`;
- invoke GitHub Copilot CLI paid model tests;
- consume the repository owner's Copilot AI credits;
- rerun H1/H2/H3/H4.

You may use your own ChatGPT Work/Astra allowance for analysis.

### Do not alter experiment result files

Do not edit:
- `docs/PREMIUM_HARNESS_RESULTS.md`
- `docs/PREMIUM_HELDOUT_RESULTS.md`

Those remain owned by the primary experiment runner.

### Luna-first identity is a prior, not evidence

The project has a deliberate emotional/product identity around Luna's low-cost abundance.

Respect it as product context, but **challenge it if it causes bad engineering or evaluation decisions**. Do not give Luna a free pass because the project likes Luna.

### Be adversarial, not supportive

Do not optimize for agreement with the current design.
The most useful result may be:
- continue;
- redesign;
- or kill the idea.

## Required output

Create exactly one primary report:

`docs/ASTRA_PREMIUM_AUDIT.md`

Commit it to:

`research/astra-premium-audit`

Do not modify any other existing file.

The report must use this structure:

# Astra Independent Premium Harness Audit

## 1. EXECUTIVE VERDICT

Choose exactly one:
- `CONTINUE_FROZEN_EVALUATION`
- `STOP_AND_REDESIGN`
- `KILL_PREMIUM_HYPOTHESIS`
- `INSUFFICIENT_EVIDENCE`

Include confidence: LOW / MEDIUM / HIGH.

## 2. STRONGEST CASE FOR THE CURRENT DESIGN

Steelman it.

## 3. STRONGEST CASE AGAINST THE CURRENT DESIGN

Red-team it.

## 4. H1 FORENSIC INTERPRETATION

Explain what H1 actually teaches and what it does **not** prove.

## 5. ARCHITECTURE REVIEW

Review:
- Terra role;
- Luna Builder role;
- Auditor role;
- context/state transfer;
- phase boundaries;
- delegation depth;
- failure containment;
- cost dynamics.

## 6. EXPERIMENT DESIGN REVIEW

Evaluate:
- arm fairness;
- hidden oracle validity;
- task selection;
- freeze discipline;
- repetition/statistics;
- contamination risks;
- cost controls.

## 7. LATEST EXTERNAL EVIDENCE

For each source:
- title;
- organization/authors;
- publication/update date;
- URL;
- exact implication for this experiment;
- whether evidence is production, benchmark, controlled mechanism study, or opinion.

## 8. WHAT WOULD CHANGE MY MIND

Give concrete observations that would update the verdict in either direction.

## 9. FREEZE-SAFE RECOMMENDATIONS

Only evaluator/process changes that can occur **without changing the frozen candidate**.

## 10. REDESIGN IDEAS — DO NOT IMPLEMENT

If and only if redesign is recommended, list candidate ideas separately.
Do not modify repo agents.

## 11. NEXT ACTION

Give at most three actions in priority order.

## 12. EVIDENCE QUALITY / UNCERTAINTY

Identify weak points in your own audit.

## Handoff back to the primary experiment runner

When complete:
1. commit `docs/ASTRA_PREMIUM_AUDIT.md` to `research/astra-premium-audit`;
2. report the resulting commit SHA to the user;
3. do not merge the branch;
4. do not open or merge a PR unless explicitly asked.

The primary experiment runner will read the committed report and decide whether to continue H2–H4.
