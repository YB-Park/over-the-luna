# Premium Harness Experiment Results

Status: **experimental**  
Branch: `experiment/premium-luna-orchestration`  
Stable baseline: `main@814a069df188d28a564c4b05fbc441c2e3092d3d`

Do not treat regression-lab cases as promotion evidence.

## Environment

- Start date: 2026-09-09
- GitHub Copilot CLI: captured per run artifact
- Premium root: GPT-5.6 Terra
- Workhorse/audit leaves: GPT-5.6 Luna
- Stable Over the Luna remains unchanged
- Initial user billing snapshot from prior experiment: 199 / 1,500 included AI credits used on 2026-09-07; approximately 1,301 remained at that time

## Phase 0 — structural runtime smoke

Run: GitHub Actions `34308800037`

Disposable task: implement and test a deterministic `canonical_slug()` contract.

| Check | Result | Evidence |
|---|---|---|
| Terra root model | PASS | session model `gpt-5.6-terra` |
| Terra direct repository/tool work blocked | PASS | root tool calls were `task` only despite global CLI pool exposing view/search/edit/execute equivalents |
| One Luna Builder mutation trajectory | PASS | exact one `Luna Builder`, model `gpt-5.6-luna`; used view/apply_patch/bash |
| Builder validation | PASS | focused pytest: 4 passed |
| One independent Luna Auditor | PASS | exact one `Luna Auditor`, model `gpt-5.6-luna`; inspected diff and reran focused checks |
| Auditor edit capability absent | PASS | agent frontmatter excludes edit; trace showed bash/view only |
| Auditor absolute non-mutation guarantee | UNRESOLVED | `execute` is still a general shell capability; this run showed no source edit, but capability-level non-mutation is not structurally guaranteed |
| Hidden deterministic oracle | PASS | workflow completed successfully after hidden post-agent assertions |
| Final audit | PASS | Auditor verdict PASS |
| AI usage | 4.594653 credits | OTel `totalNanoAiu=4594653000` |

Observed trajectory:

```text
Terra
  -> Luna Builder
  -> Terra
  -> Luna Auditor
  -> Terra
```

The experiment therefore establishes the core runtime direction:
- expensive parent can remain tool-thin;
- Luna Builder can own real mutation/validation;
- a separate Luna Auditor can inspect the finished work;
- the user does not choose Luna vs Terra inside the run.

### Phase 0 caveat

The Auditor boundary is **behaviorally read-only, not capability-proof read-only**, because `execute` can theoretically mutate a workspace. The experiment currently relies on:
- no `edit` tool;
- strict Auditor instructions;
- ephemeral test environments;
- trace/result inspection.

This must remain an explicit product-risk item until a narrower runtime execution capability exists or a different artifact-first audit design proves better.

## Regression laboratory

Purpose: test mechanisms against already-solved historical failures. These cases are not held-out and cannot support promotion.

### R1 — httpcore wrong-belief cascade

Goal: rerun the historical AnyIO import-race case that defeated Terra Deep Judgment and determine whether the new **Critical Belief Gate** prevents the wrong lock-based causal model from reaching mutation.

Expected mechanism:
- Terra should identify lazy-import synchronization as a high-blast causal belief;
- before Builder mutation, one Luna evidence/falsification probe should discriminate lock-based lazy imports from removing lazy imports via conditional module-level imports;
- Builder should not receive the previously failed per-instance/backend-affinity lock contract;
- accepted-direction oracle: no lazy imports inside synchronization setup; optional AnyIO/Trio behavior preserved through conditional module-level imports.

Status: **R1-v1 incomplete / redesign signal**.

Run: GitHub Actions `34308983274`.

Observed trajectory:
- Terra -> Luna Architect -> Luna Builder -> Luna Auditor -> Terra.
- Terra itself remained tool-thin.
- Luna Architect used **64** repository tool calls and approximately **416k tokens** before Builder.
- Builder used 31 tool calls; Auditor used 22.
- total session usage: **14.020983 AI credits**.

Mechanism outcome:
- materially better than the prior failed Deep Judgment direction: the candidate **did not** add lazy-import locks or backend-affinity locking;
- it moved required `anyio` import to module scope and published primitive state before `_backend`, eliminating the observed AnyIO first-use import window and the partial-publication cleanup failure;
- however, it left `trio` as a lazy import inside async synchronization setup and did not use the accepted conditional-import guards for both backends;
- merged httpcore PR #692 removes lazy async-function imports for **both** `trio` and `anyio` with module-level conditional imports and explicit missing-backend errors.

Therefore R1-v1 does **not** satisfy the accepted-direction regression oracle. It is a partial causal improvement, not a PASS.

Harness issue:
- the workflow attempted the historical full pytest suite before the static oracle;
- 182 tests passed, but 12 known integration cases errored because the external `httpbin` fixtures were not installed;
- `set -o pipefail` therefore stopped the step before the static oracle executed.
- This is a test-harness sequencing bug and is separate from the model result. The accepted-direction comparison above was recovered from the uploaded diff and merged PR #692.

Architecture signal:
- allowing a full stable Luna Architect call to self-certify a high-blast causal belief is too expensive and too broad for the premium control plane;
- the Critical Belief Gate should use a **bounded causal discrimination context** before mutation rather than a complete sealed-work-set Architect pass;
- the next regression revision should introduce/route through a small Luna causal Probe with an explicit search/read budget and output centered on competing hypotheses and falsifying evidence.


### R1-v2 — bounded Causal Probe regression

Run: GitHub Actions `34309773528`.

Result: **FAIL — mechanism did not contain the wrong intervention class.**

Observed trajectory:

```text
Terra
  -> Luna Causal Probe
  -> Luna Builder
  -> Luna Auditor (REPAIR)
  -> Luna Builder repair
  -> Luna Auditor (PASS)
  -> Terra
```

Key observations:
- Causal Probe ran before mutation, so the routing boundary itself worked.
- Probe violated its prompt budget: **32** read/search tool calls vs the intended maximum of 18.
- Probe correctly identified partial publication and lazy import as relevant, but retained a high-confidence preference for serializing lazy AnyIO import and atomic per-instance initialization.
- First Builder implemented a guarded lazy AnyIO importer plus delayed backend publication.
- Auditor correctly found a remaining concurrent per-instance initialization race and requested repair.
- Second Builder added per-instance `threading.Lock` guards and preserved lazy AnyIO/Trio import behavior.
- Focused existing tests: **83 passed** in the external regression step; Builder/Auditor focused suites also passed.
- Accepted-direction static oracle: **FAIL** because lazy backend imports remained.
- Merged httpcore PR #692 instead removes async-function lazy imports for both `trio` and `anyio` via module-level conditional imports.
- Total session usage: **15.238303 AI credits**.

This is more concerning than R1-v1:
- the dedicated Probe did not reduce evidence cost enough;
- the Auditor made the internally coherent but historically wrong intervention **stronger**, demonstrating that verification of an incorrect design can amplify the wrong abstraction;
- correctness-oriented review without a simplicity/intervention-class check is insufficient;
- a premium control plane should not turn a causal belief into a prescribed synchronization architecture unless repository evidence makes that architecture necessary.

**Architecture conclusion:** retire the current Causal Probe as an implementation-direction authority. The premium root should use evidence to establish *what must stop being true* and *what invariants must hold*, while Luna Builder retains solution search among simpler structural alternatives. A separate post-change audit should challenge not only correctness but also whether the patch introduced machinery unnecessary to satisfy the observed failure and acceptance contract.


### R1-v3 — Builder-owned local diagnosis + simplicity audit

Run: GitHub Actions `34315816016`.

Result: **PARTIAL — major mechanism improvement, historical full-fix oracle still not satisfied.**

Observed trajectory:

```text
Terra -> Luna Builder -> Luna Auditor -> Terra
```

No pre-mutation Architect/Probe was used.

Measured:
- Builder: 29 tool calls, ~208k tokens;
- Auditor: 15 tool calls, ~69k tokens;
- total session usage: **7.741410 AI credits**;
- focused external tests: **83 passed**;
- Auditor: **PASS** with no consequential findings.

Patch behavior:
- removed all lazy `anyio` imports from `AsyncLock`, `AsyncEvent`, and `AsyncSemaphore`;
- imported required AnyIO once at module load;
- for `AsyncLock`, delayed backend publication until lock construction succeeds and made failed/pre-setup cleanup safe;
- introduced **no** new locks, caches, import guards, or other coordination state;
- kept optional Trio imports lazy inside synchronization methods.

Historical-shape oracle: **FAIL**, because merged PR #692 removes async-method lazy imports for both AnyIO and Trio using module-level conditional imports.

Interpretation:
- v3 materially improves on v1/v2: it is ~49% of v2's cost and avoids the over-engineered lock-based intervention;
- the original observed AnyIO first-import failure class is structurally removed;
- however, the analogous lazy-import pattern remains for Trio, so the harness did not independently recover the full historical structural correction;
- the oracle is intentionally stricter than the observed AnyIO symptom and partially encodes the merged patch's broader symmetry. Therefore record this as a partial regression result, not a simple correctness failure or success.

**Decision:** stop tuning on R1. It has already served its purpose. The regression shows that Builder-owned diagnosis + simplicity-aware audit is preferable to the dedicated Causal Probe, but does not prove the premium architecture is robust. Continue with a different solved regression and then freeze before held-out evidence.


### R2 — Django ASGI lifecycle regression

Primary agent run: GitHub Actions `34316282753`.  
Recovered hidden-oracle validation: GitHub Actions `34316996629`.

Agent trajectory:

```text
Terra -> Luna Architect -> Luna Builder -> Luna Auditor -> Terra
```

Measured:
- Architect: 22 tool calls, ~141k tokens;
- Builder: 41 tool calls, ~848k tokens;
- Auditor: 21 tool calls, ~317k tokens;
- total session usage: **16.107360 AI credits**.

Builder and Auditor both reported the local ASGI suite at 22/22 before hidden injection.

The original one-shot's hidden-test injection step failed with `curl (23) Failure writing output to destination`; therefore that same-run 22/22 result was **not** accepted as hidden evidence.

A zero-AI-credit recovery workflow then:
1. downloaded the exact R2 artifact/diff;
2. reconstructed `django/django@b3dc80682e678b20c89fb2a430c0bc77960a29ac`;
3. applied the candidate diff;
4. fetched accepted Django commit `11393ab1316f973c5fbb534305750740d909b4e4`;
5. forced `tests/asgi/tests.py` from that accepted commit into the reconstructed candidate;
6. verified the injected file by checksum and byte comparison;
7. ran the ASGI suite from the isolated candidate workspace.

Recovered hidden accepted result: **22/22 PASS**.

Interpretation:
- the simplified premium architecture preserves the strongest positive result from the earlier Deep Judgment experiment;
- unlike the old checkpoint handoff, the current product-shaped harness keeps Terra as mission/integration owner while Luna performs repository mapping, implementation, tests, and independent audit;
- R2 is regression evidence only, not promotion evidence.

## Regression-lab decision

Stop tuning against solved historical cases.

Current lessons:
- Phase 0 structural orchestration: PASS.
- R1 httpcore: dedicated pre-mutation causal planning was counterproductive; Builder-owned local diagnosis plus simplicity-aware audit was materially cheaper and avoided lock proliferation, but did not independently recover the full historical Trio+AnyIO conditional-import correction.
- R2 Django: hidden accepted lifecycle behavior PASS.

**Freeze candidate architecture for held-out evaluation.** Do not modify role prompts/contracts in response to held-out outcomes unless the held-out phase is explicitly abandoned and the candidate is returned to redesign status.
