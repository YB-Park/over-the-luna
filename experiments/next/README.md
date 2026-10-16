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

## Small one-shot P0b CLI auth gate

GitHub now documents that **personally owned repositories** may use the
short-lived Actions `GITHUB_TOKEN` with `copilot-requests: write` to call
Copilot CLI; usage bills the owner's Copilot seat. No separate stored PAT is
normally required for this route.

`.github/workflows/copilot-one-shot.yml` has two explicit gates:
a change to `experiments/next/ONE_SHOT_RUN.md` **and** a commit message
containing `[run-p0b-luna-once]`. Ordinary pushes, docs changes and CI do
not run this billable workflow.

Each authorized run attempts **one non-interactive GPT-6 Luna user prompt**,
with `--available-tools=view` (no shell/write), `--max-ai-credits=30`
(**CLI minimum accepted: 30 credits = $0.30 soft response limit**, not an absolute billing guarantee), an 8-minute
job timeout and read-only repository permission. The verifier prints only
small categorical evidence, never the raw session transcript.

If auth fails, classify as BLOCKED and check account Copilot seat,
model opt-in and GitHub policy rather than adding more calls. This is a
CLI authentication probe, **not** an Agent Host or plugin-compatibility test.

Official docs:
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/copilot-cli-in-github-actions
- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-in-actions
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

Note: the first smoke attempt failed before inference because the current CLI rejects `--max-ai-credits=2` (minimum 30). This is a **configuration failure, not a Copilot auth/model failure**. The following explicitly triggered run tests the corrected flag.

## Pending runtime gates (not yet run)

1. Confirm Copilot account eligibility and access to GPT-6 Luna, Haiku 5.5, GPT-6.1 Sol, Sonnet 5.5 in the user's actual Copilot Agent Host.
2. Confirm exact configured model/effort of Main and one named read-only subagent from runtime traces. A configured model name is not proof of execution.
3. Confirm a harmless previously enabled MCP/extension tool and check strict leaf boundaries.
4. Record any auth/policy failures as ENVIRONMENT/BLOCKED, never as model quality failure.
5. Only after authorization, run a very small manually triggered, credit-capped paid test. Never add an **unguarded recurring** paid workflow; only deliberate one-shot marker-triggered calls.

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
| P0b CLI authentication + short response | [Success #38836438484](https://github.com/YB-Park/over-the-luna/actions/runs/38836438484) | **PASS auth/response**, model identity NOT independently observed | Check model catalogue; Host still pending |
| P0b four-model SDK catalogue | [Success #38836601586](https://github.com/YB-Park/over-the-luna/actions/runs/38836601586) | **17 models listed**; Luna 6 / Haiku 5.5 / Sonnet 5.5 present; Sol 6.1 absent | Investigate Sol access/visibility, do not infer model weakness |
| P0d Copilot SDK BYOK Sol | [Success #38851012090](https://github.com/YB-Park/over-the-luna/actions/runs/38851012090) | **PASS SDK isolated provider session**, not Host mixing | Agent Host live runtime still required |
| P1a paired review | [Actions #38851868295](https://github.com/YB-Park/over-the-luna/actions/runs/38851868295) | 5/5 all 3 strategies; no benefit from always-on Sol review | Keep optional, move on |
| P1b corrected real edits | [Actions #38852797334](https://github.com/YB-Park/over-the-luna/actions/runs/38852797334) | 2/2 all 4 models; model/tool-policy confound fixed | STOP tiny benchmarks; product dogfood |
| Plugin vs native agent in actual VS Code work | Real work and user acceptance | NOT RUN | Evaluate only during usable product candidate dogfood |
| P2 additional models | Targeted work under actual developer requirements | NOT RUN | Only if quality or risk evidence justifies an escalation |

## Read-only candidate model catalogue

The `catalog` job in the same gated workflow starts the Copilot SDK
and calls `client.listModels()` without creating a model session or sending
a prompt. It is only triggered by `ONE_SHOT_MODEL_CATALOG.md` plus
`[list-copilot-candidates-once]` in the commit message. Presence in the
catalogue is **not** proof that a requested model will execute in a VS Code
Agent Host session. Next, compare the actual Host model and tool traces.

The [first short CLI auth smoke](https://github.com/YB-Park/over-the-luna/actions/runs/38836438484)
succeeded with `--model=gpt-6-luna`, but its exported JSONL lacked an
independent model identifier. Thus authentication is PASS and model identity
remains INCONCLUSIVE. The earlier 2-credit attempt failed before inference
because the Copilot CLI requires a minimum of 30 AI Credits for
`--max-ai-credits`; no account/model conclusion was drawn from that error.

No secrets, raw user tasks, or privileged data belong in this repository's experiment logs.
