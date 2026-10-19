# P16 — actual VS Code Host RC2 plugin registration without inference

**Corrected finding:** P15's no-turn creating lifecycle was not evidence
of login failure. VS Code deliberately defers session materialization
until the first send; see src/vs/platform/agentHost/node/agentSideEffects.ts
(the _failSessionCreationIfStillCreating comment) and
src/vs/platform/agentHost/node/agentHostStateManager.ts.

**New independent gate:** Publish the actual research root plugin through
AHP session/activeClientSet, matching upstream VS Code Copilot integration
test `copilotMockLlm.integrationTest.ts` for a plugin agent delegating to
a sibling. Check the host's authoritative session customizations container
and EXACT set of eight children before any model turn.

Actual RC2 source has plugin.json and agents/ at repository root;
the VS Code parser supports that Copilot plugin format. A host plugin
registered with 8 names is NOT a working named handback or runtime
permission enforcement. `creating` without a first message is expected.
Test executes on the public repository only and has ZERO Copilot model
request permissions, no account tokens, BYOK, tunnels or private logs.
Output contains role count/boolean and load status but NO paths, token,
source contents or conversation text.

Upstream implementation references:
- https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/test/node/providerIntegration/copilotMockLlm.integrationTest.ts
- https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentPlugins/common/pluginParsers.ts
- https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/common/state/protocol/channels-session/state.ts

**One shot** via docs/P16_HOST_PLUGIN_SENTINEL.md and commit marker
[p16-host-plugin-once]. A plugin PASS would allow designing one bounded
real first-turn Architect test with authenticated GitHub Copilot Host;
without a completed named leaf and returned packet, product value is still
unverified. No stable release or PR merge.

## P16 actual outcome and P17 go gate

First P16 run [#39189065308](https://github.com/YB-Park/over-the-luna/actions/runs/39189065308) published a plain `file:` URI, which the Host interprets as **client-owned**: without a filesystem bridge it stayed `loading`. Upstream `agentPluginManager.ts` explicitly supports `vscode-agent-host-file:` for host-local directories. Corrected [#39189246326](https://github.com/YB-Park/over-the-luna/actions/runs/39189246326) **PASS**: native AHP connected, plugin `loaded`, exactly **8/8** roles and both Main/Architect found. No inference in P16. This warrants exactly one bounded P17 real native delegation turn. It does not by itself prove delegation or effective tools security.
