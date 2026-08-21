# Over the Luna 🌙

**English** · [한국어](README.ko.md)

> **Use more Luna. Pay for judgment only when it earns its place.**

**Over the Luna is a VS Code-native GPT-5.6 Luna coding harness for GitHub Copilot.** It keeps one Main Luna responsible for implementation while using short-lived Luna leaf contexts for planning, repository discovery, skepticism, research, recovery, and review.

**v1.1 is the current stable contract.** It adds evidence-backed routing and assurance boundaries, an ambient-tools Main that preserves the developer's VS Code tool environment, a sealed Architect handback, artifact-first review, and one human-selected **Premium Review** backed by Claude Sonnet 5.

VS Code Agent Plugins are still a Preview feature, so platform behavior can evolve independently of this project.

## Install

### Requirements

- A current VS Code build with GitHub Copilot enabled.
- Agent Plugins enabled by your organization (`chat.plugins.enabled`).
- **GPT-5.6 Luna** available in your Copilot model policy.
- **Claude Sonnet 5** is optional and used only when you explicitly choose Premium Review.

### Install from Git

1. Open the VS Code Command Palette.
2. Run **`Chat: Install Plugin From Source`**.
3. Enter:

   ```text
   https://github.com/YB-Park/over-the-luna
   ```

4. Reload VS Code if needed.
5. In Copilot Chat, select **Over the Luna**.

## v1.1 in one picture

```text
                              You
                               │
                               ▼
                        Over the Luna
                        GPT-5.6 Luna
                  Main implementation owner
                               │
                 investigation + assurance
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
  Luna Planner           Luna Architect          Luna Skeptic
 requirements             repo evidence            challenge
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               │
                        compact evidence
                               │
                               ▼
                          Main Luna
                    edit / execute / validate
                               │
                  failure? ────┴──── review?
                      │                  │
                Luna Recovery      Luna Reviewer
                      │                  │
                      └──────────┬───────┘
                                 ▼
                         Main Luna reports
                                 │
                     premium judgment useful?
                                 │
                                 ▼
                         Premium Review
                       Claude Sonnet 5
                          HUMAN CLICK
```

Two additional evidence lanes are available when useful:

- **Luna Researcher** — current public documentation, specifications, and release notes.
- **Luna Tool Worker** — bounded use of the developer's already configured VS Code MCP and extension tools.

## Routing = investigation + assurance

v1.1 separates **how much discovery is needed** from **how much post-change assurance is needed**.

### Investigation

- **SIMPLE** — the implementation neighborhood is clear after bounded local orientation. Main works directly.
- **STANDARD** — an unknown repository contract, dependency, or broad semantic pattern must be discovered. Main delegates that disposable discovery to **Luna Architect** before broad self-scouting.
- **DEEP** — several independent uncertainties or consequential cross-cutting risks justify up to three distinct initial Luna advisory calls.

When Architect returns sufficient evidence, it also returns the complete `MUTATION_TARGETS` work set. Main prints `Boundary sealed — work set: ...` and does not replay broad repository discovery before mutation.

### Assurance

- **NONE** — only for genuinely mechanical, locally bounded changes with a direct validation assertion.
- **REVIEW** — normal semantic work gets exactly one named **Luna Reviewer** pass after focused validation.
- **RISK** — auth/security, concurrency/idempotency, transactions, migrations, persistence/data integrity, rollback, or important public contracts require at least one post-change named Luna Reviewer.

Reviewer receives the current unified diff plus acceptance criteria and validation evidence. Main remains the only mutation owner and adjudicates any finding.

## Agent map

| Agent | Model | Visible | Tool boundary | Purpose |
|---|---|---:|---|---|
| **Over the Luna** | GPT-5.6 Luna | ✅ | VS Code-owned selected tools | Main worker + coordinator |
| Luna Planner | GPT-5.6 Luna | ❌ | no tools | acceptance / constraints |
| Luna Architect | GPT-5.6 Luna | ❌ | read/search | repository evidence + sealed work set |
| Luna Skeptic | GPT-5.6 Luna | ❌ | read/search | challenge consequential assumptions |
| Luna Researcher | GPT-5.6 Luna | ❌ | read/search/web | current public evidence |
| Luna Tool Worker | GPT-5.6 Luna | ❌ | inherits selected tools | bounded MCP / extension evidence |
| Luna Recovery | GPT-5.6 Luna | ❌ | read/search | failure-anchored diagnosis |
| Luna Reviewer | GPT-5.6 Luna | ❌ | read/search | artifact-first independent review |
| **Premium Review** | Claude Sonnet 5 | ✅ | read/search | human-selected different-model judgment |

All automatic leaf agents are non-recursive (`agents: []`). Only **Over the Luna** and **Premium Review** are intended to appear in the normal user-selectable agent UI.

## VS Code-owned tools

Over the Luna does **not** install or own MCP servers. Main intentionally omits a fixed `tools` list so the developer's selected built-in, MCP, and extension tools remain VS Code-owned. Luna Tool Worker uses the same ambient path for a bounded external-tool question when isolation is useful.

Strict read-only leaves declare narrow tool lists and do not inherit arbitrary mutation-capable integrations.

Tool visibility is not authorization. External mutation—sending messages, changing tickets or databases, pushing, deploying, creating PRs, or modifying cloud resources—requires an explicit developer request for that effect.

See [`docs/MCP.md`](docs/MCP.md) for the runtime contract and troubleshooting guidance.

## Premium Review

Premium inference is one visible human decision, not a model menu.

- Backing model: **Claude Sonnet 5**.
- Handoff: exactly one **Premium Review** action.
- `send: false`: the prompt is prepared but the premium request is not sent until the developer chooses to send it.
- The premium agent is read/search only and cannot delegate.
- The handoff and Premium Review agent preserve the natural language of the user's latest substantive request; code, paths, commands, and verdict labels remain verbatim.
- If the requested premium model is unavailable, the product should surface that fact rather than silently claiming the requested premium judgment happened.

## Design principles

> **Parallelize thinking; serialize mutation.**

> **Main Luna owns the work, not all of the thinking.**

The goal is not minimum token count or maximum agent count. Cheap Luna inference is spent where an independent context can reduce wrong-direction work, keep broad disposable discovery out of Main, diagnose a concrete failure, or verify a completed artifact.

## Why this design

The references below do **not** benchmark GPT-5.6 Luna or prove that this exact harness is optimal. They are evidence for the design choices. Over the Luna also tests those choices against real VS Code/Copilot runtime behavior before promoting them into the stable contract.

### Cheap inference should buy selective test-time compute

[Scaling Test-time Compute for LLM Agents](https://arxiv.org/abs/2506.12928) finds that additional inference-time computation can improve agent performance, while also showing that the strategy and timing of that compute matter. Over the Luna therefore does not fan out by default: **SIMPLE / STANDARD / DEEP** controls investigation spend, while **NONE / REVIEW / RISK** independently controls assurance spend.

### More agents are not automatically better

OpenAI's [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) recommends maximizing a single agent before adding multi-agent complexity. [TeamBench](https://arxiv.org/abs/2605.07073) likewise shows that team value is conditional and that verifier roles can even hurt when the underlying task does not benefit from the extra coordination. That is why **Main Luna implements directly** and every leaf call must buy a specific kind of evidence, isolation, recovery, or assurance.

### Isolate disposable context, not mutation ownership

Anthropic's [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) shows where parallel isolated contexts help, while also noting that coding has fewer naturally independent subtasks and higher coordination costs than broad research. VS Code describes subagents as independent focused contexts that return results to the main agent ([VS Code Subagents](https://code.visualstudio.com/docs/agents/run/subagents)). Over the Luna follows that boundary: Council agents investigate and challenge; **one Main Luna remains the sole automatic repository mutation owner**.

### Compress discovery instead of replaying it

Microsoft's [SWE-Edit](https://www.microsoft.com/en-us/research/publication/swe-edit-rethinking-code-editing-for-efficient-swe-agent/) identifies context coupling and irrelevant context accumulation as practical problems in software-engineering agents. Over the Luna therefore lets Architect explore in a clean context, return a compact evidence packet and complete `MUTATION_TARGETS`, then seals that work set so Main can implement without rehydrating the same broad discovery into its mutable context.

### Failure and verification should be evidence-anchored

[PROBE](https://arxiv.org/abs/2605.08717) motivates failure-anchored diagnosis and bounded recovery rather than blind persistence. [AgentLens](https://arxiv.org/abs/2605.12925) shows why a passing outcome alone can hide poor software-agent trajectories. Over the Luna therefore triggers Recovery from concrete failure evidence and gives Reviewer the **actual current unified diff, acceptance criteria, and validation results** instead of asking for a vague second opinion.

### Human attention is also a budget

More internal work does not require more user-visible narration. OpenAI's [model guidance](https://developers.openai.com/api/docs/guides/latest-model) treats reasoning effort and output verbosity as separate controls and recommends explicit verbosity constraints for agentic workflows. v1.1.1 applies the same principle at the harness layer: routine successful mechanics stay quiet; failures, blockers, consequential findings, and human decisions stay visible; explicit requests for detail still expand normally.

## Scope and limitations

Over the Luna is an orchestration layer, not a security boundary. It relies on VS Code trust, approvals, sandboxing, organization policy, and the developer's configured tools. It does not bypass GitHub Copilot feature/model policy or acquire models outside the catalog available to the developer.

The automatic core is intentionally **GPT-5.6 Luna only**. If Luna is unavailable, the harness does not silently substitute another automatic model.

## Project docs

- [`docs/DESIGN.md`](docs/DESIGN.md) — v1.1 architecture and invariants.
- [`docs/MCP.md`](docs/MCP.md) — MCP/extension-tool contract.
- [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) — runtime release checks.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution and architecture rules.
- [`CHANGELOG.md`](CHANGELOG.md) — release history.

## License

MIT. See [`LICENSE`](LICENSE).

Over the Luna is a community project and is not an official GitHub, Microsoft, or OpenAI product.
