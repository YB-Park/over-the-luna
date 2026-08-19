# v1.1 artifact-first Reviewer ablation — 2026-08-19

This experiment isolates Reviewer behavior from Main routing and mutation. The exact same already-completed patch was reviewed twice by the current Luna Reviewer and twice by an experimental artifact-first bounded Reviewer.

The reviewed patch came from the earlier `bounded-mutation-boundary` workflow artifact. It passed the visible repository test suite and plugin validation. Both Reviewer variants received the same:

- acceptance criteria;
- visible validation output;
- exact completed diff;
- concrete correctness/compatibility/test rubric.

No Reviewer could mutate or run commands.

## Known oracle

The workflow established two additional facts outside the Reviewer prompt.

### Patch-relevant oracle: cross-trace span-ID collision

A hidden trace with repeated span IDs across two different trace IDs fails the new ownership contract. The reviewed patch indexes parent spans only by `span_id`, so a tool in one trace can resolve through an identically named span from another trace.

This is directly relevant to the new `tool_ownership` feature because the patch extends the existing nearest-agent traversal to tool attribution.

Hidden cross-trace oracle: **FAIL** for the reviewed patch.

### Pre-existing limitation: package-style import

`python -c 'import scripts.analyze_tool_ownership'` also fails on the reviewed patch because the module uses an absolute `from analyze_otel import ...` import.

However, the fixed base revision already used the same absolute import in `scripts/analyze_tool_ownership.py`. Therefore this is a **pre-existing limitation**, not evidence that the reviewed patch broke an established consumer. A Reviewer may reasonably mention it as residual/VERIFY if package import is relevant, but it should not be treated as a demonstrated regression without evidence of such a consumer.

## Results

| Reviewer | Repeat | Repo tools | Input | Output | Cross-trace issue found? | Outcome |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| current | 1 | 0 | 7,593 | 485 | no | PASS |
| current | 2 | 0 | 7,592 | 630 | no | PASS on core behavior + speculative should-fix about re-exported imported names |
| artifact-first | 1 | 0 | 7,810 | 421 | no | PASS |
| artifact-first | 2 | 0 | 7,809 | 398 | no | PASS |

All four exact diff hashes remained unchanged.

## Current Reviewer behavior

The first current-Reviewer run returned a clean PASS and explicitly described nested ownership, orphan/Main fallback, global tool preservation, and legacy JSON compatibility as correct.

The second returned one `should-fix`: because the standalone module previously imported `OP_EXECUTE_TOOL`, `is_main_agent`, and `nearest_agent`, changing those imports removes the names as incidental module attributes and *could* break a hypothetical consumer importing them from `scripts.analyze_tool_ownership`.

No repository evidence established such a consumer or public re-export contract. The concern is therefore at most a compatibility `VERIFY`, not a supported must/should-fix regression.

Neither current Reviewer inspected unchanged helper context. Neither found the cross-trace ownership defect.

## Artifact-first Reviewer behavior

Both artifact-first runs returned PASS with **zero repository reads**.

The candidate was cheaper in output than the current Reviewer in this tiny sample, but input was essentially the same and it did not improve correctness detection.

Its strict bias toward treating the exact patch as self-sufficient suppressed the very read needed to catch the important issue: the changed ownership code calls unchanged `nearest_agent()`, whose parent-index semantics are not fully visible in the diff.

## Falsification

This experiment falsifies a tempting assurance shortcut:

> “Exact diff + validation evidence is enough; a good Reviewer should normally need no repository reads.”

That is too strong.

A patch can be locally readable while its correctness depends on an unchanged helper/parser/import/runtime contract. If the Reviewer never closes that semantic dependency, artifact-first review can produce a confident but incomplete PASS.

The current Reviewer already often behaves artifact-first when the prompt contains the exact patch. Replacing it with a stricter zero-read-biased prompt did not buy meaningful value here.

## Refined assurance concept — artifact-first dependency closure

The next candidate should retain artifact-first evidence **but require a narrow dependency-closure checkpoint before PASS**.

For each changed behavior:

1. inspect the exact patch first;
2. identify unchanged helpers/parsers/serializers/import contracts that the changed code relies on for acceptance-critical semantics;
3. inspect only those concrete definitions/callers needed to close the dependency;
4. do not perform broad repository discovery;
5. return PASS only after those acceptance-critical dependencies are either verified or explicitly marked `VERIFY`.

For the reviewed patch, a correct dependency closure would at minimum inspect the unchanged `nearest_agent()` / span-index semantics because the new tool-ownership feature depends directly on them.

This is different from general repository review: it is **artifact-first, dependency-directed context expansion**.

## Assurance trajectory rule still required

The earlier integrated mutation experiment remains strong evidence that normal `REVIEW` must also have a hard trajectory bound:

- exactly one Reviewer invocation for normal `REVIEW`;
- Main adjudicates findings and repairs accepted issues;
- Main revalidates repairs;
- repairs do **not** automatically trigger another Reviewer;
- a second independent review requires explicit `RISK` escalation with a distinct rubric.

Reviewer evidence selection and Reviewer invocation count are separate controls; v1.1 needs both.

## Next gate

Compare the current artifact-first shape against a **dependency-closure Reviewer** on the same exact patch. Success requires:

- targeted repository reads, not broad browsing;
- repeatable detection of the cross-trace ownership risk or a precise `VERIFY` for the unresolved span-parent contract;
- lower false-positive pressure than broad review;
- bounded token/tool cost;
- no mutation and no second Reviewer.
