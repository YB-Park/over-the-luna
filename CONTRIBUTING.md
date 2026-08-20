# Contributing

Contributions are welcome, especially evidence from real VS Code/Copilot usage.

## Architecture invariants

Preserve these constraints unless a change is backed by clear runtime evidence:

- **automatic core is GPT-5.6 Luna only**;
- Main Luna is the single automatic repository mutation owner;
- routing separates SIMPLE / STANDARD / DEEP investigation from NONE / REVIEW / RISK assurance;
- broad unknown semantic discovery goes to Luna Architect before Main accumulates repository-wide scouting context;
- a sufficient Architect packet seals the complete `MUTATION_TARGETS` work set and Main does not replay broad discovery before mutation;
- normal semantic REVIEW uses exactly one named artifact-first Luna Reviewer trajectory;
- RISK gets at least one named post-change Luna Reviewer;
- Council/review agents are independent leaf contexts, not a management chain;
- extra calls must answer a real uncertainty, isolate useful context, diagnose concrete failure evidence, or verify a completed artifact;
- preserve the developer's existing VS Code selected built-in/MCP/extension tools;
- treat organization/enterprise Copilot feature and model policy as a hard runtime boundary, never something to bypass;
- do not bundle credentials, OAuth, MCP servers, or trust policy;
- external side effects are never inferred;
- premium inference is one visible human-selected **Premium Review**, not an automatic path or model menu.

## Tool boundaries

**Inherited-tool roles** intentionally omit `tools`:

- Over the Luna
- Luna Tool Worker

**Strict roles** keep explicit tool lists:

- Luna Planner → no tools
- Luna Architect → read/search
- Luna Skeptic → read/search
- Luna Researcher → read/search/web
- Luna Recovery → read/search
- Luna Reviewer → read/search
- Premium Review → read/search

All leaves remain `agents: []`.

Main intentionally omits `agents` as well. The exact permitted Council names are sealed in the instruction contract. Do not add arbitrary installed custom agents merely because their descriptions look relevant.

## Model boundaries

Automatic core:

- GPT-5.6 Luna only.

Manual visible premium profile:

- Premium Review → Claude Sonnet 5.

Adding any non-Luna automatic model or additional premium menu requires new evidence-backed architecture review rather than a convenience fallback.

## Premium handoff

Premium Review must remain:

- user visible;
- `disable-model-invocation: true`;
- read/search only;
- non-recursive (`agents: []`);
- absent from the automatic Council path;
- targeted by exactly one visible handoff with `send: false`;
- language-continuous with the user's latest substantive request.

If the backing model is unavailable, surface that fact rather than silently claiming the requested premium judgment occurred.

## External side effects

Reading external context does not authorize mutation. Pushing, deploying, creating PRs, updating tickets, sending messages, changing databases, or modifying cloud resources requires an explicit request for that effect.

## Reporting orchestration changes

When proposing a routing or role change, report the task type, Mode + Assurance, leaf roles invoked, whether those calls changed a decision or isolated useful context, wall-clock/token effect when visible, correctness/rework effect, tool/MCP environment, and the evidence that would cause the added complexity to be removed again.

## Before opening a PR

- Run `python scripts/validate_plugin.py`.
- Review `docs/SMOKE_TEST.md` when runtime behavior changes.
- Update `CHANGELOG.md` for user-visible changes.
- Bump `plugin.json` only when the change is intended for a new release.
- Keep README and design docs focused on the current supported architecture; historical experiments belong in the changelog or Git history.
