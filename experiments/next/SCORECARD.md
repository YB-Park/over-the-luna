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
