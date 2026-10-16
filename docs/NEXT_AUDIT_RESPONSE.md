# Independent audit response — 2026-10-16

Independent reviewer summary supplied by the project owner, followed by
source reinspection. This document is **not** a claim that the full product
is validated. Prior research evidence must be interpreted narrowly.

## Confirmed serious findings

1. **Grader false positives (HIGH).** The original qualification
   `fixture.py:hidden` checks 2 output examples for `broad_contract`,
   but does not prove that `src.identity.canonical_account_id` is
   actually reused. Both implementation cases ignore the model-authored
   regression test's executable validity. We reproduced this defect with a stale golden test and two classes of constructed counterexample in a no-credit CI test. The proposed
   `audit_oracle.py` adds syntax/runtime focused test checks and observes
   a real call to the shared helper, without altering the historical
   fixture or retroactively rerunning API calls.
   **Additional finding during corrective CI:** The original
   `fixture.apply_golden("broad_contract")` updates the implementation
   but leaves the old `test_exporter.py` assertion expecting the
   unnormalized `ACCT_ABC`. Therefore even the historical **golden**
   implementation passes `hidden()` yet fails the focused regression
   test. We verified this directly during the new CI.
2. **Host tool semantics (HIGH).** `agents/luna-planner.agent.md`
   declares `tools: []`. Current upstream VS Code
   `toSdkCustomAgents` maps an empty tools array to `null`,
   documented/tested as all tools. The loaded plugin uses conditional
   `pluginDirectories` vs selected `customAgents` paths, so actual
   exposure under the user's installed build is **NOT TESTED**.
   Do not describe instruction-only no-tools as an enforced security boundary.
   The minimal product candidate must not register a separate zero-tool
   Planner pending an effective tool-denial mechanism.
3. **Wrong object evaluated (HIGH).** The 5-review and 2-code-fixture
   experiments ran custom SDK harness prompts, **not the actual shipped
   Main/Architect/Reviewer agents or VS Code Agent Host**. They can
   establish transport, tool configuration, and bounded acceptance only;
   not product gain over native Copilot Agent.

## Historical run correction — not a regrade

[Corrected implementation Actions #38852797334](https://github.com/YB-Park/over-the-luna/actions/runs/38852797334)
reports 2/2 on the **original behavioral hidden gate** for all 4
models. It does **not** prove helper reuse, valid edited test files, or
full acceptance. Patches/diffs were not retained; the stricter gate
cannot be applied retroactively. Preserve the prior numbers as historical
measurements, labeled **INCOMPLETE ACCEPTANCE CHECK**, not model-level
PASS on every requirement.

[Paired review Actions #38851868295](https://github.com/YB-Park/over-the-luna/actions/runs/38851868295)
was 5/5 in each strategy on simple, low-effort cases. No observed
marginal gain from Sol on that sample, not proof strong review is
generally wasteful.

## Design consequences

- **Luna-first remains a reversible starting hypothesis**, not an
  empirically proven optimum. Haiku's reported Copilot nano-AIU in
  the two corrected implementations was 335,076,500 vs Luna 155,587,500;
  this meter is not a verified USD bill. Sol uses a distinct OpenAI
  API bill; NULL is UNKNOWN, not zero.
- **Do not duplicate Host built-ins** before testing a minimal
  candidate. Start with one Main, optional native exploration/review
  as justified, and external deterministic acceptance validation.
- **Remove unsafe assumptions, not working v1.1.1 code yet.**
  An agent instruction is not equivalent to a tool denylist.
  Tool inheritance, subagent recursion, write restrictions and
  external-provider data disclosure need an actual runtime boundary.
- **No more tiny benchmark grids or provider availability rechecks.**
  All four models are available in the user's Host per user confirmation.
  The highest-value next experiment is native Agent vs actual small
  candidate on the *same* work and Main model, observing outcome,
  retries, credits/API USD and user interaction.
- Keep plugin/SDK experimental provider behavior **separate** from
  the observed user runtime until there is actual product integration.

## Minimum next work, in order

1. **Safe smallest candidate**: one Main, no ambient zero-tool
   Planner pretending to be sandboxed. Keep read-only leaves disabled
   until actual tool restrictions can be enforced; verify MCP and
   permissions only on a real editing use case, not model catalogue.
2. **Strict real acceptance**: for any new coding experiment run
   focused tests plus original hidden behavior, helper contract and
   syntax checks; save sanitized diff, fixture SHA, runtime version and
   execution status. Do NOT run untrusted model-edited tests with
   GitHub/OpenAI keys in that subprocess's environment.
3. **Native comparison and dogfood**: choose several genuine developer
   requests. Compare native Copilot Agent and minimal candidate using
   the same model; note full result, interruptions, manual corrections
   and **separate** Copilot AI Credits / OpenAI USD costs.

**Stop rule**: if a layer adds coordination or permission risk without
a demonstrated real-work improvement, simplify or fall back to native.

## Evidence locations

- [Historical fixture](https://github.com/YB-Park/over-the-luna/blob/f7c1c7b0a19f81432553862b006c860c923719ec/experiments/gpt6_luna/fixture.py#L210-L294)
- [Product Planner](https://github.com/YB-Park/over-the-luna/blob/main/agents/luna-planner.agent.md)
- [VS Code custom agent conversion](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/copilot/copilotPluginConverters.ts#L115-L163)
- [VS Code conversion test](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/test/node/copilotPluginConverters.test.ts#L403-L420)
- [Our originally evaluated SDK runner](../experiments/next/implement_model_comparison.mjs)
- [No-credit constructed counterexample audit](../experiments/next/audit_oracle.py)

## Corrective no-credit verification (successful)

[GitHub Actions #38855702794](https://github.com/YB-Park/over-the-luna/actions/runs/38855702794)
used the **pinned** historical fixture commit
`f7c1c7b0a19f81432553862b006c860c923719ec` and did **not**
invoke a model. It checked:
- The original golden implementation for broad_contract passes old hidden
  grading but fails the old focused regression test (stale assertion).
- A temporary repaired golden with updated focused tests passes strict
  checks; the risk_idempotency golden also passes.
- A fabricated Python SyntaxError in each regression test is accepted by
  the original hidden grader but rejected by strict grading.
- A fabricated exporter duplicating the account normalizer without calling
  the shared helper is accepted by original hidden grading but rejected
  when helper invocation is dynamically observed.

This **does not re-grade** the four models' historical changes; the
original patches were never archived. The corrective test is deliberately
limited to these known blind spots, not a full general-purpose benchmark.
