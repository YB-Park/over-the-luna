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
      [CI #39219481908](https://github.com/YB-Park/over-the-luna/actions/runs/39201552015),
      SHA-256 `32e43951f768d66ba2f02134c70201ff24c241d381a2ee21e3744720e575aa18`.
      15 static role tests, 13 accounting tests, 8 negative ZIP tests PASS.
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

## P20 — offline source-based review: independently pin published ZIP

The P19 `scripts/pilot_archive.py` only validated path allowlist, basic
frontmatter envelopes, CRC and plugin identity; it returned its own
SHA-256 but did **not compare against a separately published trusted digest**.
A repacked archive with `Next Architect` changed from
`tools: ['read', 'search']` to `tools: ['edit', 'search']` could therefore
pass the old structural check despite breaking the intended role policy.
This is a **real review finding about the downloaded package**, not proof
that VS Code enforces an agent's declared tool restrictions.

**Observed fixed CI:** [#39219481908](https://github.com/YB-Park/over-the-luna/actions/runs/39203115287)
passed 15 release tests, **8** ZIP/negative tests and 13
role-accounting tests; published the 15-member RC2 ZIP with SHA-256
`dcb49af6379b27bbf745f9bc188e578765f784a7b47a45587c8237b6c656c383` (37,654 bytes). No live Copilot or subagent ran.

**Fix:** pilot verifier CLI now **requires** `--expected-sha256`,
which must come from this PR's successful Actions package digest, not
from the ZIP itself. Offline negative test builds a structurally valid,
CRC-valid, repacked ZIP with widened Architect tool declaration and
checks that the pinned digest rejects it. Missing/malformed digests fail.
Low-level `verify(archive)` remains available for structural diagnostic
tests and **is not authenticated package approval**. CI uses the
freshly built in-job digest to test this contract, which cannot replace
the user's out-of-band digest check when downloading.

**Scope/evidence:** source diff inspection and deterministic regression,
not a completed native Host `Next Reviewer` invocation. This closes one
packaging-integrity defect, **not** Council handback, subagent read-only
enforcement, or signed-in Host readiness. No other authorized branches
are modified. This audit does not demand another paid model turn.

## P21 — current Copilot-vs-Local compatibility diagnostic (2026-10-19)

- [x] Inspected protected stable v1.1.1 Main and Next RC2 against current
      VS Code documentation: old Main explicitly instructs
      `agent/runSubagent`, now documented under **Local harness**, while
      modern **Copilot harness** runs in the separate Agent Host and offers
      provider-native task delegation. Do **not** assume a model, UI or
      extension version determines the harness.
- [x] Next Main now distinguishes both harnesses and treats an explicit
      named-delegation diagnostic as a measurable task: one permitted
      subagent attempt or an honest
      `NAMED_DELEGATION_UNAVAILABLE` /
      `DELEGATION_ATTEMPT_FAILED` state. It never silently claims a
      Council completion because the model answered directly.
- [x] [Harness diagnostic recipe](HARNESS_DIAGNOSTIC.md) covers selected
      harness, agent source version, applied system instructions,
      actual tool definitions and observable Agent Flow Chart. No private
      transcripts exported, no new paid Host runs.
- [x] [No-model CI #39219481908](https://github.com/YB-Park/over-the-luna/actions/runs/39219481908)
      **PASS** before P22: 15 release + 8 ZIP negative + 13 accounting = **36**
      tests, independent package grader, ZIP SHA-256 `32e43951f768d66ba2f02134c70201ff24c241d381a2ee21e3744720e575aa18` and 15
      allowlisted members. The static green gate is not live Host
      named-subagent proof.
- [ ] The user-side signed-in VS Code session still needs one
      controlled forced Architect test and private Chat Debug
      confirmation. Missing UI chrome alone does not establish a
      missing native task. No stable `main` or RC1 modifications.

## P22 — user-confirmed explicit stable Reviewer invocation

- [x] User observed **real visible subagent call** after a specific
      `Luna Reviewer` request, with hovered name, model, reasoning
      effort and context window. Ordinary requests previously
      showed **zero calls**, not a UI-only display problem.
- [x] Stable v1.1.1 already contains a strict post-edit Reviewer
      rule. Not proof that it executes automatically in the current
      signed-in Host; do not modify protected main on a hunch.
- [x] Next's research Main now re-checks **post-edit assurance
      separately from DIRECT investigation**. On a real semantic
      diff/tests it selects conditional ONE `Next Reviewer` call
      or reports `REVIEW_UNVERIFIED` with the missing capability.
- [ ] Signed-in Next user test: one meaningful low-risk diff without
      mentioning any role, then observe `Next Reviewer` start,
      completion and grounded packet. A forced stable `Luna Reviewer`
      event is not proof of Next automatic routing.
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

  Latest P22 [CI #39220584169](https://github.com/YB-Park/over-the-luna/actions/runs/39220584169) **PASS**: 16 release/role + 8 ZIP negative + 13 accounting = **37** tests; no model calls, ZIP SHA-256 `32e43951f768d66ba2f02134c70201ff24c241d381a2ee21e3744720e575aa18`, size 38,487 bytes.
