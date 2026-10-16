# Next Harness — minimal experiment runbook

Research-only. This directory is **not** an alternative shipped plugin, and it must not create billable Copilot calls automatically.

## First experiment: P0 / model-only static qualification

**Question:** Can the current stable v1.1.1 agent topology be converted into a GPT-6 Luna candidate without inadvertently changing tools, prompts, role structure, or premium boundaries?

**Control:** unmodified `main` v1.1.1 plugin (GPT-5.6 Luna automatic core).  
**Candidate:** same contents except exactly 8 automatic agent frontmatter lines `model: GPT-5.6 Luna` → `model: GPT-6 Luna`.  
**What this proves:** candidate transformation is mechanically isolated.  
**What this does not prove:** GPT-6 is available, better, less costly, or runnable in Agent Host.

This adapts the already-existing **model-only** builder from `research/gpt6-luna-model-qualification` instead of developing another benchmark framework.

Local no-credit commands:

```bash
python -m pip install 'PyYAML==6.0.2'
python scripts/validate_plugin.py
python experiments/next/build_variant.py \
  --source . --verify-pair \
  --control-output /tmp/otl-next-control \
  --candidate-output /tmp/otl-next-luna6
```

The research branch CI runs the same checks on push without calling any LLM. Treat PASS only as a **static gate**.

## Pending runtime gates (not yet run)

1. Confirm Copilot account eligibility and access to GPT-6 Luna, Haiku 5.5, GPT-6.1 Sol, Sonnet 5.5 in the user's actual Copilot Agent Host.
2. Confirm exact configured model/effort of Main and one named read-only subagent from runtime traces. A configured model name is not proof of execution.
3. Confirm a harmless previously enabled MCP/extension tool and check strict leaf boundaries.
4. Record any auth/policy failures as ENVIRONMENT/BLOCKED, never as model quality failure.
5. Only after authorization, run a very small manually triggered, credit-capped paid test. Never add a push-triggered paid workflow.

## Success and stop criteria

- P0 passes only if existing stable validator succeeds and the model-only pair differs by exactly the eight expected model lines.
- P0 failure: fix the builder or platform assumptions; do not edit shipped agents to hide a failure.
- Do not grow the test suite unless it answers a named product decision.
- When the simple approach is adequate, stop testing and ship the simplest proven configuration.
- Use [the product decision charter](../../docs/NEXT_HARNESS.md) for principles, next gates, and decision log.

## Result ledger

| Gate | Evidence | Outcome | Next decision |
| --- | --- | --- | --- |
| P0 model-only static pair | [Actions run #38833915882](https://github.com/YB-Park/over-the-luna/actions/runs/38833915882) | **PASS — static only** | Proceed to separate, manually authorized runtime gate |
| P0b Copilot authentication/policy | Authenticated runtime trace | NOT RUN | User account + permissions needed |
| P1 native vs harness | Real work/hidden task checks | NOT RUN | Require P0b |
| P2 additional models | Specific scoped ablation | NOT RUN | Require P1 weakness to justify |

No secrets, raw user tasks, or privileged data belong in this repository's experiment logs.
