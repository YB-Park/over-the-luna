# Over the Luna: VSCode harness distribution 🌙

**A thin, human-guided, Luna-first multi-model harness for GitHub Copilot in VS Code.**

> The moon got cheap enough to change the architecture.

Over the Luna routes work by role instead of sending every token to the biggest model. It is for developers who want to stay in VS Code, keep important decisions visible, and use orchestration only when it earns its cost.

This is deliberately **not** an autonomous swarm.

- **Sonnet routes and synthesizes.**
- **Luna does most discovery, implementation, and first-line review.**
- **Kimi owns coherent long, bounded jobs.**
- **MAI handles mechanical repetition.**
- **Opus is a human-gated escalation.**
- **Haiku is fallback only.**

No MCP server. No daemon. No execution hooks. No custom extension runtime. Just VS Code/GitHub Copilot Agent Plugin primitives.

## Install

### VS Code — recommended

1. Use VS Code **1.128.0 or newer** with GitHub Copilot enabled.
2. Open the Command Palette.
3. Run **`Chat: Install Plugin From Source`**.
4. Paste:

   `https://github.com/YB-Park/over-the-luna`

5. Open Copilot Chat and choose **Luna Solo** or **Over the Luna**.

Agent Plugins are a VS Code preview feature and can be disabled by organization policy through `chat.plugins.enabled`.

### Copilot CLI — installation transport

```bash
copilot plugin install YB-Park/over-the-luna
```

The distributed agents use `target: vscode`; the CLI command is useful for installing the plugin for VS Code, not as a promise that this harness is tested as a Copilot CLI workflow.

### If your organization blocks Agent Plugins

Clone the repository and copy `agents/*.agent.md` to either:

- User-wide: `~/.copilot/agents`
- Workspace-only: `.github/agents`

## Two entry points

### 🌙 Luna Solo

Direct single-model coding with GPT-5.6 Luna. It can read, search, edit, execute validation, and manage todos, but it cannot delegate.

Use this when a normal IDE-agent loop is enough.

### 🚀 Over the Luna

Actual harness mode.

The coordinator is fixed to **Claude Sonnet 5** and intentionally has only:

- `agent`
- `todo`

It cannot read/edit/execute against the repository. Every substantive repository task must cross a worker boundary.

Even a small clear fix normally routes to **Luna Implementer**. If that boundary is not worth it, use Luna Solo.

A healthy run starts with a visible route such as:

`Route: Luna Explorer → Luna Implementer → Luna Reviewer`

## Parent tools vs worker tools

This distinction is important.

When **Over the Luna** is active, direct edit/terminal tools being unavailable on the parent Sonnet coordinator is **expected**.

A delegated custom subagent uses its own configured model, tools, and instructions. Therefore:

- parent cannot edit and delegates → normal;
- parent says it cannot edit and stops instead of delegating → routing failure;
- Luna Implementer/Kimi/MAI actually starts but cannot edit/execute → subagent tool-resolution failure.

The earlier v0.2.1 design temporarily blurred these layers. v0.3 restores the strict coordinator boundary and makes runtime failures observable.

## Routing map

```text
                              You
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
            Luna Solo                 Over the Luna
           GPT-5.6 Luna               Claude Sonnet 5
          direct/no harness           router + synthesis
                                             │
                ┌────────────────────────────┼───────────────────────────┐
                │                            │                           │
          Luna Explorer               Luna Researcher             implementation
          repo discovery              current docs/web                  │
                                                                         ▼
                                     ┌───────────────────────────────────┼───────────────────┐
                                     │                                   │                   │
                              Luna Implementer                    MAI Mechanical      Kimi Deep Worker
                              default coding                      repetition          long bounded work
                                     │                                   │                   │
                                     └───────────────────────────────────┼───────────────────┘
                                                                         ▼
                                                                  Luna Reviewer
                                                                  default review
                                                                         │
                                                         high-risk / uncertainty only
                                                                         ▼
                                                                 Sonnet Reviewer
                                                                         │
                                                        human explicitly wants more
                                                                         ▼
                                                           Opus Critical Reviewer
                                                             MANUAL HANDOFF ONLY
```

## Agent set

| Agent | Primary model | Visible | Role |
|---|---|---:|---|
| **Over the Luna** | Claude Sonnet 5 | ✅ | Router/synthesizer only |
| **Luna Solo** | GPT-5.6 Luna | ✅ | Direct coding, no delegation |
| Luna Explorer | GPT-5.6 Luna | ❌ | Read-only repository discovery |
| Luna Researcher | GPT-5.6 Luna | ❌ | Read-only current docs/web research |
| Luna Implementer | GPT-5.6 Luna | ❌ | Default coding + validation |
| Luna Reviewer | GPT-5.6 Luna | ❌ | Default read-only review |
| **MAI Mechanical** | MAI-Code-1-Flash | ❌ | Deterministic repetitive edits |
| **Kimi Deep Worker** | Kimi K2.7 Code | ❌ | Coherent long multi-file implementation |
| Sonnet Reviewer | Claude Sonnet 5 | ❌ | Second-line high-risk review |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | Human-gated read-only critical review |
| Haiku 4.5 | fallback | ❌ | Availability fallback only |

The three user-facing entry/handoff agents are marked `disable-model-invocation: true`, so they are not meant to be silently selected as subagents. Hidden workers remain available to the coordinator.

## Routing rules

**Normal implementation → Luna Implementer.**

**Unknown repository shape → Luna Explorer** before implementation.

**Current external facts → Luna Researcher** only when version-sensitive docs/API information is actually needed.

**Mechanical repetition → MAI Mechanical.** DTOs, schemas, mappers, mocks, boilerplate, mechanical renames, obvious lint/type fixes, pattern replication.

**Long coherent bounded work → Kimi Deep Worker.** Prefer one owner over several overlapping implementers.

**Default review → Luna Reviewer.**

**High-risk review → Sonnet Reviewer.** Architecture, auth/security, concurrency, data integrity, migrations, public contracts, or explicit Luna uncertainty.

**Critical review → Opus handoff.** Never automatic.

## Failure behavior

A harness failure is not permission for Sonnet to quietly become the coder.

If worker invocation, model routing, or worker tooling fails, the coordinator should report:

`HARNESS_FAILURE: <reason>`

Then the developer can explicitly choose **Continue directly with Luna**. That manual handoff preserves convenience without hiding the fact that the harness path failed.

## Model behavior and availability

The full harness requires **Claude Sonnet 5** as the coordinator. Other roles have conservative fallback lists where appropriate.

VS Code chooses a custom subagent model from its explicit/configured preference before the parent model. A requested subagent model cannot exceed the parent's cost tier; if it does, VS Code falls back to the parent model. When model identity matters, inspect the model shown on the expanded subagent.

The intended model set is:

- GPT-5.6 Luna
- Claude Sonnet 5
- Kimi K2.7 Code
- MAI-Code-1-Flash
- Claude Opus 4.8
- Claude Haiku 4.5

Your Copilot plan and organization policy must enable the models you use. In particular, enterprise administrators can restrict individual models.

## Recommended thinking effort

| Model | Start with | Notes |
|---|---|---|
| GPT-5.6 Luna | **Medium** | General worker/reviewer default; High for hard Luna Solo work |
| Claude Sonnet 5 | **Low / Medium** | Routing and rare second-line review |
| Kimi K2.7 Code | Default | Give clear bounded acceptance criteria |
| MAI-Code-1-Flash | Default | Best after design decisions are fixed |
| Claude Opus 4.8 | **High** | Human-gated critical review only |

Do not maximize reasoning blindly. The target is the minimum sufficient intelligence at each stage.

## Human-in-the-loop rules

1. Luna Solo means direct work, no harness.
2. Over the Luna means repository work is delegated.
3. Initial parallel fan-out is capped at three workers.
4. Parallelize independent discovery/research, not overlapping implementations.
5. One coherent subsystem normally has one implementation owner.
6. Material architecture/product decisions return to the developer.
7. Reviewers are structurally non-editing: no `edit` or `execute` tool.
8. Opus escalation is always user-visible.
9. Harness failure is visible; recovery to Luna is a manual choice.

## Validation

Every push and pull request runs `scripts/validate_plugin.py` in GitHub Actions. It checks:

- YAML frontmatter;
- `target: vscode` on every agent;
- allowed model names;
- documented primary tool aliases;
- valid subagent/handoff references;
- manual-only entry agents;
- Sonnet-only router configuration;
- router-only coordinator tools;
- implementation-worker read/search/edit/execute access;
- reviewers having neither edit nor execute;
- no recursive worker delegation.

Static validation cannot prove VS Code runtime behavior. Before normal use or a meaningful release, run [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md).

## Troubleshooting

If a coding request under Over the Luna stops because the **parent** edit tool is disabled, capture the route and response: the coordinator should have delegated.

If an expanded implementation **worker** lacks edit/execute, capture:

- VS Code version;
- Copilot extension version;
- plugin version;
- parent agent/model;
- route line;
- subagent name and displayed model;
- exact missing/disabled tool message;
- expanded subagent tool calls;
- Chat customization diagnostics/debug output.

See [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md).

## Versioning

Over the Luna follows semantic versioning. This hardening revision is **v0.3.0**.

- Patch (`0.3.x`): prompt/routing/compatibility fixes.
- Minor (`0.x.0`): new agents or meaningful harness behavior changes.
- Major (`x.0.0`): breaking installation/configuration or behavioral changes.

See [`CHANGELOG.md`](CHANGELOG.md).

## Updating

Source-installed plugins can be updated through the Agent Plugins UI. After updating, reload VS Code before comparing behavior across versions.

Copilot CLI users can run:

```bash
copilot plugin update over-the-luna
```

## Uninstall

From VS Code, open **Agent Plugins - Installed**, right-click **Over the Luna**, and choose **Uninstall**.

```bash
copilot plugin uninstall over-the-luna
```

## References

- VS Code custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code subagents: https://code.visualstudio.com/docs/agents/subagents
- VS Code Agent Plugins: https://code.visualstudio.com/docs/agent-customization/agent-plugins
- GitHub custom-agent configuration: https://docs.github.com/en/copilot/reference/custom-agents-configuration
- GitHub Copilot supported models: https://docs.github.com/en/copilot/reference/ai-models/supported-models

## License

MIT
