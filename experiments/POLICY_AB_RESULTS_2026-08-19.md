# v1.1 policy A/B — live results

These controlled Copilot runs compare released v1.0 routing with candidate v1.1 assurance policies. They are evidence, not a release decision.

## Shared setup

The variants start from byte-identical small Python repositories and receive the same normal user task:

- make `preview_order` use the same established customer-ID validation/normalization as `create_order`;
- add focused regression tests;
- preserve return shape and quantity semantics;
- run relevant tests;
- do not use premium review.

Runtime:

- GitHub Actions;
- Copilot CLI 1.0.80;
- GPT-5.6 Luna;
- checked-out Over the Luna plugin loaded with `--plugin-dir`;
- same allowed tools and hard AI-credit ceiling for compared variants;
- OTel content capture disabled;
- separate clean fixture and plugin copy per variant;
- hidden post-run evaluation outside the agent-visible repository tests.

The candidates change Main routing/assurance instructions only. Main remains the single mutation owner and uses the same read-only `Luna Reviewer` leaf as v1.0.

## Run A — full direct-assurance candidate

### Released-policy baseline

Observed route:

`Mode: SIMPLE — direct Luna`

- Agent invocations: 1
- Reviewer invocations: 0
- Model calls: 7
- Tool calls: 10
- OTel input/output tokens: 98,932 / 957
- Main input/output tokens: 98,932 / 957
- First mutation tool: `apply_patch`
- Visible repository tests: PASS
- Hidden evaluation: PASS
- Copilot event duration: about 17.1 seconds

The patch was correct but received no automatic independent review despite being a behavioral mutation with new tests.

### `DIRECT/ISOLATE/DEEP + NONE/REVIEW/RISK` candidate

Observed route:

`Route: DIRECT + REVIEW`

- Agent invocations: 2
- Subagents: 1 (`Luna Reviewer`)
- Reviewer invocations: 1
- Model calls: 8
- Tool calls: 13
- OTel input/output tokens: 103,367 / 1,724
- Main input/output tokens: 99,503 / 1,259
- Reviewer input/output tokens: 3,864 / 465
- First mutation tool: `apply_patch`
- Visible repository tests: PASS
- Hidden evaluation: PASS
- Reviewer verdict: PASS
- Copilot event duration: about 32.4 seconds

The Reviewer inspected the final state and confirmed that `preview_order` reused `_normalize_customer_id`, preserved return/quantity semantics, and had focused coverage. It did not mutate the repository.

### Patch equivalence and overhead

Baseline and candidate produced the same implementation/test diff:

- one call to `_normalize_customer_id` added to `preview_order`;
- tests added for normalization, blank ID, and non-string ID;
- no unrelated changes.

Compared with baseline:

- total input tokens: 98,932 → 103,367 (**+4.5%**);
- additional reviewer input/output: 3,864 / 465;
- Main input remained essentially flat (98,932 → 99,503);
- model calls: 7 → 8;
- wall-clock/event-stream duration increased by roughly 15 seconds in this sample.

This is a useful trade-off signal: token overhead was modest, but latency overhead was not negligible.

## Run B — minimal late-review candidate

The second candidate deliberately kept the public investigation vocabulary `SIMPLE / STANDARD / DEEP`. It changed the instructions to say explicitly that complexity mode controls investigation only and added a late gate requiring one fresh Reviewer for non-trivial mutation.

### Released-policy baseline

Observed route:

`Mode: SIMPLE — direct Luna`

- Agent invocations: 1
- Reviewer invocations: 0
- Model calls: 5
- Tool calls: 7
- OTel input/output tokens: 68,330 / 790
- Visible repository tests: PASS
- Hidden evaluation: PASS

### Minimal late-review candidate

Observed route:

`Mode: SIMPLE — direct Luna`

- Agent invocations: 1
- Reviewer invocations: **0**
- Model calls: 5
- Tool calls: 8
- OTel input/output tokens: 66,178 / 933
- Visible repository tests: PASS
- Hidden evaluation: PASS

The candidate produced the same correct diff as its baseline but **did not execute the explicitly required late Reviewer**. Its final response reported the implementation and tests and ended without an assurance pass.

## Cross-run interpretation

The first two live candidate runs support a more specific hypothesis than “review instructions need to be stronger”:

> **An early `SIMPLE — direct Luna` trajectory label may act as a strong global frame. A later textual review rule can be ignored even when it says the Reviewer is required. Making assurance a first-class state at the initial route decision may materially improve adherence.**

This is consistent with earlier v1.0 mutation observations where automatic Reviewer invocation was 0/2 despite the released contract already saying non-trivial completed changes should receive one Luna Reviewer.

However, one run per candidate is not enough to distinguish a real prompt-structure effect from stochastic model behavior.

## What these samples support

1. A clear local task can remain a single-Main implementation while a late fresh Reviewer is added without changing the patch.
2. A first-class `DIRECT + REVIEW` state produced the intended review behavior once with modest token overhead.
3. Merely appending a strong late-review gate to the existing `SIMPLE` framing did **not** produce the intended behavior in its first live run.
4. Reviewer latency matters even when Luna token cost is small.
5. Neither run proves correctness improvement: all baseline/candidate patches passed visible and hidden evaluation before review.

## What remains unresolved

- Reviewer precision on harder patches. Earlier forced-review evidence includes one materially incorrect finding, so increased invocation alone is not success.
- Whether the full vocabulary rename to `DIRECT / ISOLATE / DEEP` is necessary.
- Whether a middle policy can preserve familiar `SIMPLE / STANDARD / DEEP` investigation labels while declaring assurance as a first-class state up front, for example `Mode: SIMPLE | Assurance: REVIEW`.
- Whether the adherence difference repeats across multiple runs of the same controlled task.
- Broad-scouting reclassification remains a separate problem and must not be hidden by assurance changes.

## Next experiment

Run a small adherence replication on the same controlled task:

- full direct-assurance candidate, additional repetitions;
- minimal late-review candidate, additional repetitions;
- a middle candidate that keeps `SIMPLE / STANDARD / DEEP` for investigation but **declares `NONE / REVIEW / RISK` at initial routing time** and rechecks it after mutation.

Measure Reviewer invocation reliability, patch equivalence, hidden correctness, tokens, and latency. Prefer the smallest policy that makes assurance reliable without increasing ceremony.
