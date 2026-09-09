# Astra Work Handoff — v2.1 B1/B2 Closure Check

Status: **narrow closure review only**  
Target branch: `research/astra-premium-v2-1-design`  
Revised RFC commit: `279607eeef6aa8561ed321cef9d944eac37f89bd`  
Prior final review: `ba6480658ff4c037dffcf3b7a84fd854c43998a5`

## Mission

Your previous verdict was:

> `REVISE_V2_1_BEFORE_IMPLEMENTATION` — HIGH confidence

You identified **exactly two blocking specification changes** and explicitly stated that no other architecture change was blocking:

- B1 — bind captured acceptance obligations across model-proposed updates;
- B2 — make authenticated user waivers terminally partial and exclude them from full success.

The primary runner has amended only the v2.1 RFC to close those two items.

Your task is **not** another architecture review.

Your task is:

> Verify whether B1 and B2 are now closed exactly enough to authorize the already-scoped minimal implementation experiment.

Do not reopen resolved P0-A/B/D/E/F/G/H unless the new B1/B2 edits themselves create a direct contradiction.

Do not propose L/T/M, Verifier, Architect, broader routing, new product thresholds, new research programs, or more literature work unless a newly introduced blocker absolutely requires it.

---

## Read

1. Your prior final review at commit:
   `ba6480658ff4c037dffcf3b7a84fd854c43998a5`
2. Revised:
   `docs/PREMIUM_V2_1_MINIMAL_CASCADE_RFC.md`
   at commit:
   `279607eeef6aa8561ed321cef9d944eac37f89bd`

Focus only on the delta relevant to B1/B2.

---

## B1 closure test

Your prior requirement:

> Controller owns captured ID, original source/anchor, original criterion content, and original required/blocking status. Models may not overwrite the authority-bearing record. U scope can be narrowed only by authenticated user revision. R obligations retain original history and any reconciliation is explicit.

Verify that the revised RFC now makes these counterexamples impossible **by specification**:

1. Retain `U1` but change `SOURCE: U -> A`, then COMPLETE.
2. Retain `U1` but change `BLOCKING: yes -> no`, then COMPLETE.
3. Retain `U1` but narrow criterion content from X+Y to X, then COMPLETE.
4. Silently delete/re-source a blocking repository-derived R obligation.
5. Replace an original obligation with a weaker model interpretation while retaining the same ID.

You are checking specification closure, not implementation correctness or semantic completeness of initial extraction.

Return:
- `B1_RESOLVED`
or
- `B1_NOT_RESOLVED`

If not resolved, quote the exact remaining ambiguity and give the smallest wording correction only.

---

## B2 closure test

Your prior requirement:

> COMPLETE requires every still-required criterion VERIFIED and no active waiver of required scope. A genuine waiver maps to PARTIAL_WITH_USER_WAIVER, never full success. A waiver on one row cannot hide another unresolved row.

Verify:

1. Valid authenticated waiver on one required criterion + all others VERIFIED -> `PARTIAL_WITH_USER_WAIVER`.
2. Same case can never emit trusted `COMPLETE`.
3. Partial outcome gives zero full-success credit.
4. Partial is treated as non-full-success in comparator capability/regression vetoes.
5. A waiver on U1 cannot mask U2 = OPEN/FAILED/UNRESOLVED.
6. Unattended promotion evaluation cannot fabricate an interactive waiver to shrink scored scope.

Return:
- `B2_RESOLVED`
or
- `B2_NOT_RESOLVED`

If not resolved, give the smallest wording correction only.

---

## Required verdict

Choose exactly one:

- `APPROVE_MINIMAL_IMPLEMENTATION_EXPERIMENT`
- `B1_B2_NOT_CLOSED`

Confidence: LOW / MEDIUM / HIGH.

Use `APPROVE_MINIMAL_IMPLEMENTATION_EXPERIMENT` if B1 and B2 are both resolved and no contradiction introduced by those edits prevents the already-defined experiment.

This approval authorizes only the design to advance to:
1. zero-AI controller/runtime implementation and smoke;
2. minimal agent implementation;
3. paid development runs only after separate owner approval and actual allowance/budget check.

It does not authorize promotion holdouts.

---

## Required output

Create exactly one new file:

`docs/ASTRA_PREMIUM_V2_1_CLOSURE_REVIEW.md`

Commit only that file to:

`research/astra-premium-v2-1-design`

Structure:

# Astra Premium v2.1 B1/B2 Closure Review

## 1. VERDICT

Verdict + confidence.

## 2. B1

`B1_RESOLVED` or `B1_NOT_RESOLVED`, with concise rationale.

## 3. B2

`B2_RESOLVED` or `B2_NOT_RESOLVED`, with concise rationale.

## 4. NEW CONTRADICTION CHECK

State whether the amendments introduced a new implementation-blocking contradiction. Do not list nonblocking polish.

## 5. NEXT ACTION

One sentence only.

---

## Constraints

Do not:
- edit any existing file;
- implement anything;
- create workflows;
- invoke Copilot;
- spend credits;
- select holdouts;
- merge;
- repeat broad external research.

When finished, report:
- commit SHA;
- verdict;
- confidence only.
