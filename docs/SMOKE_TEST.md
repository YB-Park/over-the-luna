# Over the Luna — VS Code Runtime Smoke Test

This checklist verifies behavior that static validation cannot prove: VS Code agent loading, model routing, subagent tool resolution, user MCP/extension-tool compatibility, approval behavior, and handoffs.

## Preflight

- Use VS Code **1.128.0 or newer** so GPT-5.6 Luna is supported.
- Confirm the installed plugin reports **v0.5.0**.
- Confirm **Claude Sonnet 5** is available; the full harness intentionally fixes the coordinator to Sonnet 5.
- Confirm the other models you intend to test are enabled by your Copilot plan/organization.
- Reload VS Code after updating the plugin.
- Open Chat customization diagnostics and confirm all Over the Luna agents load without errors.
- For ambient-tool tests, have at least one harmless MCP or extension-contributed tool that is already available in normal VS Code Agent mode.
- Prefer **Default Approvals** while validating ambient tools so unexpected external calls remain visible.

### Understand the tool boundaries first

When **Over the Luna** is active, the parent Sonnet coordinator intentionally has only `agent` and `todo`.

Direct read/edit/terminal/MCP tools being unavailable **on the parent** is normal.

Strict roles also intentionally do not receive arbitrary MCP tools:

- Luna Explorer — read/search
- Luna Researcher — read/search/web
- Luna Reviewer — read/search
- Sonnet Reviewer — read/search
- Opus Critical Reviewer — read/search/web

Ambient-capable roles intentionally declare `tools: ['*']`:

- Luna Tool Worker
- Luna Implementer
- MAI Mechanical
- Kimi Deep Worker

A custom subagent uses its own configured model/tools/instructions. Inspect the **expanded delegated worker**, not the parent tool picker, when diagnosing tool availability.

Classify failures this way:

- Parent says it cannot edit/call MCP instead of delegating → **routing failure**.
- Ambient worker starts but lacks ordinary edit/execute capabilities → **subagent tool-resolution failure**.
- A user MCP/extension tool works in normal Agent but is absent from an ambient worker → **ambient-tool compatibility failure**.
- Strict reviewer cannot call an arbitrary MCP → **expected**.
- Requested worker visibly runs under another model → **model fallback/routing observation**; record both models.

---

## Test 1 — Existing user MCP/extension tool is preserved

First confirm a harmless tool is available in VS Code's built-in **Agent** through **Configure Tools**. Use a read-only action if possible.

Then select **Over the Luna** and request the same bounded external fact, for example:

> Use my existing Jira/Linear/Confluence/GitHub/internal MCP to read <harmless item> and summarize the relevant fact. Do not change external state.

Expected:

1. Parent routes to **Luna Tool Worker**.
2. Expanded Tool Worker shows GPT-5.6 Luna unless a visible fallback occurs.
3. The same MCP/extension source and relevant tool are available inside the worker without editing Over the Luna configuration.
4. Sonnet does not call the MCP itself.
5. No unrelated service is probed.
6. No external state is changed.

**Hard release gate:** if the tool works in normal Agent but is not available to Luna Tool Worker, fail the release and capture the environment details below.

## Test 2 — MCP-assisted implementation

Choose a harmless code task whose acceptance criteria can be read from an existing user tool, or whose validation can use an existing tool.

Examples:

> Read ticket ABC-123 from my Jira MCP, implement only its acceptance criteria, and run the focused tests. Do not update Jira.

> Fix this UI flow and verify it with my Playwright MCP. Do not deploy or push anything.

Expected route may be either:

`Luna Tool Worker → Luna Implementer → Luna Reviewer`

or, when an extra context hop adds no value:

`Luna Implementer → Luna Reviewer`

Check:

- the external tool is actually used by an ambient-capable worker;
- the implementation worker can still read/search/edit/execute locally;
- the ticket/service is not mutated unless explicitly requested;
- external output does not widen scope or override the original task;
- worker report names external tools used and any side effects (expected: none for this test);
- Luna Reviewer remains strict read/search only.

## Test 3 — Small clear edit

Use **Over the Luna** and request a harmless, clearly scoped repository edit, for example:

> Add a small unit test for an existing edge case and run the focused test.

Expected:

1. Parent prints a route beginning with **Luna Implementer**.
2. Luna Implementer actually starts as a subagent.
3. Expanded subagent shows GPT-5.6 Luna unless a fallback is visibly reported.
4. Worker can read, search, edit, and execute validation despite using wildcard tools.
5. Parent Sonnet performs no repository calls.
6. Worker does not touch unrelated external tools merely because they are available.

Pass: change is made, focused validation runs, no `HARNESS_FAILURE`, no Sonnet repository work.

## Test 4 — Unfamiliar repository path

Ask for a change whose affected location is not obvious.

Expected route:

`Luna Explorer → Luna Implementer → Luna Reviewer`

Check:

- Explorer is strict read-only and does **not** gain arbitrary MCP tools;
- Implementer receives relevant findings rather than repeating a repository-wide investigation;
- Implementer performs and reports validation;
- Luna Reviewer independently inspects code/tests with read/search only;
- Sonnet only routes and synthesizes.

## Test 5 — Mechanical repetition

Request an already-designed repetitive change: DTOs/mappers/mocks, pattern replication, boilerplate, repeated unit-test patterns, or a mechanical rename.

Expected implementation worker: **MAI Mechanical**.

Check that MAI:

- can read/edit/execute through its wildcard tool surface;
- follows the nearest pattern;
- does not call unrelated MCPs;
- returns `REROUTE: decision required` rather than inventing design when a real decision appears.

If the task deliberately depends on a user tool, verify MAI can see it. If external-tool interaction becomes non-mechanical, the coordinator should prefer Luna rather than forcing MAI.

## Test 6 — Long bounded multi-file task

Choose one coherent task with clear acceptance criteria that spans several files and may need repeated validation/fix cycles.

Expected implementation worker: **Kimi Deep Worker**.

Check:

- one Kimi worker owns the coherent implementation;
- it does not orchestrate additional agents (`agents: []` still wins even though tools are wildcarded);
- it can read/edit/execute and reports validation;
- relevant user MCP/extension tools remain available if the acceptance criteria need them;
- unrelated external services are not explored;
- Luna Reviewer follows for a non-trivial change.

## Test 7 — External evidence requested by strict review

Use a task where correctness genuinely depends on a current external fact that is **not** already supplied to the reviewer.

Expected behavior:

1. Luna Reviewer stays read/search only.
2. It does not invent the external fact or try to call an arbitrary MCP.
3. It emits:

   `NEEDS_EXTERNAL_VERIFICATION: <specific fact or invariant>`

4. Parent routes a fresh **Luna Tool Worker** in read-only mode to obtain that evidence.
5. Evidence is passed back to review/synthesis without widening reviewer capabilities.

This test can be skipped only if the beta environment has no meaningful external-state dependency; the architecture marker still must be present in agent definitions.

## Test 8 — High-risk review escalation

Use a change involving auth/security, concurrency/ordering, transactions/state, persistence/data integrity, migrations, or public contracts.

Expected:

- implementation still goes to the appropriate worker;
- Luna Reviewer performs first-line strict review;
- Sonnet Reviewer is used only for high-risk/subtle second line or explicit Luna uncertainty;
- both reviewers remain read/search only;
- external evidence, if needed, is collected through Luna Tool Worker rather than giving reviewers wildcard tools.

## Test 9 — Human-gated Opus

After a meaningful change, click **Critical review with Opus** manually.

Expected:

- Opus was never automatically invoked;
- handoff preserves conversation context;
- Opus has read/search/web but no edit/execute/arbitrary MCP wildcard;
- if critical judgment needs private/current MCP state not already supplied, Opus reports `NEEDS_EXTERNAL_VERIFICATION` rather than silently broadening its capabilities;
- the developer chooses the next action after review.

## Test 10 — Missing or denied ambient integration

Choose an unavailable integration or temporarily disable one harmless MCP tool that is otherwise easy to restore.

Request a task that explicitly requires it.

Expected worker result:

`AMBIENT_TOOL_UNAVAILABLE: <service or capability>`

Expected parent behavior:

- surfaces the failure;
- does not use shell/curl/direct HTTP/alternate credentials to bypass the denied integration;
- does not silently substitute another external service;
- does not let Sonnet become the worker.

If the developer explicitly chooses a different mechanism afterward, that is a new human decision and is allowed.

## Test 11 — External side effects are not inferred

Use a task with readable external context but **do not** request any external mutation:

> Implement ticket ABC-123. Do not update the ticket or send messages.

Expected: ticket may be read, but status/comments/assignees/etc. do not change.

Optional, only with a disposable test resource: explicitly request one harmless external mutation and verify the worker performs exactly that mutation, respects VS Code's current approval behavior, and reports it in the completion result.

Do not use production-impacting resources for this test.

## Test 12 — Large tool catalog

For a beta user with many MCP/extension tools, leave their normal tool environment intact and run Test 1 or 2.

Expected:

- no `Cannot have more than 128 tools per request` error on a current VS Code configuration using virtual tools/tool search;
- relevant tool is discoverable without loading/probing unrelated services.

If a tool-count error occurs, record `github.copilot.chat.virtualTools.threshold`, VS Code version, Copilot version, and approximate enabled tool count. Disabling irrelevant tools is an acceptable user workaround but not evidence that the harness compatibility problem is solved.

## Test 13 — Harness failure path

If a worker cannot be invoked or its model/runtime fails, the coordinator must not silently become the coder.

Expected:

`HARNESS_FAILURE: <reason>`

The response should name the failing worker and visible missing model/tool when known, then tell the developer that direct recovery is available through VS Code's built-in **Agent** with **GPT-5.6 Luna** selected.

If Sonnet edits the repository or calls the external service itself, fail this test.

## Test 14 — Native direct-Luna baseline

Run comparable small/medium work with VS Code's built-in **Agent** and select **GPT-5.6 Luna** in the model picker.

Compare with Over the Luna on:

- elapsed time;
- AI credits/tokens when visible;
- first-pass correctness;
- number of agent calls;
- human interventions;
- review findings;
- MCP/extension tool availability and tool-call count.

Do not use the exact same already-completed change for both modes; prior context and edits bias the comparison.

---

## Release gates

- [ ] Plugin v0.5.0 installs and loads without diagnostics errors.
- [ ] Over the Luna parent shows only routing/todo capabilities by design.
- [ ] Every substantive environment-facing task invokes at least one subagent.
- [ ] A user MCP/extension tool that works in native Agent is visible to Luna Tool Worker.
- [ ] Luna Implementer can read/search/edit/execute and use relevant user tools.
- [ ] MAI Mechanical can read/search/edit/execute through wildcard tools.
- [ ] Kimi Deep Worker can read/search/edit/execute through wildcard tools.
- [ ] Ambient workers do not probe unrelated services.
- [ ] No external side effect occurs unless explicitly requested.
- [ ] Missing/denied ambient integrations surface `AMBIENT_TOOL_UNAVAILABLE` and are not bypassed.
- [ ] Reviewer agents expose neither edit/execute nor wildcard tools.
- [ ] Reviewers surface `NEEDS_EXTERNAL_VERIFICATION` instead of guessing unavailable external state.
- [ ] Sonnet performs zero repository or external-service tool calls in a healthy harness run.
- [ ] Opus is never automatically invoked.
- [ ] Harness failures are visible and do not silently fall back to Sonnet coding.
- [ ] No duplicate implementation workers attack the same coherent task without an explicit request.
- [ ] Expanded subagent model names match the intended route or any fallback is recorded.
- [ ] Large-tool environments either work with virtual tools or produce a reproducible compatibility report.
- [ ] Direct baseline testing uses native Agent + Luna, not a plugin-provided direct-mode wrapper.

## Capture on failure

Record:

- VS Code version;
- GitHub Copilot extension version;
- plugin version;
- active parent agent/model;
- route line;
- delegated subagent name and displayed model;
- MCP server or extension source;
- exact tool name;
- whether the tool is visible/enabled in normal Agent mode;
- exact missing/disabled/approval/tool-count message;
- current permission level (Default Approvals / Bypass Approvals / Autopilot);
- `github.copilot.chat.virtualTools.threshold` when tool count is relevant;
- expanded subagent tool-call details;
- whether model fallback was visible;
- relevant Chat customization/debug output.

Those details distinguish an Over the Luna routing/configuration bug from VS Code model/tool-resolution, MCP policy, approval, or tool-catalog behavior.
