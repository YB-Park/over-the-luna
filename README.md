# Over the Luna Next — RC2 role-topology research 🌙

[한국어](README.ko.md)

**NOT A STABLE RELEASE.** This is a research branch for designing
efficient collaborator placement, **not an indiscriminate return to a
large Council**. The [stable v1.1.1](https://github.com/YB-Park/over-the-luna/tree/main)
and [one-Main RC1](https://github.com/YB-Park/over-the-luna/pull/19)
remain separate and intact.

The user was correct: the original v1.1 Council resulted from extensive
experiments. We restore **its functional breakthroughs**, not just its
agent count. Read [role allocation and other harness research](docs/ROLE_TOPOLOGY.md).

## Actual role set

One visible **Over the Luna Next** Main, plus seven hidden, **conditional** roles:
**Architect** (repository evidence), **Reviewer** (real patch),
**Skeptic** (pre-change contradiction), **Researcher** (public changing docs),
**Recovery** (actual failing attempts), and **Sol/Sonnet Specialists** as
two interchangeable high-end, selected-model independent opinions.

Architect/Reviewer/Skeptic/Researcher/Recovery initially use GPT-6 Luna;
Sol and Sonnet are pinned to their respective Host model names. **Claude
Haiku 5.5 is not excluded**: choose it as Main in the model picker;
automatic Haiku routing is deliberately not asserted as economical.
No compulsory Sol/Sonnet calls, no automated BYOK integration, no custom
MCP credentials. No more than one strong specialist for the same
question by default.

The files are **role capabilities at rest**, not eight models called
on every task. For local work Main runs alone; complex work selects
only the roles relevant to its uncertainty. Main retains repository
mutation, tests, decisions and final response.

## Standalone trial (no company data export)

After no-credit CI passes, obtain the **branch-specific allowlisted ZIP**
from GitHub Actions or clone this branch separately. Extract and register
its absolute path in VS Code **User** `chat.pluginLocations`,
with `chat.plugins.enabled` as organizationally approved. Disable the
earlier `over-the-luna-next` RC1 or research *duplicate plugin identity*
while trialing, but **never remove stable v1.1.1**. Select
`Over the Luna Next` in Copilot Agent Host, model selected by user.

**This is a candidate, not proven real Host behavior.** The company
environment's role permissions, leaf model routing and external provider
policies have not been demonstrated for this topology. Frontmatter
`tools: ['read','search']` is a request, not proof of enforced
read-only execution. `agents: []` is similarly a declaration.
**Do not delegate secrets or sensitive code to an alternative provider
without company and user authorization.**

Rollback: disable this local plugin path, switch to stable v1.1.1 or RC1
or native Copilot. Do not change enterprise permissions merely to make
the agent work. No user internal worktree diff/chat logs need uploading.

**Research stop rule:** one static role/packaging gate, then only a
decision-relevant SDK integration check if needed. Do not add endless
fixture families or run every model by habit. `main` is untouched.

## Delegation acceptance — current blocker

The RC2 plugin roles are registered, but the standalone Copilot SDK task runner **cannot** prove subagent handback: it returned `Standalone server does not support session effect 'custom_agent_prompt'`. This is an unsupported standalone session interaction, not a model benchmark result. **Never infer Main → Architect → Reviewer success from registration alone.**

[Host-only role acceptance and privacy-preserving trial](docs/HOST_DELEGATION_GATE.md) defines exactly one OPTIONAL, public-repo native Copilot Host check and a yes/no outcome. The owner should not export internal work files, logs or chat transcripts. No paid Actions role-repeat is planned. Stable main and RC1 are unchanged.
