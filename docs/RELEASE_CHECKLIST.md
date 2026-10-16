# Over the Luna Next — RC release gate

**Candidate:** `v2.0.0-rc.1`. **Not yet stable.**

## Static gate (automated, free)
- [ ] Distinct `over-the-luna-next` manifest with exactly one Main and expected version.
- [ ] No pinned model, forced `tools: []`, hidden Council, hooks, skills, MCP server or bundled credentials.
- [ ] Regression tests reject injected agent files, bad frontmatter, missing/invalid manifest and forbidden extensions.
- [ ] Release ZIP is SHA-256 reproducible, uses an allowlist and passes validation after extraction.
- [ ] English/Korean installation, upgrade caveats and one-step rollback are documented.
- [ ] Exact RC commit's GitHub Actions job passes without any paid model calls.

## Product gate (not automatic)
- [x] The *research* plugin package was loaded/selected and executed in Copilot SDK: [P3 evidence](https://github.com/YB-Park/over-the-luna/actions/runs/38860678994).
- [x] SDK actual Next and SDK default each passed one independently graded public coding task: [P4 evidence](https://github.com/YB-Park/over-the-luna/actions/runs/38860917956). **No unique Next quality advantage established.**
- [x] User reports research Next appears in corporate VS Code and initial read-only use had no issues. No internal logs were exported.
- [ ] **This root-packaged RC** itself has not been installed in the user's corporate Host; Host tool permission/approval semantics remain partially unverified.
- [ ] No proven cost advantage or quality improvement over native VS Code Copilot Agent; user value remains an explicit stable-release decision.

## Promotion decision
Distribute only as **opt-in RC** after CI PASS. Stable tag/main merge needs explicit review and a convincing user-value/rollback rationale. Never merge the entire experimental research PR #18 as a substitute for this clean package. No repeated corporate testing, internal data export or automatic Sol review. If native Copilot is just as good, simplify or stop instead of adding compulsory agents.

**Rollback:** disable the RC `chat.pluginLocations` entry and choose stable Over the Luna or native Agent. Stable `main` must remain intact until separately approved.
