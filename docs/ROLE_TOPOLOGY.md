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

## Routing policy P9 — separate evidence and assurance decisions (2026-10-19)

This is a **model-facing judgment policy**, not a rigid keyword classifier, a new
agent, or a claim that a larger Council is inherently better. A model can
infer intent from loose user requests; forcing an exhaustive checklist on
every turn wastes context. Instead make two quiet decisions:

1. **Investigation:** Can Main resolve the missing fact with bounded local
   reads or existing tests? If yes, **DIRECT**. If the unknown is broad
   repository structure, choose one **Architect**; an untestable consequential
   pre-edit assumption, **Skeptic**; current external vendor facts,
   **Researcher**; evidenced unresolved implementation failure after
   basic tool/policy triage, **Recovery**. No duplicate lens for the same fact.
2. **Assurance:** When the patch is mechanical and an exact assertion closes
   the contract, no review. When a semantic or high-risk edit needs independent
   assurance, send real current diff + test evidence to **Reviewer** or one
   authorized **Sol/Sonnet** specialist for the *same post-edit question*.
   A strong review can **replace**, not automatically follow, a Luna review.
   Its prompt must have real hunks, acceptance, changed paths and test results.
   For distinct pre- and post-edit risks, Skeptic and a reviewer can both help.

| Authentic task shape | Investigation | Post-edit assurance | Reason |
| --- | --- | --- | --- |
| Named one-line default plus exact assertion | Main direct | None | No missing decision |
| Unknown caller/serializer contract across modules | Architect once | Reviewer only if final edit warrants | Broad search is disposable |
| Reproducible validation failure with known cause | Main direct repair | According to actual diff risk | Recovery would repeat facts |
| Consequential migration assumption without deterministic oracle | Skeptic before edit | Independent real-diff review after | Two different questions/times |
| Vendor API changed upstream since pinned integration | Researcher once | Only if edit warrants | Dated public fact isolated |
| Security-sensitive patch with materially hard post-edit invariant | No leaf unless missing contract | Reviewer OR authorized Sol/Sonnet with real diff | Premium replaces duplicate judgment |
| Host policy blocks named subagent | Do not bypass; report limitation | No fabricated review | Authorization outweighs orchestration |

### Boundary and measurement

- **No extra agent solely for task length, token count, or an abstract risk
  score.** A delegated question must be self-contained, decision-changing,
  and economical after child setup + returned-packet + Main reread costs.
  If one narrow local check settles the question, do that instead.
- **Evidence handback is required:** named completion, returned findings,
  changed paths/source pointers; for cross-model claims verify executed
  provider/model. Prompt declarations and registry discovery are insufficient.
- **Premium escalation is substitution where equivalent**, not a ritual
  third stage. Do not claim a pre-edit consult has independently reviewed
  an unseen patch. Respect company provider/tool/data policy.
- **Provider/model defaults stay pinned per leaf**; Copilot Host guidance
  says do not override delegation `model`, `reasoning_effort`, or
  `context_tier` unless explicitly requested.
- **Value per task** = accepted requirement/invariant coverage, severity of
  discovered defects, avoided rework/duplicated reads, elapsed time,
  Copilot usage counters and tokens, plus developer interruptions. Report
  SDK/Copilot usage independently from any OpenAI API USD; do not infer
  monetary savings from prompt character counts.

### External patterns actually checked (not imported benchmarks)

- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents):
  independent self-contained work and concise descriptions; direct Main
  for short/iterative tasks. Subagents still spend tokens and child handbacks
  consume context. We borrow its **route-by-description** lesson, not its
  runtime tool/permission semantics.
- [Codex subagents](https://developers.openai.com/codex/agent-configuration/subagents):
  independent parallel workstreams, and explicitly higher token usage.
  We retain one mutation owner; no parallel fan-out by default.
- [OpenCode agents](https://dev.opencode.ai/v2/docs/agents/):
  primary vs subordinate modes and explicit subagent permissions.
  Host-native Copilot security must be checked separately.
- [Aider architect/editor](https://aider.chat/docs/usage/modes.html):
  optional reasoning/editing separation costs two requests. We do not
  force an Architect pass before every Luna code edit.
- [Oh My OpenAgent / Oh My OpenCode](https://github.com/code-yeongyu/oh-my-openagent):
  model selection by role/task and provider options; helpful as a routing
  idea, not evidence that automatic fallback or a large always-on DAG is
  appropriate for the enterprise Copilot Host.
- [VS Code subagents by harness](https://code.visualstudio.com/docs/agents/run/subagents):
  short edits generally stay direct, and the Copilot native delegation
  differs from the Local `agent/runSubagent` path.

### Experiment stop/go (no fabricated success)

**Offline structural gate first:** check product prompt's independent
investigation/assurance contract, premium post-edit artifact precondition,
provider protection, allowed role set and existing release/security invariants
in the public repository CI. This validates **packaged instructions only**,
not LLM routing performance or actual Host permissions.

**One decision-relevant paid evaluation once Host-native delegation can
actually complete**: use an authentic public cross-module change where a real
diff and hidden deterministic acceptance oracle exist. Record explicit named
handbacks, the decision each role changed, detected regressions, end-to-end
Copilot meter/tokens/latency, compared with an appropriate direct path.
Cap the paid attempts prospectively; permit a further trial only if a
distinct product choice remains unresolved. If Host task invocation fails or
telemetry is missing, classify **INCONCLUSIVE**, don't rerun standalone SDK
plugin subagents: P5 already isolated the `custom_agent_prompt` failure.

**Role-retirement triggers:** when repeated *authentic* cases show a role
returns already-known facts, creates no independent correction, or cannot
complete under Host policy, merge its capability into Main or another role.
Re-add Planner/Tool Worker only after their distinct utility and effective
permissions have been shown. Neither file count nor model reputation wins
without task evidence.

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

## Product gate after SDK boundary diagnosis (2026-10-18)

The standalone SDK `custom_agent_prompt` failure is fully attributed to its missing session interaction; repeating the same GitHub Actions delegation probe does not produce new evidence. The [minimal Copilot Agent Host gate](HOST_DELEGATION_GATE.md) describes a **single optional public-repository check** and a privacy-preserving yes/no classification. The RC2 distribution now includes this gate in the allowlisted ZIP. Separately validate real diff-backed Reviewer results when useful work supplies a natural patch; do not manufacture test tasks or request internal enterprise materials.

**Important upstream nuance:** the [VS Code plugin converter](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/copilot/copilotPluginConverters.ts) forwards SDK agent tool/model/prompt settings but does not demonstrate an enforceable `agents: []` denial in every runtime path. Leaf read-only and no-recursion declarations are **policy hypotheses, not security guarantees**. Effective tool permissions remain a release risk until Host policy confirms them.
