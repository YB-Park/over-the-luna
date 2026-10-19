# P10 — offline evidence and token accounting

This is a **measurement utility**, not a router benchmark. Historical P5
source: [actual public Actions artifact](https://github.com/YB-Park/over-the-luna/actions/runs/38869234496).
The compact fixture contains **only** published aggregate per-message
usage, tool-start names, lifecycle lists, and accepted quality flags. No
prompts, code diffs, logs, corporate inputs, or credentials.

Run \`python scripts/role_trace_accounting.py --summary tests/fixtures/p5_role_accounting.json\`.
The script never calls a model, VS Code Host, SDK, web endpoint or tool.
It prints a bounded, sanitized aggregate suitable for internal review;
do **not** export internal sessions to run it. Full source artifacts can
remain where policy requires.

Strict distinctions:
- A \`task\` tool-start means **attempt**, not specialist contribution.
- A named started/completed event pair means **lifecycle observed**,
  not returned evidence, independent judgment or Host-native execution.
- \`roleChain: true\` and agent-registration metadata are not proof.
- The single P5 pair had both quality passes but no demonstrated
  Council contribution. The subsequent diagnostic identified
  standalone \`custom_agent_prompt\` failure; this analyzer **does not**
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
\`hostHandbackProven\` deliberately remains false. It must not be
promoted to true by self-reported prose or a metadata flag.
