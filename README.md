# Over the Luna: VSCode harness distribution 🌙

**A thin, human-guided, Luna-first multi-model harness for GitHub Copilot in VS Code.**

> The moon got cheap enough to change the architecture.

Over the Luna routes work by *role* instead of sending every token to the biggest model. It is for developers who want to stay in VS Code, keep important decisions visible, and use orchestration only when it earns its cost.

This is deliberately **not** an autonomous swarm.

- **Sonnet routes and synthesizes. It does not edit the repository in harness mode.**
- **Luna does most discovery, implementation, and first-line review.**
- **Kimi takes coherent long, bounded jobs.**
- **MAI handles mechanical repetition.**
- **Opus is a human-gated escalation, not an automatic tax.**
- **Haiku is fallback only.**

No MCP server. No daemon. No hooks that execute code. No custom extension runtime. Just a small Copilot Agent Plugin.

## Install

### VS Code — recommended

1. Use VS Code **1.128.0 or newer** with GitHub Copilot enabled.
2. Open the Command Palette.
3. Run **`Chat: Install Plugin From Source`**.
4. Paste:

   `https://github.com/YB-Park/over-the-luna`

5. Open Copilot Chat and choose **Luna Solo** or **Over the Luna**.

Agent Plugins are a VS Code preview feature and can be disabled by organization policy through `chat.plugins.enabled`.

### Copilot CLI

```bash
copilot plugin install YB-Park/over-the-luna
```

### If your organization blocks Agent Plugins

Clone the repository and copy `agents/*.agent.md` to either:

- User-wide: `~/.copilot/agents`
- Workspace-only: `.github/agents`

All distributed agents are explicitly scoped with `target: vscode`.

## Two entry points, on purpose

### 🌙 Luna Solo

Direct single-model coding with GPT-5.6 Luna.

Use it when you want the normal IDE-agent experience without orchestration overhead. Luna reads, edits, validates, and stops. It cannot delegate.

### 🚀 Over the Luna

A real harness boundary.

The Sonnet coordinator intentionally has only the **agent** and **todo** tool sets. It routes repository work to specialized workers and synthesizes their results.

For a healthy coding task, the parent Sonnet session should make **zero repository read/edit/execute tool calls**.

Even a small clear fix routes to **Luna Implementer**. If that extra agent boundary is not useful for the task, choose **Luna Solo** instead.

The coordinator prints a short route before delegation, for example:

`Route: Luna Explorer → Luna Implementer → Luna Reviewer`

### Parent edit tools being disabled is normal

When **Over the Luna** is active, direct edit/terminal tools on the parent coordinator are intentionally unavailable.

That does **not** mean an implementation worker lacks those tools. A custom subagent uses the model, tools, and instructions from its own agent definition.

The runtime failure to care about is:

> **Luna Implementer/Kimi/MAI is actually running as a subagent and its own edit/execute tools are unavailable.**

See [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) for the exact checks.

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
               ┌─────────────────────────────┼────────────────────────────┐
               │                             │                            │
          Luna Explorer                Luna Researcher              implementation
          repo discovery               docs / web                         │
                                             │                             │
                                  ┌──────────┴───────────┐                 │
                                  │                      │                 │
                           external facts only     repo facts only         │
                                                                         route
                                             ┌────────────────────────────┼──────────────────────┐
                                             │                            │                      │
                                      Luna Implementer               MAI Mechanical       Kimi Deep Worker
                                      default coding                 repetition           long bounded work
                                             │                            │                      │
                                             └────────────────────────────┼──────────────────────┘
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

| Agent | Primary model | Visible | Tools / purpose |
|---|---|---:|---|
| **Over the Luna** | Claude Sonnet 5 | ✅ | `agent`, `todo`; routing/synthesis only |
| **Luna Solo** | GPT-5.6 Luna | ✅ | Direct read/edit/execute, no delegation |
| Luna Explorer | GPT-5.6 Luna | ❌ | Read-only codebase discovery |
| Luna Researcher | GPT-5.6 Luna | ❌ | Read-only external/documentation research |
| Luna Implementer | GPT-5.6 Luna | ❌ | Default implementation + focused validation |
| Luna Reviewer | GPT-5.6 Luna | ❌ | Default independent review; no edit tool |
| **MAI Mechanical** | MAI-Code-1-Flash | ❌ | Boilerplate/repetition/deterministic edits |
| **Kimi Deep Worker** | Kimi K2.7 Code | ❌ | Long-horizon coherent multi-file bounded work |
| Sonnet Reviewer | Claude Sonnet 5 | ❌ | Second-line high-risk/subtle review; no edit tool |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | Human-gated highest-stakes review; no edit tool |
| Haiku 4.5 | fallback | ❌ | Availability fallback; no artificial primary role |

## Routing rules

**Default implementation → Luna.** Small fix or normal feature: Luna Implementer.

**Unknown repo shape → Luna Explorer.** Use it only when scope, dependency paths, or existing patterns are unclear.

**Current external knowledge → Luna Researcher.** Use it for current APIs/docs/versions, not for facts already in the repository.

**Mechanical repetition → MAI.** DTOs, schemas, mappers, mocks, boilerplate, repeated test patterns, obvious lint/type fixes, mechanical renames.

**Long coherent bounded job → Kimi.** Prefer one Kimi owner when a multi-file task benefits from a sustained implementation thread and repeated test/fix cycles.

**Default review → Luna.** Sonnet review is an escalation, not the normal path.

**High-risk review → Sonnet.** Architecture, auth/security, concurrency, persistence/data integrity, migrations, public contracts, or uncertainty reported by Luna Reviewer.

**Critical review → Opus handoff.** The coordinator never silently invokes Opus.

## Failure behavior

Over the Luna does not hide harness failure by letting Sonnet quietly become the coder.

If worker invocation or worker tooling fails, the coordinator should report:

`HARNESS_FAILURE: <reason>`

Then the developer can explicitly choose **Continue directly with Luna**. This keeps recovery convenient while preserving the distinction between a healthy harness run and direct single-model work.

## Model fallback caveat

Custom subagents can define their own prioritized model list. VS Code uses the configured model before falling back to the parent model.

A requested subagent model cannot exceed the parent model's cost tier. If it does, VS Code falls back to the parent model. Therefore, verify the model displayed on an expanded subagent when model identity matters.

Opus is intentionally a handoff rather than an automatic subagent so premium review remains explicit and its model identity is visible to the developer.

## Why not give every model a primary role?

Model diversity is useful only when a role earns it. Luna is the default for the wide/high-frequency portion of this harness, so **Haiku is deliberately not given a primary job just to make the diagram look more diverse**.

New model-specific roles should be added only after repeatable real-world evidence shows an advantage.

## Human-in-the-loop rules

1. **Luna Solo** means direct work, no harness.
2. **Over the Luna** means repository work is delegated; Sonnet is the router/synthesizer.
3. Initial parallel fan-out is capped at three workers.
4. Parallelize independent discovery/research, not overlapping implementations.
5. One coherent subsystem should normally have one implementation owner.
6. Broad architecture/product decisions remain visible to the developer.
7. Review agents report findings rather than silently rewriting code.
8. Opus escalation is always user-visible.
9. Harness failure is visible; direct Luna recovery is a manual handoff.

## Model availability

The intended routing set is:

- GPT-5.6 Luna
- Claude Sonnet 5
- Kimi K2.7 Code
- MAI-Code-1-Flash
- Claude Opus 4.8
- Claude Haiku 4.5 (fallback)

Your GitHub Copilot plan or organization must enable the relevant models.

## Recommended model settings

| Model | Start with | Notes |
|---|---|---|
| GPT-5.6 Luna | **Medium** | General worker/reviewer default; High for hard Luna Solo work |
| Claude Sonnet 5 | **Low / Medium** | Router and rare second-line reviewer |
| Kimi K2.7 Code | Default | Give it clear bounded acceptance criteria |
| MAI-Code-1-Flash | Default | Use after design decisions are already made |
| Claude Opus 4.8 | **High** | Human-gated critical review only |

Do not blindly maximize reasoning. The target is the minimum sufficient intelligence at each stage.

## Validation

Every push/PR runs `scripts/validate_plugin.py` in GitHub Actions. It checks, among other things:

- YAML frontmatter parses;
- every agent is `target: vscode`;
- only the intended model set is referenced;
- tool aliases are from the documented primary set;
- worker and handoff references exist;
- Over the Luna remains router-only;
- implementation workers retain read/search/edit/execute;
- reviewers do not receive the edit tool;
- workers cannot recursively delegate.

Static validation cannot prove VS Code runtime behavior. Before normal use or a meaningful release, run [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md).

## Troubleshooting

If a coding request under **Over the Luna** stops because the parent says edit or terminal tools are disabled, that is a **routing failure**: the coordinator should have delegated instead of trying to edit itself.

If an expanded **Luna Implementer**, **Kimi Deep Worker**, or **MAI Mechanical** subagent lacks its own edit/execute capabilities, capture:

- VS Code version;
- Copilot extension version;
- plugin version;
- parent and subagent model shown in chat;
- route line;
- exact disabled-tool error;
- expanded subagent tool-call details;
- Chat customization diagnostics/debug information.

Those details distinguish our routing/configuration bug from a VS Code subagent tool-resolution problem.

## Versioning

Over the Luna follows semantic versioning. This hardening revision is **v0.3.0**.

- Patch (`0.3.x`): prompt fixes, routing tuning, compatibility fixes.
- Minor (`0.x.0`): new agents, routing behavior, or notable harness features.
- Major (`x.0.0`): breaking installation/configuration or behavioral changes.

See [`CHANGELOG.md`](CHANGELOG.md) for release notes.

## Updating

Source-installed plugins can be updated through the Agent Plugins UI. VS Code periodically checks plugin sources for updates.

Copilot CLI users can update with:

```bash
copilot plugin update over-the-luna
```

After updating, reload VS Code before comparing runtime behavior across versions.

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
- GitHub custom-agent configuration: https://docs.github.com/en/copilot/reference/custom-agents-configuration
- GitHub Copilot supported models: https://docs.github.com/en/copilot/reference/ai-models/supported-models

## License

MIT
