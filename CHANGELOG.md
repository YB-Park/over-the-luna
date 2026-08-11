# Changelog

All notable changes to **Over the Luna** are documented here.

The project follows [Semantic Versioning](https://semver.org/).

## v0.4.0 — 2026-08-11

Close-beta simplification: the plugin now owns only behavior that is unique to the harness.

### Changed

- Removed the user-facing **Luna Solo** custom agent. Direct single-model Luna coding is already available through VS Code's built-in **Agent** plus the model picker.
- Removed plugin-specific direct-Luna recovery handoffs from **Over the Luna** and **Opus Critical Reviewer**.
- Harness failures now stay visible and point the developer to native **Agent + GPT-5.6 Luna** for manual direct recovery.
- Updated README, design notes, and smoke tests so native Agent + Luna is the no-harness baseline.
- Updated static validation to prevent accidental reintroduction of the redundant direct-mode wrapper.

### Why

`Luna Solo` did have small configuration differences from the built-in Agent: narrower tools, `agents: []`, and a concise behavior prompt. Those differences did not justify another visible product surface. Over the Luna should add orchestration, not duplicate VS Code's native direct-agent workflow.

## v0.3.0 — 2026-08-11

Pre-production hardening after a full review against the current VS Code and GitHub Copilot custom-agent/subagent specifications.

### Changed

- Restored **Over the Luna** to a strict router/synthesizer boundary with only `agent` and `todo` tools.
- Fixed the full harness coordinator to **Claude Sonnet 5** so worker model routing is not silently distorted by a cheaper parent-model fallback.
- Added `disable-model-invocation: true` to user-facing entry/handoff agents so they are selected deliberately rather than nested automatically.
- Added a human-visible **Continue directly with Luna** handoff instead of allowing silent Sonnet direct-execution fallback.
- Routed Opus's **Fix accepted findings with Luna** handoff to the visible **Luna Solo** entry point rather than a hidden worker.
- Made all review agents structurally non-mutating by removing both `edit` and `execute`; implementation workers own validation execution and report results for review.
- Added `target: vscode` to every distributed agent so the compatibility promise matches the product this project actually tests.
- Normalized tool declarations to GitHub's documented primary aliases (`execute`, `read`, `edit`, `search`, `agent`, `web`, `todo`). Compatible aliases remain valid, but primary aliases are easier to audit.
- Clarified the distinction between a parent coordinator's intentionally disabled repository tools and a worker subagent's own tool configuration.
- Corrected model cost-tier documentation: when a requested subagent model is above the parent model's cost tier, VS Code falls back to the parent model.
- Tightened routing instructions so the first repository-facing action in harness mode is a worker delegation.
- Added explicit `HARNESS_FAILURE` reporting instead of hiding delegation/runtime problems behind Sonnet implementation.
- Updated validation workflow actions to current Node 24-based major versions.

### Added

- `scripts/validate_plugin.py` static validation for plugin/agent architecture, including handoff visibility and manual-only entry-agent checks.
- GitHub Actions validation on pushes and pull requests.
- `docs/SMOKE_TEST.md` with runtime release gates for model routing, worker tool availability, review escalation, manual Opus use, and failure recovery.

### Review finding that changed the design

The v0.2 live-test symptom — parent edit tools appearing disabled — was initially interpreted as evidence that restricting coordinator tools also disabled worker tools. A deeper review of the current VS Code subagent specification showed that this conflated two different tool surfaces.

A coordinator with only the `agent` tool is a supported orchestration pattern, while a custom subagent uses its own configured model/tools/instructions. Therefore v0.3 treats parent edit/terminal unavailability as **expected** and tests the implementation worker's own edit/execute capabilities separately.

## v0.2.1 — 2026-08-11

Interim hotfix made during live investigation.

### Changed

- Temporarily restored broad repository tools to the Sonnet coordinator and allowed visible direct-execution fallback after observing disabled parent editor tools.
- Switched several tool declarations to compatible aliases while investigating tool resolution.

### Superseded by v0.3.0

The broader coordinator capability solved the immediate dead-end but reintroduced the original risk: Sonnet could become the implementation agent instead of the router. The later specification review showed that the parent and custom-subagent tool surfaces should be evaluated separately. v0.3.0 restores the strict harness boundary and adds a manual Luna recovery path.

## v0.2.0 — 2026-08-11

First routing-focused revision based on real VS Code testing.

### Changed

- Made **Over the Luna** router-only so substantive repository work went through workers.
- Routed small tasks to **Luna Implementer** instead of Sonnet.
- Added **Luna Reviewer** as the default independent review path.
- Reserved **Sonnet Reviewer** for architecture/security/concurrency/data-integrity/contracts or uncertain Luna reviews.
- Explicitly preferred **MAI Mechanical** for deterministic repetition and **Kimi Deep Worker** for coherent long-horizon work.
- Added a one-line route summary for model-routing visibility.

### Why

v0.1 behaved too much like "Sonnet with optional helpers" because delegation was advisory.

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

v0.x releases are expected to evolve quickly based on real VS Code usage and tester feedback.
