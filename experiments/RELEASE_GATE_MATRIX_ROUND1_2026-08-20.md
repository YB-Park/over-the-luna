# v1.1 release-gate matrix — round 1 (2026-08-20)

This matrix tests the integrated candidate against four deliberately different product boundaries. It is not a success-rate benchmark; each case has a different expected routing/assurance shape.

## Product criterion

The v1.1 goal remains: spend cheap Luna inference only where it buys context isolation or independent engineering value. Do not increase agent count for its own sake. Main remains the sole mutation owner and premium inference remains human-selected.

## Cases and expected boundaries

| Case | Expected investigation | Expected assurance | Main purpose |
| --- | --- | --- | --- |
| tiny | SIMPLE | NONE | prove mechanical work stays cheap and reviewer-free |
| local | SIMPLE | REVIEW | prove local behavioral work gets one fresh review without planning ceremony |
| broad | STANDARD + Architect | REVIEW | prove broad disposable discovery is isolated and not replayed in Main |
| risk | bounded investigation | RISK | prove concurrency/idempotency work is explicitly recognized as consequential |

All four runs used the same integrated candidate, GPT-5.6 Luna only, no premium model, Main-only mutation, OTel content capture disabled, and a temporary one-shot workflow.

## Results

### tiny — correctness PASS, routing FAIL

- route: `Mode: SIMPLE — direct Luna | Assurance: REVIEW`;
- hidden behavior: PASS;
- Reviewer calls: **1** (expected 0);
- Reviewer tool calls: **13 views**;
- Reviewer input/output: 21,882 / 1,393 tokens;
- the Reviewer attempted to reconstruct the patch by reading repository directories and `.git` internals, including `.git/HEAD`, logs, refs, objects, and index.

The implementation itself was the exact two-line mechanical change requested: change `DEFAULT_PAGE_SIZE` 50 -> 64 and update the existing exact test.

**Interpretation:** the candidate's NONE threshold is too weak. A tiny mechanically validated scalar/default change still anchored as REVIEW, violating the goal that trivial work remain cheap and non-bureaucratic.

This also exposed an evidence-packet problem: Main told Reviewer to inspect the current diff instead of actually supplying the diff. Because Reviewer has only read/search tools, it tried to reverse-engineer the uncommitted patch from `.git`, exceeding its intended read budget.

### local — PASS

- route: `SIMPLE + REVIEW`;
- Architect: 0;
- Reviewer: 1;
- hidden behavior: PASS;
- Reviewer views: 3;
- patch correctly routes `update_headers` through the established request-ID normalizer and adds focused validation coverage.

This is the desired `SIMPLE + REVIEW` shape: no investigative ceremony, one bounded independent assurance pass, Main-only mutation.

### broad — correctness/routing mostly PASS, handback boundary FAIL

- route: `STANDARD — Luna Architect | Assurance: REVIEW`;
- Architect: 1;
- Reviewer: 1;
- hidden behavior: PASS;
- Architect views: 14;
- Main views after Architect: 4 concrete files;
- Main did not use `rg`/`glob` after Architect.

However, immediately after Architect handback Main ran:

`find . -maxdepth 3 -type f | sort`

That is repository-wide discovery through `bash`. It bypasses the current wording, which closes read/search replay but does not explicitly close shell-based broad inventory.

**Interpretation:** epistemic ownership must close *discovery behavior*, not only named read/search tools. After Architect, broad `find`, recursive `ls`, `git grep`, `git ls-files`, etc. must be treated as boundary rehydration unless a specific missing fact is declared.

### risk — PASS

- route: `Mode: STANDARD — Luna Architect | Assurance: RISK`;
- Architect: 1;
- Reviewer: 1;
- hidden concurrency/idempotency oracle: PASS;
- Reviewer found a real determinism/overlap weakness in the first concurrency regression test;
- Main accepted the finding, repaired the test, revalidated, and did not recursively buy another Reviewer.

The final implementation uses a lock-map guard plus per-key lock, preserving parallelism across distinct keys and leaving failed charges uncached.

This is good evidence that first-class RISK is reachable and that one strong invariant-aware review can add value without forcing two reviews merely because RISK permits them.

## Round-1 verdict

The integrated candidate is **not yet productization-ready** because two release-boundary properties failed:

1. tiny mechanical mutation did not stay `NONE`;
2. Architect handback could be bypassed through shell-based broad discovery.

A third structural weakness was exposed even though it did not break the local/broad/risk cases:

3. Main does not reliably hand Reviewer a concrete patch artifact. Reviewer must never be asked to reconstruct an uncommitted diff from repository metadata.

## Required refinement before round 2

1. Add an explicit semantic NONE checklist. A scalar/default/text/mechanical change with no control-flow, validation, identity, data-shape, security, concurrency, persistence, or public-contract consequence and an exact mechanical test should be NONE.
2. Close Architect handback across all repository-discovery mechanisms, including shell-based inventory/search.
3. Require Main to supply Reviewer a concrete diff/hunk artifact plus validation evidence. If no artifact is supplied, Reviewer should return `VERIFY: completed patch artifact missing` rather than inspect `.git` or remap the repository.
4. Make Reviewer read budget a hard stop and prohibit `.git`/directory inventory for patch reconstruction.
5. Re-run the **same four fixtures** so round 2 is a direct policy comparison rather than a new-task anecdote.
