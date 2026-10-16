# Over the Luna Next 🌙 — v2.0.0-rc.1

**English** · [한국어](README.ko.md)

> One Main. Real verification. Additional judgment only when it earns its place.

**Release candidate, not stable.** One visible **Over the Luna Next** Agent. No mandatory Council, Premium Review, forced router, API bridge, provider keys, MCP/hook/skill bundles or paid-model automation. The **VS Code Host** chooses the model, tools, approvals and workspace permissions.

## Install beside stable v1.1.1

The default repository branch `main` is still the **stable v1.1.1**. Do not install the default GitHub URL and assume it points to Next.

1. From the passing [release-candidate CI](https://github.com/YB-Park/over-the-luna/actions/workflows/validate.yml?query=branch%3Arelease%2Fnext-v2.0.0-rc1), download the `over-the-luna-next-v2.0.0-rc.1` artifact and extract the inner ZIP into a local directory. Or check out branch `release/next-v2.0.0-rc1` separately and use its root as the plugin directory.
2. In VS Code **User** settings, keep existing settings and add your extracted folder's absolute path to `chat.pluginLocations`. Ensure `chat.plugins.enabled` is allowed by company policy:

   ```json
   {"chat.pluginLocations": {"/ABSOLUTE/PATH/over-the-luna-next-rc": true}}
   ```

3. Disable the earlier *research* `over-the-luna-next` plugin location during this RC trial, so duplicate plugin IDs don't collide. **Do not remove stable v1.1.1.**
4. Reload VS Code if necessary, choose **Over the Luna Next**, and select the model directly in the Host. GPT-6 Luna is a sensible starting hypothesis, **not pinned**.

## Safe use and rollback

Clear changes proceed directly; verify meaningful changes using real diffs and tests, not only LLM claims. Important auth, concurrency, data-integrity and public-contract risks may justify host-native independent scrutiny. **Prompts are not security sandboxes**. Effective read/write rights and MCP policies remain host-owned. This RC never automatically calls Sol, other external providers or extra subagents.

Breaking change: the previous v1.1.1 Council, forced Reviewer, Premium UI and routing contracts **are intentionally removed**. Existing users dependent on those workflows should remain on stable.

**Rollback:** disable the RC entry in `chat.pluginLocations`, then select the unchanged stable **Over the Luna** or native Copilot Agent. No corporate artifacts/logs need to leave the company environment.

## Evidence and readiness

The [research branch](https://github.com/YB-Park/over-the-luna/tree/research/next-harness-foundation) and [research Draft PR #18](https://github.com/YB-Park/over-the-luna/pull/18) contain bounded SDK studies and an independent audit. The SDK successfully loaded the actual research Next package, but **no general improvement over native VS Code Copilot in accuracy or cost is proven**, and this separately packaged RC hasn't yet been installed in the user's company Host. [Release checklist](docs/RELEASE_CHECKLIST.md).

**CI is static and packaging only: zero paid model requests.**
