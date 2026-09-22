# Premium v2.1 Live Audit Runbook

Status: **runtime calibration only — no product conclusion**  
Branch: `experiment/premium-v2-1-minimal-cascade`  
Approved design anchor: `5e1c7ac425acf2e35b2b015260301f150af2c65d`

This runbook is for the first real Premium v2.1 runtime trace. It deliberately
uses a synthetic one-file bug. It must not be counted as a promotion holdout,
capability win, or product-quality result.

## 1. What this smoke is allowed to establish

The first live audit is only allowed to answer:

1. Does the experimental plugin load in the intended VS Code Agent Host?
2. Do plugin-level lifecycle hooks actually fire?
3. Does the root invoke exactly one `Premium v2.1 Luna Builder` child?
4. Are the root and child backend identities observable as Terra and Luna?
5. Do PostToolUse events contain enough execution data to create receipts?
6. Does Stop produce a controller final record?
7. What exact event field shapes does this runtime expose?

It does **not** establish semantic-completeness, tamper resistance, product
quality, cost advantage, promotion readiness, or general multi-repository
reliability.

## 2. Keep the first run in audit mode

Do not switch `OTL_V2_1_HOOK_MODE` to `enforce` before this trace.

The committed `experiments/premium_v2_1_plugin/hooks.json` must still contain
`OTL_V2_1_HOOK_MODE=audit` on every lifecycle hook.

Reason: the first run is schema calibration. A mistaken parser or tool-name
assumption must not spend extra model turns or block a legitimate tool before
we have observed the actual Agent Host payload.

## 3. Current VS Code plugin/hook facts

As of 2026-09-23, the current VS Code documentation states:

- existing Copilot-format plugins without the Agent Plugins 1.0 schema remain
  supported;
- Copilot-format plugin hooks are discovered from root `hooks.json`;
- plugin-level hooks run when the plugin is enabled;
- `chat.useCustomAgentHooks` is specifically for hooks embedded in custom
  agent frontmatter and is not the enablement switch for plugin-level hooks;
- local plugin directories can be registered with `chat.pluginLocations`;
- hook execution can still be disabled by VS Code/organization policy;
- Agent Host OTel can emit `invoke_agent`, `chat`, and `execute_hook` spans;
  `execute_hook` carries the hook type and execution result, giving an
  independent cross-check that a configured hook actually ran;
- `chat.useHooks` is treated here as a possible policy/configuration gate:
  current documentation describes both hook-disable policy behavior and
  Local-harness scope, so effective Agent Host behavior is proved by the live
  trace rather than inferred from a text setting.

References:

- https://code.visualstudio.com/docs/agent-customization/agent-plugins
- https://code.visualstudio.com/docs/agent-customization/hooks
- https://code.visualstudio.com/docs/enterprise/ai-settings

## 4. Zero-AI preflight

From the experiment checkout:

```bash
python scripts/premium_v2_1_local_preflight.py \
  --workspace /path/to/the/experiment/checkout
```

Expected static result before the live run:

- `experimental_plugin.valid = true`;
- `experimental_plugin.hook_mode = "audit"`;
- `configuration_status = "READY_FOR_PLUGIN_INSTALL_OR_LIVE_AUDIT"`.

The report intentionally does not require
`chat.useCustomAgentHooks=true`.

If an external state directory is supplied, the preflight can confirm only that
it is structurally outside the workspace. It cannot prove that an agent shell
cannot access it.

## 5. Register the nested experimental plugin in VS Code

The stable root of this repository is a different plugin. Do **not** install the
repository root and assume that it represents v2.1.

The synthetic workspace generator in the next section now writes a workspace
`.vscode/settings.json` that enables Agent Plugins for the disposable workspace
and registers the exact current checkout path:

`<checkout>/experiments/premium_v2_1_plugin`

through `chat.plugins.enabled=true` and `chat.pluginLocations`.

An organization policy can still override local plugin enablement; if that
happens, classify it as a runtime/policy blocker rather than changing the
experiment contract.

This is the preferred smoke path because the plugin source stays outside the
synthetic mutation workspace while VS Code receives an explicit local plugin
location.

If automatic workspace registration is not honored in the active profile,
manually add the same path:

```jsonc
{
  "chat.pluginLocations": {
    "/absolute/path/to/over-the-luna/experiments/premium_v2_1_plugin": true
  }
}
```

Then confirm in Agent Customizations / Plugins that
`over-the-luna-premium-v2-1-experiment` is enabled and that
`Premium Cascade v2.1 (Experimental)` is selectable.

Do not infer hook loading from registration alone. In VS Code, use
**Developer: Show Agent Debug Logs** or the **GitHub Copilot Chat Hooks** output
channel and look for hook loading/execution diagnostics.

## 6. Create the synthetic smoke workspace

Use a fresh directory that is not H1, H2, H3, or H4:

```bash
python scripts/premium_v2_1_make_smoke_workspace.py \
  --output /tmp/otl-premium-v2-1-smoke
```

On Windows, choose any disposable local path instead of `/tmp`.

The generator also records the experimental plugin path in:

`/tmp/otl-premium-v2-1-smoke/.vscode/settings.json`

(or the equivalent path you selected).

The same workspace settings enable **metadata-only OTel capture** with content
capture disabled and write JSONL **outside** the mutation workspace, for example:

`/tmp/otl-premium-v2-1-smoke-copilot-otel.jsonl`

The generator prints the exact `otel_output` path. Keeping telemetry outside
the workspace is required so telemetry writes do not invalidate the controller's
workspace digest.

Open **this synthetic directory**, not the main Over the Luna checkout, as the
VS Code workspace for the paid smoke.

The generated test is expected to fail before the agent runs:

```bash
cd /tmp/otl-premium-v2-1-smoke
python -m unittest -v
```

The fixture is intentionally trivial: `increment(value)` is documented to
return `value + 1` but initially returns `value - 1`.

## 7. VS Code Agent Host smoke — preferred product-target trace

Open only the synthetic smoke directory as the working workspace.

Select:

`Premium Cascade v2.1 (Experimental)`

Submit exactly one task:

> RUNTIME SMOKE ONLY. Work only in this tiny local repository. The public
> function increment(value) is documented to return value plus one, but the
> implementation is wrong and the included unittest fails. Make the smallest
> correct fix, preserve the function signature, run the focused local test, and
> stop. Follow the Premium v2.1 controller metadata contract exactly. Do not add
> unrelated files or features.

Do not continue the conversation with a second user prompt. v2.1 runtime
lifecycle semantics are being calibrated as a **single-mission, single-prompt**
experiment.

Do not manually correct controller metadata during this first run.

## 8. Evidence to preserve immediately after the VS Code run

The hook adapter defaults to external controller state under:

`~/.copilot/over-the-luna-v2-1/state`

Preserve:

- the corresponding `*.events.jsonl`;
- the corresponding controller `*.json`;
- the smoke workspace `.otl-v2-1/controller-proposal.json`;
- `.otl-v2-1/receipt-index.json`;
- `.otl-v2-1/final-record.json`;
- the final working-tree diff;
- the focused unittest result;
- Agent Debug Logs / hook diagnostics needed to prove plugin hook loading;
- the generator-reported external VS Code OTel JSONL file.

Raw event logs can contain prompts/tool arguments. The synthetic smoke is safe
for repository review; do not upload analogous raw traces from proprietary
workspaces without review/redaction.

After the run, prefer collecting the review packet with the zero-AI collector:

```bash
python scripts/premium_v2_1_collect_smoke_evidence.py \
  --workspace /tmp/otl-premium-v2-1-smoke \
  --output /tmp/otl-premium-v2-1-evidence
```

The collector refuses non-smoke workspaces, selects exactly one matching hook
session unless a session key is supplied, reruns the focused unittest, captures
the diff/status, copies controller/OTel evidence, produces the deterministic
trace report, and writes a SHA-256 manifest. These hashes protect the collected
copy; they do **not** prove that same-user state was untampered before
collection.

## 9. Deterministic trace summary

Run:

```bash
python scripts/premium_v2_1_trace_report.py \
  --state-dir ~/.copilot/over-the-luna-v2-1/state \
  --workspace /tmp/otl-premium-v2-1-smoke \
  --otel-output /tmp/otl-premium-v2-1-smoke-copilot-otel.jsonl
```

For the first calibration, inspect the raw `field_shapes` as well as the
summary. The reporter deliberately fails to infer missing facts.

A candidate for a later enforce-mode change requires, at minimum:

- one unambiguous single-mission runtime session;
- all seven configured lifecycle events in the raw hook trace;
- successful Agent Host `execute_hook` OTel evidence for those same hook
  types under the selected root trace;
- exactly one Builder Agent-tool dispatch, one Builder start, one Builder stop,
  and the matching Builder Agent-tool completion;
- at least one current collected PASS execution receipt;
- matching current workspace/external final-record copies with trusted
  `COMPLETE`;
- exactly one selected root invoke and one rooted Builder invoke;
- resolved root Terra and Builder Luna identities;
- no parse errors or unexplained OTel topology conflicts.

The smoke workspace enables the VS Code file OTel exporter specifically so hook
execution and resolved root/child model identity can be cross-checked in the
same run. If the actual Agent Host OTel shape differs, leave the affected fact
as `NOT_OBSERVED` or `CONFLICT`; do not infer it from frontmatter. Fix the
parser against the raw trace and repeat the synthetic audit rather than
weakening the gate.

## 10. Copilot CLI audit smoke — secondary evaluation adapter

CLI is useful for machine-readable model/subagent telemetry, but it is not
assumed runtime-equivalent to VS Code Agent Host.

Current GitHub documentation supports noninteractive authentication with a
user-owned fine-grained PAT that has the **Copilot Requests** account permission
and is supplied as `COPILOT_GITHUB_TOKEN`.

References:

- https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli
- https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions
- https://docs.github.com/en/copilot/reference/hooks-reference

The previous built-in Actions-token path failed before inference with
`Access denied by policy settings`. Do not repeat that same path.

The repository secret probe also established that
`COPILOT_GITHUB_TOKEN` was not configured at that time. Do not put a token in
the repository, issue, chat, artifact, or workflow log.

A non-executable workflow template is stored with the experiment. Only copy it
into `.github/workflows/` for a one-shot run after the secret exists, and
remove the one-shot workflow again after the trace is captured.

The CLI credit cap is a runaway guard, not a claim about exact billing. The
synthetic task and one-shot execution are the primary spend controls.

## 11. Enforce-mode promotion rule

Do **not** switch to enforce mode merely because the synthetic code fix passed.

A separate enforce-mode commit is permitted only after review of a real audit
trace establishes:

- exact PreToolUse tool names/argument shapes needed for gating;
- exact Builder Agent-tool + SubagentStart/SubagentStop identity/ordering fields;
- exact PostToolUse result shape needed for receipt classification;
- usable session identity;
- Stop semantics and one-correction behavior;
- no unexplained missing lifecycle event;
- OTel `execute_hook` coverage agrees with the hook adapter's own event log;
- root/Builder invoke parentage is unambiguous.

If the runtime differs from the parser, fix the parser and repeat a synthetic
audit run. Do not weaken controller invariants merely to obtain COMPLETE.

## 12. Known limits that remain after a successful smoke

Even a perfect first smoke leaves these unresolved:

- criterion extraction completeness is semantic and not proven by the
  deterministic controller;
- a passing execution receipt does not prove relevance to a criterion;
- external state placement is not tamper protection against same-user shell
  access;
- authenticated interactive waiver creation is not implemented in the plugin
  runtime;
- multi-prompt / resumed-session lifecycle semantics are not part of the first
  candidate;
- Agent Host and Copilot CLI hook behavior may differ;
- no promotion holdout is selected or authorized;
- H1-H4 are not fresh holdouts for this redesign.

A successful smoke therefore advances only **runtime feasibility**, not product
promotion.
