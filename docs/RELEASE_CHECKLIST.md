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
