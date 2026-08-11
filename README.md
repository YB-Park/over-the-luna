# Over the Luna: VSCode harness distribution 🌙

**A thin, human-guided, Luna-first multi-model harness for GitHub Copilot in VS Code.**

> The moon got cheap enough to change the architecture.

Over the Luna packages a small set of VS Code custom agents that route work by *role* instead of sending every token to the biggest model.

It was designed for developers who like VS Code, want to keep human decisions in the loop, and used to think multi-agent harnesses were too automated and too token-hungry.

This is deliberately **not** an autonomous swarm.

- **Luna does most of the work.**
- **Sonnet coordinates and reviews.**
- **Kimi takes long, bounded jobs.**
- **MAI handles mechanical repetition.**
- **Opus is a human-gated escalation, not an automatic tax.**
- **Haiku is only a fallback.**

No MCP server. No daemon. No hook that runs code. No giant system prompt. Just a small Copilot agent plugin.

## Install

### VS Code — easiest

1. Use a current VS Code with GitHub Copilot enabled.
2. Open the Command Palette.
3. Run **`Chat: Install Plugin From Source`**.
4. Paste:

   `https://github.com/YB-Park/over-the-luna`

5. Open Copilot Chat and choose either **Luna Solo** or **Over the Luna**.

Agent Plugins are currently a VS Code preview feature and can be disabled by organization policy through `chat.plugins.enabled`.

### Copilot CLI

```bash
copilot plugin install YB-Park/over-the-luna
```

VS Code discovers plugins installed by Copilot CLI automatically.

### If your organization blocks Agent Plugins

Custom agents themselves can still be installed as files.

Clone this repository, then copy `agents/*.agent.md` to one of:

- User-wide: `~/.copilot/agents`
- Workspace-only: `.github/agents`

macOS/Linux:

```bash
mkdir -p ~/.copilot/agents
cp agents/*.agent.md ~/.copilot/agents/
```

PowerShell:

```powershell
$dest = Join-Path $HOME ".copilot\agents"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item ".\agents\*.agent.md" $dest
```

## Two entry points, on purpose

### 🌙 Luna Solo

Use this for normal day-to-day coding.

It is intentionally **not a harness**. It does not delegate. It uses GPT-5.6 Luna directly with a concise "inspect only what you need, edit, validate, stop" workflow.

If the task is straightforward, stay here.

### 🚀 Over the Luna

Use this when decomposition actually helps:

- multi-file features
- unfamiliar repositories
- independent research that can run in parallel
- a change that benefits from an independent review
- a bounded long-horizon task

The coordinator uses **Claude Sonnet 5** and may delegate to cheap/specialized workers. Initial fan-out is capped by prompt policy; it is not supposed to spawn a swarm just because it can.

## Routing map

```text
                         You
                          │
              ┌───────────┴───────────┐
              │                       │
         Luna Solo             Over the Luna
        GPT-5.6 Luna          Claude Sonnet 5
        no delegation            coordinator
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
        Luna Explorer          Luna Researcher          Luna Implementer
        repo discovery         docs / web research      default coding
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                  MAI Mechanical             Kimi Deep Worker
                  deterministic work          long bounded work
                         │                         │
                         └────────────┬────────────┘
                                      │
                               Sonnet Reviewer
                                      │
                       high-risk / want a second opinion
                                      │
                              HUMAN CLICKS HANDOFF
                                      ▼
                           Opus Critical Reviewer
```

## Agent set

| Agent | Default model | Visible to user | Purpose |
|---|---|---:|---|
| **Over the Luna** | Claude Sonnet 5 | ✅ | Thin coordinator; delegates only when useful |
| **Luna Solo** | GPT-5.6 Luna | ✅ | Direct everyday coding, no subagents |
| Luna Explorer | GPT-5.6 Luna | ❌ | Read-only codebase discovery |
| Luna Researcher | GPT-5.6 Luna | ❌ | Read-only external/documentation research |
| Luna Implementer | GPT-5.6 Luna | ❌ | Default bounded implementation worker |
| Kimi Deep Worker | Kimi K2.7 Code | ❌ | Long-horizon, multi-file bounded work |
| MAI Mechanical | MAI-Code-1-Flash | ❌ | Boilerplate, repetitive tests, deterministic edits |
| Sonnet Reviewer | Claude Sonnet 5 | ❌ | Independent non-editing review |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | Human-gated high-stakes review |

## Why Opus is a handoff

VS Code subagents cannot request a model above the parent model's cost tier. More importantly, this project intentionally keeps expensive/high-stakes escalation **visible to the human**.

The coordinator never silently calls Opus.

At the end of a meaningful change, the **Critical review with Opus** handoff lets you explicitly choose when the premium review is worth it.

This is a feature, not a workaround.

## Recommended model settings

VS Code currently lets supported models use configurable Thinking Effort, but custom-agent frontmatter does not expose a per-agent reasoning-effort field. The selected effort is remembered per model, so one Luna setting applies across Luna roles.

Recommended starting point:

| Model | Start with | Notes |
|---|---|---|
| GPT-5.6 Luna | **Medium** | Best general harness default; raise to High for hard direct work |
| Claude Sonnet 5 | **Low / Medium** | Coordinator should spend tokens on routing quality, not endless thinking |
| Claude Opus 4.8 | **High** | Only when you deliberately hand off |
| Kimi K2.7 Code | Default | Give it clear acceptance criteria |
| MAI-Code-1-Flash | Default | Use only after design decisions are already made |

Do not blindly maximize reasoning. The goal is the **minimum sufficient intelligence at each stage**.

## Human-in-the-loop rules

Over the Luna is intentionally conservative:

1. It does not delegate trivial work just to look agentic.
2. Initial parallel fan-out is limited to three workers.
3. Broad architecture, auth/security, payments, migrations, destructive changes, and major behavior changes require a visible plan before implementation.
4. Opus escalation is always a user-visible handoff.
5. Workers are given narrow tools and narrow scope.
6. Review agents report findings; they do not silently rewrite the implementation.
7. The coordinator should return decisions to the human instead of hiding them inside a long autonomous loop.

## Model availability

This plugin assumes the models are available in your GitHub Copilot plan or enabled by your organization:

- GPT-5.6 Luna
- Claude Sonnet 5
- Claude Opus 4.8
- Kimi K2.7 Code
- MAI-Code-1-Flash
- Claude Haiku 4.5 (fallback only)

The agent files include conservative fallback lists where appropriate. If your organization disables a model, Copilot can try the next available model in the configured list.

As of August 2026, GitHub lists GPT-5.6 Luna as requiring VS Code 1.128.0 or newer. Keep VS Code and the Copilot extension current.

## Design philosophy

The project is based on four ideas:

**1. Harness overhead must earn its keep.**  
A subagent call is not free just because Luna is cheap. Delegate only when context isolation, parallelism, or independent review is worth the extra loop.

**2. Cheap intelligence belongs in the wide part of the funnel.**  
Discovery and routine implementation happen often. Put Luna there.

**3. Premium intelligence belongs at leverage points.**  
Planning quality and critical review can prevent many downstream mistakes. Use Sonnet and Opus there, but sparingly.

**4. The human is still the architect.**  
The harness should compress mechanical work and context management, not make product or architecture decisions invisible.

See [`docs/DESIGN.md`](docs/DESIGN.md) for the routing rationale and current limitations.

## Updating

If installed from source in VS Code, use the Agent Plugins UI to check for updates. VS Code checks plugin sources for updates periodically.

If installed with Copilot CLI:

```bash
copilot plugin update over-the-luna
```

## Uninstall

From VS Code, open **Agent Plugins - Installed**, right-click **Over the Luna**, and choose **Uninstall**.

From Copilot CLI:

```bash
copilot plugin uninstall over-the-luna
```

## References

This project is intentionally built on public VS Code/GitHub Copilot primitives rather than a custom runtime:

- VS Code custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code subagents: https://code.visualstudio.com/docs/agents/subagents
- VS Code Agent Plugins: https://code.visualstudio.com/docs/agent-customization/agent-plugins
- GitHub Copilot supported models: https://docs.github.com/en/copilot/reference/ai-models/supported-models
- GitHub Copilot plugin reference: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference

## License

MIT
