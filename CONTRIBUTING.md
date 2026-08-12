# Contributing

Contributions are welcome, especially evidence from real VS Code/Copilot usage.

## Principles

Preserve these constraints:

- human-guided, not swarm-by-default;
- **automatic core is GPT-5.6 Luna only**;
- premium Sonnet/Opus use requires visible human choice;
- Main Luna is the repository mutation owner;
- council agents are independent leaf contexts, not a management chain;
- extra agent calls must answer a real uncertainty, diagnose a real failure, or verify a concrete rubric;
- council outputs stay compact;
- preserve the developer's existing VS Code MCP/extension tool selection;
- do not bundle credentials, OAuth, MCP servers, or trust policy;
- external side effects are never inferred;
- current VS Code runtime behavior outranks cross-product assumptions.

## Council-role burden of proof

Do not add a new Luna role just because Luna tokens are cheap.

A new role should provide a repeatable benefit that Main Luna cannot get as efficiently in the same context, such as:

- independent requirement decomposition;
- repository evidence isolated from requirement assumptions;
- adversarial assumption checking;
- failure-anchored diagnosis;
- independent rubric verification;
- bounded external context isolation.

Remove or merge a role if it mostly restates predictable information.

## Complexity budget

Changes must preserve:

- SIMPLE → zero default subagents;
- STANDARD → one or at most two justified advisory calls;
- DEEP → at most three initial independent advisory calls;
- Recovery → concrete failure evidence first, default maximum two calls;
- review → one reviewer normally, at most two distinct-rubric reviewers for DEEP/high-risk work.

Do not increase these budgets without real runtime evidence.

## Tool boundaries

**Inherited-tool roles** intentionally omit `tools`:

- Over the Luna
- Luna Tool Worker

This preserves current VS Code selected-tool inheritance. Do not replace omission with `tools: ['*']`.

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

Do not add Kimi, MAI, Haiku, Sonnet, or Opus as an automatic core fallback/worker without a new evidence-backed architecture review.

## Premium handoffs

Sonnet and Opus must remain:

- user visible;
- `disable-model-invocation: true`;
- non-mutating;
- absent from Main Luna's `agents` allow-list.

Handoffs must use `send: false` so the developer explicitly chooses whether premium execution happens.

## Reporting experiments

When proposing an orchestration change, report:

1. task type and complexity mode;
2. council/review roles invoked;
3. whether those calls changed a decision or caught a real issue;
4. wall-clock effect;
5. token/credit effect when visible;
6. correctness / rework effect;
7. tool/MCP environment;
8. what evidence would cause the new role or budget to be removed again.

Prompt tokens and management traffic are part of the product cost.
