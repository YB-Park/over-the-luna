# Over the Luna — VS Code Runtime Smoke Test

This checklist verifies behavior static validation cannot prove: selected-tool inheritance, MCP compatibility, Luna-first routing, bounded Kimi escalation, coordinator discipline, strict review, and failure handling.

## Preflight

- Update/reinstall the plugin and confirm **v0.7.0**.
- Reload VS Code.
- Confirm Claude Sonnet 5 is available for the coordinator.
- Open Chat customization diagnostics and confirm all **9 agents** load without errors.
- Confirm there is **no MAI Mechanical agent**.
- Have at least one harmless MCP/extension tool that works in VS Code's built-in Agent.
- Prefer normal/default approval settings during compatibility testing.

## Tool model

The coordinator and ambient workers intentionally omit `tools` so VS Code can preserve the active selected-tool map.

Inherited-tool roles:

- Over the Luna
- Luna Tool Worker
- Luna Implementer
- Kimi Deep Worker

Strict roles:

- Luna Explorer — read/search
- Luna Researcher — read/search/web
- Luna Reviewer — read/search
- Sonnet Reviewer — read/search
- Opus Critical Reviewer — read/search/web

The parent Sonnet may technically see environment tools for inheritance, but a healthy run permits direct Sonnet calls only for delegation and optional todo/task coordination.

Any direct read/search/edit/execute/web/MCP/extension/environment call by Sonnet is a `HARNESS_VIOLATION`.

---

## Test 1 — Existing user MCP is inherited

First use a harmless read-only MCP/extension tool in native VS Code Agent and confirm it works.

Then select **Over the Luna** and request the same bounded fact.

Expected:

1. route includes **Luna Tool Worker**;
2. Sonnet itself does not call the MCP;
3. Luna Tool Worker invokes the same existing tool without hardcoded server configuration;
4. no unrelated service is probed;
5. no external state changes.

**Hard release gate:** native Agent works + Luna Tool Worker cannot call the same tool = fail.

## Test 2 — User tool selection is preserved

Disable one harmless MCP/tool in Configure Tools, or use one already disabled by policy.

Request a Tool Worker task that requires it.

Expected:

- worker does not re-enable or bypass it;
- required unavailable capability returns `AMBIENT_TOOL_UNAVAILABLE: <service or capability>`;
- no direct HTTP/shell/alternate credential bypass occurs.

## Test 3 — Ordinary implementation

Request a small clearly scoped repository edit and focused validation.

Expected route begins with **Luna Implementer**.

Check:

- Luna performs repository work;
- focused validation runs;
- Sonnet only routes/synthesizes;
- Luna Reviewer follows when the change is non-trivial.

## Test 4 — Mechanical repetition is still Luna

Request deterministic repeated work such as unit-test pattern replication, DTO/schema/mapper/mock boilerplate, a mechanical rename, or obvious lint/type fixes.

Expected implementation worker: **Luna Implementer**, not a dedicated MAI worker.

Check:

- Luna follows the nearest existing pattern;
- no unnecessary redesign appears;
- the expanded implementation subagent normally shows GPT-5.6 Luna;
- if MAI-Code-1-Flash appears, record it as the configured **model fallback**, not a routing role;
- Luna Reviewer follows for a non-trivial change.

## Test 5 — Multi-file work starts with Luna

Choose one coherent bounded task with clear acceptance criteria spanning several coupled files and likely requiring multiple validation/fix cycles.

Expected initial implementation worker: **Luna Implementer**.

This is a critical v0.7 behavior check: **Kimi must not be selected initially merely because the task is large, long, or multi-file.**

Check:

- one Luna implementation owner holds the thread;
- local/MCP tools work when relevant;
- validation/fix iterations continue while progress is converging;
- no duplicate implementation worker attacks the same task.

## Test 6 — Kimi explicit escalation route

Use a bounded disposable task and explicitly ask the harness to use **Kimi Deep Worker** for the implementation.

Expected:

- Sonnet routes to Kimi Deep Worker;
- expanded subagent shows **Kimi K2.7 Code** unless VS Code visibly substitutes a runtime fallback, which must be recorded;
- Kimi owns only the bounded implementation;
- Kimi does not spawn other agents;
- normal Luna Reviewer follows for non-trivial work.

This verifies Kimi remains available without making it a default route.

## Test 7 — Natural `ESCALATE_KIMI` observation

Do not force this solely for release testing. During real beta use, record any Luna Implementer result containing:

`ESCALATE_KIMI: <specific reason>`

When it occurs, verify:

1. the reason is concrete non-convergence/context-continuity evidence, not just task size;
2. Sonnet passes the original acceptance criteria, current implementation state, changed areas, and failed validation to Kimi;
3. Kimi continues the same bounded task instead of restarting broad discovery;
4. a missing product/architecture decision is returned to the developer rather than escalated.

A natural Kimi escalation is useful evidence, but absence of one during a small smoke suite is **not** a release failure.

## Test 8 — MCP-assisted implementation

Use a harmless code task whose acceptance criteria or validation needs an existing MCP/extension tool.

Examples:

> Read ticket ABC-123 from my Jira MCP, implement only its acceptance criteria, and run focused tests. Do not update Jira.

> Fix this UI flow and verify it with my Playwright MCP. Do not deploy or push anything.

Expected route may use Tool Worker first when context isolation is useful, or Luna Implementer directly when the tool naturally belongs inside implementation.

Check:

- ambient worker actually uses the external tool;
- implementation retains local edit/execute capabilities;
- external state is not mutated unless explicitly requested;
- Sonnet performs zero environment-facing tool calls.

## Test 9 — Strict reviewer external verification

Use a review whose verdict depends on a current private/external fact.

Expected:

1. strict reviewer does not call arbitrary MCP directly;
2. reviewer returns `NEEDS_EXTERNAL_VERIFICATION: <specific fact or invariant>`;
3. coordinator delegates a fresh Luna Tool Worker in read-only mode;
4. evidence returns to review/synthesis;
5. no external mutation occurs.

## Test 10 — External side-effect boundary

Ask for code work that requires reading an external item but do not request any external update.

Expected:

- required read is allowed;
- ticket/comment/assignment, remote data, PRs, pushes, deploys, messages, and cloud state remain unchanged.

## Test 11 — High-risk review escalation

Use auth/security, concurrency/ordering, transactions/state, persistence/data integrity, migrations, or public-contract work.

Expected:

- implementation still begins with Luna unless an explicit Kimi request is made or Luna later emits `ESCALATE_KIMI`;
- Luna Reviewer performs first-line review;
- Sonnet Reviewer appears only for high-risk/subtle second-line judgment or explicit Luna uncertainty;
- both reviewers remain non-mutating.

## Test 12 — Human-gated Opus

Click **Critical review with Opus** manually after meaningful work.

Expected:

- Opus is never automatically invoked;
- handoff preserves context;
- Opus remains read/search/web only;
- developer chooses the next action.

## Test 13 — Coordinator discipline

Across all tests, inspect expanded tool calls.

Expected Sonnet direct calls:

- subagent delegation: yes;
- todo/task coordination: optional;
- repository read/search/edit/execute: **0**;
- MCP/extension tools: **0**;
- web/browser/database/cloud/source-control environment tools: **0**.

Any direct environment-facing Sonnet call fails the harness even if the task succeeds.

## Test 14 — Native Luna baseline

Run comparable fresh work in native Agent + GPT-5.6 Luna.

Compare:

- elapsed time;
- tokens/credits when visible;
- first-pass correctness;
- agent calls;
- human interventions;
- review findings.

For any Kimi escalation observed in beta, additionally ask whether Kimi provided a clear advantage over simply continuing with Luna. That evidence determines whether the Kimi routing branch survives future versions.

---

## Release gates

- [ ] Plugin loads as v0.7.0 with **9 agents** and no MAI Mechanical worker.
- [ ] Native-Agent MCP tool is callable by Luna Tool Worker.
- [ ] User-disabled tool remains unavailable to inherited-tool workers.
- [ ] Luna Implementer can read/edit/execute locally.
- [ ] Mechanical repetition routes to Luna Implementer.
- [ ] Multi-file bounded work routes to Luna Implementer initially.
- [ ] Kimi is not selected initially merely because work is large/multi-file.
- [ ] Explicit Kimi request can invoke Kimi Deep Worker as Kimi K2.7 Code, or any runtime substitution is visibly recorded.
- [ ] Strict reviewers do not receive arbitrary MCP/edit/execute capabilities.
- [ ] Reviewer external-state uncertainty uses `NEEDS_EXTERNAL_VERIFICATION` + Tool Worker.
- [ ] Sonnet performs **zero direct environment-facing tool calls** in healthy runs.
- [ ] No external mutation is inferred.
- [ ] Opus is never automatically invoked.
- [ ] Harness/integration failures stay visible and are not bypassed.
- [ ] No duplicate implementation workers attack the same coherent task without explicit request.

## Capture on failure or escalation

Record:

- VS Code version;
- Copilot version if visible;
- plugin version;
- route line;
- delegated subagent and displayed model;
- exact MCP/tool and Configure Tools state when relevant;
- native-Agent result for the same MCP/tool;
- validation result/failure;
- any `ESCALATE_KIMI` reason and implementation state handed to Kimi;
- any direct Sonnet environment tool call;
- relevant Chat customization diagnostics/debug output.
