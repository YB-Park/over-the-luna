# Over the Luna 🌙

**A thin, human-guided, Luna-only context-isolation harness for GitHub Copilot in VS Code.**

> Spend cheap Luna compute on independent evidence, not bureaucracy.

Over the Luna v0.8 changes the architecture around GPT-5.6 Luna's unusually low token cost. **Main Luna now does the repository work directly.** Extra Luna subagents are used only when isolated planning, repository evidence, skepticism, recovery, research, external tools, or independent review are likely to improve the result.

**Premium models are never automatic.** Main Luna can recommend a visible **Review with Sonnet** or **Critical review with Opus** handoff, but the developer decides whether to click it.

## Install

### VS Code

1. Use a current VS Code build with GitHub Copilot enabled.
2. Open the Command Palette.
3. Run **`Chat: Install Plugin From Source`**.
4. Paste `https://github.com/YB-Park/over-the-luna`.
5. Reload VS Code and choose **Over the Luna** in Copilot Chat.

Agent Plugins are a VS Code preview feature and can be disabled by organization policy.

## The v0.8 idea

The automatic core is Luna-only:

```text
                              You
                               │
                               ▼
                        Over the Luna
                        GPT-5.6 Luna
                  main worker + coordinator
                               │
             complexity / uncertainty budget
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

Additional evidence lanes:

- **Luna Researcher** — current public documentation / standards.
- **Luna Tool Worker** — the developer's existing VS Code MCP and extension tools.

## Core rules

### Parallelize thinking; serialize mutation

Main Luna is the only automatic repository mutation owner. Council agents are leaf nodes with `agents: []` and are read-only except Luna Tool Worker, which can use user-configured external tools for a bounded task. External mutation still requires an explicit developer request.

This avoids competing implementation branches while still buying more independent Luna reasoning when the task deserves it.

### Complexity budget

The main agent chooses one of three modes:

| Mode | Default extra Luna calls | Intended use |
|---|---:|---|
| **SIMPLE** | 0 | Clear local change, obvious pattern, low risk |
| **STANDARD** | 1–2 | One or two real uncertainties worth isolating |
| **DEEP** | up to 3 initial calls | Multiple independent uncertainties or costly wrong direction |

Examples:

`Mode: SIMPLE — direct Luna`

`Mode: STANDARD — Luna Architect`

`Mode: DEEP — Luna Planner ∥ Luna Architect ∥ Luna Skeptic`

DEEP is **not** triggered merely by file count. The point is independent uncertainty, not ceremonial fan-out.

### Compact context hops

Council workers can inspect deeply inside their isolated context, but return compact output. The design target is:

> **Think widely inside the leaf; speak narrowly back to Main Luna.**

Planner, Architect, Skeptic, Researcher, Tool Worker, Recovery, and Reviewer all have explicit compact-output contracts.

### Recovery is evidence-triggered

Luna Recovery is called only after concrete failure evidence exists. It diagnoses the failure and suggests one bounded next attempt. Main Luna performs the fix.

Default recovery budget is two Recovery calls for the same bounded task. If those attempts still do not converge, the harness surfaces the blocker rather than hiding it behind an infinite agent loop.

### Review is rubric-driven

Tiny mechanically validated changes can finish without a separate reviewer.

Non-trivial changes get one Luna Reviewer. DEEP/high-risk work can use two independent Luna Reviewer calls in parallel, but with **different rubrics** such as:

- correctness / acceptance criteria;
- regression / security / data / concurrency risk.

Do not run two vague "review everything" copies.

## Human-visible premium escalation

The automatic agent allow-list contains **only Luna agents**.

Main Luna may return:

`RECOMMEND_SONNET: <specific reason>`

or, for unusually consequential uncertainty:

`RECOMMEND_OPUS: <specific reason>`

The agent picker exposes:

- **Over the Luna** — normal Luna-only harness entry.
- **Sonnet Reviewer** — manual premium second opinion.
- **Opus Critical Reviewer** — manual highest-stakes review.

Over the Luna also provides handoff buttons for Sonnet and Opus. Both use `send: false`, so premium execution requires a visible developer action.

## Existing MCP and extension tools

Over the Luna does **not** bundle MCP servers.

The main agent and Luna Tool Worker intentionally omit `tools` so current VS Code selected-tool inheritance preserves the developer's active MCP and extension tools. Server configuration, credentials, trust, approvals, sandboxing, Configure Tools selection, and organization policy remain owned by VS Code / the developer / the organization.

The plugin does not hardcode Jira, Confluence, GitHub, database, browser, cloud, or internal MCP names.

External side effects are never inferred. Reading a ticket does not authorize updating it; implementing code does not authorize pushing, deploying, messaging, remote writes, PR creation, or cloud mutation.

See [`docs/MCP.md`](docs/MCP.md).

## Agent set

| Agent | Model | Visible | Tool boundary | Purpose |
|---|---|---:|---|---|
| **Over the Luna** | GPT-5.6 Luna | ✅ | inherits active selection | main worker + coordinator |
| Luna Planner | GPT-5.6 Luna | ❌ | no tools | acceptance/work contract |
| Luna Architect | GPT-5.6 Luna | ❌ | read/search | repo structure / impact |
| Luna Skeptic | GPT-5.6 Luna | ❌ | read/search | assumption challenge |
| Luna Researcher | GPT-5.6 Luna | ❌ | read/search/web | current public evidence |
| Luna Tool Worker | GPT-5.6 Luna | ❌ | inherits active selection | MCP/extension evidence |
| Luna Recovery | GPT-5.6 Luna | ❌ | read/search | failure diagnosis |
| Luna Reviewer | GPT-5.6 Luna | ❌ | read/search | independent rubric review |
| **Sonnet Reviewer** | Claude Sonnet 5 | ✅ | read/search | manual premium judgment |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | read/search/web | manual critical judgment |

No Kimi, MAI, Haiku, or Sonnet model participates in the automatic core.

## Thinking effort

Over the Luna does not pretend to pin per-agent reasoning effort in `.agent.md`. Current VS Code exposes reasoning/thinking effort through model/session configuration rather than a custom-agent frontmatter field. v0.8 therefore controls cost and latency through **agent-call budget, scope, compact outputs, and stop conditions** instead of undocumented effort settings.

## Validation

Every push and pull request runs `scripts/validate_plugin.py`.

CI enforces:

- exact 10-agent architecture;
- automatic core models are **GPT-5.6 Luna only**;
- Kimi/MAI/old Implementer/Explorer roles stay retired;
- Main Luna's exact council allow-list;
- all council agents remain leaf nodes;
- strict read-only tool boundaries for management/review roles;
- selected-tool inheritance only where needed for Main Luna and Tool Worker;
- no bundled MCP configuration;
- compact-output contracts;
- visible Sonnet/Opus handoffs use `send: false`;
- reviewers remain non-mutating.

Static validation cannot prove orchestration quality. Run [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) before distribution.

## What to measure in the experiment

Compare v0.8 with v0.7 and native Agent + Luna on real tasks:

- wall-clock time;
- total input/output tokens or credits when visible;
- number of subagent calls;
- Main Luna token share;
- first-pass correctness;
- validation/recovery loops;
- review findings;
- human interventions;
- how often Sonnet/Opus handoffs are actually worth using.

The hypothesis is not "more agents are better." It is:

> **Cheap Luna compute can buy independent planning and verification, while direct Main-Luna execution avoids unnecessary implementation context hops.**

## Versioning

Current experiment: **v0.8.0 — Luna Council**.

See [`CHANGELOG.md`](CHANGELOG.md) and [`docs/DESIGN.md`](docs/DESIGN.md).

## License

MIT
