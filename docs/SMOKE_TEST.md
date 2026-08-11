# Over the Luna — VS Code Runtime Smoke Test

This checklist verifies behavior that static validation cannot prove: VS Code agent loading, model routing, subagent tool resolution, and handoffs.

## Preflight

- Use VS Code **1.128.0 or newer** so GPT-5.6 Luna is supported.
- Confirm the installed plugin reports **v0.4.0**.
- Confirm **Claude Sonnet 5** is available; the full harness intentionally fixes the coordinator to Sonnet 5.
- Confirm the other models you intend to test are enabled by your Copilot plan/organization.
- Reload VS Code after updating the plugin.
- Open Chat customization diagnostics and confirm all Over the Luna agents load without errors.

### Parent edit tools being disabled is expected

When **Over the Luna** is active, the parent Sonnet coordinator intentionally has only the `agent` and `todo` tool sets.

Direct read/edit/terminal tools being unavailable **on the parent** is therefore normal. It is not a worker-tool failure.

A custom subagent has its own model/tools/instructions. The important check is whether the expanded delegated worker gets the tools declared in its own agent file.

Classify failures this way:

- Parent says it cannot edit instead of delegating → **routing failure**.
- Luna Implementer/Kimi/MAI starts but lacks edit/execute → **subagent tool-resolution failure**.
- Requested worker visibly runs under a different model → **model fallback/routing observation**; record both models.

---

## Test 1 — Small clear edit

Use **Over the Luna** and request a harmless, clearly scoped repository edit, for example:

> Add a small unit test for an existing edge case and run the focused test.

Expected:

1. Parent prints a route beginning with **Luna Implementer**.
2. Luna Implementer actually starts as a subagent.
3. Expanded subagent shows GPT-5.6 Luna unless a fallback is visibly reported by the product.
4. Worker can read, search, edit, and execute validation.
5. Parent Sonnet performs no repository read/edit/execute calls.

Pass: change is made, focused validation runs, no `HARNESS_FAILURE`, no Sonnet repository work.

## Test 2 — Unfamiliar repository path

Ask for a change whose affected location is not obvious.

Expected route:

`Luna Explorer → Luna Implementer → Luna Reviewer`

Check:

- Explorer is read-only and compact.
- Implementer receives relevant findings rather than repeating a repository-wide investigation.
- Implementer performs and reports validation.
- Luna Reviewer receives the requirement + implementation report and independently inspects code/tests.
- Luna Reviewer has no edit or execute capability.
- Sonnet only routes and synthesizes.

## Test 3 — Mechanical repetition

Request an already-designed repetitive change: DTOs/mappers/mocks, pattern replication, boilerplate, repeated unit-test patterns, or a mechanical rename.

Expected implementation worker: **MAI Mechanical**.

Check that MAI can read/edit/execute, follows the nearest pattern, and returns `REROUTE: decision required` rather than inventing a design when a real decision appears.

## Test 4 — Long bounded multi-file task

Choose one coherent task with clear acceptance criteria that spans several files and may need repeated test/fix cycles.

Expected implementation worker: **Kimi Deep Worker**.

Check:

- one Kimi worker owns the coherent implementation;
- it does not orchestrate additional agents;
- it can read/edit/execute and reports validation;
- Luna Reviewer follows for a non-trivial change.

## Test 5 — High-risk review escalation

Use a change involving auth/security, concurrency/ordering, transactions/state, persistence/data integrity, migrations, or public contracts.

Expected:

- implementation still goes to the appropriate worker;
- Luna Reviewer performs first-line read-only review;
- Sonnet Reviewer is used only for the high-risk/subtle second line or explicit Luna uncertainty;
- both reviewers remain read/search only.

## Test 6 — Human-gated Opus

After a meaningful change, click **Critical review with Opus** manually.

Expected:

- Opus was never automatically invoked;
- handoff preserves conversation context;
- Opus has read/search/web but no edit/execute;
- the developer chooses the next action after the review rather than being auto-routed to an implementation agent.

## Test 7 — Harness failure path

If a worker cannot be invoked, its model is unavailable, or its required tool is unexpectedly missing, the coordinator must not silently become the coder.

Expected:

`HARNESS_FAILURE: <reason>`

The response should name the failing worker and visible missing model/tool when known, then tell the developer that direct recovery is available through VS Code's built-in **Agent** with **GPT-5.6 Luna** selected.

If Sonnet edits the repository instead, fail this test.

## Test 8 — Native direct-Luna baseline

Run comparable small/medium work with VS Code's built-in **Agent** and select **GPT-5.6 Luna** in the model picker.

Compare with Over the Luna on:

- elapsed time;
- AI credits/tokens when visible;
- first-pass correctness;
- number of agent calls;
- human interventions;
- review findings.

Do not use the exact same already-completed change for both modes; prior context and edits bias the comparison.

---

## Release gates

- [ ] Plugin installs and loads without diagnostics errors.
- [ ] Over the Luna parent shows only routing/todo capabilities by design.
- [ ] Every substantive repository task invokes at least one subagent.
- [ ] Luna Implementer can read/search/edit/execute successfully.
- [ ] MAI Mechanical can read/search/edit/execute successfully.
- [ ] Kimi Deep Worker can read/search/edit/execute successfully.
- [ ] Reviewer agents expose neither edit nor execute.
- [ ] Sonnet performs zero repository tool calls in a healthy harness run.
- [ ] Opus is never automatically invoked.
- [ ] Harness failures are visible and do not silently fall back to Sonnet coding.
- [ ] No duplicate implementation workers attack the same coherent task without an explicit request.
- [ ] Expanded subagent model names match the intended route or any fallback is recorded.
- [ ] Direct baseline testing uses native Agent + Luna, not a plugin-provided direct-mode wrapper.

## Capture on failure

Record:

- VS Code version;
- GitHub Copilot extension version;
- plugin version;
- active parent agent/model;
- route line;
- delegated subagent name and displayed model;
- exact missing/disabled tool message;
- expanded subagent tool-call details;
- whether model fallback was visible;
- relevant Chat diagnostics/debug output.

Those details distinguish an Over the Luna routing/configuration bug from a VS Code model/tool-resolution problem.
