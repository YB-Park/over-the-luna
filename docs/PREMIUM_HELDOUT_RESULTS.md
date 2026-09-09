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
| H1 redis hiredis close | A | | | | | | |
| H1 redis hiredis close | B | | | | | | |
| H1 redis hiredis close | C | | | | | | |
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

Add only when the sequential repetition rule triggers.

## Interim product decision

Pending.
