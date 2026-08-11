# Changelog

All notable changes to **Over the Luna** will be documented here.

The project follows [Semantic Versioning](https://semver.org/).

## v0.2.0 — 2026-08-11

First routing-focused revision based on real VS Code testing.

### Changed

- **Over the Luna is now router-only.** The Sonnet coordinator no longer has repository read/search/execute/edit tools; substantive repository work must go through a worker.
- Small tasks now route directly to **Luna Implementer** instead of being solved by the Sonnet coordinator.
- Added **Luna Reviewer** as the default independent review path.
- **Sonnet Reviewer** is now reserved for second-line review of architecture, security/auth, concurrency, persistence/data integrity, migrations, contracts, or uncertain Luna reviews.
- Routing rules now explicitly prefer **MAI Mechanical** for deterministic repetition and **Kimi Deep Worker** for coherent long-horizon bounded implementation.
- The coordinator emits a one-line route summary so model routing is visible to the developer.

### Why

v0.1 behaved too much like "Sonnet with optional helpers" because delegation was advisory. v0.2 separates the two product modes:

- **Luna Solo** = direct single-model work.
- **Over the Luna** = actual multi-model harness; coordinator routes and synthesizes, workers inspect and change the repository.

Haiku remains a fallback rather than receiving an artificial primary role. Opus remains a human-gated critical-review handoff.

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
