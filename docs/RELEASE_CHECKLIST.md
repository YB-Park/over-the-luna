# Role-topology RC2 — decision gate (not a public release)

## Free, static test (automated)
- [ ] Exactly one user-visible Main and seven hidden role-specific leaves.
- [ ] Main inherits Host-selected model/tools. No `tools: []` anywhere.
- [ ] Explicit nonempty leaf read/search lists, `agents: []` and pinned
      initial leaf model labels; this checks DECLARATION ONLY.
- [ ] Negative tests for hidden/visible roles, unknown agents, model mismatch,
      accidental MCP/hook/skill bundles, malformed manifest and ZIP integrity.
- [ ] Reproducible allowlisted ZIP + no-cost GitHub Actions success.
- [ ] Clear role→trigger→evidence→owner and rollback docs.

## Native Agent Host integration stages (public Actions, no inference)
- [x] VS Code `code agent host` starts, authenticates AHP transport and
      negotiates 1.0.0; native provider `copilotcli` advertised.
- [x] Copilot `createSession` accepted and session channel subscribed.
- [x] P15 no-turn `creating` was a normal provisional-session state, not a valid readiness failure.
- [ ] RC2 plugin registered with actual Host session; named task finishes
      and returns independent evidence.
- [ ] Host-native complex-task role selection improves accepted quality or
      avoids rework relative to justified direct evidence.

**Stop:** Do not repeat P5 SDK subagent probes or claim Council value from
Host boot/registry alone. No further paid attempts should be repeated
until the actual first-turn `chat/error` is diagnosable and approved
Host credentials/model policy permit a meaningful named-role call.

## P16/P17 actual Host integration findings (2026-10-19)

- [x] Official native Host and \`copilotcli\` provider available.
- [x] Provisional no-turn \`creating\` is expected; **NOT an auth failure**.
- [x] Native Host parses \`vscode-agent-host-file:\` plugin and publishes exactly
      8/8 Next roles, including Architect and Main (P16 PASS).
- [x] One authorized Actions **first turn submitted** with GPT-6 Luna
      explicitly requested and Next Main selected (P17).
- [ ] Native Host completes a turn without chat error; P17 received
      \`chat/error\` before the task tool started (root cause UNVERIFIED).
- [ ] Next Architect completes with named role, authenticated execution,
      returned source evidence and meaningful decision change.
- [ ] Independent Reviewer with real diff and acceptance tests.
- [ ] Effective tool/data policy enforced by Host in running leaf.

A no-turn session \`ready\` state is **not** a valid prerequisite:
the provider materializes lazily at first send. Only one P17 paid-eligible
public request was submitted; exact token billing was not observed.
Never count a plugin registry, chat-start action or \`task\` **attempt**
as Council handback. There is no grounds for main/stable release.


## Product behavior (NOT established by static tests)
- [x] Earlier single-Main research plugin package loaded and ran in SDK.
- [x] All RC2 roles recognized as separate identities by real Copilot SDK.
- [ ] One actual Host-native Architect → Main → Reviewer trajectory observed (standalone SDK cannot supply plugin custom_agent_prompt).
- [ ] Host leaf read-only/no-recursion contract confirmed before treating
      leaf permissions as a security boundary.
- [ ] Sol vs Sonnet backing model used as requested; no silent fallback.
- [ ] Corporate workspace model/provider approvals; no unconsented external
      data transmission.
- [ ] Role specialization improves actual user work or avoids rework/attention
      cost relative to default Main/native; not an automatic assumption.

## Go / no-go
Retain roles by marginal evidence, not by a 'smallest agents' ideology.
No further model catalogue checks; the user confirmed all models available.
No automatic API bridge, mandatory premium opinion, main merge or stable tag.
Research and release remain separated; **RC1 and v1.1.1 stay intact**.

### Important standalone SDK boundary

[One-shot causal diagnostic](https://github.com/YB-Park/over-the-luna/actions/runs/38870191856) returned `Standalone server does not support session effect 'custom_agent_prompt'` for the correctly qualified Next Architect. This is **not a failed model routing policy** and cannot be cured by more prompt or cost benchmarks. RC2 is not Host-integrated until its actual Host-native named role handback is observed. No corporate artifacts should be exported to demonstrate it.

### Host-native acceptance (privacy-preserving, minimal)

- [ ] Optional, **one** public-repo Copilot Agent Host invocation of Next Architect completes and returns a decision/evidence/work-set packet. See [gate](HOST_DELEGATION_GATE.md). No internal artifacts exported.
- [ ] Later, where a genuine **public** patch exists, the named Next Reviewer receives real diff/test evidence and returns an independent specific finding or grounded PASS. No fake second stage on an empty diff.
- [ ] Effective read/write approvals, denied write attempts and provider boundaries remain separate Host-policy checks; a self-reported yes/no is not enforcement telemetry.
- [ ] Do not promote the new Council as operationally verified merely because the standalone SDK registers agents. No more standalone `custom_agent_prompt` retry experiments.
