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

Status: not yet run.
