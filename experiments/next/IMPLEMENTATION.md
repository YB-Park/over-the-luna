# P1b — Actual code editing, independent hidden acceptance tests

Following [P1a paired review](PAIRED_REVIEW.md), whose three strategies all
scored 5/5 and yielded no case for always-on Sol review, test one additional
product-relevant question:

**Do any of the four accessible models offer a clear quality advantage on
real, tool-based implementation work, rather than toy review labels?**

Two previously constructed, externally graded cases are **reused**, not
invented to favor a specific model:
- `broad_contract`: discover and apply an existing account-ID contract
  from a sibling module.
- `risk_idempotency`: guarantee first-write event semantics under duplicate
  replay. Both already have deterministic hidden tests and golden selftests in
  `research/gpt6-luna-model-qualification`.

Run 2 cases × 4 model-only strategies: `gpt-6-luna`,
`claude-haiku-5.5`, `gpt-6.1-sol` (direct OpenAI API BYOK),
`claude-sonnet-5.5`. Each model is at `low` reasoning effort.
No model access check — the user confirms all four appear in their VS Code
Copilot Agent Host. This runner is an independent GitHub Actions SDK evaluation,
not an Agent Host compatibility probe.

Each task is materialized into a separate TEMPORARY, isolated workspace
under `runner.temp`. Only read/search/edit tools are allowed; no shell,
network, git push, or external actions. File writes are restricted to
case-specific source/test paths and unexpected changed paths fail validation.
Tests run OUTSIDE the model context after it finishes editing. The model
cannot invoke the hidden grader or read its test code via its tool allowlist.

Record actual model IDs, full-run correctness, changed paths, token usage,
elapsed time, failures. Separate Copilot accounting and direct OpenAI API
charges; do not add token counts as if they had identical prices.

The benchmark is intentionally only eight model sessions. Do not infer
general rankings from a pair of toy repositories; if all models pass,
prefer simple Luna-first routing and move to actual product dogfooding rather
than building a huge test harness.

## Run gate

One explicit research-branch push changing `ONE_SHOT_IMPLEMENT.md` with
commit marker `[run-implementation-once]`; not an automatic repeated workflow.
No retries. Stop on provider errors. If runtime tools cannot edit in the
isolated workspace, classify as **INFRASTRUCTURE INCONCLUSIVE**, not a bad
model.

Status: Prepared; outcome pending.
