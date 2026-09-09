# Astra Work Handoff — Premium v2.1 Final Pre-Implementation Review

Status: **final design gate before any implementation**  
Target branch: `research/astra-premium-v2-1-design`  
Revised RFC commit: `9991878aa93e6d3058103ac32a9edea510bcbc32`  
Your prior v2 audit: `bcccc43d2250fc7771fda4e9ed3da76a1ca01401`

## Mission

You previously returned:

> `REVISE_BEFORE_IMPLEMENTATION` — HIGH confidence

The primary runner accepted the central critique and replaced the broad adaptive L/T/M design with a much smaller v2.1 hypothesis.

Your task now is **not** another open-ended architecture brainstorm.

Your task is:

> Determine whether the revised v2.1 specification has resolved the P0 blockers sufficiently to justify a small implementation/compliance experiment.

Do not implement anything and do not run paid Copilot.

---

## Read in this order

1. Your prior report:
   `docs/ASTRA_PREMIUM_V2_DESIGN_AUDIT.md`
2. Revised RFC:
   `docs/PREMIUM_V2_1_MINIMAL_CASCADE_RFC.md`
3. Prior v2 RFC only for delta/context:
   `docs/PREMIUM_V2_PRE_IMPLEMENTATION_RFC.md`
4. Prior H1 / v1 evidence only as needed:
   - `docs/PREMIUM_HELDOUT_RESULTS.md`
   - `docs/PREMIUM_HARNESS_RESULTS.md`
   - prior Astra audit.

The revised RFC is the object under review.

---

## What changed

The revised design intentionally removes most of v2:

- no L/T/M predictive router;
- no Lane M;
- no Verifier;
- no Architect by default;
- no repeated up/down model switching;
- no automatic cross-family review.

Candidate hypothesis:

```text
bounded Terra intake
    ->
one continuous Luna Builder attempt
    ->
completion reconciliation
    ->
if concrete blocking semantic evidence remains:
    one Terra takeover
    ->
final reconciliation
```

The root may not pre-scout/solve before Luna.

Takeover is monotone L -> T only.

The design adds:
- ordered acceptance authority U/R/A;
- compact criterion register;
- runtime execution receipts;
- machine controller outcomes distinct from model prose;
- explicit hook-failure semantics;
- quiescent mutation ownership transfer;
- full-attempt economics;
- sealed post-freeze sampling with independent future randomness;
- evaluator isolation;
- finite development/pilot budget;
- program-level kill rule.

---

## Primary review question

Choose whether **this exact minimal hypothesis** is sufficiently specified to spend the next small amount of Copilot credits implementing/testing it.

Do not reject merely because semantic correctness cannot be formally guaranteed.

Do reject/revise if the document still claims an enforcement property the runtime cannot plausibly provide or if the experiment cannot identify the candidate's value.

---

## Required checks against your prior P0 findings

For every item below, mark:
- `RESOLVED`
- `PARTIALLY_RESOLVED`
- `UNRESOLVED`

### P0-A — executable routing policy

Does the one-way rule now define:
- initial path;
- evidence-based escalation;
- no-escalation classes;
- termination;
- excluded components?

Is there still hidden self-routing ambiguity large enough to confound the experiment?

### P0-B — acceptance trust boundary

Does v2.1 correctly distinguish:
- record consistency;
- semantic judgment;
- user-visible prose?

Is the criterion-register + runtime-receipt proposal the smallest plausible useful control?

Does the stop-hook failure behavior avoid an impossible hard guarantee?

### P0-C — acceptance authority / waiver

Are U/R/A authority and waiver semantics sufficient?

Can a model still launder a user requirement through reclassification in a way the proposed deterministic controller would silently accept?

If so, specify the smallest fix.

### P0-D — primary runtime

Is "VS Code Local custom-agent execution" specific enough at design time if exact installed versions/settings are required by a zero-AI preflight before any paid run?

If not, state exactly what must be committed before implementation rather than before paid evaluation.

### P0-E — ownership transfer

Are synchronous return, quiescence, workspace identity, background-process handling, checkpoint rules, and user-edit preservation sufficiently specified for a prototype?

Do not demand atomicity if the runtime cannot expose it; assess whether the claim is honestly bounded.

### P0-F — economics

Does full-attempt accounting fix survivorship?

Review:
- hard capability regressions;
- <=75% raw-Terra weighted mean and credits/full-success;
- D3/D4 overhead;
- block/abstention treatment.

Identify any remaining metric that can reward selective failure.

### P0-G — holdout selection / oracle timing

Does independent future randomness remove designer-controlled seed manipulation?

Does sealed curator preflight solve the "discover broken oracle only after paying" problem without leaking accepted material?

### P0-H — finite scope and kill rule

Does the 16-attempt development maximum and v2.1-as-second-material-design rule prevent indefinite redesign?

Review the budget rule:
`min(1,000 credits, 70% of then-remaining included allowance, lower owner authorization)`.

Is this too large, too small, or malformed for the stated project?

---

## Special challenge: is Luna-first prefix still justified?

The minimal candidate always pays one Luna attempt before Terra takeover.

This is now the main scientific risk.

Attack it:

- On hard D1 tasks, is the Luna prefix likely to poison/anchor Terra more than it saves?
- Can continuation/restart logging resolve that?
- Does the Stage 2 forced-L / forced-T contrast actually test complementarity?
- Is there a simpler candidate that should be tested first instead, such as integrated Terra + bounded Luna worker?
- Does forcing Luna-first merely preserve project identity rather than follow evidence?

If you recommend changing this core sequence before implementation, that is a substantive verdict.

---

## Special challenge: controller complexity

Assess whether criterion register + execution receipts + hooks + ownership transfer are too much infrastructure for a first candidate.

The controller exists to prevent another known-risk -> PASS control failure, but if the control mechanism costs more complexity than the orchestration hypothesis deserves, say so.

Give a smallest acceptable version if simplification is required.

---

## Required verdict

Choose exactly one:

- `APPROVE_MINIMAL_IMPLEMENTATION_EXPERIMENT`
- `REVISE_V2_1_BEFORE_IMPLEMENTATION`
- `REJECT_MINIMAL_CASCADE_THESIS`
- `STOP_PREMIUM_RESEARCH`

Confidence: LOW / MEDIUM / HIGH.

An approval authorizes only:
1. zero-AI runtime/controller preflight;
2. implementation of the minimal candidate;
3. the bounded **development** matrix if separately approved by the owner.

It does **not** authorize fresh promotion holdouts automatically.

---

## If you approve

Specify the exact **minimum implementation**:
- agent roles/files;
- hook/controller primitives;
- trusted state;
- tool access;
- escalation contract;
- what can remain prompt-level;
- what must be deterministic;
- exact zero-AI smoke tests required before first paid run.

Do not write the files.

Also give:
- top three ways the implementation could accidentally violate the approved design;
- the earliest kill signal.

---

## If you require revision

List only **blocking** changes.

Do not expand back into L/T/M or add optional components unless absolutely necessary.

A third large design cycle is itself evidence against the product.

---

## External research

Use fresh external sources only if:
- runtime documentation changed;
- a source directly contradicts/supports a remaining blocker;
- a new orchestration result materially changes the minimal-cascade decision.

Do not repeat a broad literature review just to make the report longer.

---

## Constraints

Do not:
- implement agent/hooks/controller code;
- modify either RFC;
- modify existing experiment results;
- create workflows;
- invoke Copilot;
- spend user credits;
- select future holdout tasks;
- merge branches.

Create exactly one new file:

`docs/ASTRA_PREMIUM_V2_1_FINAL_REVIEW.md`

Commit only that file to:

`research/astra-premium-v2-1-design`

---

## Required report structure

# Astra Premium v2.1 Final Pre-Implementation Review

## 1. EXECUTIVE VERDICT

Verdict + confidence.

## 2. P0 BLOCKER MATRIX

P0-A through P0-H, each RESOLVED/PARTIALLY_RESOLVED/UNRESOLVED.

## 3. MINIMAL CASCADE THESIS

Is Luna-first one-way takeover worth the first implementation?

## 4. ACCEPTANCE CONTROLLER

Is the proposed controller minimal and credible?

## 5. ECONOMICS / EXPERIMENT IDENTIFIABILITY

Can the bounded development matrix answer the question?

## 6. RUNTIME FEASIBILITY

Exact implementation prerequisites.

## 7. BLOCKING CHANGES, IF ANY

Only blockers.

## 8. APPROVED MINIMUM IMPLEMENTATION, IF ANY

No code.

## 9. EARLIEST KILL SIGNALS

## 10. NEXT ACTION

At most three actions.

## 11. UNCERTAINTY

---

## Handoff back

When complete:
1. commit only the final review;
2. report commit SHA;
3. report verdict + confidence only;
4. do not merge.

The primary runner will decide whether to implement or stop.
