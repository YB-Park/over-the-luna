# Contributing

Contributions are welcome, especially evidence from real VS Code/Copilot usage.

## Architecture invariants

Preserve these constraints unless a change is backed by clear runtime evidence:

- human-guided, not swarm-by-default;
- **automatic core is GPT-5.6 Luna only**;
- premium Sonnet/Opus use requires visible human choice;
- Main Luna is the single automatic repository mutation owner;
- council agents are independent leaf contexts, not a management chain;
- extra calls must answer a real uncertainty, isolate useful read-only context, diagnose a real failure, or verify a concrete rubric;
- council outputs stay compact;
- preserve the developer's existing VS Code MCP/extension tool selection;
- do not bundle credentials, OAuth, MCP servers, or trust policy;
- external side effects are never inferred;
- current VS Code runtime behavior outranks assumptions from other products or older platform behavior.

## Council-role burden of proof

Do not add a new Luna role merely because Luna inference is inexpensive.

A role should provide a repeatable benefit that Main Luna cannot get as efficiently in the same context, such as:

- independent requirement decomposition;
- broad repository evidence isolated from implementation state;
- adversarial assumption checking;
- failure-anchored diagnosis;
- independent rubric verification;
- bounded external-context isolation.

Remove or merge a role if it mostly restates predictable information.

## Routing budget

Changes must preserve:

- SIMPLE → zero default subagents;
- STANDARD → one or at most two justified advisory calls;
- DEEP → at most three initial independent advisory calls;
- Recovery → concrete failure evidence first, default maximum two calls;
- review → one reviewer for normal non-trivial work, at most two distinct-rubric reviewers for DEEP/high-risk work.

There is no target subagent-usage percentage. Optimize for useful context isolation and independent judgment, not agent count.

## Tool boundaries

**Inherited-tool roles** intentionally omit `tools`:

- Over the Luna
- Luna Tool Worker

This preserves the VS Code selected-tool inheritance path. Do not replace omission with a generic `tools: ['*']` assumption.

**Strict roles** keep explicit tool lists:

- Luna Planner → no tools
- Luna Architect → read/search
- Luna Skeptic → read/search
- Luna Researcher → read/search/web
- Luna Recovery → read/search
- Luna Reviewer → read/search
- Sonnet Reviewer → read/search
- Opus Critical Reviewer → read/search/web

All council/review agents remain `agents: []`.

## Model boundaries

Automatic core:

- GPT-5.6 Luna only.

Manual visible premium profiles:

- Claude Sonnet 5
- Claude Opus 4.8

Adding any non-Luna automatic model requires a new evidence-backed architecture review rather than a convenience fallback.

## Premium handoffs

Sonnet and Opus must remain:

- user visible;
- `disable-model-invocation: true`;
- non-mutating;
- absent from Main Luna's automatic `agents` allow-list.

Handoffs use `send: false` so the developer explicitly chooses whether premium execution happens.

## External side effects

Reading external context does not authorize mutation. Pushing, deploying, creating PRs, updating tickets, sending messages, changing databases, or modifying cloud resources requires an explicit request for that effect.

## Reporting orchestration changes

When proposing a routing or role change, report:

1. task type and mode;
2. council/review roles invoked;
3. whether those calls changed a decision, compressed useful context, or caught a real issue;
4. wall-clock effect;
5. token/credit effect when visible;
6. correctness/rework effect;
7. tool/MCP environment;
8. what evidence would cause the new role or budget to be removed again.

Prompt tokens, latency, and management traffic are part of the product cost.

## Before opening a PR

- Run `python scripts/validate_plugin.py`.
- Review `docs/SMOKE_TEST.md` when runtime behavior changes.
- Update `CHANGELOG.md` for user-visible changes.
- Bump `plugin.json` only when the change is intended for a new release.
- Keep README and design docs focused on the current supported architecture; historical experiments belong in the changelog or Git history.
