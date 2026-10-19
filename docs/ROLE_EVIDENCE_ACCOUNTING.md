# P10 — offline evidence and token accounting

This is a **measurement utility**, not a router benchmark. Historical P5
source: [actual public Actions artifact](https://github.com/YB-Park/over-the-luna/actions/runs/38869234496).
The compact fixture contains **only** published aggregate per-message
usage, tool-start names, lifecycle lists, and accepted quality flags. No
prompts, code diffs, logs, corporate inputs, or credentials.

Run `python scripts/role_trace_accounting.py --summary tests/fixtures/p5_role_accounting.json`.
The script never calls a model, VS Code Host, SDK, web endpoint or tool.
It prints a bounded, sanitized aggregate suitable for internal review;
do **not** export internal sessions to run it. Full source artifacts can
remain where policy requires.

Strict distinctions:
- A `task` tool-start means **attempt**, not specialist contribution.
- A named started/completed event pair means **lifecycle observed**,
  not returned evidence, independent judgment or Host-native execution.
- `roleChain: true` and agent-registration metadata are not proof.
- The single P5 pair had both quality passes but no demonstrated
  Council contribution. The subsequent diagnostic identified
  standalone `custom_agent_prompt` failure; this analyzer **does not**
  infer the causal failure from P5 alone.
- Input/output token event totals and summed **reported Copilot nano-AIU**
  are separate quantities; no conversion to OpenAI API USD or inferred
  monetary price. Unknown meters remain null, never a fake zero.
- Observed input-token delta is not evidence that delegation caused
  all of it, nor a general performance/cost ranking.

**Decision gate:** Keep Council quality and Host-native value unverified
until a real named leaf completes in VS Code Copilot Host, returns
source-specific evidence, and influences a decision. A narrowly bounded
paid task is justified when it can establish that value; rerunning the
known unsupported standalone SDK plugin-leaf path is not.

**Scope:** Accounting reports conservative observations only. The
runtime does not emit a verified Host receipt in this schema, so
`hostHandbackProven` deliberately remains false. It must not be
promoted to true by self-reported prose or a metadata flag.

## P11 — immutable source provenance and acceptance integrity

On 2026-10-19 the exact original public Actions ZIP
[run 38869234496, artifact 12032631126](https://github.com/YB-Park/over-the-luna/actions/runs/38869234496)
was downloaded and examined locally (no new model calls). The extracted
`summary.json` has SHA-256:

`9f678b2c60267e95f414b098d28da3c5de713d09c075b04147c5967784b5b504`

The event-by-event input/output/nano-AIU arrays and named task starts in
the previous compact fixture matched the original. The fixture now also
retains the independent grader's **complete check map**, failed-check list,
test count, observed-model flag, unexpected-change list and runtime error,
without retaining prompts, patches, approval data or unrelated tool details.

`python scripts/p5_fixture_provenance.py --source /path/to/extracted/summary.json --fixture tests/fixtures/p5_role_accounting.json`

This offline reproducibility command compares the **pinned original
summary hash** and a strict field allowlist against the committed fixture.
It does not download anything; the source file must be the **public P5**
artifact, not a company log. Any source mismatch fails, and no private
content is printed.

`qualityAccepted` now requires all archived independent checks to pass,
an empty failed-check list, positive actual test count, observed model,
no unexpected changes and no runtime error in addition to the recorded
acceptance/pass flags. An inconsistent source cannot turn those two flags
alone into a quality pass.

The GitHub Actions tests use a deterministic offline fixture and
synthetic adversarial modifications; they **do not** fetch an expiring
artifact in CI. The immutable hash and extractor permit on-demand
reproduction from the public original, without SDK or inference costs.
This proves historical **trace fidelity**, not Council's causal benefit,
Host permissions, or correct agent choice on new tasks.
