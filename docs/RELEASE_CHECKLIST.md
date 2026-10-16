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
- [ ] All RC2 roles recognized as separate identities by real Copilot SDK.
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
