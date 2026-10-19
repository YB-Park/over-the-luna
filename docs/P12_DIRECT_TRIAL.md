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

## Observed results — 2026-10-19

Real [P12 one-shot Actions #39185467397](https://github.com/YB-Park/over-the-luna/actions/runs/39185467397), archived artifact
`p12-direct-main-public-pair` (id `12158115456`):
both arms completed and **passed** independently held-out missing/invalid
toolCallId checks, existing plus authored regression tests, and the scoped
change oracle. Both changed the same implementation to require a valid
nonempty string call ID; both performed two view calls and one apply_patch;
neither launched a subagent. Tests differ in their specific extra cases.

| Metric | Plain SDK | RC2 selected Main |
| --- | ---: | ---: |
| Input tokens | 18,402 | 23,821 |
| Output tokens | 715 | 733 |
| Reported Copilot nano-AIU | 139,712,500 | 143,455,500 |
| Elapsed ms | 9,830 | 9,059 |
| Usage events | 3 | 3 |
| Grader accepted | Yes | Yes |

RC2 used **5,419 more input tokens (+29.4%)** and **3,743,000 more
reported nano-AIU (+2.7%)**. Its wall clock time was 771 ms shorter.
The differences are observations from **one non-blinded paired run**,
not a causal estimate of Main prompt overhead or a population-level
quality ranking. Nano-AIU is not OpenAI API USD. This task deliberately
excluded all delegation tools, so it does **not** demonstrate the
conditional Architect/Reviewer topology actually operating.

**Product decision:** Keep the direct Main route; both paths passed
without leaves. Main-prompt footprint warrants a *focused reduction*
only if it preserves essential role/permission/verification behavior.
No need to add a Planner or more paid subagent calls based on this one
trial. The real public accounting bug discovered by the independent
oracle was fixed on the research branch with negative regression tests.
Actual named VS Code Copilot Host delegation is still the product gate.

**Measurement limitation:** P12's runner snapshots the four known seed
files rather than an exhaustive worktree inventory; the recorded
changed-path assertion covers those seed files and permitted write
requests. It does not independently prove absence of all new files.
Do not present it as absolute filesystem security enforcement.
