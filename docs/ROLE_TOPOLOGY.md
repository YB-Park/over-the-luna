# Role allocation for Over the Luna Next — RC2 research

**Status: hypothesis-driven architecture candidate, NOT stable v2.0.**
Separate from [v2.0.0-rc.1 one-Main baseline](https://github.com/YB-Park/over-the-luna/pull/19),
and from the protected [v1.1.1 stable product](https://github.com/YB-Park/over-the-luna/tree/main).

## What we correct from our earlier direction

v1.1.1 Council **was not arbitrary overhead**: its Architect isolates broad
discovery and returns a sealed evidence packet; Reviewer independently
audits an actual diff; Skeptic examines assumptions before mutation;
Researcher tracks moving public facts; Recovery diagnoses observed
failure; Tool Worker bridges native MCP; Planner formalizes acceptance.
It arose from product experiments and deserves *controlled refinement*,
not wholesale deletion. The later small SDK model benchmarks **did not
test this shipped multi-agent workflow**, so do not treat those scores as
evidence Council is ineffective.

We **retain distinct useful semantic roles**. We loosen rigid scan/file
counts and don't blindly inherit an immutable sealed work set: an
underestimated acceptance-critical caller/test must be inspectable.

## Other harnesses consulted (pattern borrowing, not result copying)

| System | Directly supported arrangement | Transferable idea | What we don't infer |
| --- | --- | --- | --- |
| [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | Independent context/model, per-agent tools and inherited constraints | Delegate disposable discovery and bounded review without flooding Main | Claude permissions do not automatically apply to VS Code Host |
| [Codex / ChatGPT Work subagents](https://developers.openai.com/codex/agent-configuration/subagents) | Specialized concurrent workers; increased token consumption | Parallel **independent evidence** only when divisible | Parallelizing every task is not a demonstrated cost saving |
| [OpenCode agents](https://dev.opencode.ai/v2/docs/agents/) | Build/Plan/Explore and configurable model/permissions | Differentiate execution vs planning/exploration and real permission enforcement | Different Host policy models must not be conflated |
| [Aider Architect/Editor](https://aider.chat/docs/usage/modes.html) | Architect reasons; Editor turns plan into edits | Strong reasoning can advise cheaper implementation; one edit owner | Two-model overhead is not always justified |
| [Oh My OpenCode](https://github.com/code-yeongyu/oh-my-opencode) | Orchestrator with distinct Explore/Librarian/Oracle specialists | Role-specific model selection and task-shaped evidence | Avoid all-on agents, uncontrolled background calls and fixed-model popularity rules |

**Principle:** an agent is worth keeping when its *separate context,
question, model or permissions* produce a clear marginal benefit,
not simply because it has a name. At rest, leaf agents cost no inference;
prompt/discovery complexity and actual delegation costs still matter.

## Deliberate RC2 role allocation

| Role | Candidate model | Trigger | Inputs / output | Why separate |
| --- | --- | --- | --- | --- |
| Main | Host selected, Luna-first by convention (Haiku/Main also supported) | Every task | User context, edits, actual tests, final synthesis | Only normal mutation owner |
| Next Architect | GPT-6 Luna | Unknown cross-file contract/blast radius | Scoped discovery → decision/evidence/relationships/work set | Isolate disposable repository search |
| Next Reviewer | GPT-6 Luna | Meaningful semantic patch; ordinarily risk work | Actual diff/tests → independent invariant check | Independent post-edit perspective |
| Next Skeptic | GPT-6 Luna | **Before** consequential design assumption | Named hypothesis → concrete counterexample | Earlier attack on hidden assumptions |
| Next Researcher | GPT-6 Luna initially | Changing external public API/spec | Official source/version/date links | Separate external evidence and context |
| Next Recovery | GPT-6 Luna | Real unexplained failure after policy/tool triage | Failure trace → bounded diagnosis | Avoid Main retry thrash and tool/model confusion |
| Next Sol Specialist | GPT-6.1 Sol | Explicitly valuable high-stakes judgment | One question → evidence-backed assessment | Different-model strong reasoning when justified |
| Next Sonnet Specialist | Claude Sonnet 5.5 | Alternative approved high-stakes judgment | **Same role** as Sol, distinct model | Different-model provider option, not another mandatory stage |

**Haiku 5.5:** user-selected Main is supported by omitted Main `model`.
A cheap-leaf Haiku variant is a testable cost hypothesis, **not an
automatically pinned replacement** without evidence. The prior
implementation task showed higher reported meter for Haiku than Luna;
this is not universal comparative pricing. Sol and Sonnet are
*alternatives*, never always invoked in sequence.

**Why not re-add Planner and Tool Worker yet?**
Planner's `tools: []` was found to map to `null` in one VS Code SDK
conversion path, making instruction-only zero-tool safety unreliable.
Main can frame acceptance directly; Planner should return only if
separate planning demonstrably adds value AND effective tools are
enforced. Tool Worker inherits all selected MCP/extension tools and
may possess unexpected write capabilities. Prefer direct user-approved
Host tools until safe role-specific control is demonstrated. Neither
role is declared unnecessary forever.

## Routing and bounded costs

- Ordinary local task: **Main → deterministic validation** (no leaf).
- Repository-wide unknown contract: **Main → Architect → Main**.
- Meaningful semantic change: **Main → focused tests/diff → Reviewer → Main**.
- Consequential unknown design: **Main → Skeptic (before) → Main → Reviewer (after)**.
- External evolving spec: **Main → Researcher → Main**.
- Actual unexplained failure: **Main → diagnostic Recovery → Main**.
- Specific high-stakes residual uncertainty or user request: **one of Sol / Sonnet** for ONE bounded independent opinion; *do not call both by default*.

**Budget:** default 0 leaves for trivial work, about 1 for meaningful
discovery or review, up to 2 cheap leaves for a combined risky
cross-file change. A premium independent opinion needs a named
decision it can change and an approved provider/data policy.
Do not impose an arbitrary numerical limit where missing correctness
would be dangerous; seek user approval for materially increasing
cost/scope. Count total credits plus any separate OpenAI USD,
elapsed time, rework and user approvals.

## Permissions and actual deployment caveats

- All leaves explicitly name nonempty read/search(/web) tool sets and
  `agents: []`; Main intentionally leaves `tools` and `model` out
  to honor Host model/tool selection.
- **Tool fields do not prove effective write denial in the user's
  installed Host.** The audit proved that `tools: []` can expand
  to all tools in one converter; other runtime paths remain distinct.
  Runtime effective denial and recursion must be confirmed before
  calling these trusted read-only *as a security boundary*.
- The user reports all four models are available in the Host. **No
  model availability catalogue checks are needed.** That says nothing
  about which provider each role uses or whether a provider silently
  substitutes a model. Record actual model usage when relevant.
- Cross-provider code transfer in a company environment must
  respect policy and user choice; **no automatic external API key
  use, secret bundling or silent sending sensitive files to BYOK**.
  If permitted backend/provider cannot be determined, do not
  claim independent Sol/Sonnet judgment.

## Minimal test-and-decision gate — no research treadmill

1. **Static shape:** all eight roles, name/model frontmatter and
   tool claims are validated; visible Main only; leaf agent files
   contain no edit or MCP access; no bundled credentials. Confirm
   Main has no pinned model/tool list, and no `tools: []` anywhere.
2. **One bounded GitHub Actions integration gate if needed:**
   actual plugin loaded, named Architect/Reviewer/strong Specialist
   registered and selected with exact identities. A single
   cross-model delegated workflow only if role/permission semantics
   require it and paid request is explicitly bounded. No toy grid.
3. **Product decision:** compare an authentic cross-module code task
   or meaningful invariant review to prior Main/native behavior;
   check *accepted quality, rework, attention, total usage*.
   If Council role produces no distinct evidence or demonstrable
   benefit, simplify THAT role. Do not erase v1's entire architecture
   because the model-only SDK test hit a performance ceiling.

**Stop condition:** RC2 should become one maintainable product
topology, not another broad model-evaluation program. RC1 stays
intact, and no merge or release tag is automatic.

## Observed role-registration gate (2026-10-16)

[GitHub Actions #38865165638](https://github.com/YB-Park/over-the-luna/actions/runs/38865165638) **PASS** with pinned SDK/CLI, actual plugin directory, without any model messages/inference.

- Registry loaded exactly the `over-the-luna-next` plugin.
- SDK returned exactly **8 registered role identities**: Main, Architect, Reviewer, Skeptic, Researcher, Recovery, Sol Specialist and Sonnet Specialist; zero unexpected entries.
- Selecting Main by its actual qualified ID and independently reading `getCurrent()` confirmed `over-the-luna-next:over-the-luna-next`.
- **This does not prove** the leaf-model assignments were used for inference, no silent provider fallback occurred, or effective read-only/non-recursive tool policy in the user's VS Code Host. Those require bounded runtime observations before product endorsement.
- This is a **metadata integration gate**, not another model competency benchmark; no corporate data transfer or paid model run occurred.

**Immediate next decision:** review whether a single real repository change involving unknown dependencies + a consequential invariant merits spending on one named leaf delegation. Do not commission a large model matrix just because eight roles were discovered.

## Empirical research triangulation: hypotheses, not transferred scores

1. **[Google Research — Towards a Science of Scaling Agent Systems (2026)](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/).** Study of **180 agent configurations** across several non-Over-the-Luna task families: parallelizable tasks benefited from centralized coordination while sequential planning tasks often degraded under multi-agent coordination. The observed error-propagation effect makes central Main verification and **conditional** parallel investigation a reasonable hypothesis. **Do not claim the paper measured our GitHub Copilot Host or Luna/Sol/Sonnet models.** Prediction: separate Architect/Researcher/Skeptic are most valuable for genuinely separable evidence needs; main code mutation remains serial.
2. **[Liu et al. — Lost in the Middle (TACL 2024)](https://aclanthology.org/2024.tacl-1.9/).** Important evidence can be used less reliably in the middle of large contexts. This supports testing compact evidence packets and avoiding unbounded Main re-reading, but **does not by itself prove that adding Architect saves credits or raises coding accuracy**. Prediction: bounded Architect summaries preserve decision-critical helper relationships, not a brittle fixed number of lines/files.
3. **[Xia et al. — Agentless (2024)](https://arxiv.org/abs/2407.01489).** A comparatively straightforward localization → patch → validation workflow performed competitively in the authors' SWE-bench Lite evaluation. This is a warning against the assumption that many named roles are necessary for every code edit. Prediction: direct Main remains best on known local problems; extra leaves require a distinct hypothesis and real acceptance evidence.

**Falsification questions:** Does Architect return a usable caller/helper/test packet that Main does NOT redundantly rediscover? Does Reviewer find meaningful defects that deterministic tests or Main alone miss? Does Skeptic catch a design-level assumption *before* any code is mutated? Does an advanced Sol/Sonnet opinion change an important decision enough to justify its provider, time and credit cost? **These are separate hypotheses**, not one synthetic score or an excuse to create a large new benchmark matrix.

## Host runtime vs standalone SDK: verified boundary (2026-10-16)

The previous role registry PASS listed the eight plugin agents, but P5 needed more. A targeted real `task` invocation for `Next Architect` reached a **standalone SDK server limitation**:

`Standalone server does not support session effect 'custom_agent_prompt'`.

[P5 causal evidence](ROLE_PIPELINE_P5.md). The task tool resolved the correct agent name and model, so repeating model benchmarks would not fix a missing host interaction. The **installed VS Code Agent Host is the intended target** and cannot be faithfully replaced by the standalone runner on this path. We preserve the original v1.1 Host-tested Council rationale rather than deleting the roles based on false-negative SDK evidence.

**Do not treat a named `task` call, registered agent, or model field as completed delegation.** Report named agent returned evidence separately. Leave stable and RC1 untouched. No company code transfer is required for future release decisions; any optional Host spot-check should minimize work and remain inside the organization.
