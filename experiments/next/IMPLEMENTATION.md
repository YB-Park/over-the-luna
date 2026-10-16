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

## Initial run — INVALID as a model-quality comparison (tool confound)

The first run's two Luna/Sol no-edit failures were traced to missing canonical editor tool names in the shared SDK allowlist. **Do not cite the initial 0/2 as model performance.** This section remains only as an error-analysis record.

### Raw observations — 2026-10-16

[GitHub Actions #38852208338](https://github.com/YB-Park/over-the-luna/actions/runs/38852208338) completed all 8 strategy/task sessions with model-specific usage and temporary result artifact (14-day retention).

| Model | broad_contract hidden test | risk_idempotency hidden test | Changed paths in both tasks |
| --- | --- | --- | --- |
| Luna 6 | FAIL | FAIL | **none** |
| Haiku 5.5 | PASS | PASS | source + focused tests |
| Sol 6.1 | FAIL | FAIL | **none** |
| Sonnet 5.5 | PASS | PASS | source + focused tests |

Observed total elapsed for the two tasks: Luna **31.4s**, Haiku **15.0s**,
Sol **25.3s**, Sonnet **19.5s**.
Input token totals: Luna **86,787**, Haiku **58,490**, Sol **20,350**,
Sonnet **63,936**. **These are not comparable dollar charges**; each provider has
different pricing, cache, and SDK overhead. Haiku output token count can be
higher due to reasoning; investigate cost stability separately.

**Crucial validity warning:** both Luna and Sol produced **no changed files**,
rather than a faulty patch. The SDK setup exposes only `view/edit/grep/glob`
and rejects shell, and no per-tool/permission audit was recorded in P1b.
Thus this result is **confounded by agent/tool execution behavior** and is
NOT evidence that Luna/Sol cannot solve the coding tasks or that Haiku/Sonnet
are generally superior. The correct label for these model-quality comparisons
is **TOOL-GATE DIAGNOSTIC REQUIRED**, not a published ranking.

**Next justified gate:** inspect one case each for Luna and Sol, capturing
tool calls and permission decisions in a no-secret trace; distinguish
model choice, tool-name mismatch, permission rejection, file-path restriction
and runtime inability to mutate. No repeat of the full 8-arm test until this
cause is understood.

Status: **EXECUTED; model-quality ranking INCONCLUSIVE due to tool execution confound**.

## Corrected matched run — 2026-10-16 (decision evidence)

[GitHub Actions #38852797334](https://github.com/YB-Park/over-the-luna/actions/runs/38852797334). Same two fixture tasks, same low reasoning effort and tool restrictions for all four models, but now with explicit canonical SDK `edit_file` / `apply_patch` alongside read/search tools. All four models actually edited both source/test files, changed **no unauthorized paths**, and passed independent hidden acceptance tests.

| Model / provider | broad_contract | risk_idempotency | Correct/2 | Elapsed total | Input tokens | Output tokens |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| GPT-6 Luna / Copilot | PASS | PASS | **2/2** | **16.267 s** | **32,207** | 1,102 |
| Haiku 5.5 / Copilot | PASS | PASS | **2/2** | **14.953 s** | 57,707 | 2,560 |
| GPT-6.1 Sol / OpenAI API | PASS | PASS | **2/2** | 39.402 s | 40,879 | 1,511 |
| Sonnet 5.5 / Copilot | PASS | PASS | **2/2** | 19.511 s | 63,709 | 2,235 |

On these two cases Haiku consumed **1.79× Luna input tokens**; because of cache/long-context tiers and separate providers, do NOT interpret this as a billed-cost ratio or as a reliable general distribution. Actual Copilot AI Credits and OpenAI API spend remain **UNKNOWN** in this report.

**Decision: STOP synthetic fixture expansion.** All four solve both selected problems once given valid tools. These simple tasks do not justify always-on strong Main or review, nor do they prove Luna always wins. Retain Luna-first as the parsimonious default and make stronger-model use conditional on a concrete weakness or high-impact verification need seen in actual work. Do not assign a separate fixed agent per model.

**Validity boundary:** this is Copilot SDK execution against isolated fixtures, **not a full end-to-end evaluation of the shipped VS Code plugin**. The user has confirmed the four candidate models are visible/available in their VS Code Copilot Agent Host; no model-availability retests are needed. Product behavior and actual total spend should be learned through deliberate real-world dogfooding, not more redundant access probes.

Status: **CORRECTED COMPARISON COMPLETE — QUALITY CEILING.**
