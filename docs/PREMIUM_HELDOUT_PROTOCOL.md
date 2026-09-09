# Premium Harness Held-Out Product Evaluation Protocol

Status: **frozen evaluation protocol**  
Experiment branch: `experiment/premium-luna-orchestration`  
Stable Over the Luna baseline: `main@814a069df188d28a564c4b05fbc441c2e3092d3d`  
Frozen Premium candidate: `experiment/premium-luna-orchestration@0083f3d81e7339f3b22e3efaa852562d7daa07e5`

## 1. Product question

This phase does not compare Luna and Terra as isolated models.

It asks whether the frozen Premium product expands the useful quality/cost frontier:

> Can the Terra-rooted, Luna-workhorse Premium Harness complete difficult work more reliably than current Over the Luna while remaining more cost-efficient and/or more robust than simply choosing raw Terra?

A candidate that only proves "Terra sometimes reasons better than Luna" fails the product question.

## 2. Frozen arms

Every task uses the same user-facing task statement across all three arms.

### A — Current Over the Luna

- plugin snapshot: stable `main@814a069d...`;
- root agent: `Over the Luna`;
- root model: GPT-5.6 Luna;
- stable v1.1 routing/review behavior remains intact;
- no automatic premium model.

This answers: **does Premium actually buy capability beyond the current product?**

### B — Raw Terra

- GitHub Copilot CLI default coding-agent harness;
- no Over the Luna custom plugin or custom agent selected;
- model explicitly set to GPT-5.6 Terra;
- same repository/tool availability as the other arms where technically applicable;
- built-in CLI behavior/delegation remains available because that is part of the real "just choose Terra" baseline.

This answers: **why not simply select the expensive model?**

### C — Frozen Premium Harness

- plugin agent files are copied from exact freeze SHA `0083f3d...`;
- root agent: `Premium Harness (Experimental)`;
- root model: GPT-5.6 Terra;
- repository evidence/implementation/audit delegated to GPT-5.6 Luna according to the frozen contracts;
- no prompt/agent changes after held-out outcomes are observed.

This answers the actual product hypothesis.

## 3. Common runtime rules

- GitHub Copilot CLI version is recorded per run.
- Reasoning effort remains at the product/default fixed setting for the full comparison; any observed effort metadata is recorded.
- Each arm starts from an independent copy of the exact same historical base commit.
- Repositories are shallow historical checkouts with no future branch/history available during model execution.
- Agents are explicitly told not to inspect git history or external services.
- No accepted PR title, PR number, head SHA, patch, changelog, or future test is available to a model during the run.
- Network access is used only by the workflow before/after model execution for fixture/dependency setup and hidden-oracle recovery.
- Each arm may edit/test its own disposable workspace.
- Arm order is predetermined per task and recorded before execution.
- One-shot paid workflows are deleted immediately after launch.
- A high credit ceiling is a runaway guard, not a target. Quality is not reduced merely to save tokens.

## 4. Hidden oracle protocol

Accepted historical behavior is revealed **only after all model arms for that task have finished**.

Preferred oracle order:

1. Capture each arm's patch/status and agent trace.
2. Fetch the accepted head/test material after model execution.
3. Inject only accepted regression tests or evaluator-owned hidden tests, never accepted production code.
4. Verify hidden test bytes/checksum when replacing a repository test file.
5. Run the same hidden oracle against all arms.
6. Separately inspect semantic patch shape against the accepted change where tests are insufficient.

A run is not credited merely because its own tests pass.

Infrastructure/oracle failures are classified separately from model failures. Recovery workflows must use **zero additional AI calls** whenever the candidate patch can be reconstructed from artifacts.


### Oracle fairness rule

Accepted upstream tests are not automatically authoritative when they depend on a
private helper name, exact internal class, or other implementation detail introduced
by the accepted patch. In that case:

- keep the accepted test result as **reference-shape evidence**;
- define an evaluator-owned behavior oracle from the precommitted task acceptance;
- make that oracle independent of accepted private symbol names;
- apply it to every already-produced arm patch with zero additional AI calls;
- record the evaluator correction before inspecting the remaining arm outcomes.

For H1 specifically, merged PR #4156's accepted test module imports the new private
`_socket_is_closed` helper. Therefore final H1 correctness will be based on a
helper-independent parser/socket behavior oracle:
- peer-close with no pending data becomes the existing retryable ConnectionError;
- pending RESP3 push data remains available and is processed before closure is reported;
- an open readable socket remains readable;
- the check does not lose or corrupt pending data.
The accepted helper-specific tests remain secondary reference evidence only.

## 5. Fixed held-out task set

These cases were selected after the Premium candidate was frozen. None was used to tune the candidate.

### H1 — Redis-py RESP3/hiredis closed-vs-pending socket bug

Repository: `redis/redis-py`  
Historical base: `b121809bd7c7107eedb6b9849180c83246419961`  
Accepted reference: merged PR #4156 (2026-07-07), hidden from agents.

Stratum:
- ambiguous debugging;
- parser/pool boundary;
- pending push data must not be consumed;
- closed pooled connection must be recycled;
- platform/socket semantics matter.

User-visible symptom supplied to all arms:
- protocol=3 + hiredis pooled connection closed by the server can be handed back as readable;
- the next command then fails instead of reconnecting;
- protocol=2+hiredis and RESP3 pure-Python do not show the same failure;
- pending RESP3 push data must remain intact.

Hidden oracle:
- accepted `tests/test_connection.py` targeted hiredis/socket-close tests;
- non-destructive distinction between pending data and EOF;
- peer-close raises the existing connection-closed error through `can_read`;
- pending push is consumed before close is reported;
- focused existing parser/connection tests.

### H2 — Pytest unraisable-warning cleanup ordering

Repository: `pytest-dev/pytest`  
Historical base: `d84fccb8a840641287b4873a411346d22591f02d`  
Accepted reference: merged PR #14499 (2026-05-27), hidden from agents.

Stratum:
- cross-plugin lifecycle/teardown ordering;
- garbage collection + warning filters + unraisable hook;
- failure can disappear while ordinary tests appear green.

User-visible symptom:
- a cyclic object whose `__del__` raises may be collected at session shutdown;
- another plugin registers a late cleanup that resets warning filters;
- an active `error::pytest.PytestUnraisableExceptionWarning` filter can be gone before the unraisable is surfaced, causing an incorrect zero exit code;
- partially failed plugin configuration must not turn shutdown into an INTERNALERROR.

Hidden oracle:
- accepted `testing/test_unraisableexception.py` targeted new regression tests;
- collection occurs while session warning filters/hook are still active;
- cleanup-stack order no longer controls correctness;
- failed `pytest_configure` remains a usage error rather than a stash-key/internal error.

### H3 — Pytest `--max-warnings` coherent feature

Repository: `pytest-dev/pytest`  
Historical base: `8ecf49ec2807768105b05dda5461b28cdad89d03`  
Accepted reference: merged PR #14372 (2026-04-16), hidden from agents.

Stratum:
- coherent product feature across CLI/config/session result/docs/tests;
- several subsystems but conceptually straightforward;
- tests whether Premium can maintain global contract without unnecessary orchestration.

Task:
- add a configurable maximum-warning threshold available via CLI and ini;
- when tests otherwise pass but warning count exceeds the configured threshold, return a dedicated exit status;
- preserve existing behavior when unset;
- validate invalid configuration cleanly;
- update user-facing documentation/changelog as the repository normally requires.

Hidden oracle:
- accepted feature tests/config behavior from the merged head;
- CLI and ini precedence/validation;
- dedicated exit-code behavior;
- no regression when threshold is absent.

### H4 — Redis-py zrevrange key-shape control

Repository: `redis/redis-py`  
Historical base: `1627c98a7900222834a925f4532abcfcbda54983`  
Accepted reference: merged PR #4244 (2026-08-05), hidden from agents.

Stratum:
- straightforward control;
- exact local contract;
- Premium should not damage correctness and should expose its overhead.

Task symptom:
- `zrevrange("myzset", ...)` passes its key metadata as a bare string while sibling sorted-set range commands pass a sequence;
- consumers treat `options["keys"]` as a sequence of Redis keys, so the string becomes one key per character;
- make the behavior consistent and add a focused regression test.

Hidden oracle:
- exact focused accepted test behavior;
- key metadata equals `["myzset"]`;
- no unrelated command behavior changes.

## 6. Screening and repetition

Predetermined screening arm order (fixed before any held-out model run):
- H1: **B Raw Terra -> C Premium -> A Over the Luna**
- H2: **C Premium -> A Over the Luna -> B Raw Terra**
- H3: **A Over the Luna -> B Raw Terra -> C Premium**
- H4: **B Raw Terra -> A Over the Luna -> C Premium**

Each arm uses `--max-ai-credits=100` as the same runaway ceiling. This is not an intended spend target.

### Screening

Run each of H1–H4 once per arm.

The first pass is used to identify:
- decisive correctness differences;
- obvious cost/coordination failures;
- tasks where stochastic variation could plausibly change the conclusion.

### Sequential repetition

Do **not** automatically run five copies of every expensive task.

For a task, expand to 3 runs per arm when:
- Premium and a comparator disagree only narrowly;
- one arm fails for a plausibly stochastic agent trajectory;
- cost/quality ordering could flip with ordinary run variance.

Expand from 3 to 5 only when the product decision for that task could still change.

A deterministic hidden-oracle failure caused by a clear wrong implementation direction does not need repetition merely to seek a lucky pass.

## 7. Scoring

Primary outcome is hidden-oracle correctness.

Per arm/task record:

### Correctness
- hidden oracle PASS/FAIL;
- requirement coverage;
- accepted-behavior gaps;
- public/API compatibility.

### Direction and robustness
- wrong-direction mutation;
- repair/replan count;
- discarded/replaced patch;
- whether review/audit caught consequential defects;
- unnecessary architecture/coordination machinery.

### Efficiency
- total AI credits;
- credits by model where exposed;
- wall time;
- root turns/checkpoints;
- subagent calls;
- repository tool calls;
- duplicate discovery.

### Product behavior
- user intervention count (target: zero after initial arm selection);
- whether Terra itself performed high-volume repository work;
- whether Premium selected a shallow path for simple work;
- whether the candidate completed a larger coherent scope than OTL.

## 8. Product decision rule

Premium is not promoted because of a single impressive win.

Evidence must support both directions:

### Against Over the Luna
Premium should show a material difficult-task capability/completion advantage across held-out work, not merely longer plans or more validation.

### Against raw Terra
Premium should provide comparable-or-better correctness with a meaningful cost/robustness advantage, or materially better correctness at comparable spend.

### Straightforward control
H4 should show no meaningful correctness regression. Large premium overhead on H4 is recorded as a usability/economics penalty even if correctness passes.

Possible final outcomes:
- `PROMOTE_FOR_PRODUCT_ARCHITECTURE_REVIEW`
- `KEEP_EXPERIMENTAL_MORE_HELD_OUT_EVIDENCE`
- `REDESIGN`
- `KILL`

## 9. Freeze discipline

Held-out outcomes may update only:
- result documents;
- evaluator workflows/oracles;
- infrastructure needed to recover an already-produced patch without AI rerun.

They may **not** change frozen agent prompts/contracts.

If a held-out result reveals a design flaw important enough to edit the candidate, Phase 3 ends and the experiment returns to `REDESIGN`; all subsequent runs belong to a new candidate version and cannot be pooled with this freeze.
