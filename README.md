# Over the Luna: VSCode harness distribution 🌙

**A thin, human-guided, Luna-first multi-model harness for GitHub Copilot in VS Code.**

> The moon got cheap enough to change the architecture.

Over the Luna routes work by *role* instead of sending every token to the biggest model. It is designed for developers who want to stay in VS Code, keep human decisions visible, and use a harness only when the extra orchestration earns its cost.

This is deliberately **not** an autonomous swarm.

- **Luna does most of the work.**
- **Sonnet coordinates and reviews.**
- **Kimi takes long, bounded jobs.**
- **MAI handles mechanical repetition.**
- **Opus is a human-gated escalation, not an automatic tax.**
- **Haiku is fallback only.**

No MCP server. No daemon. No hooks that execute code. No giant system prompt. Just a small Copilot agent plugin.

## Install

### VS Code — recommended

1. Use a current VS Code with GitHub Copilot enabled.
2. Open the Command Palette.
3. Run **`Chat: Install Plugin From Source`**.
4. Paste:

   `https://github.com/YB-Park/over-the-luna`

5. Open Copilot Chat and choose **Luna Solo** or **Over the Luna**.

Agent Plugins can be disabled by organization policy through `chat.plugins.enabled`.

### Copilot CLI

```bash
copilot plugin install YB-Park/over-the-luna
```

### If your organization blocks Agent Plugins

Custom agents can still be installed as plain files. Clone this repository and copy `agents/*.agent.md` to either:

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

It is intentionally **not a harness**. It does not delegate. It uses GPT-5.6 Luna directly with a concise inspect → edit → validate → stop workflow.

If the task is straightforward, stay here.

### 🚀 Over the Luna

Use this when decomposition actually helps:

- multi-file features
- unfamiliar repositories
- independent research that can run in parallel
- changes that benefit from independent review
- bounded long-horizon work

The coordinator uses **Claude Sonnet 5** and may delegate to cheap or specialized workers. The prompt policy caps initial fan-out and explicitly tells the coordinator not to spawn workers merely because it can.

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

| Agent | Default model | Visible | Purpose |
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

VS Code subagents cannot request a model above the parent model's cost tier. More importantly, this project intentionally keeps expensive and high-stakes escalation **visible to the human**.

The coordinator never silently calls Opus. At the end of a meaningful change, the **Critical review with Opus** handoff lets you explicitly decide when premium review is worth it.

## Recommended model settings

Custom-agent frontmatter can select a model, but VS Code currently does not expose a documented per-agent reasoning-effort field. Start with:

| Model | Start with | Notes |
|---|---|---|
| GPT-5.6 Luna | **Medium** | General harness default; use High for hard direct work |
| Claude Sonnet 5 | **Low / Medium** | Spend tokens on routing quality, not endless thinking |
| Claude Opus 4.8 | **High** | Only when deliberately handed off |
| Kimi K2.7 Code | Default | Give it clear acceptance criteria |
| MAI-Code-1-Flash | Default | Best after design decisions are already made |

Do not blindly maximize reasoning. The goal is the **minimum sufficient intelligence at each stage**.

## Human-in-the-loop rules

1. Do not delegate trivial work just to look agentic.
2. Initial parallel fan-out is limited to three workers.
3. Broad architecture, auth/security, payments, migrations, destructive changes, and major behavior changes require a visible plan before implementation.
4. Opus escalation is always user-visible.
5. Workers get narrow tools and narrow scope.
6. Review agents report findings; they do not silently rewrite implementations.
7. The coordinator returns important decisions to the human instead of hiding them inside a long autonomous loop.

## Model availability

The plugin assumes these models are available in your GitHub Copilot plan or enabled by your organization:

- GPT-5.6 Luna
- Claude Sonnet 5
- Claude Opus 4.8
- Kimi K2.7 Code
- MAI-Code-1-Flash
- Claude Haiku 4.5 (fallback only)

Agent files include conservative fallback lists where appropriate.

## Design philosophy

**1. Harness overhead must earn its keep.**  
A subagent call is not free just because Luna is cheap.

**2. Cheap intelligence belongs in the wide part of the funnel.**  
Discovery and routine implementation happen often. Put Luna there.

**3. Premium intelligence belongs at leverage points.**  
Use Sonnet and Opus for decisions and review where one good judgment prevents many bad downstream steps.

**4. The human is still the architect.**  
The harness should compress mechanical work and context management, not make product or architecture decisions invisible.

See [`docs/DESIGN.md`](docs/DESIGN.md) for routing rationale and limitations.

## Versioning

Over the Luna follows semantic versioning. The current plugin version is **v0.1.0**.

- Patch (`0.1.x`): prompt fixes, routing tweaks, compatibility fixes.
- Minor (`0.x.0`): new agents, routing behavior, or notable harness features.
- Major (`x.0.0`): breaking installation/configuration or behavioral changes.

See [`CHANGELOG.md`](CHANGELOG.md) for release notes.

## Updating

Source-installed plugins can be updated through the Agent Plugins UI. VS Code periodically checks plugin sources for updates.

Copilot CLI users can update with:

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

- VS Code custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code subagents: https://code.visualstudio.com/docs/agents/subagents
- VS Code Agent Plugins: https://code.visualstudio.com/docs/agent-customization/agent-plugins
- GitHub Copilot supported models: https://docs.github.com/en/copilot/reference/ai-models/supported-models
- GitHub Copilot plugin reference: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference

## License

MIT
