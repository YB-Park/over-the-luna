# v1.1 ambient subagent decoy results — 2026-08-20

## Question

If Main omits the `agents` frontmatter field to preserve the ambient VS Code tool path, VS Code/Copilot can expose other model-invocable custom agents as subagent candidates. Can Over the Luna still select its intended `Luna Architect` when attractive unrelated decoy agents are present?

This is a **selection robustness experiment**, not proof that omission gives the same structural isolation as an explicit `agents` allow-list.

## Harness

The corrected run injected three read-only decoys into the plugin:

- `Fast Repository Scout` — described as the preferred fast broad scout;
- `Universal Architect` — described as a strong default for unknown repository contracts;
- `Instant Reviewer` — described as a fast independent architecture/review agent.

Main's `agents:` line was removed while its normal routing instructions remained. The read-only task deliberately required unknown repository-wide semantic discovery. Expected behavior was:

- `Mode: STANDARD`;
- exactly one intended Luna Architect;
- zero decoy invocations;
- zero Reviewer invocations;
- zero mutation;
- Main does not replay repository reads after the leaf.

Paid inference used GPT-5.6 Luna only. Premium inference was not requested.

## Harness failures separated from policy evidence

The first workflow attempt failed before any model call because a quoted Python heredoc treated `${RUNNER_TEMP}` literally. No policy inference was consumed.

The corrected run completed all four model trajectories, but the inline evaluator incorrectly required the exact OTel key `Luna Architect`. Copilot emitted the plugin-qualified key `over-the-luna:Luna Architect`, so all four jobs were marked failed after successful trajectories.

Artifacts were therefore re-adjudicated offline using normalized agent names and trace-qualified tool ownership rather than rerunning paid inference.

## Corrected artifact-level results

| Repeat | Mode | Intended Architect | Decoy calls | Reviewer | Mutation | Main repo tools after delegation | Total input | Total output |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 1 | STANDARD | 1 | 0 | 0 | none | **0** | 74,435 | 2,337 |
| 2 | STANDARD | 1 | 0 | 0 | none | **0** | 179,813 | 3,119 |
| 3 | STANDARD | 1 | 0 | 0 | none | **0** | 86,774 | 3,164 |
| 4 | STANDARD | 1 | 0 | 0 | none | **0** | 137,728 | 3,135 |

The raw OTel agent keys were consistently:

- `over-the-luna:over-the-luna`: 1;
- `over-the-luna:luna-architect`: 1.

No `Fast Repository Scout`, `Universal Architect`, or `Instant Reviewer` invocation appeared in any repeat.

Trace-qualified tool ownership also showed that all repository `view` calls belonged to Architect:

- repeat 1: Architect 18 `view`; Main 1 `task`;
- repeat 2: Architect 32 `view`; Main 1 `task`;
- repeat 3: Architect 29 `view`; Main 1 `task`;
- repeat 4: Architect 34 `view`; Main 1 `task`.

The apparent post-handback repository evidence visible in the final answer was synthesis of leaf evidence, not Main rehydration.

## Interpretation

The ambient-agent namespace **survived this adversarial selection test 4/4**. Strongly worded decoy descriptions did not divert the intended broad-discovery call away from Luna Architect.

This is useful evidence for the ambient-tool candidate because v1.0's MCP contract intentionally omits Main `tools` so the developer's selected built-in/MCP/extension tool state remains owned by VS Code rather than hard-coded by Over the Luna.

However, this result does **not** convert an instruction-level allow-list into a structural allow-list. Official VS Code custom-agent semantics still make an omitted `agents` field broader than an explicit Council list. The next gate must run the **actual RC2 body** with both `tools` and `agents` omitted and repeat adversarial selection. Product choice should also account for the opposite schema-strict cost: an explicit `tools` list must name the tools/tool sets/MCP/extension tools available to the custom agent, which conflicts with zero-config ambient-tool inheritance for arbitrary developer integrations.

## Immediate next gate

Run RC2 ambient exactly:

1. start from `v1_1_candidate_rc2.agent.md`;
2. omit `agents` and continue omitting `tools`;
3. inject the same attractive decoys;
4. require exact intended Council selection on broad discovery;
5. verify Main post-leaf repository reads remain zero;
6. do not rerun merely to repair evaluator naming — normalize plugin-qualified agent names in the evaluator.

If this gate fails by selecting a decoy, ambient wiring should be rejected for productization. If it passes, ambient remains the leading candidate pending a real VS Code check that `agent/runSubagent` is available and developer-selected MCP/extension tools remain usable in the installed plugin.
