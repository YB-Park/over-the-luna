# Changelog

All notable changes to **Over the Luna** will be documented here.

The project follows [Semantic Versioning](https://semver.org/).

## v0.2.1 — 2026-08-11

Hotfix for VS Code built-in tool availability discovered during live testing.

### Fixed

- Restored the normal VS Code `read`, `search`, `edit`, `shell`, `web`, and `vscode` tool sets on the **Over the Luna** coordinator. v0.2.0 restricted the coordinator to `agent`/`todo`, which also made built-in editing tools such as `replace_string_in_file` appear disabled in the active custom-agent session and could leave the workflow unable to recover when a worker path failed.
- Kept Luna-first delegation as a behavioral routing rule instead of enforcing it by crippling the active VS Code tool surface.
- Added an explicit, visible emergency fallback: if subagent invocation or worker tooling fails, Sonnet may use built-in tools only after reporting `Fallback: Sonnet direct execution — <reason>`.
- Replaced the non-standard `execute` alias with the current custom-agent `shell` alias across implementation and review agents.

### Why

Tool availability and model-routing policy are different concerns. The harness should prefer workers by instruction and routing, while preserving the editor's normal built-in capabilities so a tool-boundary mistake cannot dead-end a coding session.

## v0.2.0 — 2026-08-11

First routing-focused revision based on real VS Code testing.

### Changed

- **Over the Luna became router-only.** The Sonnet coordinator removed repository read/search/execute/edit tools; substantive repository work had to go through a worker.
- Small tasks routed directly to **Luna Implementer** instead of being solved by the Sonnet coordinator.
- Added **Luna Reviewer** as the default independent review path.
- **Sonnet Reviewer** became second-line review for architecture, security/auth, concurrency, persistence/data integrity, migrations, contracts, or uncertain Luna reviews.
- Routing rules explicitly preferred **MAI Mechanical** for deterministic repetition and **Kimi Deep Worker** for coherent long-horizon bounded implementation.
- The coordinator emitted a one-line route summary so model routing was visible to the developer.

### Why

v0.1 behaved too much like "Sonnet with optional helpers" because delegation was advisory. v0.2 separated the two product modes:

- **Luna Solo** = direct single-model work.
- **Over the Luna** = multi-model harness with worker-first routing.

The hard tool restriction introduced here was corrected in v0.2.1 after real VS Code testing showed that it degraded the active tool surface.

## v0.1.0 — 2026-08-11

Initial public test release.

### Added

- VS Code / GitHub Copilot Agent Plugin packaging.
- **Luna Solo** for direct, no-harness everyday work.
- **Over the Luna** Sonnet coordinator for selective orchestration.
- Luna-based Explorer, Researcher, and Implementer workers.
- Kimi K2.7 Deep Worker for long bounded tasks.
- MAI-Code-1-Flash Mechanical worker for deterministic repetition.
- Sonnet Reviewer for independent review.
- Human-gated Opus 4.8 Critical Reviewer handoff.
- Conservative fan-out and human-in-the-loop routing rules.
- Installation, design, and contribution documentation.

### Release philosophy

v0.x releases are expected to evolve quickly based on real VS Code usage and tester feedback. Prompt/routing fixes remain patch releases unless they materially change harness behavior.
