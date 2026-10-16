# Native Copilot Agent vs Over the Luna Next — product dogfooding

**Purpose:** find out whether the *real agent customization* improves
completed developer work, not whether GPT-6 Luna can already solve tiny
SDK fixtures. No long benchmark framework and no automatic API spend.

The tested artifact is
[`candidate-plugin/`](candidate-plugin/README.md), **not** the
existing v1.1.1 root plugin or the custom SDK runners from P0/P1.

## Start only after a local effective-policy check

Select the **Copilot** Agent Host and ensure the intended research agent
is active. Use the same host model (**GPT-6 Luna** as initial control),
selected tools/MCP, reasoning effort, permissions and workspace trust for
both native and candidate. User already confirmed the four model choices
are available; no model catalogue retest is requested.

**Never treat `tools: []` as a zero-tools guarantee.**
The candidate has **no leaf agents**; it never claims an enforceable
read-only helper. The main executable receives the host-selected tools
and works under the host's effective approvals.

## A small set of genuine developer jobs

Begin with **one or two** meaningful current tasks that the user
actually wants to complete. Only expand to a research/document review,
a broader repository contract change, or repetitive maintenance if
the earlier real jobs expose an important difference.

For coding, use two clean/equivalent worktrees of the same repository
revision or two equivalent pending tasks; do not let the first agent's
patch become the next agent's starting hint. Avoid copying output from
one arm into the other. Compare completion with normal repository tests,
build checks, diff scope and reviewed acceptance criteria — **do not
trust a tool's green exit as complete acceptance**.

**One-task paired protocol:**

1. Write the actual user need and a *human-checkable acceptance
   criterion* before starting. Record initial repo SHA and relevant
   unchanged tests/contract.
2. Run native Copilot Agent with the selected model. Record model/effort,
   actual tools, duration, prompts/interruptions, passes/failures and
   any second-pass manual fix, plus cost/credits evidence if available.
3. Run Over the Luna Next on an equivalent clean state with the same
   model and tool permissions. Record the same evidence. Alternate
   execution order on the next task to reduce ordering effects.
4. Save sanitized diffs and run actual focused tests, including the
   model-edited regression tests. Evaluate shared-helper reuse and
   other *non-behavior-only* requirements. A success assertion is not
   ground truth.
5. Compare: independently accepted outcomes, wrong changes,
   rework, total paid usage, attention/permissions, elapsed time and
   developer friction. Never blend Copilot AI Credits and OpenAI API
   USD as if they were the same meter.

A single paired task is a **learning case**, not statistically reliable
proof. Prefer deciding whether to keep, simplify or discard the
candidate over calculating spurious precision.

## Read-only task?

Measure accurate conclusions, real sources, misleading assertions,
unnecessary delegations and zero unintended file changes. External API
research and normal web search need valid citations; user-side
external effects still require authorization.

## Stop conditions

- Effective tool policy differs unexpectedly from the selected host policy.
- An unrequested external write or sensitive cross-provider transfer occurs.
- The runtime silently substitutes the specified comparison model.
- A task is completed with poorer quality or noticeably more user friction
  without a compensating demonstrated gain.
- Enough concrete evidence exists to keep or reject a layer; don't run
  paid experiments just to enlarge a sample.

## Decisions to record

`KEEP`: candidate demonstrably improves something worth the added
complexity. `SIMPLIFY`: an instruction or native capability makes an
extra layer unnecessary. `REJECT`: native agent is as good or better
under realistic use. `UNKNOWN`: mismatched runtime or insufficient
evidence. All are legitimate outcomes.

Use [SCORECARD.md](SCORECARD.md) to record one case; product decisions
go in [docs/NEXT_HARNESS.md](../../docs/NEXT_HARNESS.md). No automatic
PR merge.

## Local observation and first implementation trial (2026-10-16)

The user confirms the research agent appears in the picker and its first
read-only repository exploration showed no anomalies. This is a **reported
smoke check**, not independent Host/runtime evidence. No further model
catalogue verification is planned.

**Next actual trial:** [GitHub Actions-only study](ACTIONS_DOGFOOD.md),
which uses the actual Next instruction body in a matched SDK pair on
**public repository fixtures**. No corporate file export or local worktree
runs are requested. The [old local paired guide](DOGFOOD_TASK_01.md) is
**OPTIONAL/DEFERRED**, not a blocker or required user task. Actions cannot
completely reproduce the actual VS Code Agent Host; evaluate that
limitation transparently.
