# P5 — actual delegated Council on a release-packaging security fix

**Hypothesis:** v1.1's tested Council intent matters most for two
separate purposes: disposable cross-module discovery (Architect), and
post-patch independent invariant verification (Reviewer). RC2 should
preserve these capabilities **without requiring many agents on ordinary
tasks**.

**This is a product decision gate**, not a model leaderboard or a
subagent-capability toy.

## Authentic public task, not a fabricated arithmetic fixture

RC2 package includes an allowlisted deterministic ZIP builder. Current
`scripts/validate_release.py` checks manifest and named files but
not source symlinks; `scripts/package_release.py` uses `.read_bytes()`
on those allowlisted paths. A symlink to a file outside the plugin
may therefore result in that external file's bytes being distributed.
This is an actual **release packaging boundary** affecting our public
product. The model work should fix the validator/packaging contract and
preserve existing tests and reproducibility.

**Required**: reject symlinked README, LICENSE, agent and docs source,
no ZIP produced from symlinked source, existing ordinary ZIP still
deterministic and valid, new regression tests really compile and pass.
No user corporate data is involved.

## Study shape

At most two model-facing `gpt-6-luna` sessions (low effort):

- **sdk_default**: normal SDK without Next package.
- **rc2_actual_plugin**: **actual RC2 plugin** registered and selected;
  ask its Main to delegate ONLY `Next Architect` then `Next Reviewer`
  around the code change. Requiring named lifecycle events prevents
  confusing instruction-shaped prose with a real subagent handoff.

Same public source SHA, tools, permissions, workspace, task acceptance,
test gate. The RC2 arm receives only one extra workflow instruction
(the behavior under test), which means this is **not a blinded pure
prompt-only comparison**. The scope of the claim is deliberately narrow.

**Scoped public-fixture tools**: the SDK does not give either agent shell,
network or external writes; host permission handler allows read
tool calls (the SDK can omit filenames in read approvals, so this is **not** a proven filesystem read sandbox), and writes only to `scripts/validate_release.py`,
`scripts/package_release.py`, `tests/test_release.py`. The external
grader runs after each agent completes with a minimal environment,
no `GITHUB_TOKEN` and no Copilot/OpenAI key. The model cannot use the
grader or inspect its hidden negative mutants in its workdir.

**Quality result:** independently execute newly authored tests, check
valid ZIP/manifest stays correct, explicitly mutate FOUR source paths
into symlinks to public external decoy and assert both validation and
packager reject them. Preserve exact generated patches, tool/
permission and subagent lifecycle/usage data. Record `pass` only
when complete acceptance passes and scope/model are correct.

**Role result:** require a real `subagent.started` and
`subagent.completed` with `Next Architect` and `Next Reviewer`
names. If implementation succeeds without these events, report
`QUALITY_PASS / ROLE_CHAIN_UNPROVEN`, not Council success.
If tool wiring blocks delegation, report the exact permission/tool
problem and stop without blaming a model.

**Cost:** one launch marker and a single fixed study; no retries or
unbounded paired sampling; explicit timeouts and GitHub credits only.
Only the same Luna model is used automatically. Sol/Sonnet and Haiku
remain candidate routes but are NOT invoked in this test. Report
Copilot nano-AIU and token counts separately; no assumed cash prices.

**Interpretation:** One study may reveal an integration defect or
suggest a marginal effect; it is not statistical proof of agent-
allocation superiority. The next design decision is to fix verified
routing/permission issues or preserve/remove a particular role,
not to benchmark every variant.

**Status:** STAGED; no paid inference sent yet.
