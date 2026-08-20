# v1.1 external integrated candidate replication — 2026-08-19

This experiment moves the integrated candidate outside the Over the Luna repository and its self-hosted analyzer task.

Each GitHub Actions job generated a fresh standalone Python repository containing a small `TTLCache`, baseline unit tests, and no Over the Luna research history. The same integrated candidate was run twice:

- Main: `v1_1_candidate_integrated.agent.md`;
- Reviewer: `v1_1_candidate_invariant_reviewer.agent.md`;
- Architect available but not forced.

Task:

- updating an existing key refreshes value, expiry, and MRU without evicting another live key at capacity;
- expired entries are purged before any capacity eviction;
- any remaining live eviction chooses exactly the live LRU entry;
- preserve `get` and the public constructor/API;
- add focused regressions.

The baseline `set()` intentionally evicted the LRU before distinguishing update from insertion and did not purge expired entries before capacity eviction.

## Runtime results

| Metric | Repeat 1 | Repeat 2 |
| --- | ---: | ---: |
| Route | SIMPLE + REVIEW | SIMPLE + REVIEW |
| Architect invocations | 0 | 0 |
| Reviewer invocations | **1** | **1** |
| Visible final tests | 6 pass | 6 pass |
| Total input | 202,919 | 172,717 |
| Total output | 5,195 | 4,053 |
| Main input | 193,588 | 163,389 |
| Reviewer input | 9,331 | 9,328 |
| Reviewer views | 3 | 4 |
| Main mutation owner | yes | yes |

The candidate correctly kept the investigation route SIMPLE because the implementation neighborhood was local and explicit. This is an important complement to the STANDARD/Architect experiments: v1.1 does not need to inflate Council usage merely to use more Luna compute.

## Reviewer precision

### Repeat 1 — PASS

The Reviewer inspected the changed cache/tests and returned PASS. Its invariant challenge was directly relevant:

> OrderedDict order remains the LRU/MRU ordering across get, update, and insertion paths.

It found no unsupported must-fix issue. The final patch already covered update-at-capacity, expiry refresh, expired purging, and live LRU behavior.

### Repeat 2 — useful SHOULD-FIX

The Reviewer found a concrete test-quality problem rather than inventing an implementation bug:

> the update-at-capacity regression called `get("a")` before the later insertion, which itself promotes `a` to MRU; therefore the test did not isolate whether `set()` performed the required MRU refresh.

Main accepted the finding, strengthened the regression so the subsequent insertion itself proves the updated key is MRU, and revalidated. Reviewer invocation count remained one.

This is a useful precision signal: the invariant-challenge rule can return PASS or a narrow supported coverage finding on unfamiliar code rather than always manufacturing an adversarial defect.

## Hidden-oracle harness error and correction

The workflow's original hidden step wrote `hidden_cache.py` under `${RUNNER_TEMP}` and executed it from the fixture directory. Python therefore placed the script directory — not the fixture — on `sys.path`, causing:

`ModuleNotFoundError: No module named 'ttlcache'`

Both workflow `hidden-tests.exit` values were therefore 1 for a **test harness import error**, not a candidate behavior failure.

The paid Copilot runs were not repeated. Instead, the exact generated baseline fixture was recreated locally and each uploaded `candidate.diff` artifact was applied unchanged with `git apply`.

The corrected hidden oracle was also strengthened so update-at-capacity updates the current MRU key; this guarantees the buggy baseline evicts the *other* live key and therefore genuinely falsifies the baseline.

Corrected oracle results:

| Artifact | Corrected hidden oracle |
| --- | --- |
| untouched baseline | **FAIL** — update at capacity evicts another live key |
| repeat 1 exact patch | **PASS** |
| repeat 2 exact patch | **PASS** |

The hidden oracle also checks:

- refreshed expiry survives beyond the original expiry;
- an expired entry is removed before a still-live neighbor is evicted;
- with no expired slot, exactly the live LRU is evicted.

## Patch behavior

Both patches implemented the required semantics while preserving the public API.

Repeat 1 used an explicit early update return, then purged expired entries before insertion capacity handling.

Repeat 2 kept one common write path but gated purge/eviction behind `key not in self._entries`, then refreshed the key and moved it to MRU.

Both shapes pass the strengthened hidden behavior contract.

## Evidence-based interpretation

This external replication strengthens three parts of the integrated candidate:

1. **Investigation state remains precise.** Local work stayed SIMPLE; no Architect was purchased merely because v1.1 has an evidence-boundary mechanism.
2. **One-review assurance adheres.** Both non-trivial mutations invoked exactly one Reviewer and stopped there, including the run where Main accepted a finding and changed the patch afterward.
3. **Invariant challenge did not collapse into generic skepticism.** One Reviewer passed a correct patch; the other found a specific MRU test contamination issue that Main could verify and repair.

Together with the self-hosted integrated replication, the automated evidence now supports the integrated policy as the leading v1.1 Luna-core design candidate.

## Automated-core decision point

The automated research gates now support promoting these ideas from open hypotheses to the **leading design candidate**:

- `SIMPLE / STANDARD / DEEP` remains the investigation vocabulary;
- `NONE / REVIEW / RISK` is a separate first-class assurance state;
- broad disposable discovery is delegated early to Architect when justified;
- Architect returns a compact evidence packet and Main does not replay that broad discovery;
- Main remains the sole mutation owner;
- normal REVIEW uses exactly one artifact-first dependency/invariant Reviewer;
- Main adjudicates and revalidates accepted repairs without automatic re-review;
- additional review belongs only to explicit, distinct `RISK` assurance.

The next gates are no longer more Copilot-CLI routing micro-tuning. They are product/runtime gates:

- actual VS Code integration/manual checks for handoff rendering, selected-tool inheritance, and interactive runtime semantics;
- premium UX decision (single premium affordance vs current two-choice Sonnet/Opus baseline);
- only then convert the research notebook into the v1.1 release design contract and versioned product changes.
