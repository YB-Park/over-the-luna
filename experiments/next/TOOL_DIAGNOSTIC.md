# P1b tool-use confound: 1 case × Luna/Sol

Not a second quality benchmark. In the original real-edit evaluation, Luna
and Sol produced **zero changed files** on both tasks while Haiku and Sonnet
made valid edits. This could reflect permission/tool behavior rather than
model intelligence.

This one-shot diagnostic repeats ONLY `risk_idempotency` for Luna and Sol,
capturing **non-secret** tool event types, permission kinds, sanitized tool
names / file basenames, allow/deny decisions and up to 500 characters of
the model's final explanation. No raw file contents, API keys or raw request
payloads are printed. No new tools or permissions are granted relative to
the first experiment. In particular, shell remains prohibited and the two
expected fixture paths are the only write-eligible paths.

[First implementation run](https://github.com/YB-Park/over-the-luna/actions/runs/38852208338).

Approval marker: a changed `ONE_SHOT_TOOL_DIAGNOSTIC.md` and head commit
message `[run-tool-diagnostic-once]`. No recurring paid test.

If the model requests `bash` rather than `edit`, or if permissions are
rejected for an otherwise legitimate path, classify as **tool policy mismatch**,
not code competence. If no tool events occur, inspect the model explanation
and environment. Do not rerun the full four-model comparison until a specific
compatibility difference has been isolated.

## Completed diagnostic and fixed-tool replay

- [First diagnostic, Actions #38852527142](https://github.com/YB-Park/over-the-luna/actions/runs/38852527142): Luna and Sol read through `view`, but both answered that no file-edit tool was available. No write permission event was even requested; this is an **exposure/selection mismatch**, not a denial of a requested valid file write.
- SDK source [Node README](https://github.com/github/copilot-sdk/blob/main/nodejs/README.md) and agent-loop docs identify canonical builtin tools `edit_file` and `apply_patch` (in addition to `view`). Initial allowlist used `edit` but did not include those names.
- After allowing `edit_file` and `apply_patch` **equally for all models**, [corrected diagnostic Actions #38852688180](https://github.com/YB-Park/over-the-luna/actions/runs/38852688180) reported actual `apply_patch` tool execution, approved write permissions for `src/ledger.py` and `tests/test_ledger.py`, and **independent hidden test PASS for Luna 6 and Sol 6.1 (both 1/1)**.
- Neither run used shell or network tools; only explicit fixture source/test files were changed.

**Decision:** earlier Luna/Sol 0/2 no-edit observation is invalid as a model-competence comparison. The benchmark harness was under-provisioning their editor tool vocabulary; this was fixed in the common tool allowlist. One four-model/two-case matched rerun is warranted; after that, stop the fixture benchmark and return to product design.

Status: **root cause confirmed; equal canonical tools fixed; 1-case Luna/Sol replay PASS**.
