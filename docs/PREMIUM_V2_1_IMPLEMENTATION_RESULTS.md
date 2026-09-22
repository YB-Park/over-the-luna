# Premium v2.1 Implementation / Runtime Results

Status: **implementation in progress; no product conclusion**  
Branch: `experiment/premium-v2-1-minimal-cascade`

This ledger records implementation/runtime evidence for the Astra-approved minimal-cascade experiment. It is separate from promotion holdout evidence.

## Approved design

Independent closure review: `5e1c7ac425acf2e35b2b015260301f150af2c65d`  
Verdict: `APPROVE_MINIMAL_IMPLEMENTATION_EXPERIMENT` (HIGH confidence)

Authorized architecture:

```text
bounded Terra intake
  -> one continuous Luna Builder attempt
  -> deterministic completion reconciliation
  -> at most one Terra takeover on concrete unresolved blocking semantic evidence
  -> stop
```

No Lane M, Architect, Verifier, repeated switching, or automatic cross-family reviewer.

## Zero-AI controller evidence

### Controller core

Implementation commits include:
- `93bc2d08a3b4f13365d0224ec9467cde5ee51171` — deterministic controller skeleton;
- `58feff8c50739cb2aec1465daa57af8cc388ca2c` — authority-record tightening;
- `5f832f6e606336a281b07f1584d3f889968fd82b` — fail-closed final-record layer;
- `16477b6a57f0fd6b894af58b0d8d4fbee12ce4e6` — final-record fixtures.

The controller deliberately enforces only record consistency. It does not claim semantic completeness of extracted criteria or relevance of a passing test.

### Isolated experimental plugin

Implemented under `experiments/premium_v2_1_plugin/`, leaving the stable root plugin untouched.

Important commits:
- `2c4d8f200fcd47dd71f99bf25ddd989ebb45ccb4` — experimental manifest;
- `46ebd6ec6a72ceb962bda07dfe560035d182e97d` — Terra root agent;
- `42a26a25d584f743104fbfe7683dd86fe1aaa5c9` — Luna Builder;
- `ed4b12addf73d3f44f5c6697f0bfd40769f3ce85` — plugin-local controller;
- `1ee8662ed2c62eabbf30b00782f013293e49b144` — lifecycle hook controller;
- `d98ce032a3fc608ae0f527595ca163fcd57b580b` — Copilot-format plugin `hooks.json`;
- `6dfc11f0680889fe7cfe4d024fe28563f57ca196` — lifecycle fixtures.

Plugin hooks are initially in **audit mode** so the first real runtime trace can calibrate actual tool/event payloads before any hook starts forcing extra AI turns.

### Zero-AI CI result

Initial plugin-lifecycle baseline:
- run `35164850687`;
- head `6dfc11f0680889fe7cfe4d024fe28563f57ca196`;
- **41/41 PASS**.

Intermediate pre-live baseline:
- run `35689194399`;
- head `ed68d11a5bad726a719d4dc595a1590ec06f6e7d`;
- **57/57 PASS**.

Latest pre-live code baseline:
- run `35799509383`;
- head `2c3db3c19a30bf8b2efa9ccabfe3d9acf6095770`;
- **137/137 PASS**.

Coverage includes:
- immutable captured U obligation;
- U→A laundering rejection;
- blocking/required downgrade rejection;
- same-ID criterion narrowing rejection;
- preserved blocking R obligations;
- forged waiver rejection;
- authenticated waiver partial semantics;
- stale/wrong-run/uncollected receipt rejection;
- missing/stale final record fail-closed semantics;
- workspace digest sensitivity;
- one-correction Stop behavior;
- pre-Builder repository-tool denial logic;
- single-Builder enforcement logic;
- post-Builder Terra takeover marking;
- metadata edits not counting as takeover;
- runtime receipt → COMPLETE fixture;
- ambiguous multi-session trace selection rejection;
- resumed/multi-prompt mission fail-closed behavior;
- malformed lifecycle state and unexpected hook-error fail-closed behavior;
- non-Builder and second-Builder dispatch rejection;
- PostToolUse defense in depth for pre-tool bypass;
- current-workspace final-record consistency;
- conflicting workspace/external final-record rejection;
- explicit FAILED/UNRESOLVED blocking-row gate before Terra takeover;
- malformed JSON/non-object hook input fail-closed behavior in enforce mode.

A separate static validator pins the experimental plugin's two-agent / seven-hook topology and audit-mode boundary before live calibration.

### Pre-live hardening pass

The first implementation review before authenticated runtime calibration found and closed several control-plane issues without invoking AI:

- `5209dacc5c89f09750b0a063ca155e37ae9867fc` / `88cbf21eda937d66217d19de20b6a3f4d0bfa884` — normalize VS Code-compatible and Copilot CLI hook payload variants, including `tool_response`, `tool_result`, camelCase tool fields, and agent-name variants;
- `8f616cdcd264368cf6fa1b6f73d18a5382418cf4` / `abdf8c1f4dbe7318ecd6acd52b918c866134f95d` — prefer the concrete Builder name when a runtime also emits a generic agent type;
- `ead8cefba2298deea0f0295c3da1e019a79895ac` through `a1cebe94f2aa35e4e3c79853d58aa9157d927bf4` — replace the obsolete agent-scoped-hook readiness assumption with plugin-level preflight checks and regression-test the settings scan;
- `6da8f98a8b6bf2a3cdadb88e58d8a1ceb3437778` / `c1a47bcf8245be055f8dfafb178eb645827bad56` — fix a real fail-open edge where the sentinel `DIGEST_ERROR` could otherwise be treated as a matching workspace revision;
- `c6b0e2ad72f2c67b8291a24e29e65e6d1b8052e8` — serialize external controller-state updates with a cross-platform lock and refuse trusted completion when no real session ID is observed;
- `be43157aba57cd5dadaa7dc887d89bf216caee22` / `a6bdc37d8f9c9c69ca70510a5f086bba94e2839e` — add a deterministic runtime-trace reporter and fail-closed calibration fixtures;
- `d91c40448e494c0e06c261bb1cefec8bf0790986` / `33f427b1bcdc9108a455b5a13f5735e50daed1a9` — add a synthetic, explicitly non-heldout smoke workspace generator;
- `434b26e8c62fd1daad5fb1b6d0a7fd8c975599fa` — add the product-target live audit runbook;
- `ed68d11a5bad726a719d4dc595a1590ec06f6e7d` — add a non-executable authenticated Actions smoke template;
- `bea8af3dd34e958ef436438a10b12530f7e74bbd` / `635ee73bb0078c619cfb239683cabdf6e62b3b79` — fail closed on ambiguous session selection and resumed/single-mission violations;
- `8854f3e42ee0d6e807e7cdc6d626a26b981af365` through `31f6d92d7080de405dce801a0dca8cf41ab62277` — reject malformed lifecycle state and unexpected hook failures;
- `5e374d8a3478d8d8d9b5839ad88c557100aa803e` / `c2fd4cbbb84f7aee7da30301ab7430fca158abc6` — harden Builder dispatch cardinality and metadata-only gating;
- `809591a72ab8cf2f6180c773349a872b4cadd266` / `425b5561495a245788d18f11389c714069ca6dad` — add PostToolUse defense in depth when a pre-tool control is bypassed;
- `eefa8521ec124a9e7ed1d9290ad2ef4aeaa0e613` / `03b7339568f3b9bd3c069859e3edb9e6269bf108` — require current-workspace and non-conflicting final-state evidence in the trace gate;
- `4ba9ada1a498074018f9352a77ab4cb2af866a0c` / `617dadef0cb7b91f189cb6ce61d768bc3c02dac1` — require an explicit captured FAILED/UNRESOLVED blocking criterion before Terra repository takeover;
- `8ca5d4a272721485bed4c12ad2426cfb96222c0e` / `76c7c96d964a034a9bbe4da79c61d19dd925b5ec` — make malformed/non-object hook input stop enforce-mode execution rather than fail open;
- `7fd4c5e48e943830be834ca56a9a86e0d6e1b46c` through `8c7f44d1fb29119c4a292790e3abff480cba545f` — bind controller state to valid phases and a fixed workspace, fail closed on unexpected lifecycle events, and align lifecycle fixtures;
- `f722a81a13fe164fc9781b623ffed603ae99e342` / `b12c48c2bf118d0784953ade8bb86e9d690cf01f` — cross-check configured hook firing against Agent Host `execute_hook` OTel evidence;
- `8e9a04879321ff68ac0e837b4b65b390774ec70a` / `d947a5f444de1adf1c06a836b898775ef8dd7750` — require Builder and hook OTel evidence to be rooted under the selected root invoke rather than accepting disconnected/stale spans;
- `af6cc61aa5518978e9c67c6b1767721c7c363a5d` through `1d430bb0eb56a8b576499c8b662359ced8939c80` — model the Builder Agent-tool wrapper lifecycle explicitly so the normal matching PostToolUse is not mistaken for a second child, and require exact dispatch/start/stop/completion evidence;
- `ae01e5b2e1d4cc786049401a04e251cf8eebff5c` / `0229b7a4892255fddc1a45acbb7e4fe80880b1ed` — tighten trusted final lifecycle and takeover phase/flag/basis consistency;
- `b103ee8d601731b09575ce2dcf42f5a69bae9082` / `f98e1769be27bafa5c103021fed87932237c6dc7` — align plugin-local controller fail-closed behavior with the reference controller and add adversarial terminal-outcome parity tests;
- `5e01d19ee0e7025d3f0c0556b69c54f578960326` through `2c3db3c19a30bf8b2efa9ccabfe3d9acf6095770` — add a zero-AI post-smoke evidence collector that selects the matching session, reruns the focused test, captures diff/state/OTel, and emits a SHA-256 manifest.

The trace reporter only marks a run as an enforce-mode **candidate** when the minimum runtime facts are actually present: one unambiguous runtime session, single-mission lifecycle counts, all seven raw lifecycle event types, successful rooted Agent Host `execute_hook` evidence, exactly one Builder Agent-tool dispatch plus one start/stop lifecycle and matching wrapper completion, at least one collected PASS execution receipt, both current/non-conflicting VALID_COMPLETE final-record copies, exactly one selected root invoke, exactly one Builder invoke rooted under it, observed root Terra identity, observed Builder Luna identity, and parse-clean hook/CLI/OTel evidence. This is an implementation gate, not a product-success verdict.

The hardening pass does not solve semantic criterion completeness, evidence relevance, same-user tamper resistance, or runtime waiver authentication.

### Zero-AI Copilot CLI plugin-parser smoke

Launch commit: `9663316c00afc77c239d6acc79746418f6b0bb26`.  
Run: `35165338218`.  
One-shot workflow removal: `21bc3f048f7eb89577bd7fbad3b054c5e5f7ccd3`.

Environment:
- Copilot CLI pinned to **1.0.85**;
- no `copilot-requests: write` permission;
- no model prompt or inference call.

Result: **PASS**.

`copilot plugin install <local-path>` accepted the experimental plugin and `copilot plugin list --json` returned exactly one enabled entry:

```json
{
  "enabled": true,
  "marketplace": "",
  "name": "over-the-luna-premium-v2-1-experiment",
  "source": "installed",
  "version": "0.0.1"
}
```

This establishes that Copilot CLI 1.0.85 accepts the legacy/Copilot-format plugin manifest/layout. It does **not** establish that hooks fire or that a live Terra→Luna transition works; those require an authenticated model session.

The CLI emitted a deprecation warning that direct path/repository plugin installs will be removed in a future release in favor of marketplace installs. That warning does not invalidate the current implementation experiment but must be revisited before any product packaging decision.

Artifact: `10474831937` (`premium-v2-1-plugin-parse`).

## Local product-runtime facts reported by owner

These are manually reported configuration facts, not a machine-captured trace:

- VS Code: `1.134.0`;
- Custom Agent support: available;
- UI: `Agent Customizations for Copilot [Agent Host]`;
- Hooks UI: available with `+ Configure Hooks`, no existing hooks listed;
- `chat.useCustomAgentHooks`: not exposed in Settings UI;
- a separately installed GitHub Copilot extension is not visible in Extensions;
- `@github/copilot: 1.0.81-0` was observed, exact role not independently established;
- repository-external controller-state placement appears structurally possible;
- tamper protection of that state against agent shell access remains **NOT_OBSERVED**.

Current official documentation supports plugin-level hooks independently of `.agent.md` agent-scoped hook settings. Actual hook loading in the owner's Agent Host remains a future product-runtime smoke, not inferred from documentation.

## Runtime smoke R0 — GitHub Actions authentication policy failure

Purpose: calibrate actual Copilot CLI plugin/hook event schemas on a trivial one-file repository before any development benchmark.

Planned CLI response limit: `--max-ai-credits=30` (a **soft** runaway guard, not intended spend or an exact billing ceiling).

### R0a — workflow bootstrap invalid

Launch commit: `373e3d07a50d28d4e19197f754094c959e85c993`.

The workflow was rejected before any job was created. No Copilot process/model was started. The one-shot workflow was removed at `a2454224e6361d35e99fd5794ab3bd17e67e5f7b`.

Classification: **WORKFLOW_BOOTSTRAP_FAIL**.  
AI/model result: **not applicable**.

### R0b — Actions Copilot authentication denied before inference

Launch commit: `ef3d61e9b8e2188945a670ff836756d01e2326fc`.  
Run: `35165005035`.  
One-shot workflow removal: `fe5ed235e057397b163ec9ce791a64034f78e3ee`.

Environment observations:
- GitHub-hosted `ubuntu-24.04` runner;
- Copilot CLI installed as **1.0.85**;
- workflow token showed `CopilotRequests: write` permission.

Copilot CLI terminated before any model/tool/plugin lifecycle work with:

`Error: Access denied by policy settings`

Captured summary:

```json
{
  "agent_exit": 1,
  "models": [],
  "subagents": [],
  "tool_starts": 0,
  "usage_credits": null,
  "wall_seconds": 2,
  "test_exit": 1
}
```

No hook-state files or workspace controller metadata were created because the failure happened before the agent/plugin lifecycle started.

Classification: **AUTH_POLICY_FAIL / INFRA**, not a model, harness, or task failure.

Credit accounting: **no model call or usage checkpoint was recorded; credit consumption was not observed.** Do not infer an exact zero-credit billing event from absence of telemetry.

Artifact: `10474616173` (`premium-v2-1-runtime-smoke`).

## Authentication-path implication

Current GitHub documentation distinguishes two Actions authentication paths:
- built-in `GITHUB_TOKEN`, oriented to organization-owned repositories with the relevant organization Copilot CLI billing policy enabled;
- a user-owned fine-grained personal access token with the **Copilot Requests** account permission, passed to CLI as `COPILOT_GITHUB_TOKEN`, which draws usage from that user's Copilot entitlement.

This repository is user-owned. Repeating R0b with the same built-in-token path has no decision value and is prohibited unless the platform/policy changes.

No secret/token should ever be pasted into chat or committed to the repository.

A one-shot secret-presence probe was later run without exposing any token value:

- run: `35183896173`;
- result: `copilot_pat_secret_present=no`;
- the probe workflow was immediately removed at branch head `b4d519cd2af35c48112e334b0cd742ac281ef045`.

Therefore an authenticated GitHub Actions paid smoke is still blocked until the owner configures a user-owned fine-grained PAT as the repository secret `COPILOT_GITHUB_TOKEN`. Repeating the built-in-token failure has no decision value.

The preferred product-target calibration path is now documented in `docs/PREMIUM_V2_1_LIVE_AUDIT_RUNBOOK.md`: load the nested experimental plugin directly in VS Code, keep all hooks in audit mode, run only the synthetic smoke workspace, preserve the raw lifecycle trace, and run `scripts/premium_v2_1_trace_report.py`.

A secondary authenticated Actions template is stored outside `.github/workflows/` under `experiments/premium_v2_1_plugin/smoke/`, so it cannot accidentally spend credits while authentication is absent.

## Current gate

Before paid development tasks:

1. zero-AI validation must remain green;
2. one real **audit-mode** VS Code Agent Host trace must establish raw hook firing and matching successful rooted `execute_hook` OTel evidence;
3. the trace must show one Builder Agent-tool dispatch, one Builder start/stop lifecycle, and the matching wrapper completion;
4. root/child resolved backend identity must be observed from rooted runtime telemetry rather than inferred from agent frontmatter;
5. PostToolUse and Stop payloads must be sufficient for current receipt/final-record parsing, with both final-record copies current and consistent;
6. any parser or topology mismatch is fixed and re-audited before changing `hooks.json` to enforce mode;
7. the live evidence should be collected with `scripts/premium_v2_1_collect_smoke_evidence.py` so hostile review receives the raw matching session plus a hashed bundle;
8. authenticated interactive waiver creation remains out of scope until a trustworthy runtime user-event path is designed;
9. controller-state tamper protection remains **NOT_OBSERVED** and must not be represented as a security boundary;
10. only after runtime calibration succeeds may real development-task spending begin.

Promotion holdouts remain unauthorized and unselected. H1-H4 are not fresh holdouts for this redesign.
