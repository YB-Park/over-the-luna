# Over the Luna 1.1 — Runtime Smoke Test

This checklist covers behavior static validation cannot prove: real VS Code subagent execution, ambient selected-tool inheritance, routing boundaries, mutation ownership, artifact-first review, and the human Premium Review spend boundary.

## Preflight

- Install/update the plugin and confirm **v1.1.0**.
- Reload VS Code and confirm GPT-5.6 Luna is available.
- Confirm **Over the Luna** and **Premium Review** are user-visible; Council leaves should remain hidden.
- Confirm customizations load without diagnostics errors.
- Keep normal/default tool approval settings.
- If testing integrations, use one harmless MCP/extension tool already permitted in the active VS Code environment.

## Test 1 — SIMPLE + NONE stays mechanical

Use an exact local scalar/default/text/metadata substitution with a direct existing assertion.

Expected:

- `Mode: SIMPLE ... | Assurance: NONE`;
- Architect 0;
- Reviewer 0;
- Main edits and validates;
- final report says review was intentionally skipped because the mechanical threshold was satisfied.

## Test 2 — SIMPLE + REVIEW stays local

Use a named local behavioral change with a clear implementation neighborhood.

Expected:

- `SIMPLE + REVIEW`;
- no investigative Architect by default;
- Main is the only mutation owner;
- focused validation runs;
- current unified diff is passed to exactly one named **Luna Reviewer**;
- accepted repair is revalidated by Main without automatic re-review.

## Test 3 — STANDARD + REVIEW isolates broad discovery

Use a task that requires discovering an unknown repository contract/dependency.

Expected:

1. bounded local orientation only;
2. route becomes STANDARD before broad Main scouting;
3. exactly the plugin **Luna Architect** handles the broad evidence pass;
4. Architect returns `DECISION / EVIDENCE / RELATIONSHIPS / MUTATION_TARGETS / UNRESOLVED`;
5. Main prints `Boundary sealed — work set: ...`;
6. Main does not replay broad repository inventory/search before mutation;
7. Main owns mutation;
8. exactly one normal Luna Reviewer sees the completed artifact.

## Test 4 — RISK gets post-change review

Use a real concurrency/idempotency, auth/security, transaction, migration, persistence/data-integrity, rollback, or important public-contract task.

Expected:

- `Assurance: RISK`;
- pre-change Architect/Skeptic only when a distinct risk question warrants it;
- at least one **named post-change Luna Reviewer** using the concrete current artifact;
- a second Reviewer only after Main names one distinct residual consequential risk and rubric;
- Main remains the sole mutation owner.

## Test 5 — ambient subagent capability and exact Council selection

Use a read-only task requiring unknown repository discovery.

Expected:

- `agent/runSubagent` is usable in the active runtime;
- selected leaf is exactly **Luna Architect**;
- unrelated installed custom agents are not selected;
- sufficient Architect handback causes no broad Main replay.

If `agent/runSubagent` is disabled by VS Code/user/org policy, treat that as an outer runtime condition rather than pretending a leaf ran.

## Test 6 — selected MCP/extension tools remain VS Code-owned

Use a harmless policy-permitted selected MCP/extension tool.

Expected:

- Main can use it without Over the Luna-specific configuration; or
- Luna Tool Worker can use it when Main delegates a bounded external-tool task;
- strict read-only leaves do not gain arbitrary mutation-capable integrations.

Fail only after confirming the sentinel tool is actually policy-permitted in the active VS Code environment.

## Test 7 — Premium Review is one human decision

From a completed change, choose **Premium Review**.

Expected:

- exactly one Premium Review handoff;
- agent switches to exact **Premium Review**;
- backing model is **Claude Sonnet 5** when available;
- prompt is prefilled but **not sent automatically** (`send: false`);
- response language follows the user's latest substantive request rather than switching to English merely because the agent instructions are English;
- Premium Review is read/search only and does not delegate.

## Test 8 — automatic model boundary

Across normal runs, all automatic Main/Council/Reviewer inference should use **GPT-5.6 Luna only**. Premium Review must never run automatically.

## Release gates

- [ ] Plugin v1.1.0 loads without customization errors.
- [ ] User-visible agents are Over the Luna + Premium Review; Council leaves remain hidden.
- [ ] SIMPLE + NONE avoids unnecessary review.
- [ ] SIMPLE + REVIEW uses one Luna Reviewer.
- [ ] STANDARD + REVIEW uses Luna Architect, seals the work set, avoids broad replay, then uses one Reviewer.
- [ ] RISK gets at least one post-change Luna Reviewer.
- [ ] Main remains the only automatic repository mutation owner.
- [ ] Existing selected MCP/extension tools remain usable through intended ambient roles.
- [ ] Strict leaves retain narrow tool boundaries.
- [ ] Premium Review targets Sonnet 5, stays `send: false`, and preserves the user's language.
- [ ] Automatic core model remains GPT-5.6 Luna only.
- [ ] No external side effect is inferred.

## Capture on failure

Record VS Code/Copilot/plugin versions, route line, agent identities, displayed models, tool calls, selected integration state, Architect packet/work set, Main actions after handback, Reviewer count/artifact, Premium handoff behavior, and any policy or model-availability message.
