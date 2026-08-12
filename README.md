# Over the Luna 🌙

**English** · [한국어](README.ko.md)

> **Use more Luna. Pay for judgment only when it earns its place.**

GPT-5.6 Luna is unusually interesting: GitHub positions it as the lightweight, cost-efficient, lowest-cost member of the GPT-5.6 family, yet in day-to-day agentic coding it is capable enough to do far more than the price tag suggests. That changes the economics of an agent harness. Instead of spending a premium model on every routing decision, **Over the Luna spends cheap Luna compute on the places where extra independent thinking can actually help**—planning, repository analysis, skepticism, recovery, research, and review—while one Main Luna keeps ownership of the real implementation.

Over the Luna is a **VS Code-native, Luna-only coding harness for GitHub Copilot**. It is deliberately thin: no daemon, no second editor UI, no bundled MCP server, no hidden premium escalation, and no swarm of competing code writers. Simple work goes straight through one Luna. Harder work can temporarily fan out into small, isolated Luna contexts and then return compact evidence to the same Main Luna. If the task genuinely deserves a stronger second opinion, Luna can recommend **Sonnet** or **Opus**, but the premium model runs only after a visible human handoff.

The project is built around one idea: **Luna is cheap enough that test-time compute becomes a design material.** We can afford to ask several independent Luna contexts to look at different parts of a difficult problem—but we still have to spend those calls carefully, because extra agents also create latency, context handoffs, and coordination failure modes.

> Pricing changes. See GitHub's current [Copilot model pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) and the [GPT-5.6 Copilot announcement](https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot/).

---

## Install

### Requirements

- A current VS Code build with GitHub Copilot enabled.
- Agent Plugins enabled by your organization (`chat.plugins.enabled`).
- **GPT-5.6 Luna** available in your Copilot model policy.
- **Claude Sonnet 5** and **Claude Opus 4.8** are optional and are used only for manual premium review handoffs.

### Install from Git

1. Open the VS Code Command Palette.
2. Run **`Chat: Install Plugin From Source`**.
3. Paste:

   ```text
   https://github.com/YB-Park/over-the-luna
   ```

4. Reload VS Code if needed.
5. In Copilot Chat, choose **Over the Luna**.

VS Code Agent Plugins are currently a Preview feature. See the official [Agent plugins documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins).

---

## What happens when you use it

The automatic core is **Luna only**. The visible **Over the Luna** agent is both the main worker and the coordinator. It edits files, runs commands, validates the change, keeps the working context, and decides whether an isolated Luna perspective would improve the result.

```text
                              You
                               │
                               ▼
                        Over the Luna
                        GPT-5.6 Luna
                  main worker + coordinator
                               │
                    complexity / uncertainty
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
  Luna Planner           Luna Architect          Luna Skeptic
 requirements             repo evidence            challenge
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               │
                       compact Work Contract
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

### A simple task

A clear local edit should stay simple:

```text
Mode: SIMPLE — direct Luna
```

Main Luna inspects the nearby pattern, makes the change, runs focused validation, and reports. **No ceremonial planner. No reviewer just to prove that a reviewer exists.**

### A normal feature with uncertainty

If the implementation is clear but the repository structure or contract is not, Main Luna can isolate the uncertainty first:

```text
Mode: STANDARD — Luna Architect
```

The Architect reads the repository in a clean context and returns only the patterns, dependency paths, constraints, and risks that change the implementation. Main Luna keeps coding ownership.

### A deep or expensive-to-get-wrong task

When there are several genuinely independent uncertainties, Main Luna can spend more Luna compute in parallel:

```text
Mode: DEEP — Luna Planner ∥ Luna Architect ∥ Luna Skeptic
```

- Planner turns the request into acceptance criteria and decisions.
- Architect checks the actual repository structure and existing patterns.
- Skeptic tries to break the proposed direction and identify hidden assumptions.

Their outputs are compressed back into a short work contract. **They do not implement competing versions of the same change.** Main Luna makes the mutation once.

### When validation fails

Failure does not automatically mean "try harder with the same trajectory." Main Luna can call **Luna Recovery** with concrete evidence: failing tests, diagnostics, observed behavior, and the current implementation state. Recovery diagnoses one bounded next attempt, then Main Luna performs it.

### When a stronger model may be worth it

Luna is allowed to say that Luna is not enough.

For architecture-sensitive, security/auth, concurrency, transactionality, migration, data-integrity, public-contract, or unusually subtle uncertainty, Main Luna or Luna Reviewer can return:

```text
RECOMMEND_SONNET: <specific reason>
```

For genuinely critical uncertainty:

```text
RECOMMEND_OPUS: <specific reason>
```

That recommendation does **not** run the premium model. VS Code shows a human-visible handoff and the developer decides whether to use it.

---

## The architecture in one sentence

> **Parallelize thinking; serialize mutation.**

Main Luna is the single automatic repository mutation owner. Council agents are short-lived leaf contexts used to collect independent evidence, not autonomous coworkers editing the same branch.

This is the central design constraint of Over the Luna.

---

## Design philosophy and the evidence behind it

These studies and engineering reports do **not** benchmark GPT-5.6 Luna or prove that this exact harness is optimal. They are evidence that shaped our architecture. We combine them with direct VS Code runtime testing and keep the design deliberately easy to simplify when an extra role fails to earn its cost.

### 1. Cheap inference can change the algorithm

GitHub describes Luna as the lightweight, cost-efficient, lowest-cost GPT-5.6 variant. We treat that as more than a billing detail: low inference cost makes it practical to buy additional independent planning or verification passes instead of reserving multi-pass workflows for expensive models.

Research on [test-time compute scaling for LLM agents](https://arxiv.org/abs/2506.12928) reports that additional test-time compute can improve agent performance, while also showing that **when** to spend reflection and how to diversify rollouts matter. That maps directly to our SIMPLE / STANDARD / DEEP budget instead of "always fan out."

### 2. More agents are not automatically better

OpenAI's [practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) recommends maximizing a single agent before introducing multi-agent complexity. TeamBench likewise found that teams can hurt when a single agent already performs well, and that a verifier is not automatically trustworthy ([TeamBench](https://arxiv.org/abs/2605.07073)).

So **Main Luna works directly by default**. Extra Luna contexts exist only when they isolate a real uncertainty.

### 3. Coding is not the same as parallel research

Anthropic's production write-up on its [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) found large benefits for breadth-first research, but also reported much higher token use and explicitly noted that coding usually has fewer truly parallelizable tasks because agents share state and dependencies.

Our answer is not parallel coding. It is **parallel read-only thinking with one mutation owner**.

### 4. Context isolation is valuable when it removes irrelevant state

VS Code itself describes subagents as focused workers with isolated context that return a compact result to the main agent ([VS Code Subagents](https://code.visualstudio.com/docs/agents/subagents)). Microsoft's [SWE-Edit](https://www.microsoft.com/en-us/research/publication/swe-edit-rethinking-code-editing-for-efficient-swe-agent/) similarly reports gains from separating code inspection from edit execution, improving resolved rate while reducing inference cost in its evaluation.

That is why Planner, Architect, Researcher, Tool Worker, Recovery, and Reviewer get clean contexts—but Main Luna keeps the implementation thread.

### 5. Context should be compressed, not endlessly forwarded

Anthropic describes search as a compression problem: subagents can inspect a wide space, then return only the useful information to the lead agent. Microsoft's [CORPGEN](https://www.microsoft.com/en-us/research/blog/corpgen-advances-ai-agents-for-real-work/) also uses isolated subagents, hierarchical planning, and adaptive summarization to control context interference and growth.

Our rule is:

> **Think widely inside the leaf; speak narrowly back to Main Luna.**

A Council agent that returns an essay when five bullets would change the decision is doing the job badly.

### 6. Scale management compute by uncertainty, not by file count

Anthropic reports that explicit effort-scaling rules were necessary to stop its orchestrator from overinvesting in simple research queries. Test-time scaling research reaches a similar conclusion: extra compute can help, but budget allocation matters.

Over the Luna therefore uses:

| Mode | Default extra Luna calls | Use it when |
|---|---:|---|
| **SIMPLE** | 0 | The path is clear and local |
| **STANDARD** | 1–2 | One or two independent uncertainties matter |
| **DEEP** | up to 3 initial calls | Several independent uncertainties make a wrong direction expensive |

A ten-file mechanical edit can still be SIMPLE. A two-file concurrency change can be DEEP.

### 7. Recover from evidence, not from blind persistence

Microsoft's [PROBE](https://www.microsoft.com/en-us/research/publication/debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents/) separates runtime evidence, diagnosis, and bounded recovery guidance. Its results support a pattern we strongly prefer over unstructured retries: diagnose the observed failure first, then make a bounded next attempt.

Luna Recovery therefore cannot be called just because Main Luna feels uncertain. It needs concrete failure evidence, and recovery loops are bounded.

### 8. Review needs a rubric; a verifier badge is not enough

[TeamBench](https://arxiv.org/abs/2605.07073) found that verifiers could approve outputs that failed deterministic grading, while Microsoft's [AgentLens](https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/) shows that even passing coding trajectories can contain blind retries, regression cycles, missing verification, and poor process quality.

So our reviewer is not asked to "look at everything carefully." Main Luna supplies a specific rubric—correctness, regression, security, data integrity, concurrency, or another relevant lens. DEEP work may use two independent reviews only when the rubrics are different.

### 9. Known workflow rules should be explicit

Microsoft's [Conductor](https://opensource.microsoft.com/blog/2026/05/14/conductor-deterministic-orchestration-for-multi-agent-ai-workflows/) argues that known workflow structure does not always need another LLM to rediscover routing from scratch; dynamic orchestration can add cost, latency, and unpredictability.

Over the Luna stays inside native VS Code custom agents rather than adding a separate workflow engine, but we borrow the principle: **budgets, role boundaries, stop conditions, and premium gates are explicit and inspectable.**

### 10. Premium judgment is a human decision

We could put Sonnet at the top of every request, or let Luna silently escalate whenever it wants. We deliberately do neither.

VS Code supports user-visible agent handoffs and prevents a subagent from silently requesting a model above the main model's cost tier ([VS Code Subagents](https://code.visualstudio.com/docs/agents/subagents)). Over the Luna turns that constraint into a product principle: **Luna may recommend expensive judgment; the human decides whether to buy it.**

### 11. Preserve the developer's VS Code instead of replacing it

The plugin does not bundle Jira, Confluence, database, browser, cloud, or internal MCP servers. It uses the developer's existing VS Code tool environment and keeps trust, approval, credentials, sandboxing, and organization policy where they already belong.

That means installing Over the Luna should add orchestration—not create a second tool ecosystem.

See [`docs/MCP.md`](docs/MCP.md).

---

## What we deliberately did not build

**No always-on premium coordinator.** Earlier versions used Sonnet as the router/synthesizer. It worked, but with Luna cheap enough to run the control plane itself, a premium model on every turn became hard to justify. Sonnet is now an optional second opinion.

**No parallel implementation swarm.** Independent planning and review parallelize well; coupled code mutation does not. We keep one implementation owner to avoid conflicting edits, duplicated exploration, and inconsistent state.

**No deep manager hierarchy.** Planner does not call Architect; Architect does not call another manager. Council agents are leaf nodes. Information returns to Main Luna in a shallow star topology instead of passing through a game of telephone.

**No fixed "deep" ritual.** File count, task length, or impressive-sounding complexity do not automatically trigger a Council. Extra calls must correspond to distinct uncertainty.

**No infinite self-reflection.** Recovery is failure-triggered and bounded. Review is rubric-driven and bounded. When the harness cannot converge safely, it surfaces the blocker.

**No hidden model diversity.** Kimi, MAI, Haiku, Sonnet, and Opus do not participate in the automatic core. Model diversity must earn a measurable role rather than exist because the catalog contains more models.

---

## Agent set

| Agent | Model | Visible | Tool boundary | Purpose |
|---|---|---:|---|---|
| **Over the Luna** | GPT-5.6 Luna | ✅ | inherits active selection | main worker + coordinator |
| Luna Planner | GPT-5.6 Luna | ❌ | no tools | acceptance / work contract |
| Luna Architect | GPT-5.6 Luna | ❌ | read/search | repository structure / impact |
| Luna Skeptic | GPT-5.6 Luna | ❌ | read/search | challenge assumptions / counterexamples |
| Luna Researcher | GPT-5.6 Luna | ❌ | read/search/web | current public evidence |
| Luna Tool Worker | GPT-5.6 Luna | ❌ | inherits active selection | MCP / extension evidence |
| Luna Recovery | GPT-5.6 Luna | ❌ | read/search | failure diagnosis |
| Luna Reviewer | GPT-5.6 Luna | ❌ | read/search | independent rubric review |
| **Sonnet Reviewer** | Claude Sonnet 5 | ✅ | read/search | manual premium second opinion |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | read/search/web | manual highest-stakes review |

All automatic subagents are leaf nodes (`agents: []`). Sonnet and Opus are manual-only profiles and are never invoked by the automatic core.

---

## MCP and extension tools

Over the Luna does **not** own your MCP configuration.

Main Luna and Luna Tool Worker intentionally preserve the active VS Code selected-tool environment so user-configured MCP and extension tools can remain available without hardcoding server names. External content is treated as evidence, never as instructions that override the developer's request.

External side effects are never inferred. Reading a ticket does not authorize updating it. Implementing code does not authorize pushing, deploying, sending messages, creating a PR, modifying a database, or changing cloud resources unless the developer explicitly requested that side effect.

See [`docs/MCP.md`](docs/MCP.md) for the runtime contract and smoke test expectations.

---

## Thinking effort

Over the Luna does not pretend to pin a per-agent reasoning-effort value in `.agent.md`. Current VS Code custom-agent configuration controls model, tools, agents, instructions, and handoffs, while model reasoning/thinking configuration is managed separately.

The harness therefore controls the things it can actually make observable:

- number of subagent calls;
- fan-out width;
- scope and role of each call;
- compact return contracts;
- validation and recovery budgets;
- review rubrics;
- stop conditions.

This is also why a slow Luna subagent is not automatically a bug: an isolated agent may be reading a fresh repository context, using tools, validating evidence, and performing its own reasoning loop. The goal is not minimum latency at any cost; it is **useful extra work with bounded coordination overhead**.

---

## Validation and release discipline

Every push and pull request runs `scripts/validate_plugin.py`.

Static CI checks the architecture: Luna-only automatic core, exact role/tool boundaries, leaf Council agents, manual premium profiles, selected-tool inheritance, no bundled MCP configuration, and retired worker roles staying retired.

Static CI cannot prove that orchestration helps. Before a release, run [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) on real VS Code tasks and pay attention to:

- first-pass correctness;
- wall-clock time;
- input/output tokens or AI credits when visible;
- number of Council calls;
- whether Council output actually changed Main Luna's decision;
- recovery loops and blind retries;
- review findings that mattered;
- how often Sonnet/Opus recommendations were worth accepting.

A Council role that repeatedly adds latency but rarely changes a decision is a candidate for deletion.

---

## Project status

Current architecture: **v0.8.0 — Luna Council**.

This is a young harness built around a fast-moving VS Code/Copilot surface. Runtime behavior outranks our assumptions. If a VS Code update or real-world test contradicts the design, we change the design.

See:

- [`docs/DESIGN.md`](docs/DESIGN.md) — architecture and invariants
- [`docs/MCP.md`](docs/MCP.md) — MCP / ambient tool contract
- [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) — runtime release gates
- [`CHANGELOG.md`](CHANGELOG.md) — why the architecture changed over time
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rules

---

## Research and engineering references

- GitHub — [GPT-5.6 Sol, Terra, and Luna in GitHub Copilot](https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot/)
- GitHub — [Models and pricing for GitHub Copilot](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)
- VS Code — [Subagents in Visual Studio Code](https://code.visualstudio.com/docs/agents/subagents)
- VS Code — [Custom agents in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- Anthropic — [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- OpenAI — [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- Microsoft Research — [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](https://www.microsoft.com/en-us/research/publication/swe-edit-rethinking-code-editing-for-efficient-swe-agent/)
- Microsoft Research — [CORPGEN advances AI agents for real work](https://www.microsoft.com/en-us/research/blog/corpgen-advances-ai-agents-for-real-work/)
- Microsoft Research — [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](https://www.microsoft.com/en-us/research/publication/debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents/)
- Microsoft Research — [AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation](https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/)
- Microsoft Open Source — [Conductor: Deterministic orchestration for multi-agent AI workflows](https://opensource.microsoft.com/blog/2026/05/14/conductor-deterministic-orchestration-for-multi-agent-ai-workflows/)
- Zhu et al. — [Scaling Test-time Compute for LLM Agents](https://arxiv.org/abs/2506.12928)
- Kim et al. — [TeamBench: Evaluating Agent Coordination under Enforced Role Separation](https://arxiv.org/abs/2605.07073)

---

## License

MIT
