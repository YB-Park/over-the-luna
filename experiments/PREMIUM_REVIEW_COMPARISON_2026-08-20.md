# v1.1 premium review comparison — 2026-08-20

This experiment evaluates the v1.1 product hypothesis that the developer-facing question should be **whether premium independent judgment is worth one explicit human decision**, not which premium model to route manually.

Premium inference remains human-selected in the product. The automated workflow below was a bounded research probe explicitly run for this product decision; all one-shot paid workflows were removed after artifact collection.

## Current public model context

At the experiment date, GitHub Copilot's official supported-model documentation lists **Claude Sonnet 5** and **Claude Opus 4.8** as GA models. GitHub's pricing reference lists Sonnet 5 below Opus 4.8 in per-token pricing.

Actual availability still depends on plan/client/policy. The runtime probe below is therefore stronger evidence for this repository's current execution environment than assuming a supported model is selectable everywhere.

## Method

Two supplied-only artifacts were reviewed under the same rubric with no repository/tool access:

### Artifact A — known subtle defect

A completed OTel ownership implementation indexed ancestry globally by `span_id` while the data model carried both `trace_id` and `span_id`. The stated requirement required correct nearest-agent ownership for files containing more than one trace.

This is the same defect family the v1.1 Luna invariant Reviewer had already detected 2/2 in controlled experiments.

Success criterion: identify the trace-scoping/identity correctness failure rather than merely ask for generic testing.

### Artifact B — known correct patch

The replicated broad account-summary patch reused the established `normalize_account_id` contract, canonicalized equivalent identifiers, preserved first canonical appearance, and rejected invalid identifiers. Visible + hidden behavior gates and two Luna Reviewer runs had already passed.

Success criterion: PASS without speculative blocking findings.

### Isolation

Each premium run used:

- an empty working directory;
- an isolated temporary agent with `tools: []`;
- no repository browsing;
- identical review rubric across model slots;
- OTel content capture disabled;
- one premium request maximum for the artifact.

## Sonnet 5 result

### Known-defect artifact

Actual model: `claude-sonnet-5`

Result: **BLOCK**.

Sonnet identified the acceptance-critical issue directly: a global `by_span_id` map and raw `parent_span_id` ancestry walk do not preserve trace scope, so a cross-trace ID collision can resolve ownership through the wrong trace. It also correctly observed that the listed visible validation did not exercise the multi-trace collision boundary.

Measured trajectory:

- premium requests: 1;
- elapsed wall time observed by workflow: ~20 s;
- API duration: ~17.2 s;
- input tokens: 8,207;
- output tokens: 1,403;
- tools: 0.

### Known-correct artifact

Actual model: `claude-sonnet-5`

Result: **PASS / APPROVE** with no findings.

Measured trajectory:

- premium requests: 1;
- elapsed wall time: ~3 s;
- API duration: ~1.0 s;
- input tokens: 8,096;
- output tokens: 17;
- tools: 0.

### Incremental-value interpretation

Sonnet demonstrated useful precision on this two-artifact check: it blocked the real defect and did not invent a blocker on the known-correct patch.

However, the defect was **not unique incremental judgment beyond the current Luna Reviewer**: the v1.1 dependency + invariant-challenge Luna Reviewer had already found the same trace-identity failure 2/2, and the correct broad patch had already passed Luna review 2/2.

Therefore this experiment supports Sonnet as a credible **optional different-model judgment**, but does not justify automatic premium spend or routine premium review after every Luna REVIEW.

## Opus 4.8 result — unavailable in this execution environment

The first matrix supplied `model: Claude Opus 4.8` in the temporary custom-agent frontmatter.

Both requested Opus jobs emitted the explicit CLI warning:

> Custom agent ... specifies model "Claude Opus 4.8" which is not available; using "claude-sonnet-5" instead

OTel and assistant events confirmed that both jobs actually ran `claude-sonnet-5`, not Opus.

Thus those outputs are **not Opus comparison data** and must not be counted as Opus quality evidence.

A follow-up explicit model-selection probe then ran:

`--model=claude-opus-4.8`

with a trivial no-tool prompt.

Result:

- exit code: **1**;
- model calls: **0**;
- stderr: `Model "claude-opus-4.8" from --model flag is not available.`

This separates the result from a mere display-name/frontmatter parsing issue: in the current Copilot CLI/account/policy environment, Opus 4.8 is not selectable.

## Product conclusion

The v1.0 two-choice premium menu is not supported by the evidence.

### Reject for v1.1 default UX

- separate `Review with Sonnet` and `Critical review with Opus` buttons as equal normal choices;
- any automatic Opus escalation;
- exposing a premium model choice that may silently fall back or be unavailable in the user's current client/plan/policy;
- routine premium review after a successful bounded Luna Reviewer.

### Leading v1.1 premium UX

Expose **one human-initiated `Premium Review` affordance**.

Candidate backing model: **Claude Sonnet 5**.

Use it only when Main reports a specific consequential residual uncertainty where a different-model judgment is plausibly worth the explicit spend, or when the developer manually asks for premium review.

Keep:

- `send: false`;
- no automatic premium subagent path;
- a clear reason for recommendation;
- graceful handling when the backing model is unavailable.

Do not expose an Opus button in the normal v1.1 cognitive path on the current evidence.

## Why one affordance is better supported

1. **Decision simplicity:** the meaningful user decision is whether to buy a premium second opinion, not model routing.
2. **Availability:** this real Copilot environment could use Sonnet 5 but could not select Opus 4.8.
3. **Precision:** Sonnet passed the two-sided oracle: real defect blocked, correct artifact approved.
4. **Incremental evidence discipline:** Sonnet did not uncover a unique defect beyond the improved Luna Reviewer in this corpus, so premium remains optional rather than routine.
5. **Safety:** one visible `send:false` human gate preserves the invariant that premium inference is never a hidden automatic expense.

## Remaining premium/runtime gate

This experiment closes the **policy/UX direction** enough to remove the two-model menu from the release candidate, but actual VS Code must still verify:

- exact custom-agent handoff rendering;
- switching to the single `Premium Review` target;
- model selection in the real VS Code client;
- `send: false` remains a genuine human confirmation boundary;
- unavailable-model behavior does not silently execute a different premium model without a visible signal.

That final UI/runtime verification belongs to the real VS Code Gate A, not another CLI quality ablation.
