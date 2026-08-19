# v1.1 broad-scouting isolation matrix — 2026-08-19

This experiment isolates the investigation problem from post-change assurance. The task is read-only; `Assurance: NONE` is appropriate. The question is whether broad disposable repository discovery actually stays out of Main Luna's context.

## Task

Against the released `main` repository, trace every repository contract that would have to change if the automatic core stopped being Luna-only while preserving the current premium human gate. Identify exact files/symbols and relationships across:

- agent model declarations/allowlists;
- validator contracts;
- documentation;
- smoke/release checks;
- premium model boundaries.

No repository mutation was allowed.

Three policies were compared:

1. released v1.0 baseline;
2. split-state assurance candidate;
3. split-state plus a stronger locality checkpoint that says broad discovery should be delegated to Luna Architect before Main accumulates it.

A tool-ownership analyzer attributed each OTel tool call to the nearest Main/leaf agent span.

## Results

| Policy | Route | Main tool work | Architect tool work | Main input | Council input | Total input |
| --- | --- | --- | --- | ---: | ---: | ---: |
| v1.0 baseline | `STANDARD — Luna Architect` | `view 17`, `rg 2`, `task 1` | `view 26` | 110,940 | 52,453 | 163,393 |
| split-state | `STANDARD — Luna Architect | Assurance: NONE` | `view 20`, `glob 1`, `rg 1`, `task 1` | `view 23` | 127,152 | 64,772 | 191,924 |
| split + locality checkpoint | `STANDARD — Luna Architect | Assurance: NONE` | `view 23`, `glob 1`, `rg 3`, `task 1` | `view 28` | 152,714 | 86,128 | 238,842 |

All runs were read-only; the worktree stayed clean.

The route label alone is therefore not a useful success metric. All three runs used Architect, but all three still paid for substantial Main-side repository reading.

## Tool chronology

Chronology exposes two distinct failure modes.

### v1.0 baseline — early delegation, then rehydration

Approximate sequence:

1. Main calls `task` at ~3.4 s.
2. Architect performs 26 `view` calls and returns at ~25.8 s.
3. Main then performs 17 `view` + 2 `rg` calls.

So delegation happened early, but Main substantially reconstructed the broad evidence afterward.

### split-state — discovery first, delegation second

Approximate sequence:

1. Main performs `glob 1`, `rg 1`, and about 20 `view` calls during the first ~11 s.
2. Only then does Main call Architect at ~16.9 s.
3. Architect performs another 23 `view` calls.
4. Main does not materially re-read after the leaf returns.

This is the clearest bad shape: the broad context was already consumed by Main before the isolation call. Architect then duplicated work rather than protecting context.

### split + locality checkpoint — delegation timing fixed, rehydration remains

Approximate sequence:

1. Main performs only a small orientation pass (`glob 1`, `rg 1`, `view 1`).
2. Main calls Architect at ~6.4 s.
3. Architect performs 28 `view` calls and returns at ~28.1 s.
4. Main then performs another 23 `view` + 2 `rg` calls.

The stronger locality checkpoint therefore appears to improve **when** delegation occurs but not what happens **after** the leaf returns.

## Interpretation

Two independent routing concerns now need explicit design treatment:

### 1. Delegation timing

When the task requires broad repository mapping, Main should isolate the discovery **before** consuming its details. The locality-checkpoint candidate improved this behavior in one run.

### 2. Post-leaf rehydration

A successful broad leaf call is not useful if Main immediately re-opens the same repository surfaces to regain confidence. Context isolation requires a handback contract strong enough that Main can continue from the leaf's compact evidence packet.

This suggests a stronger design concept than merely “use Architect earlier”:

> **Leaf evidence should cross a deliberate context boundary. Main should verify only unresolved or mutation-critical points, not replay the broad investigation.**

For read-only repository-mapping tasks, the default after a sufficient Architect packet should be to synthesize directly without further broad repository tools.

For mutation tasks, Main should read the concrete mutation targets and immediately adjacent implementation context, not reconstruct all discovery that led to those targets.

## Important falsification

This experiment falsifies two tempting v1.1 shortcuts:

- “reduce SIMPLE by encouraging more STANDARD” — all three runs were STANDARD and still differed materially in context economics;
- “call Architect more often” — Architect invocation alone can increase total inference when Main duplicates the same search/read work.

The target behavior is **epistemic ownership**, not agent count or mode label.

## Next candidate

Test a stronger **evidence-packet / tool-closed handback** contract:

- Architect returns compact exact file/symbol evidence, invariant relationships, unresolved items, and concrete mutation targets when relevant;
- after handback, Main does not re-open already-covered broad evidence merely for confirmation;
- Main repository reads after Architect are reserved for unresolved items and concrete mutation-local context;
- read-only broad mapping should normally require no post-leaf repository reads.

Measure pre-leaf and post-leaf Main tool calls separately, not just total calls.
