# Over the Luna 🌙

**English** · [한국어](README.ko.md)

> **Use more Luna. Pay for judgment only when it earns its place.**

GPT-5.6 Luna changes the economics of an agent harness. It is inexpensive enough that extra planning, repository analysis, skepticism, recovery, research, and review can be practical without putting a premium model on every turn. **Over the Luna uses that cheap test-time compute deliberately while keeping one Main Luna responsible for the actual implementation.**

Over the Luna is a **VS Code-native, Luna-only coding harness for GitHub Copilot**. It is intentionally thin: no daemon, no second editor UI, no bundled MCP server, no hidden premium escalation, and no swarm of agents competing to edit the same code. Simple work stays simple. Harder work can fan out into small isolated Luna contexts, then return compact evidence to the same Main Luna.

If Luna decides that a stronger second opinion would materially reduce risk, it can recommend **Claude Sonnet 5** or **Claude Opus 4.8**. Those models never run automatically; the developer chooses a visible handoff.

**Over the Luna 1.0 defines the stable harness contract.** VS Code Agent Plugins themselves are still a Preview feature, so platform behavior can continue to evolve.

> Model pricing changes. Check GitHub's current [Copilot model pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) before making cost assumptions.

---

## Install

### Requirements

- A current VS Code build with GitHub Copilot enabled.
- Agent Plugins enabled by your organization (`chat.plugins.enabled`).
- **GPT-5.6 Luna** available in your Copilot model policy.
- **Claude Sonnet 5** and **Claude Opus 4.8** are optional and used only for manual premium review handoffs.

### Install from Git

1. Open the VS Code Command Palette.
2. Run **`Chat: Install Plugin From Source`**.
3. Enter:

   ```text
   https://github.com/YB-Park/over-the-luna
   ```

4. Reload VS Code if needed.
5. In Copilot Chat, select **Over the Luna**.

VS Code installs agent plugins directly from Git repositories. See the official [Agent Plugins documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins).

---

## How it works

The automatic core is **GPT-5.6 Luna only**. The visible **Over the Luna** agent is both the main worker and the coordinator.

```text
                              You
                               │
                               ▼
                        Over the Luna
                        GPT-5.6 Luna
                  main worker + coordinator
                               │
                 locality / uncertainty / risk
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
                         │                 │
                         ▼                 ▼
                  Review with Sonnet   Critical with Opus
                     HUMAN CLICK          HUMAN CLICK
```

Two additional evidence lanes are available when needed:

- **Luna Researcher** — current public documentation, specifications, release notes, and version-sensitive facts.
- **Luna Tool Worker** — bounded use of the developer's already configured VS Code MCP and extension tools.

### SIMPLE — direct Luna

A clear local change with an obvious nearby pattern should stay direct:

```text
Mode: SIMPLE — direct Luna
```

Main Luna inspects the local context, edits, validates, and reports. No planner or reviewer is added merely because one exists.

### STANDARD — isolate useful read-only work

A task becomes STANDARD when one or two isolated perspectives can materially help. That includes uncertainty, but also **context pollution**: a mechanically simple edit can still justify Luna Architect if finding the correct pattern requires broad repository scouting.

```text
Mode: STANDARD — Luna Architect
```

Main Luna keeps the mutable implementation context. The Architect searches broadly in a clean context and returns only decision-changing file/symbol evidence.

### DEEP — spend more Luna compute where it matters

When several independent uncertainties or risk boundaries matter, Main Luna can use up to three initial advisory calls, preferably in parallel:

```text
Mode: DEEP — Luna Planner ∥ Luna Architect ∥ Luna Skeptic
```

Planner clarifies acceptance and constraints. Architect grounds the work in repository reality. Skeptic tries to falsify consequential assumptions. Their outputs are compressed before Main Luna implements anything.

### Recovery — diagnose from evidence

Luna Recovery is not speculative reflection. It is used only after concrete failure evidence exists, such as a focused test that still fails after a meaningful attempt or repository behavior that contradicts the current plan. Recovery returns one bounded diagnosis and next attempt; Main Luna performs the mutation.

### Review — independent, rubric-driven

Tiny mechanically validated changes may finish without a separate reviewer. **Non-trivial completed changes get one Luna Reviewer** with a specific rubric such as correctness, regression, security, concurrency, data integrity, or migration safety. DEEP/high-risk work may use two reviewers only when the rubrics are genuinely different.

### Premium judgment — visible human choice

For architecture-sensitive, security/auth, concurrency, transactionality, migration, data-integrity, public-contract, or unusually subtle uncertainty, Luna can return:

```text
RECOMMEND_SONNET: <specific reason>
```

For unusually consequential uncertainty:

```text
RECOMMEND_OPUS: <specific reason>
```

The recommendation does **not** run the premium model. VS Code shows a handoff and the developer decides whether to use it.

---

## The architecture in one sentence

> **Parallelize thinking; serialize mutation.**

And one companion rule:

> **Main Luna owns the work, not all of the thinking.**

Main Luna is the single automatic repository mutation owner. Council agents are short-lived leaf contexts that gather independent evidence, not autonomous coworkers editing the same branch.

---

## Why this design

The research below does not benchmark GPT-5.6 Luna or prove that this exact harness is optimal. It informs the design choices, which are also checked against real VS Code runtime behavior.

### Cheap inference can change the algorithm

Low inference cost makes extra independent passes practical. Research on [test-time compute scaling for LLM agents](https://arxiv.org/abs/2506.12928) shows that additional compute can improve agent performance, while also showing that **when** and **how** the compute is spent matters. Over the Luna therefore scales advisory work with SIMPLE / STANDARD / DEEP instead of always fanning out.

### More agents are not automatically better

OpenAI's [practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) recommends maximizing a single agent before introducing multi-agent complexity. TeamBench likewise reports cases where teams or verifiers hurt instead of help ([TeamBench](https://arxiv.org/abs/2605.07073)). That is why Main Luna implements directly and every extra call needs a concrete reason.

### Coding benefits from isolation more than competing writers

Anthropic's [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) shows the value of breadth-first parallel research while noting the higher coordination/token cost and the fact that coding has fewer naturally independent tasks. VS Code itself describes subagents as isolated focused contexts that return results to the main agent ([VS Code Subagents](https://code.visualstudio.com/docs/agents/subagents)). Over the Luna parallelizes read-only thinking, not competing code mutation.

### Compress context instead of forwarding everything

Microsoft's [SWE-Edit](https://www.microsoft.com/en-us/research/publication/swe-edit-rethinking-code-editing-for-efficient-swe-agent/) and [CORPGEN](https://www.microsoft.com/en-us/research/blog/corpgen-advances-ai-agents-for-real-work/) both support the value of role/context separation and controlled context transfer. Council agents can explore widely, but they return compact evidence to Main Luna.

### Failure should trigger diagnosis, not blind persistence

Microsoft's [PROBE](https://www.microsoft.com/en-us/research/publication/debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents/) motivates an evidence → diagnosis → bounded recovery pattern. Luna Recovery follows that shape and has a bounded retry budget.

### Verification needs a specific lens

A generic "review everything" pass is easy to over-trust. Microsoft's [AgentLens](https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/) highlights process failures that can hide behind passing outcomes. Over the Luna uses explicit reviewer rubrics and keeps premium judgment visible to the human.

---

## Agent map

| Agent | Model | Visible | Tool boundary | Purpose |
|---|---|---:|---|---|
| **Over the Luna** | GPT-5.6 Luna | ✅ | inherits active selection | main worker + coordinator |
| Luna Planner | GPT-5.6 Luna | ❌ | no tools | acceptance / work contract |
| Luna Architect | GPT-5.6 Luna | ❌ | read/search | repository structure / impact |
| Luna Skeptic | GPT-5.6 Luna | ❌ | read/search | challenge consequential assumptions |
| Luna Researcher | GPT-5.6 Luna | ❌ | read/search/web | current public evidence |
| Luna Tool Worker | GPT-5.6 Luna | ❌ | inherits active selection | bounded MCP / extension evidence |
| Luna Recovery | GPT-5.6 Luna | ❌ | read/search | failure diagnosis |
| Luna Reviewer | GPT-5.6 Luna | ❌ | read/search | independent rubric review |
| **Sonnet Reviewer** | Claude Sonnet 5 | ✅ | read/search | manual premium second opinion |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | read/search/web | manual highest-stakes review |

All automatic subagents are leaf nodes (`agents: []`). Sonnet and Opus are manual-only profiles and are never invoked by the automatic core.

---

## MCP and extension tools

Over the Luna does **not** install or own MCP servers. Main Luna and Luna Tool Worker preserve the developer's active VS Code selected-tool environment, while strict council/review roles use narrow explicit tool lists.

Tool visibility is not authorization. External reads may be inferred when clearly necessary for the requested outcome; **external mutation is never inferred**. Updating tickets, sending messages, pushing, deploying, changing databases, creating PRs, or modifying cloud resources requires an explicit developer request for that effect.

See [`docs/MCP.md`](docs/MCP.md) for the runtime contract and troubleshooting guidance.

---

## Thinking effort

Over the Luna does not encode undocumented per-agent reasoning-effort fields in `.agent.md`. Reasoning/thinking configuration is managed by VS Code/model controls. The harness instead controls observable work-shaping mechanisms:

- advisory fan-out;
- context-isolation triggers;
- compact output contracts;
- one mutation owner;
- evidence-triggered recovery;
- reviewer count and rubric;
- explicit stop conditions and human premium gates.

---

## Scope and limitations

Over the Luna is an orchestration layer, not a security boundary. It relies on VS Code trust, approval, sandboxing, organization policy, and the developer's configured tools. Agent Plugins are currently a Preview VS Code feature, so runtime behavior may change across VS Code/Copilot releases.

The automatic core intentionally optimizes around **GPT-5.6 Luna**. If Luna is unavailable in your organization, the harness does not silently substitute another automatic model.

---

## Project docs

- [`docs/DESIGN.md`](docs/DESIGN.md) — current architecture and invariants.
- [`docs/MCP.md`](docs/MCP.md) — MCP/extension-tool contract.
- [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) — runtime release checks.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution and architecture rules.
- [`CHANGELOG.md`](CHANGELOG.md) — release history.

## License

MIT. See [`LICENSE`](LICENSE).

Over the Luna is a community project and is not an official GitHub, Microsoft, or OpenAI product.
