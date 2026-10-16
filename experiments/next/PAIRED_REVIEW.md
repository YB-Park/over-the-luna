# P1 Miniature paired code-review decision test (not a leaderboard)

## One product question
Does giving an otherwise adequate Luna Main **one independent Sol check**
catch acceptance-critical bugs or prevent false approvals enough to be worth
the extra API charge, versus Luna doing it itself or using Sol as Main?

**Arms (same prompt/code, different execution approach)**
A. Copilot-billed `gpt-6-luna` direct review.
B. Copilot-billed `gpt-6-luna` Main delegates once to OpenAI API
   `openai-sol/gpt-6.1-sol` leaf, then Main adjudicates.
C. OpenAI API-billed `gpt-6.1-sol` direct review.

The task fixtures intentionally include **3 genuine defects and 2 clean
implementations**, adapted from existing `gpt6_luna` fixture ideas.
`review_oracle.py` executes behavioral assertions to establish labels.
The models see only acceptance criteria and candidate implementation;
the oracle/tests are not included in prompts, and tools are unavailable
apart from arm B's one `task` delegation.

Quality metric: correct `VERDICT: MUST-FIX|PASS` plus proper model routing.
Record reasoning summary for manual assessment when verdict is insufficient.
Record token usage per *actually observed model* and elapsed time.
AI Credits (GitHub) and USD/API (OpenAI) have different billing sources;
**do not treat total tokens or reported nano-AIU as direct combined USD cost**.

The independent benchmark is deliberately tiny and may show a ceiling
effect. **Do not claim statistical superiority, tune prompts to these
five examples, or build more agent roles based on one run.** If Luna is
already correct on all 5, test one more realistic weak spot before
spending more on cross-model review.

## Bounded execution contract

- Requires BOTH a changed `ONE_SHOT_REVIEW_PAIR.md` and commit marker
  `[run-review-pairs-once]`; no automatic paid test on normal push.
- At most 5 cases × 3 approaches = **15 short sessions**; stop early on
  routing/auth/runtime problems. Every model at low reasoning effort.
- No file/network/shell tools in direct arms; mixed arm permits only
  `task` to a no-tools Sol leaf.
- No changes to `main`, existing shipped agent code or production
  architecture. GitHub Actions secrets are only used as environment inputs.
- Temporary JSON result artifact, short retention, no raw credentials.
- No repeat runs until results are reviewed and the next product decision
  explicitly requires one.

## Decision guidance

- If Luna alone is equally accurate at lower total cost, do not add Sol
  review by default. It might still be useful on specific failures.
- If Sol alone beats mixed at similar effective cost, experiment with
  a strong Main for that task instead of automatically escalating.
- If reviews hallucinate on clean patches, weigh false positives heavily.
- If all arms pass, **quality benefit is inconclusive**, not evidence of
  agent-layer value; end the test without adding complexity.

Status: first bounded batch **COMPLETE**; see observed results below.

## Observed results — 2026-10-16

[GitHub Actions #38851868295](https://github.com/YB-Park/over-the-luna/actions/runs/38851868295) — all 15 model runs completed. [Temporary run artifact](https://github.com/YB-Park/over-the-luna/actions/runs/38851868295) records per-model usage details; artifact expires after 14 days.

| Strategy | Correct / 5 | Total elapsed | Input tokens | Output tokens | Actual models |
| --- | ---: | ---: | ---: | ---: | --- |
| Luna direct | **5/5** | 11,246 ms | 17,591 | 246 | `gpt-6-luna` |
| Luna + Sol leaf | **5/5** | 37,768 ms | 60,519 | 1,513 | `gpt-6-luna`, `gpt-6.1-sol` |
| Sol direct | **5/5** | 14,816 ms | 17,632 | 180 | `gpt-6.1-sol` |

Every incorrect candidate was detected; both correct candidates passed without false positives. The Luna + Sol leaf route was actually exercised, not inferred from text; the model usage stream recorded both provider models.

**Decision:** this set is at the **quality ceiling** for all three strategies; it gives **zero observed marginal defect-detection gain** from always adding Sol. The mixed route took **3.36× Luna-only wall time** and **3.44× input tokens**, and is not justified as *default review* on this evidence. **Those are not USD cost ratios.** SDK `copilotUsage.totalNanoAiu` is not a combined Copilot + OpenAI USD bill; consult each provider's billing records. Tiny sample cannot determine general model superiority.

**Next experiment, only if useful:** one or two actual implementation tasks with independent hidden tests, or an observed Luna weakness in real user work. Do not add reviewers or rerun these easy cases to seek a significant p-value. Keep Sol optional, not automatic.
