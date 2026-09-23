# Premium v2.1 — Pre-Live Code Freeze

Status: **PRE-LIVE CODE FREEZE / AUDIT MODE ONLY / NO PRODUCT CONCLUSION**  
Branch: `experiment/premium-v2-1-minimal-cascade`  
Approved design closure: `5e1c7ac425acf2e35b2b015260301f150af2c65d`  
Frozen code snapshot: `8290643334712493f06978a40ec3acb9b4d6c2b4`  
Zero-AI CI run: `35800930744` — **153/153 PASS**

## Why freeze here

The remaining high-value unknowns are runtime facts, not additional imagined
controller rules.

Continuing to tune hook parsing, event ordering, or telemetry attribution before
observing the target VS Code Agent Host would risk overfitting to documentation
or guessed payloads. Therefore `82906433...` is the pre-live code freeze.

Documentation-only review material may be updated after this snapshot. Any
runtime/controller/plugin code change creates a new code snapshot and must
re-establish the zero-AI baseline before a paid/live run.

## Frozen architecture

```text
Terra root
  -> bounded intake
  -> exactly one Luna Builder Agent-tool dispatch
  -> one observed Luna Builder lifecycle
  -> deterministic reconciliation
  -> at most one Terra takeover with captured FAILED/UNRESOLVED blocking basis
  -> deterministic final record
  -> stop
```

No Architect, Verifier, Auditor, Lane M, repeated delegation, or automatic
cross-family reviewer.

All seven configured plugin hooks remain in `OTL_V2_1_HOOK_MODE=audit`.

## What the zero-AI baseline establishes

The code/tests establish consistency rules, including:

- immutable captured U0 authority and preserved admitted R obligations;
- rejection of authority downgrade/narrowing/replacement;
- execution-only, current-revision PASS receipt requirements;
- root-only workspace digest exclusions and three-way digest parity between the
  reference controller, plugin controller, and trace reporter;
- malformed/digest-error/external-state fail-closed behavior;
- exact single-mission lifecycle counters;
- exact Builder wrapper dispatch/start/stop/completion accounting;
- non-Builder/second-Builder attempt detection;
- bounded-intake and PostToolUse defense-in-depth checks;
- takeover basis and final takeover-state consistency;
- fixed workspace binding and metadata symlink-escape rejection;
- dual final-record consistency and current-workspace validation;
- rooted OTel attribution for root, Builder, and hook evidence;
- independent `execute_hook` OTel coverage checks;
- reference/plugin controller terminal-outcome parity;
- synthetic smoke fixture pinning and zero-AI evidence collection.

These are coded invariants. They are not runtime proof, semantic correctness
proof, or a security boundary.

## Facts intentionally still NOT_OBSERVED

The first live trace must establish or falsify:

1. the nested experimental plugin actually loads in the owner's VS Code Agent
   Host;
2. plugin-level hooks actually execute under the effective local/organization
   policy;
3. the real seven event payload shapes and ordering;
4. whether the normal Builder Agent-tool wrapper ordering matches the adapter;
5. whether a successful local execution exposes enough PostToolUse result data
   for a collected receipt;
6. how a non-zero child process is surfaced by Agent Host;
7. whether Stop semantics match the one-correction model;
8. whether Agent Host OTel contains usable rooted `invoke_agent`, `chat`, and
   `execute_hook` evidence;
9. the resolved root model is Terra and the resolved Builder model is Luna;
10. synchronous child completion / writer quiescence behavior;
11. same-user access to controller state remains **NOT a trusted security
    boundary**.

## Exact next evidence-producing action

Use only the committed synthetic smoke. It is runtime calibration, never a
promotion holdout.

1. Run the zero-AI local preflight.
2. Generate a fresh synthetic workspace with
   `scripts/premium_v2_1_make_smoke_workspace.py`.
3. Open only that workspace in VS Code.
4. Confirm the experimental plugin/custom agent is enabled.
5. Select `Premium Cascade v2.1 (Experimental)`.
6. Submit the single prompt from
   `docs/PREMIUM_V2_1_LIVE_AUDIT_RUNBOOK.md`.
7. Do not send a second prompt and do not manually repair metadata.
8. Collect evidence with
   `scripts/premium_v2_1_collect_smoke_evidence.py`.
9. Review the raw trace and deterministic report before any enforce-mode edit.

## Decision after the audit smoke

### Runtime matches the frozen assumptions

If the raw evidence satisfies the deterministic calibration gate, the result is
only **CANDIDATE_FOR_SEPARATE_ENFORCE_MODE_RETEST**.

Create a separate enforce-mode change and rerun the same synthetic fixture
before any real development-task experiment.

### Runtime schema/order differs

Treat the mismatch as calibration evidence. Make the smallest parser/adapter
change justified by the raw trace, re-establish zero-AI CI, create a new
pre-live snapshot, and repeat the same synthetic audit.

Do not weaken acceptance invariants merely to make the trace pass.

### Plugin/hooks are blocked by product or policy

Classify the result as runtime/policy infeasibility for this target configuration.
Do not route around the restriction by silently changing architecture or
claiming prompt-only enforcement.

## Explicitly not authorized by this freeze

- no stable `main` changes;
- no v1 frozen-candidate tuning;
- no H1/H2/H3/H4 reuse as fresh holdouts;
- no broad adaptive L/T/M resurrection;
- no default Architect/Verifier/Auditor;
- no promotion experiment;
- no product-quality/economics conclusion;
- no claim of tamper-proof trusted state.
