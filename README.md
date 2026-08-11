# Over the Luna: VSCode harness distribution 🌙

**A thin, human-guided, Luna-first multi-model harness for GitHub Copilot in VS Code.**

> The moon got cheap enough to change the architecture.

Over the Luna routes work by *role* instead of sending every token to the biggest model. It is designed for developers who want to stay in VS Code, keep human decisions visible, and use a harness only when the extra orchestration earns its cost.

This is deliberately **not** an autonomous swarm.

- **Sonnet routes first; direct repository work is an explicit fallback only.**
- **Luna does most discovery, implementation, and first-line review.**
- **Kimi takes coherent long, bounded jobs.**
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

## Two entry points, on purpose

### 🌙 Luna Solo

Use this for direct single-model work.

It intentionally does **not** delegate. Luna inspects, edits, validates, and stops.

### 🚀 Over the Luna

Use this when you explicitly want a harness.

Starting with **v0.2.1**, the Sonnet coordinator is **worker-first, not tool-disabled**. Normal repository work should be delegated to workers, but VS Code's built-in read/search/edit/shell/web tool surface stays enabled so the custom agent does not cripple the editor or dead-end when a worker path fails.

Even a small clear fix normally routes to **Luna Implementer**. If you do not want that extra agent boundary, use **Luna Solo** instead.

The coordinator prints a short route before delegation, for example:

`Route: Luna Explorer → Luna Implementer → Luna Reviewer`

If subagent invocation or worker tooling fails, the coordinator may recover with direct built-in tools, but it must make that visible:

`Fallback: Sonnet direct execution — <reason>`

That fallback is a harness failure signal, not the normal route.

## Routing map

```text
                              You
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
            Luna Solo                 Over the Luna
           GPT-5.6 Luna               Claude Sonnet 5
          direct/no harness             ROUTER FIRST
                                             │
               ┌─────────────────────────────┼────────────────────────────┐
               │                             │                            │
          Luna Explorer                Luna Researcher              implementation
          repo discovery               docs / web                         │
                                                                        route
                                             ┌───────────────────────────┼──────────────────────┐
                                             │                           │                      │
                                      Luna Implementer              MAI Mechanical       Kimi Deep Worker
                                      default coding                repetition           long bounded work
                                             │                           │                      │
                                             └───────────────────────────┼──────────────────────┘
                                                                         ▼
                                                                  Luna Reviewer
                                                                  default review
                                                                         │
                                                          high-risk / uncertainty only
                                                                         ▼
                                                                 Sonnet Reviewer
                                                                         │
                                                         user explicitly wants more
                                                                         ▼
                                                           Opus Critical Reviewer
                                                             HUMAN HANDOFF ONLY
```

## Agent set

| Agent | Primary model | Visible | Purpose |
|---|---|---:|---|
| **Over the Luna** | Claude Sonnet 5 | ✅ | Worker-first router/synthesizer; built-in tools retained for visible emergency fallback |
| **Luna Solo** | GPT-5.6 Luna | ✅ | Direct everyday coding, no subagents |
| Luna Explorer | GPT-5.6 Luna | ❌ | Read-only codebase discovery |
| Luna Researcher | GPT-5.6 Luna | ❌ | Read-only external/documentation research |
| Luna Implementer | GPT-5.6 Luna | ❌ | Default implementation worker |
| **Luna Reviewer** | GPT-5.6 Luna | ❌ | Default independent review |
| **MAI Mechanical** | MAI-Code-1-Flash | ❌ | Boilerplate, repetitive tests, deterministic edits |
| **Kimi Deep Worker** | Kimi K2.7 Code | ❌ | Long-horizon coherent multi-file bounded work |
| **Sonnet Reviewer** | Claude Sonnet 5 | ❌ | Second-line high-risk/subtle review |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | Human-gated highest-stakes review |
| Haiku 4.5 | fallback | ❌ | Availability fallback; no artificial primary role |

## Routing rules

**Default implementation → Luna.** Small task or normal feature: Luna Implementer.

**Unknown repo shape → Luna Explorer.** Use it before implementation only when scope/dependency paths are unclear.

**Current external knowledge → Luna Researcher.** Do not invoke it for facts already in the repository.

**Mechanical repetition → MAI.** DTOs, schemas, mappers, mocks, boilerplate, repeated test patterns, obvious lint/type fixes, mechanical renames.

**Long coherent bounded job → Kimi.** Prefer one Kimi owner when a multi-file task needs a sustained implementation thread and repeated test/fix cycles.

**Default review → Luna.** Sonnet review is an escalation, not the normal path.

**High-risk review → Sonnet.** Architecture, auth/security, concurrency, persistence/data integrity, migrations, public contracts, or uncertainty reported by Luna Reviewer.

**Critical review → Opus handoff.** The coordinator never silently invokes Opus.

## Tool-boundary rule

Model routing policy and VS Code tool availability are separate concerns.

The active **Over the Luna** custom agent keeps the standard built-in `read`, `search`, `edit`, `shell`, `web`, and `vscode` tool sets available. Workers still define narrower role-specific tool lists.

The coordinator is instructed not to use direct repository tools during a healthy harness run. This avoids the v0.2.0 failure mode where removing the tools at the custom-agent level caused built-in editing capabilities such as `replace_string_in_file` to appear disabled and made recovery impossible.

## Why not give every model a role?

Model diversity is useful only when a role earns it. Luna is currently the best default for the wide/high-frequency part of this harness, so **Haiku is deliberately not given a primary job just to make the model diagram look more diverse**. It remains a fallback.

The project can add new model-specific roles when real testing shows a repeatable advantage.

## Human-in-the-loop rules

1. Choosing **Luna Solo** means no harness.
2. Choosing **Over the Luna** means repository work is worker-first; Sonnet direct execution must be an explicit fallback with a reason.
3. Maximum initial parallel fan-out is three workers.
4. Parallelize independent discovery/research, not overlapping implementations.
5. Broad architecture/product decisions remain visible to the developer.
6. Review agents report findings rather than silently rewriting code.
7. Opus escalation is always user-visible.

## Model availability

The full intended routing set is:

- GPT-5.6 Luna
- Claude Sonnet 5
- Kimi K2.7 Code
- MAI-Code-1-Flash
- Claude Opus 4.8
- Claude Haiku 4.5 (fallback)

Your Copilot plan or organization must enable the relevant models. Custom subagents use the model configured in their own agent definition. VS Code does not run a subagent if the requested model exceeds the parent model's cost tier.

## Recommended model settings

| Model | Start with | Notes |
|---|---|---|
| GPT-5.6 Luna | **Medium** | General worker/reviewer default; High for hard direct Luna Solo work |
| Claude Sonnet 5 | **Low / Medium** | Router and rare second-line reviewer |
| Kimi K2.7 Code | Default | Clear bounded acceptance criteria |
| MAI-Code-1-Flash | Default | Deterministic work after decisions are made |
| Claude Opus 4.8 | **High** | Human-gated review only |

## Troubleshooting tool availability

If **Over the Luna** says an edit tool such as `replace_string_in_file` is disabled:

1. Confirm the installed plugin is **v0.2.1 or newer**.
2. Update/reinstall the source plugin and run **Developer: Reload Window**.
3. Open the chat tool picker and verify the standard edit tools are available for the active custom agent.
4. If a worker still reports that its own edit tools are unavailable, capture the subagent name/model and the expanded tool call. That indicates a VS Code subagent/custom-agent tool-resolution issue rather than the intended Over the Luna policy.

## Versioning

Over the Luna follows semantic versioning. The current plugin version is **v0.2.1**.

- Patch (`0.2.x`): prompt fixes, routing tuning, compatibility fixes.
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

## License

MIT
