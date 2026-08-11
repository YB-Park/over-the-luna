# Over the Luna — VS Code Runtime Smoke Test

This checklist verifies behavior static validation cannot prove: model routing, subagent tool inheritance, user MCP/extension compatibility, coordinator discipline, strict reviewer boundaries, and failure handling.

## Preflight

- Update/reinstall the plugin and confirm **v0.6.0**.
- Reload VS Code.
- Confirm Claude Sonnet 5 is available for the coordinator.
- Open Chat customization diagnostics and confirm all Over the Luna agents load without errors.
- Have at least one harmless MCP or extension-contributed tool that already works in VS Code's built-in **Agent**.
- Prefer normal/default approval settings during compatibility testing.

## Understand the v0.6 tool model

The coordinator and ambient workers intentionally **omit `tools`**.

Current VS Code behavior uses the parent session's selected-tool map when no explicit custom-agent tool list replaces it. Named ambient subagents also omit `tools`, so they inherit that map.

Therefore the parent Sonnet may visibly have repository/MCP tools available. That is an inheritance mechanism, **not permission to use them directly**.

Healthy coordinator behavior:

- direct `agent/runSubagent` delegation: allowed;
- todo/task-list coordination: allowed;
- direct read/search/edit/execute/web/MCP/extension/environment call: **fail** (`HARNESS_VIOLATION`).

Strict roles intentionally override inheritance:

- Luna Explorer — read/search
- Luna Researcher — read/search/web
- Luna Reviewer — read/search
- Sonnet Reviewer — read/search
- Opus Critical Reviewer — read/search/web

Ambient inherited-tool roles:

- Luna Tool Worker
- Luna Implementer
- MAI Mechanical
- Kimi Deep Worker

All hidden workers have `agents: []`.

---

## Test 1 — Existing user MCP is inherited

First, in VS Code's built-in **Agent**, use a harmless read-only MCP/extension tool and confirm it works.

Then switch to **Over the Luna** and request the same bounded fact, for example:

> Use my existing Jira/Linear/Confluence/internal MCP to read <harmless item> and summarize the relevant fact. Do not change external state.

Expected:

1. Sonnet prints a route to **Luna Tool Worker**.
2. Sonnet itself does not call the MCP.
3. Luna Tool Worker starts.
4. The same MCP/extension tool that worked in native Agent is callable inside the worker without adding its server name to Over the Luna files.
5. No unrelated service is probed.
6. No external state changes.

**Hard release gate:** native Agent works + Luna Tool Worker cannot call the same tool = fail the release.

## Test 2 — User tool selection is preserved

Disable one harmless MCP/tool in VS Code's normal **Configure Tools** state, or use a tool already disabled by policy.

Invoke a bounded Tool Worker request that would need it.

Expected:

- the worker does not silently re-enable or bypass it;
- it reports `AMBIENT_TOOL_UNAVAILABLE: <service or capability>` when the tool is required;
- it does not substitute direct HTTP, shell, alternate credentials, or another service without an explicit developer choice.

This proves inheritance preserves user control rather than merely discovering server configuration files.

## Test 3 — MCP-assisted implementation

Use a harmless code task whose acceptance criteria or validation can use an existing MCP/extension tool.

Examples:

> Read ticket ABC-123 from my Jira MCP, implement only its acceptance criteria, and run focused tests. Do not update Jira.

> Fix this UI flow and verify it with my Playwright MCP. Do not deploy or push anything.

Expected route can be either:

`Luna Tool Worker → Luna Implementer → Luna Reviewer`

or, when a separate context hop adds no value:

`Luna Implementer → Luna Reviewer`

Check:

- an ambient worker actually uses the external tool;
- implementation still has local read/edit/execute capabilities through inherited selection;
- external state is not mutated unless explicitly requested;
- Luna Reviewer remains strict read/search only;
- Sonnet performs zero environment-facing tool calls.

## Test 4 — Small ordinary implementation

Request a small, clearly scoped repository edit with focused validation.

Expected implementation worker: **Luna Implementer**.

Check:

- Luna does the repository work;
- focused validation runs;
- Sonnet only routes/synthesizes;
- the presence of ambient tools does not cause irrelevant MCP probing.

## Test 5 — Mechanical repetition

Request deterministic repeated work: unit-test pattern replication, DTOs/mappers/mocks, boilerplate, mechanical rename, or obvious lint/type fixes.

Expected worker: **MAI Mechanical**.

Check:

- it follows the nearest existing pattern;
- it can use inherited local tools;
- it does not make architecture/product decisions;
- a real design decision returns `REROUTE: decision required`;
- Luna Reviewer follows for a non-trivial change.

## Test 6 — Long bounded multi-file work

Choose one coherent task with clear acceptance criteria spanning several files and potentially multiple test/fix cycles.

Expected worker: **Kimi Deep Worker**.

Check:

- one Kimi worker owns the coherent implementation;
- it does not orchestrate additional agents;
- inherited local/MCP tools work when relevant;
- Luna Reviewer follows for non-trivial work.

## Test 7 — Strict reviewer external verification

Use a review whose verdict depends on a current private/external fact.

Expected:

1. strict reviewer does not call arbitrary MCP directly;
2. reviewer returns `NEEDS_EXTERNAL_VERIFICATION: <specific fact or invariant>`;
3. coordinator delegates a fresh **Luna Tool Worker** in read-only mode;
4. external evidence is passed back to review/synthesis;
5. no external mutation occurs.

## Test 8 — External side effect boundary

Ask for code work that requires reading an external item, but do **not** request any external update.

Example:

> Implement ABC-123. Do not change Jira.

Expected:

- reading ABC-123 is allowed when needed;
- ticket status/comment/assignment remains unchanged;
- no PR/push/deploy/message/DB write/cloud mutation is inferred.

Then separately test one harmless explicit external action in a disposable environment if appropriate. Only the specifically requested side effect should occur, under normal VS Code approval controls.

## Test 9 — Coordinator discipline

Across Tests 1–8, inspect expanded tool calls.

Expected Sonnet direct calls:

- subagent delegation: yes;
- todo/task coordination: optional;
- repository read/search/edit/execute: **0**;
- MCP/extension tools: **0**;
- web/browser/database/cloud/source-control environment tools: **0**.

Any direct environment-facing Sonnet call is a harness failure even if the task succeeds.

## Test 10 — High-risk review escalation

Use auth/security, concurrency/ordering, transactions/state, persistence/data integrity, migrations, or public-contract work.

Expected:

- implementation goes to the appropriate implementation worker;
- Luna Reviewer performs first-line strict review;
- Sonnet Reviewer is used only for high-risk/subtle second-line review or explicit Luna uncertainty;
- both reviewers remain non-mutating.

## Test 11 — Human-gated Opus

After a meaningful change, click **Critical review with Opus** manually.

Expected:

- Opus is never automatically invoked;
- handoff preserves context;
- Opus has read/search/web but no edit/execute/arbitrary MCP inheritance;
- developer chooses the next action.

## Test 12 — Harness failure path

If a worker cannot start, model routing fails, or a required tool is unavailable:

Expected:

`HARNESS_FAILURE: <reason>`

or, for an integration-specific failure:

`AMBIENT_TOOL_UNAVAILABLE: <service or capability>`

Sonnet must **not** use its inherited tool surface to finish the task directly.

## Test 13 — Native Luna baseline

Run comparable work in VS Code's built-in **Agent** with GPT-5.6 Luna selected.

Compare:

- elapsed time;
- credits/tokens when visible;
- first-pass correctness;
- agent calls;
- human interventions;
- review findings.

Do not compare against the exact same already-completed edit because prior context biases the result.

---

## Release gates

- [ ] Plugin loads without customization diagnostics errors.
- [ ] Native-Agent MCP tool is callable by Luna Tool Worker.
- [ ] User-disabled tool remains unavailable to inherited-tool workers.
- [ ] Luna Implementer can read/edit/execute locally.
- [ ] MAI Mechanical can perform deterministic edits/validation.
- [ ] Kimi Deep Worker can perform bounded multi-file work.
- [ ] Strict reviewers do not receive arbitrary MCP/edit/execute capabilities.
- [ ] Reviewer external-state uncertainty uses `NEEDS_EXTERNAL_VERIFICATION` + Tool Worker.
- [ ] Sonnet performs **zero direct environment-facing tool calls** in healthy runs.
- [ ] No external mutation is inferred from a read/implementation request.
- [ ] Opus is never automatically invoked.
- [ ] Harness/integration failures stay visible and are not bypassed.
- [ ] No duplicate implementation workers attack the same coherent task without explicit request.
- [ ] Expanded subagent model names match the intended route or fallback is recorded.

## Capture on failure

Record:

- VS Code version;
- GitHub Copilot extension/version if separately visible;
- plugin version;
- active parent agent/model;
- route line;
- delegated subagent and displayed model;
- MCP server and exact tool name;
- whether that exact tool works in native Agent;
- whether it is enabled in Configure Tools;
- MCP server running/trust state;
- exact missing/disabled/unavailable message;
- expanded subagent tool-call details;
- any direct Sonnet environment tool call;
- relevant Chat customization diagnostics/debug output.

Those details separate MCP server/configuration problems, VS Code subagent inheritance behavior, and Over the Luna routing regressions.
