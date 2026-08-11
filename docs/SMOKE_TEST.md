# Over the Luna — VS Code Runtime Smoke Test

This checklist verifies behavior that static validation cannot prove: the VS Code agent runtime, model routing, subagent tool resolution, and handoffs.

## Preflight

Before testing:

- Use VS Code **1.128.0 or newer** so GPT-5.6 Luna is supported.
- Confirm the installed plugin reports **v0.3.0**.
- Confirm your GitHub Copilot organization/plan enables the models you intend to test.
- Reload VS Code after updating the plugin.
- Open Chat customizations diagnostics and confirm the Over the Luna agents load without configuration errors.

### Important: the coordinator having no edit tool is expected

When **Over the Luna** is active, the parent Sonnet coordinator intentionally has only the agent and todo tool sets.

It is therefore normal for direct edit/terminal tools to appear unavailable **on the parent coordinator**.

That is not a failure by itself. The important check is that the delegated worker receives the tools declared in its own agent definition.

If the parent says it cannot complete a coding task merely because its own edit tool is unavailable, instead of delegating, record that as a **routing failure**.

If an expanded **Luna Implementer**, **Kimi Deep Worker**, or **MAI Mechanical** subagent cannot use its own edit or execute tools, record that as a **subagent tool-resolution failure**.

---

## Test 1 — Small clear edit

Use **Over the Luna** and request a harmless, clearly scoped repository edit.

Example:

> Add a small unit test for an existing edge case and run the focused test.

Expected behavior:

1. Parent prints a route beginning with **Luna Implementer**.
2. A **Luna Implementer** subagent actually starts.
3. The expanded subagent shows GPT-5.6 Luna as its model, unless Copilot visibly falls back because of availability/cost-tier rules.
4. The worker can read, edit, and execute validation.
5. Parent Sonnet does not inspect/edit repository files itself.

Pass criteria:

- worker performs the repository change;
- focused validation runs;
- no `HARNESS_FAILURE`;
- no Sonnet repository work.

## Test 2 — Unfamiliar repository path

Ask for a change whose affected location is not obvious.

Expected route:

`Luna Explorer → Luna Implementer → Luna Reviewer`

Check that:

- Explorer is read-only;
- Explorer returns compact file/symbol findings;
- Implementer receives enough context to work without repeating a full repository-wide investigation;
- Luna Reviewer independently checks the completed change;
- Sonnet only routes and synthesizes.

## Test 3 — Mechanical repetition

Request an obviously repetitive, already-designed change, for example several DTOs/mappers/mocks or a mechanical rename following an existing pattern.

Expected implementation worker:

**MAI Mechanical**

Check that MAI:

- follows an existing pattern;
- does not invent architecture decisions;
- can edit and execute focused validation;
- returns `REROUTE: decision required` instead of guessing when a real design decision appears.

## Test 4 — Long bounded multi-file task

Choose a coherent task with clear acceptance criteria that spans several files and likely needs repeated test/fix cycles.

Expected implementation worker:

**Kimi Deep Worker**

Check that:

- one Kimi worker owns the coherent implementation rather than several overlapping workers;
- Kimi does not attempt to orchestrate more agents;
- relevant tests/diagnostics run;
- a Luna review follows when the change is non-trivial.

## Test 5 — High-risk review escalation

Use a change involving one of:

- authentication/authorization;
- concurrency or ordering;
- transactions/state machines;
- persistence/data integrity;
- migration behavior;
- public API/schema compatibility.

Expected behavior:

- implementation is still routed to the appropriate worker;
- **Luna Reviewer** performs first-line review;
- **Sonnet Reviewer** is used only for the high-risk/subtle second-line review or explicit Luna uncertainty.

Sonnet Reviewer must not edit files.

## Test 6 — Human-gated Opus

After a meaningful change, use the **Critical review with Opus** handoff manually.

Expected behavior:

- Opus is never automatically invoked by the coordinator;
- the handoff preserves the conversation context;
- Opus reviews without editing;
- the **Fix accepted findings with Luna** handoff is available afterward.

## Test 7 — Harness failure path

If a worker cannot be invoked, its configured model is unavailable, or its required tool is unexpectedly missing, verify that the coordinator does **not** silently become the implementer.

Expected behavior:

`HARNESS_FAILURE: <reason>`

The response should identify the failing worker and the visible missing model/tool when known, then offer the **Continue directly with Luna** handoff.

If Sonnet silently edits the repository instead, fail this test.

## Test 8 — Luna Solo baseline

Run comparable small/medium work with **Luna Solo**.

Compare with Over the Luna on:

- elapsed time;
- AI credits/tokens when visible;
- first-pass correctness;
- number of agent calls;
- human interventions;
- review findings.

Do not use the exact same completed change for both tests; cached context and prior edits would bias the comparison.

---

## Release gates

Before treating a version as ready for normal use, all of these should hold:

- [ ] Agent Plugin installs and loads without diagnostics errors.
- [ ] Over the Luna parent has only routing/todo capabilities by design.
- [ ] A substantive repository task always invokes at least one subagent.
- [ ] Luna Implementer can read/edit/execute successfully.
- [ ] MAI Mechanical can read/edit/execute successfully.
- [ ] Kimi Deep Worker can read/edit/execute successfully.
- [ ] Reviewer agents cannot edit.
- [ ] Sonnet performs zero repository tool calls in a healthy Over the Luna run.
- [ ] Opus is never automatically invoked.
- [ ] Harness failures are visible and do not silently fall back to Sonnet coding.
- [ ] No duplicated implementation workers are launched for the same coherent task without an explicit request.

## What to capture when a test fails

Record:

- VS Code version;
- GitHub Copilot extension version;
- plugin version;
- active parent agent/model;
- delegated subagent name and displayed model;
- the route line;
- the exact missing/disabled tool message;
- expanded subagent tool calls when available;
- whether the model visibly fell back;
- relevant Chat diagnostics/debug output.

This information is much more useful than a screenshot of only the final error message because it distinguishes routing failures from VS Code model/tool-resolution failures.
