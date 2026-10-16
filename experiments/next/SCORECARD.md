# Small experiment scorecard

Copy this template only for an experiment that could change a product decision. Keep results brief; an empty result is **not** a PASS.

| Field | Entry |
| --- | --- |
| Date / experiment / decision ID | |
| Task and observable acceptance criteria | |
| Runtime (VS Code build / Copilot CLI / Agent Host / plugin revision) | |
| Control and candidate | |
| Exactly one changed variable | |
| Requested model/effort vs **observed** model/effort | |
| Tools and leaf calls actually observed | |
| Correctness evidence (independent checks) | |
| Total AI Credits or cost + provenance; otherwise UNKNOWN | |
| Elapsed time and retries | |
| Unusual cost, failures, or policy denials | |
| Decision: ADOPT / REJECT / RETEST / UNKNOWN | |
| What result would reverse this decision? | |

**Rules:** Authentication and policy failures are BLOCKED, not model failures. Reviewer PASS is not ground truth. Avoid numerical P95 claims from tiny samples. Never include tokens or secrets.

## Paired real-work recording — native vs Next

Use the existing generic table above separately for **both** arms.
For each paired task record:
- stable starting revision and clean-worktree state;
- same Host/model/effort/tools/permissions in both arms (or classify INVALID);
- accepted output and changed-file diff (or link to a sanitized stored diff);
- actual focused/edited tests run and missing acceptance invariants;
- model/tool IDs, retries, approvals, developer corrections, elapsed time;
- Copilot credits vs OpenAI API costs **separately**, with source/UNKNOWN;
- final `KEEP / SIMPLIFY / REJECT / UNKNOWN` decision.
