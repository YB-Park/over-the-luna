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

Status: pending.
