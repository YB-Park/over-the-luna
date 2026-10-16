# One-shot P1b implementation comparison — 2026-10-16

Explicitly trigger one bounded comparison on two pre-existing hidden-test fixtures: broad_contract and risk_idempotency. Compare Luna 6, Haiku 5.5, Sol 6.1 and Sonnet 5.5 under identical low-effort settings and isolated temp workspaces. No git push, no repository changes by the models, no shell tool, no repeat. This does not claim Agent Host verification; the user has already confirmed access to the named models in that environment and asked us to proceed with experiments.

## Corrected shared editor tool surface — one explicit matched rerun

The first comparison was invalid for model ranking: Luna and Sol could not edit because the experimental allowlist omitted canonical SDK editor tools. The tool diagnostic confirmed both model families edit successfully when `apply_patch` is enabled. Perform exactly one matched two-task/four-model rerun with the corrected `view/read_file/edit/edit_file/apply_patch/grep/glob` allowlist. Then stop this benchmark and decide from observed evidence; do not auto-repeat.
