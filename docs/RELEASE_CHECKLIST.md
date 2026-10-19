# Role-topology RC2 — decision gate (not a public release)

## Free, static test (automated)
- [x] Exactly one user-visible Main and seven hidden role-specific leaves.
- [x] Main inherits Host-selected model/tools. No `tools: []` anywhere.
- [x] Explicit nonempty leaf read/search lists, `agents: []` and pinned
      initial leaf model labels; this checks DECLARATION ONLY.
- [x] Negative tests for hidden/visible roles, unknown agents, model mismatch,
      accidental MCP/hook/skill bundles, malformed manifest and ZIP integrity.
- [x] Reproducible allowlisted ZIP + no-cost GitHub Actions success.
- [x] Clear role→trigger→evidence→owner and rollback docs.

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


## P18 — verified zero-model catalog in ephemeral real Host

- [x] AHP returned `copilotcli` and **two protected resources**.
- [x] AHP root advertised **zero Copilot models** within a bounded
      observation, including no `gpt-6-luna` or `auto`
      ([P18 #39197886981](https://github.com/YB-Park/over-the-luna/actions/runs/39197886981)).
- [x] Future genuine Architect-turn harness now requires exact
      advertised Luna ID before submitting any model turn.
- [x] A named leaf must be identified in actual
      `chat/toolCallReady.toolInput`; its independent source evidence
      must come from a successful **task result**, not Main's summary.
- [ ] Actual cause of P17 `chat/error` still unknown. No model or
      authorization claim can be inferred solely from a zero catalog.
- [ ] Genuine Council completion remains unverified; no paid repeats
      until the real Host catalog and approved identity permit a turn.

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

## P19 — pragmatic opt-in pilot shipment decision (2026-10-19)

- [x] **Pilot package READY**: allowlisted ZIP containing 8 agents plus
      `docs/PILOT_GUIDE.md`, and a stdlib-only ZIP auditor; built on
      [CI #39201552015](https://github.com/YB-Park/over-the-luna/actions/runs/39201552015),
      SHA-256 `46c7138136180a256360bf6eaa9d1ba14f676587568b5e1f85bcf8730122c7b1`.
      14 static role tests, 13 accounting tests, 6 negative ZIP tests PASS.
- [x] **Evidence-calibrated runtime instructions**: safe direct work may
      produce `PILOT_DIRECT_OK` without pretending Council ran. A blocked
      named leaf must produce `NAMED_DELEGATION_UNAVAILABLE`; high-impact
      changes without a real independent check must retain
      `REVIEW_UNVERIFIED`. A declaration is not Host enforcement.
- [x] **Reversible installation path**:
      `chat.plugins.enabled` and local `chat.pluginLocations` in *user*
      settings, approved Copilot harness, no duplicate Next identity and
      immediate disable/rollback. No automatic settings edits, provider
      relays, enterprise policy bypass or corporate artifact exports.
- [ ] **Personal/limited alpha ACTIVE**: requires a signed-in developer
      actually selecting the plugin and confirming one low-risk direct
      outcome; this has **not been observed in this session**. Safe
      package alone never implies a working session.
- [ ] **Council beta**: require one genuine named Architect return and
      one independent post-edit Reviewer on real diff/test evidence,
      across at least three decision-relevant tasks, with **zero severe
      tool/policy/data boundary incidents**. Document minor defects;
      no 100%-perfection or exhaustive model matrix required.
- [ ] **Public stable release**: separate owner authorization after
      pilot incidents, upgrade/rollback and effective Host permissions
      are reviewed. Do not merge research PR or tag a release here.

**Decision:** publishable *inside this research branch* as an opt-in
limited pilot candidate. Productization is **staged**: direct usefulness
can be trialed now; never market Council assurance before actual
leaf-return evidence. Existing `main` v1.1.1 and RC1 untouched.

## Go / no-go
Retain roles by marginal evidence, not by a 'smallest agents' ideology.
Do not equate user-visible VS Code model availability with the separate ephemeral Actions Host model catalog. P18 observed zero Copilot model entries in the latter; fail closed before requesting Luna there.
No automatic API bridge, mandatory premium opinion, main merge or stable tag.
Research and release remain separated; **RC1 and v1.1.1 stay intact**.

### Important standalone SDK boundary

[One-shot causal diagnostic](https://github.com/YB-Park/over-the-luna/actions/runs/38870191856) returned `Standalone server does not support session effect 'custom_agent_prompt'` for the correctly qualified Next Architect. This is **not a failed model routing policy** and cannot be cured by more prompt or cost benchmarks. RC2 is not Host-integrated until its actual Host-native named role handback is observed. No corporate artifacts should be exported to demonstrate it.

### Host-native acceptance (privacy-preserving, minimal)

- [ ] Optional, **one** public-repo Copilot Agent Host invocation of Next Architect completes and returns a decision/evidence/work-set packet. See [gate](HOST_DELEGATION_GATE.md). No internal artifacts exported.
- [ ] Later, where a genuine **public** patch exists, the named Next Reviewer receives real diff/test evidence and returns an independent specific finding or grounded PASS. No fake second stage on an empty diff.
- [ ] Effective read/write approvals, denied write attempts and provider boundaries remain separate Host-policy checks; a self-reported yes/no is not enforcement telemetry.
- [ ] Do not promote the new Council as operationally verified merely because the standalone SDK registers agents. No more standalone `custom_agent_prompt` retry experiments.
