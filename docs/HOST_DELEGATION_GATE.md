# Over the Luna Next — real Copilot Agent Host delegation gate

**Product decision gate; not a synthetic model benchmark.** No company files, chat transcripts, logs, credentials or model spend details must be exported outside the user's organization. The owner's company VS Code remains their everyday working environment, not a test-data supplier.

## Why a Host gate exists

- [P5 code task](https://github.com/YB-Park/over-the-luna/actions/runs/38869234496) produced valid fixes in both SDK arms. The plugin arm attempted `task` twice but no leaf completed.
- [One-shot causal diagnostic](https://github.com/YB-Park/over-the-luna/actions/runs/38870191856) resolved the exact qualified `over-the-luna-next:next-architect` identity and model, then reported `Standalone server does not support session effect 'custom_agent_prompt'`.
- [VS Code custom-agent docs](https://code.visualstudio.com/docs/agent-customization/custom-agents) state that `user-invocable: false` hides a selectable agent while `disable-model-invocation` controls availability for other agents. [Copilot harness subagent docs](https://code.visualstudio.com/docs/agents/run/subagents) describe a harness-native delegation path, distinct from the **Local** harness's `agent/runSubagent`.
- The [VS Code SDK conversion path](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/copilot/copilotPluginConverters.ts) passes plugin agent prompts/models/non-empty tool lists into SDK. This does not prove effective Host approvals and does not make `agents: []` a guaranteed recursion sandbox.

## Historical P14/P15 observations (superseded by corrected P16/P17 gate below)

This gate is now grounded in a **real VS Code Agent Host process**, not only
the standalone Copilot SDK. The independent official CLI was launched
inside isolated public GitHub Actions runners with AHP over an authenticated
localhost endpoint; no chat turns or model inference occurred.

| Evidence gate | Observed result | Relevance |
| --- | --- | --- |
| H0 Host startup and AHP transport | **PASS** — [P14 #39186857999](https://github.com/YB-Park/over-the-luna/actions/runs/39186857999), negotiated AHP 1.0.0 | Actual Host, not standalone SDK |
| H1 Copilot backend advertised | **PASS** — native provider ID `copilotcli`, confirmed in VS Code source and P15 runtime | Provider is registered, not necessarily authenticated |
| H2 Native Copilot session create + subscribe | **PASS** — [P15 #39187067070](https://github.com/YB-Park/over-the-luna/actions/runs/39187067070) | Creation request accepted, separate lifecycle remains pending |
| H3 No-turn ready state | **NOT APPLICABLE** — P15 remained provisionally `creating` because first send had not occurred | This is not an auth or session failure |
| H4 RC2 plugin loaded and named Architect returned packet | **UNVERIFIED** | No Council performance claim |
| H5 Reviewer independently checked a real patch | **UNVERIFIED** | No completeness claim |

The VS Code Copilot backend [advertises protected resources](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/copilot/copilotAgent.ts);
its GitHub Copilot resource requests a
[user-authenticated GitHub authorization scope](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/common/githubEndpoints.ts).
An Actions job token with `copilot-requests: write` is **not proven
interchangeable** with an actual signed-in Copilot session. P15 did not
capture a diagnostic proving whether authorization, SDK initialization,
or another blocker held the session at `creating`; do not guess.

**Next justified experiment is NOT another Main-vs-Luna baseline.** A genuine first-turn Host observation, not no-turn session readiness,
is required before declaring named Architect execution; later use a consequential genuine patch for Reviewer. Do not
attempt a token relay, alternate provider, or repeated paid standalone SDK
calls to bypass an unresolved authentication boundary. No corporate
workspace exports or repeated local tests are required.

## Corrected first-turn materialization contract — P16/P17

**P15 was not a valid readiness gate.** Current VS Code implements
**provisional/lazy sessions**: a session with no first message can
legitimately remain at \`creating\` until SDK materialization happens on
the first \`sendMessage\`. This is explicit in
[AgentSideEffects](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/agentSideEffects.ts)
and [AgentHostStateManager](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/node/agentHostStateManager.ts).
P15's repeated \`creating\` **does not establish an authentication problem**.
We did not observe an auth failure there; previous speculation should
not be used as the product stop condition.

The relevant real Host stages are now:

| Gate | Observed evidence | Meaning |
| --- | --- | --- |
| H0 Official Host AHP transport | P14 AHP \`1.0.0\` PASS | Real process |
| H1 Copilot provider session accepted | P15 \`copilotcli\`, create+subscribe PASS | Provisional, not materialized |
| H2 RC2 plugin loaded by Host | [P16 #39189246326](https://github.com/YB-Park/over-the-luna/actions/runs/39189246326) **loaded; 8/8 exact roles** | Native plugin and Architect present |
| H3 First public turn submitted | [P17 #39189500097](https://github.com/YB-Park/over-the-luna/actions/runs/39189500097) PASS | Selected Next Main with requested Luna model, one turn |
| H4 Turn executed normally | **NOT VERIFIED**: P17 emitted \`chat/error\` | Host error occurred, no established root cause |
| H5 Named Architect invocation | **NOT VERIFIED**: \`task\` starts **0**, completions **0** | No claimed Council handback |
| H6 Reviewer on actual patch | **NOT VERIFIED** | Keep draft; no release |

One important protocol integration discovery: plain \`file:\` plugin
sources are **client-owned** and require a client filesystem bridge.
P16 first run [#39189065308](https://github.com/YB-Park/over-the-luna/actions/runs/39189065308)
stayed \`loading\`; VS Code's
[host-file scheme](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/common/agentPluginManager.ts)
\`vscode-agent-host-file:\` resolved that in the same public runner.
P16 then loaded all eight agents before any inference.

**P17 is a real native AHP first-turn attempt**, not a fake SDK
subagent test. It requested GPT-6 Luna once, but \`chat/error\` came before
any named task started. No use of premium models; actual charged
tokens/price are **unknown** without meter data. Neither P17 nor the
earlier P15 logs prove an auth or a model-selection root cause.
The probe was subsequently hardened to record **coarse error class only**
(no raw message or credential), for a future legitimately authorized
Host opportunity; this change was **not** tested by a second paid run.

**Next valuable gate:** obtain a genuinely functional authenticated Host
turn with approved user/provider policy, then see the named task and
returned source packet. Do not burn credits on the same unsupported SDK
path, assume an Actions job token equals an authorized user, bypass
enterprise settings, or ask for private workspace exports. The real
Host plugin integration already passed; no more Main-only benchmarks.


## P18 actual Host model catalog — absence is a stop condition

[P18 real Host #39197886981](https://github.com/YB-Park/over-the-luna/actions/runs/39197886981)
reused an isolated public GitHub Actions host and the official
job-scoped Copilot permission, without **any** chat/model turns.
AHP 1.0.0, provider `copilotcli` **PASS**. Over the bounded root
observation, the provider advertised **0 model entries**, including no
`gpt-6-luna` and no `auto`; it advertised **2 protected resource
entries**. Those are metadata counts, not a credential/auth error or a
model-billing measurement.

**Correct inference:** P17 selected `gpt-6-luna` without first
verifying the Host-advertised available model catalog. P17 `chat/error`
is compatible with absent model authorization/catalog, but its exact
cause remains **UNKNOWN**. A model available to a signed-in user's VS
Code picker does not imply availability to an ephemeral Actions job
token. Zero models at this point in this runner is not proof that Copilot
is broken, that Luna is unsupported globally, or that credentials must
be exported. Another blind paid P17 retry would not answer the routing
question.

**Fail-closed test gate implemented:** the native Architect trial
now reads the actual root `AgentInfo.models` catalog again before the
first turn. When the exact `gpt-6-luna` model is absent or disabled,
record `BLOCKED_MODEL_NOT_ADVERTISED` and submit **zero turns**.
On a future authenticated Host where it is advertised, a completed
named `task` and a source-grounded **tool return** (not Main's prose)
are both required before calling it a real handback. The AHP
`chat/toolCallReady.toolInput` field now carries the named-agent
selection proof, per upstream protocol. These guards are tested offline
and **were not used to replay a paid model turn**.

## Acceptance flow: Main → Architect → Main

For this narrow read-only check, Main requests one Architect observation, Architect returns the packet, and Main assesses it. Reviewer is excluded until a real diff exists.

## Optional single check, only with PUBLIC repository content

This is a **single optional read-only check**, not an expectation of repeated local trials. When the owner already has a public copy of `YB-Park/over-the-luna` in VS Code, select the **Copilot** Agent Host (not Local) and **Over the Luna Next** from the RC2 research plugin. Use the currently selected Luna model; don't alter company permission, MCP, provider or account settings.

Paste this one request in a fresh session; do **not** send any sensitive corporate context:

> This is a read-only check of the public over-the-luna repository. Use the **named Next Architect** subagent once to examine the real relationship between `scripts/validate_release.py`, `scripts/package_release.py` and their release ZIP allowlist. Ask it to return **DECISION, EVIDENCE, RELATIONSHIPS, WORK_SET, UNCERTAINTIES** with exact public file paths/symbols. As Main, report the returned Architect packet separately from your own assessment. Do not modify files, use other subagents, deploy, push, or access other workspaces. If the delegation tool reports `custom_agent_prompt`, permission or name errors, quote the category only and report `INCONCLUSIVE` rather than claiming Architect was used.

### Local-only pass criteria

PASS (Host path only): the named **Next Architect** was actually invoked and completed; Main cites the *returned* source-specific packet, not merely a prompt mentioning the role. FAIL: observed task failure or blocked policy. INCONCLUSIVE: no trustworthy role completion evidence. Note that even PASS would not prove effective read-only permissions or different-model independence.

**DO NOT EXPORT** company code, complete transcripts, file diffs, approval logs, screenshots containing internal material, BYOK metadata, or model secrets. If the user chooses to share a result externally, the safest optional feedback is only **`HOST_ARCHITECT_PASS`**, **`HOST_ARCHITECT_BLOCKED`**, or **`HOST_ARCHITECT_UNKNOWN`**. It is okay to share nothing.

Reviewer is intentionally NOT part of this quick check: a meaningful Reviewer needs a *real* before/after diff and test outcomes. Verify that naturally on a future approved public task, not by inventing a patch merely to satisfy a gate.

## Release implications and stop rule

A successful standalone SDK registry plus a failed standalone `custom_agent_prompt` call is **not proof of a broken VS Code Host**. Conversely, a picker-visible RC2 role does not establish completed delegation. Keep RC2 opt-in and PR draft until actual Host-native collaboration is observed. No re-running the same paid GitHub Actions probe, no unapproved provider relay, and no corporate artifact transfer. If company policy blocks a reliable Host gate, classify `INCONCLUSIVE`; preserve stable v1.1.1.
