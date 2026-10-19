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
