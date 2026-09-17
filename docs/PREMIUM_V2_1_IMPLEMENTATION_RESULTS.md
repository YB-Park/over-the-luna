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

Run: `35164850687`  
Head: `6dfc11f0680889fe7cfe4d024fe28563f57ca196`  
Conclusion: **PASS**

Observed: **41/41 tests passed**.

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
- runtime receipt → COMPLETE fixture.

A separate static validator now pins the experimental plugin's two-agent / seven-hook topology and audit-mode boundary before live calibration.

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

Planned ceiling: `--max-ai-credits=30` (runaway ceiling, not intended spend).

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

## Current gate

Before paid development tasks:

1. static experimental-plugin validation must pass;
2. runtime authentication must reach a real model call through an authorized supported path;
3. first real plugin trace must show whether hooks load and expose expected event schemas;
4. audit-mode schema calibration must be completed before switching plugin hooks to enforce mode;
5. real development costs begin only after runtime calibration succeeds.

Promotion holdouts remain unauthorized and unselected.
