# Changelog

All notable changes to **Over the Luna** are documented here.

The project follows [Semantic Versioning](https://semver.org/).

## v1.0.0 — 2026-08-12

First stable release of the Luna-only VS Code/GitHub Copilot harness.

### Stable runtime contract

- GPT-5.6 Luna is the only automatic model.
- Main Luna owns repository mutation, commands, validation, synthesis, and the live implementation trajectory.
- Council roles are shallow leaf contexts used for planning, repository evidence, skepticism, research, recovery, and review.
- Routing uses bounded SIMPLE / STANDARD / DEEP budgets.
- Broad disposable repository scouting can be isolated through Luna Architect even when the eventual edit is simple.
- Recovery is failure-evidence-triggered and bounded.
- Normal non-trivial work receives an independent rubric-driven Luna Reviewer pass.
- Claude Sonnet 5 and Claude Opus 4.8 remain manual-only, user-visible premium review handoffs.
- Main Luna and Luna Tool Worker preserve the developer's active VS Code selected-tool environment; strict roles retain narrow explicit tool boundaries.
- External side effects are never inferred.

### Release hardening

- Rewrote README and Korean README around the current v1.0 behavior instead of the pre-release evolution story.
- Reworked `docs/DESIGN.md`, `docs/MCP.md`, and `docs/SMOKE_TEST.md` into current-state operational documentation.
- Removed development-only comparisons and version-specific implementation-history prose from user-facing docs.
- Condensed pre-1.0 history in this changelog while preserving the full Git history.
- Updated contribution guidance to keep future user-facing docs free of stale architecture narratives.
- Bumped the plugin and static validator contract to v1.0.0.

## Pre-1.0 development milestones

The pre-1.0 series was an iterative design period. Full details remain available in Git history; the milestones that materially shaped the stable architecture are summarized here.

### v0.8.1 — Council balance refinement

Clarified that Main Luna is the implementation owner, not the only reasoning context. Broad read-only repository exploration became an explicit context-isolation trigger for Luna Architect, and non-trivial independent review was strengthened.

### v0.8.0 — Luna Council

Moved the automatic control plane to GPT-5.6 Luna, introduced Planner / Architect / Skeptic / Recovery roles, made Main Luna the direct implementation owner, and moved Sonnet/Opus to visible human-selected premium review handoffs.

### v0.7.0 — Luna-first simplification

Reduced specialist routing after Luna's cost/capability profile made several dedicated worker roles difficult to justify. This established the rule that a routing branch must earn its complexity with measurable benefit.

### v0.6.0 — VS Code tool-inheritance correction

Aligned ambient MCP/extension-tool behavior with actual VS Code selected-tool inheritance: Main/ambient roles omit `tools`, while strict roles use explicit tool lists. This remains the basis of the v1.0 tool contract.

### v0.1.0–v0.5.0 — Prototyping

Explored premium coordinators, model-specialist workers, reviewer boundaries, and ambient-tool compatibility. These releases were development iterations rather than stable distribution contracts.
