# Dogfood 01 — Native Copilot Agent vs Over the Luna Next

**Status: READY FOR LOCAL EXECUTION, NOT YET EXECUTED**

2026-10-16 user report: the Next agent was visible in the picker and its
first read-only repository exploration showed **no notable anomalies**.
This is a *user-reported smoke observation*, not an independently
archived Host tool trace, nor a code-edit validation.

## Real repository improvement to compare

Our independent audit found a dangerous mismatch between the human
belief that `tools: []` means no tools and the Host path where this can
become an unrestricted `null`. The research plugin's own
`scripts/validate_candidate.py` protects against such declarations,
but has no isolated, deterministic negative regression tests.

**Task:** make the Next candidate's static validator testable against
a temporary plugin root, then prove that it rejects unsafe mutations.
This changes real safety-focused project tooling, not a toy benchmark.

**Acceptance criteria, fixed BEFORE running either agent:**

1. Existing command `python scripts/validate_candidate.py` still
   succeeds on the unchanged research candidate.
2. Add an optional `--root PATH` CLI argument so the validator can
   inspect a temporary copied candidate directory. Default remains the
   current `experiments/next/candidate-plugin`.
3. Add `tests/test_validate_candidate.py` using Python standard-library
   `unittest` and temporary candidate copies, with no model API calls.
   Test a valid copied candidate PASS and at least these distinct FAILs:
   - injected `tools: []` in the main agent;
   - injected `model:` pinning a model;
   - an additional `*.agent.md` leaf;
   - an invalid/missing manifest;
   - a bundled `.mcp.json` or `mcp.json`.
4. Run `python -m unittest discover -s tests -p 'test_validate_candidate.py'`
   and `python scripts/validate_candidate.py`. Include the real command
   exit status and number of tests, not just a claimed PASS.
5. Don't change the production/root `plugin.json`, existing v1.1.1
   `agents/`, the Next candidate plugin files, or policy/permissions.
   Intended code changes are `scripts/validate_candidate.py` and
   `tests/test_validate_candidate.py` only. No Git commit, push or PR
   is requested from either agent.

The candidate may improve or simplify the architecture of the validator
internally. Acceptance is **behavior-based**, and final diffs must be
reviewed for unintended changes. Do not supply a ready-made patch or
the other agent's output to either run.

## Frozen baseline

Once this task document is committed, use the **exact commit SHA** of
this task document as the starting point for both local worktrees.
Do not start one arm on a newer SHA than the other.
At time of task drafting the prior research HEAD was
`1375d0ee351bbd2e18f14d3ffd4431519a9aafa3`;
the commit adding this document becomes the real trial baseline.

## Local paired execution

In a disposable parent folder next to your existing clone, run from the
original repository:

```bash
git fetch origin research/next-harness-foundation
git worktree add --detach ../otl-native <TRIAL_BASELINE_COMMIT_SHA>
git worktree add --detach ../otl-next <TRIAL_BASELINE_COMMIT_SHA>
```

Open the two worktrees in **two separate VS Code windows/chats**.
Use the same **GPT-6 Luna model, reasoning effort, Host tools, MCP,
workspace trust and approvals** for both. Do not expose one arm's
outputs or working tree as the other arm's input.

- **Native arm:** VS Code built-in Agent, workspace `otl-native`.
- **Next arm:** `Over the Luna Next (Research)`, workspace `otl-next`.

Send the exact same task text below to each arm **as the first chat
message in a fresh chat**. The trial baseline contains this document
so both arms can inspect it if needed, but the task text itself is
sufficient.

### Exact prompt for BOTH agents

> Improve the actual research candidate validator `scripts/validate_candidate.py`.
> The current validator only checks a fixed in-repo plugin directory;
> add optional CLI `--root PATH` that validates a passed plugin directory
> while keeping the original default command working.
>
> Add standard-library unittest coverage in
> `tests/test_validate_candidate.py` using temporary copies of
> `experiments/next/candidate-plugin/`. Assert that a pristine copy
> passes and deliberate mutations are rejected: `tools: []` or a pinned
> `model:` in the Main frontmatter; a second `*.agent.md` leaf;
> missing/invalid `plugin.json`; and a bundled `.mcp.json` (or
> `mcp.json`). The validator must return a failing exit code for those
> broken candidates.
>
> Only modify `scripts/validate_candidate.py` and
> `tests/test_validate_candidate.py`; do not modify the actual candidate
> plugin, v1.1.1 code or any secrets. Do not commit or push.
>
> Execute `python -m unittest discover -s tests -p 'test_validate_candidate.py'`
> and `python scripts/validate_candidate.py`. Check the final diff and
> report actual exit statuses, tests run, changed paths and any remaining
> uncertainty. Avoid unrelated improvements or subagent calls unless
> genuinely needed.

### Outside-agent independent verification

After each run, in that worktree inspect:

```bash
python -m unittest discover -s tests -p 'test_validate_candidate.py'
python scripts/validate_candidate.py
python scripts/validate_candidate.py --root experiments/next/candidate-plugin
git diff --check
git status --short
git diff -- scripts/validate_candidate.py
```

Also inspect the newly created untracked test file (plain `git diff`
will not show untracked files). Don't auto-commit either arm.

## Record objectively

| Evidence | Native | Next |
| --- | --- | --- |
| Exact repo starting SHA | TBD | TBD |
| Model / effort / actual tools | TBD | TBD |
| Valid default / explicit `--root` | TBD | TBD |
| Negative mutation tests run + pass | TBD | TBD |
| Scope / diff / malformed tests | TBD | TBD |
| Error/retry/manual corrections | TBD | TBD |
| Elapsed time | TBD | TBD |
| Copilot credits consumed / UNKNOWN | TBD | TBD |
| Outcome + subjective friction | TBD | TBD |

Decide `KEEP / SIMPLIFY / REJECT / UNKNOWN` from **actual result and
attention/cost**. A single paired task does not prove statistical superiority.
If both arms perform equally well, that's information—not a reason to
generate more benchmark variants.

**Neither arm is authorized to publish changes.** The user or project owner
may later adopt a chosen patch separately after review.
