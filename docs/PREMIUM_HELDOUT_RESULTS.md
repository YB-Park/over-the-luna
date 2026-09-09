# Premium Harness Held-Out Results

Protocol: `docs/PREMIUM_HELDOUT_PROTOCOL.md`  
Frozen Premium candidate: `0083f3d81e7339f3b22e3efaa852562d7daa07e5`

## Arm definitions

- A — Current Over the Luna / GPT-5.6 Luna
- B — raw Copilot CLI default agent / GPT-5.6 Terra
- C — frozen Premium Harness / Terra root + Luna workhorse/auditor

## Screening

| Task | Arm | Hidden oracle | AI credits | Wall time | Root/subagents | Repair/replan | Direction/complexity notes |
|---|---|---|---:|---:|---|---:|---|
| H1 redis hiredis close | A | **FAIL — 3/4 corrected behavior oracle** | 5.694290 | 167s | Main Luna + Architect (28 tools / 220k tokens) + Reviewer (3 tools / 10.8k tokens); 59 tool starts total | 1 reviewer-driven repair, no replan | Correctly chose non-destructive MSG_PEEK and repaired unsupported/racy peek exceptions, but the fallback returns readable on SSL-like recv-flags rejection and therefore misses real EOF. Same hidden correctness as Premium at ~39% of its cost. |
| H1 redis hiredis close | B | **PASS — 4/4 corrected behavior oracle** | 71.013030 | 222s | Raw Terra only; no subagents; 66 tool starts | 0 | Different but behaviorally valid intervention: when readiness fires, read into hiredis' persistent parser buffer. EOF becomes the existing ConnectionError while pending RESP3 push remains available to read_response(). ~4.84x Premium cost and ~12.47x OTL cost. |
| H1 redis hiredis close | C | **FAIL — 3/4 corrected behavior oracle** | 14.671259 | 355s | Terra root + Luna Builder (72 tools / 1.618M tokens) + Luna Auditor (30 tools / 305k tokens); 104 tool starts total | 0; Auditor PASS | Builder/Auditor validated MSG_PEEK, peer-close recovery, and pending-push preservation, but both accepted a ValueError/unsupported-flags fallback that treats a real EOF as reusable. ~2.58x OTL cost and ~2.13x OTL wall time without a correctness gain. |
| H2 pytest teardown | A | | | | | | |
| H2 pytest teardown | B | | | | | | |
| H2 pytest teardown | C | | | | | | |
| H3 pytest max warnings | A | | | | | | |
| H3 pytest max warnings | B | | | | | | |
| H3 pytest max warnings | C | | | | | | |
| H4 redis key shape | A | | | | | | |
| H4 redis key shape | B | | | | | | |
| H4 redis key shape | C | | | | | | |

## Repetitions

### H1
No repetition triggered. The corrected hidden failure is deterministic and tied to a concrete intervention choice, not an ambiguous stochastic trajectory. Re-running to search for a lucky alternative would violate the sequential rule.

Other tasks: pending.

## H1 evaluator correction

The first accepted-test injection was implementation-coupled because it imported the accepted helper name `_socket_is_closed`, so it was not used for final scoring.

A subsequent behavior oracle initially contained an SSL-like fake socket without a real `fileno()`. Re-reading the accepted-head check exposed that the accepted Redis patch itself failed that test, while the workflow incorrectly appeared green because `pytest | tee` lacked `pipefail`. That fourth test was therefore invalid and discarded.

Final zero-AI oracle run: GitHub Actions `34352923102`.

The corrected fourth test wraps a **real kernel socket** (real `fileno`/poll/EOF semantics) while making only `recv(..., flags)` behave like an SSL socket by raising `ValueError`. The exact same four behavior tests were run against all frozen arm diffs and the accepted Redis head.

Final oracle:
- accepted Redis head: **4/4 PASS**
- Raw Terra: **4/4 PASS**
- Frozen Premium: **3/4 FAIL**
- Over the Luna: **3/4 FAIL**

This recovery used zero additional AI calls.

## H1 product interpretation

H1 is a **clear negative result for the frozen Premium product**.

Against current Over the Luna:
- Premium did not improve hidden correctness;
- Premium cost ~2.58x more and took ~2.13x wall time;
- Premium used substantially more repository work (104 tool starts; Builder alone used ~1.62M tokens);
- its independent Auditor still returned PASS despite the acceptance-critical SSL-like EOF gap.

Against raw Terra:
- Premium was ~4.84x cheaper, but Raw Terra was the only evaluated arm to satisfy the full corrected hidden oracle;
- Raw Terra also finished faster (222s vs 355s), despite much higher token/credit spend.

Therefore H1 does not place Premium on the desired Pareto frontier. It demonstrates both sides of the product challenge: raw Terra can buy a real correctness edge at extreme cost, while the current Premium decomposition can spend substantially more than OTL without obtaining that edge.

## Interim product decision

After H1 only: **continue held-out screening; do not redesign yet and do not promote.** One held-out task is insufficient for a product conclusion, but H1 is material evidence against the frozen candidate and must remain in the final decision set.
