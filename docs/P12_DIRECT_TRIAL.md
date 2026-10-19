# P12 — one bounded paid DIRECT-path product experiment

Question: Does RC2 Main instruction overhead materially affect the quality
and total usage of an authentic bounded public code fix versus plain SDK?
The P5 arms had different role-calling instructions, so P5 did not isolate
direct-path Main instruction overhead.

Work: Fix the real P10 missing/invalid toolCallId matching bug in
scripts/role_trace_accounting.py and add a test in
tests/test_role_trace_accounting.py. The independent grader exercises
missing, empty, nonstring, mismatched, valid and repeated IDs. Both arms
get the SAME prompt, Luna low reasoning, source snapshot, tool set and
edit policy. Subagent tools are deliberately absent in BOTH arms.
Only this two-session Actions workflow performs inference. No retries
or premium models are scheduled. No external company data or logs.

Interpretation: DIRECT SDK instruction overhead only. This cannot prove
Host-native subagent handback or actual Council benefit. Check independent
quality oracle, token totals, Copilot nano-AIU, time and tool attempts.
One sample is directional and confounded by execution randomness.
If a run fails due to environment, mark INCONCLUSIVE rather than rerun
unsupported leaf delegation.

Preparation is static and free. A separate sentinel commit containing
docs/P12_DIRECT_SENTINEL.md and [run-p12-once] starts the paid job once.
