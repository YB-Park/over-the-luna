# Premium v2.1 — Pre-Live Adversarial Review Packet

Status: **PRE-LIVE / AUDIT MODE / NOT A PROMOTION CANDIDATE**  
Branch: `experiment/premium-v2-1-minimal-cascade`  
Approved design closure: `5e1c7ac425acf2e35b2b015260301f150af2c65d`  
Implementation snapshot before this packet: `76c7c96d964a034a9bbe4da79c61d19dd925b5ec`  
Zero-AI CI run: `35747955477` — **89/89 PASS**

This document is intentionally written for hostile review. It is not a product
announcement and it does not claim that Premium v2.1 is correct, secure,
economical, or ready to ship.

## 1. Exact hypothesis under test

The approved candidate is deliberately narrow:

```text
Terra root
  -> bounded intake
  -> exactly one continuous Luna Builder attempt
  -> deterministic reconciliation
  -> at most one Terra takeover when captured blocking evidence remains unresolved
  -> stop
```

There is no Architect, Verifier, Auditor, Lane M, repeated Luna/Terra switching,
or automatic cross-family review.

Completion authority is intended to come from:

- preserved criterion authority;
- runtime execution receipts;
- current-workspace identity;
- deterministic controller reconciliation;
- a matching final controller record.

Agent prose is never the trusted completion signal.

## 2. Why this exists

The frozen Premium v1 candidate was stopped after H1. On the corrected hidden
oracle:

- Over the Luna: 3/4;
- frozen Premium: 3/4;
- raw Terra: 4/4.

The acceptance-critical SSL-like limitation reached Builder, Terra, and Auditor,
yet the frozen Premium trajectory still accepted completion. That made
acceptance/adjudication control a first-class failure mode, not merely a context
compression problem.

Astra subsequently rejected the larger adaptive L/T/M v2 design as
underidentified and recommended testing the smallest one-way cascade first.
The v2.1 closure review then returned
`APPROVE_MINIMAL_IMPLEMENTATION_EXPERIMENT`.

H1-H4 are not fresh promotion holdouts for this redesign.

## 3. What is implemented

The stable root plugin is not modified by this experiment. The v2.1 runtime is
isolated under:

`experiments/premium_v2_1_plugin/`

It contains:

- a Terra root custom agent;
- one hidden non-recursive Luna Builder;
- Copilot-format plugin-level `hooks.json`;
- a plugin-local deterministic controller;
- a lifecycle hook adapter.

All plugin hooks remain in:

`OTL_V2_1_HOOK_MODE=audit`

The first live run is schema/runtime calibration only.

## 4. Zero-AI evidence already established

At implementation snapshot `76c7c96d...`:

- static plugin validator: PASS;
- agent topology: exactly 2 agents;
- lifecycle topology: exactly 7 configured hooks;
- audit-mode boundary: preserved;
- Python/controller suite: **89/89 PASS**;
- CI run: `35747955477`.

The zero-AI suite now exercises, among other cases:

- missing user obligation;
- U -> A authority laundering;
- blocking/required downgrade;
- same-ID criterion narrowing;
- deletion/replacement of a previously captured repository obligation;
- forged waiver;
- stale/wrong-run/uncollected receipts;
- `DIGEST_ERROR` fail-closed behavior;
- missing/stale/conflicting final records;
- current-workspace digest mismatch;
- weak/missing session identity;
- ambiguous multi-session trace selection;
- repeated/resumed mission rejection;
- malformed lifecycle counters;
- malformed hook JSON/non-object input in enforce mode;
- exactly-one Builder lifecycle;
- non-Builder delegation attempt;
- second subagent attempt;
- pre-Builder repository work;
- metadata-exemption abuse through command tools;
- post-tool defense-in-depth for a bypassed pre-tool gate;
- Terra takeover without an explicit captured blocking residual;
- one-correction Stop behavior.

These tests prove only the coded consistency rules.

## 5. Runtime parser evidence already established

A zero-AI Copilot CLI plugin parser smoke used CLI 1.0.85 and confirmed that the
legacy/Copilot-format experimental plugin can be installed and listed as
enabled.

That smoke did not invoke a model and did not establish hook firing.

The first attempted live Actions path using the built-in workflow token failed
before inference with:

`Access denied by policy settings`

A later one-shot secret-presence probe established:

`COPILOT_GITHUB_TOKEN = not configured`

Repeating the same built-in-token path has no experimental value.

## 6. Current platform contracts used by the implementation

Current documentation checked on 2026-09-23:

- VS Code plugin hooks support `SessionStart`, `UserPromptSubmit`,
  `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`,
  `SubagentStop`, and `Stop`.
- VS Code `UserPromptSubmit` exposes the submitted `prompt`.
- VS Code custom-agent `SubagentStart.agent_type` is documented as the agent
  name.
- VS Code `Stop` exposes `stop_hook_active`.
- Existing Copilot-format plugins remain supported.
- Copilot-format plugins may use `${PLUGIN_ROOT}`.
- `chat.useCustomAgentHooks` is the switch for hooks embedded in custom-agent
  frontmatter; this experiment uses plugin-level hooks instead.
- Copilot CLI OTel emits top-level and subagent `invoke_agent` spans and child
  `chat` spans. Top-level invokes carry `server.address/server.port`, while
  `gen_ai.response.model` on chat spans identifies the resolved model.
- `github.copilot.nano_aiu` must be read from the root invoke span rather than
  summed across child chat spans.

References:

- https://code.visualstudio.com/docs/agent-customization/agent-plugins
- https://code.visualstudio.com/docs/agent-customization/hooks
- https://code.visualstudio.com/docs/agents/reference/hooks-reference
- https://docs.github.com/en/copilot/reference/hooks-reference
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

Documentation is not runtime evidence. Every material assumption above remains
subject to the first live trace.

## 7. Current deterministic control boundaries

### 7.1 User authority

The first observed user prompt is captured externally as immutable `U0`.

Additional `UserPromptSubmit` events are treated as unsupported single-mission
behavior and persist a controller error.

### 7.2 Repository obligations

Builder/root may propose repository-derived blocking obligations, but once an R
obligation is observed it is copied into controller-owned state.

Later deletion, narrowing, re-sourcing, or downgrade does not erase it.

### 7.3 Builder cardinality

Enforce logic permits only the named
`Premium v2.1 Luna Builder`.

The dispatch is marked at PreToolUse, before SubagentStart, so losing a start
event cannot silently authorize a second child.

Trusted final reconciliation separately requires exactly one observed Builder
start and a completed Builder lifecycle.

### 7.4 Pre-Builder work

In enforce mode, root repository tools are denied before Builder dispatch.

Because lifecycle hooks are not treated as a security boundary, PostToolUse also
records a control error if repository/tool work is nevertheless observed before
Builder ownership.

### 7.5 Terra takeover

After Builder returns, metadata-only file operations may reconcile controller
metadata without counting as takeover.

A direct root repository tool is eligible to become the one Terra takeover only
when a controller-captured required blocking criterion is explicitly
`FAILED` or `UNRESOLVED` in the proposal.

This proves only that an unresolved blocking row exists. It **does not prove**
that the residual is semantic/repository-local rather than infrastructure-only.
That distinction remains a model judgment to be measured.

If a pre-tool gate is bypassed but PostToolUse later observes the root repository
operation, the same blocking-row check runs as defense in depth. An unjustified
operation persists a control error and cannot become trusted COMPLETE.

### 7.6 Receipts

A VERIFIED required criterion must reference current runtime receipts.

For trusted verification, receipts must match:

- run identity;
- current workspace revision;
- collected execution status;
- PASS result;
- command/test identity;
- test-asset identity field;
- environment identity field.

A receipt proves observed execution consistency, not semantic relevance.

### 7.7 Workspace identity

The digest covers relevant file bytes, paths, executable bits, symlink targets,
new files, and deletions.

`.git` and controller metadata are excluded.

A digest failure cannot be represented as a valid revision.

The trace reporter independently recomputes the current workspace digest and
rejects a stale final record.

### 7.8 Final record

The runtime writes a controller final record into external state and workspace
metadata.

The trace gate fails closed when:

- no final record is observed;
- schema/outcome is malformed;
- run ID disagrees with the selected hook session;
- workspace revision is stale;
- Builder count is not exactly one;
- final phase is not reconcilable;
- workspace and external final records disagree.

### 7.9 Trace selection

The deterministic trace reporter does not merge multiple sessions.

If several state/event sessions are present, an explicit session key is required
or calibration fails closed.

## 8. Known unresolved attack surfaces

These are not minor caveats. Reviewers should treat them as active attack
targets.

### A. Same-user state tampering — NOT_OBSERVED

External state placement is structural separation, not a security boundary.

A model with a shell running as the same OS user may be able to read or modify
the state directory. File placement, hashes, and locks do not prove tamper
resistance.

No claim of unforgeable trusted state is currently allowed.

### B. Semantic criterion completeness — NOT SOLVED

The deterministic layer can preserve captured authority but cannot prove that
the original user request was decomposed correctly or that no acceptance
criterion was omitted.

Capturing the whole original prompt as U0 reduces authority loss but does not
solve interpretation.

### C. Evidence relevance — NOT SOLVED

A current passing execution receipt does not prove that the check meaningfully
tests the criterion it is cited for.

The model still performs the relevance judgment.

### D. Semantic-vs-infrastructure takeover classification — NOT SOLVED

The controller now requires an explicit FAILED/UNRESOLVED blocking row before
Terra repo work.

It does not independently establish that the residual is local semantic evidence
rather than an unavailable dependency, service, policy decision, or other
non-escalatable condition.

### E. Failed-command capture in VS Code — NOT_OBSERVED

Current VS Code documentation describes `PostToolUse` as firing after a tool
completes successfully.

Whether an `execute` tool whose child process exits non-zero is surfaced as a
successful tool result with an exit code, or as a failure that produces no
PostToolUse event, must be observed.

Do not claim that failing-test receipts are available in Agent Host before that
trace exists.

### F. Hook timeout / bypass behavior — NOT A SECURITY BOUNDARY

GitHub Copilot CLI documentation explicitly states that command-hook timeouts can
fail open for pre-tool gating. VS Code runtime behavior must be observed rather
than inferred.

Post-tool phase checks reduce silent acceptance after some bypasses but cannot
undo an operation that already happened.

### G. User waiver authentication — NOT IMPLEMENTED

The controller has partial/waiver semantics, but the plugin runtime does not yet
implement a trustworthy interactive user-event path that creates authenticated
waivers.

A model-authored waiver is rejected.

### H. Writer quiescence / atomic ownership transfer — NOT_OBSERVED

Synchronous child return is expected, but atomic absence of background writers
during transfer has not been established in the target runtime.

### I. Runtime model identity — NOT_OBSERVED

Frontmatter requests Terra and Luna. That is not backend identity evidence.

The trace gate requires observed resolved model identity before becoming an
enforce-mode candidate.

### J. Product economics / quality — NOT TESTED

No fresh promotion experiment is authorized yet.

A successful synthetic smoke establishes runtime feasibility only.

## 9. First live smoke — exact purpose

The first live smoke uses only the synthetic `increment(value)` fixture created
by:

`scripts/premium_v2_1_make_smoke_workspace.py`

It is prohibited from counting as:

- a promotion holdout;
- a capability win;
- a cost-frontier result.

The first live run asks only:

1. does the experimental plugin load in VS Code Agent Host;
2. do plugin-level hooks actually fire;
3. does exactly one Luna Builder lifecycle occur;
4. are real event field shapes compatible with the parser;
5. can usable execution receipts be captured;
6. does Stop produce a consistent final record;
7. can root/child resolved backend identities be observed.

Use:

`docs/PREMIUM_V2_1_LIVE_AUDIT_RUNBOOK.md`

Do not switch hooks to enforce mode before reviewing the raw audit trace.

## 10. Enforce-mode candidate gate

A code fix passing is insufficient.

The deterministic trace gate currently requires:

- one selected runtime session;
- exactly one session ID;
- required lifecycle events observed;
- single-mission lifecycle counts;
- exactly one Builder start and stop;
- at least one collected PASS receipt;
- a current, non-conflicting, VALID_COMPLETE final record;
- current workspace revision match;
- observed root Terra resolved identity;
- observed Builder Luna resolved identity;
- parse-clean hook, CLI, and OTel evidence.

If any item is absent, the result remains **NOT READY FOR ENFORCE MODE**.

Passing this gate authorizes only a separate enforce-mode implementation/retest.
It does not authorize product promotion.

## 11. Adversarial review questions

Reviewers should attempt to produce concrete counterexamples for at least these
questions:

1. Can model-editable metadata cause trusted COMPLETE while a preserved required
   criterion is unresolved?
2. Can a required U or R obligation be dropped, narrowed, re-sourced, or
   downgraded without a controller error?
3. Can a forged or stale receipt satisfy a required criterion?
4. Can a test pass at revision R and still justify completion after mutation
   R+1?
5. Can workspace metadata and external state disagree while the trace gate still
   reports VALID_COMPLETE?
6. Can a second subagent be launched through a tool-name or argument-shape
   variant?
7. Can a root repository operation occur before Builder ownership without
   becoming visible as noncompliance?
8. Can Terra take over after Builder despite no FAILED/UNRESOLVED captured
   blocking criterion?
9. Can metadata-only detection be abused with a command that also accesses
   product files?
10. Can session/resume behavior merge two missions under one authority record?
11. Can absent or conflicting backend identity be mistaken for Terra/Luna
    evidence?
12. Can OTel parentage cause a child model to be attributed to root or vice
    versa?
13. Can malformed hook state/input make enforce mode fail open?
14. Can same-user shell access rewrite external controller state and all
    cross-checks consistently?
15. Can a semantically irrelevant but technically passing test be used to verify
    U0?
16. Can infrastructure failure be mislabeled as semantic residual and buy an
    unjustified Terra takeover?
17. Can hook timeout or missing PostToolUse allow an operation that neither
    blocks nor leaves enough evidence to invalidate completion?
18. Does any current assertion exceed what the target runtime actually
    demonstrates?

A useful review should distinguish:

- a deterministic-controller bug;
- a hook/runtime feasibility bug;
- a semantic-model judgment limitation;
- a security-boundary limitation;
- an experiment-design problem.

Do not collapse those into one generic verdict.

## 12. Explicit non-goals / forbidden regression

Do not respond to a failure by:

- modifying stable main;
- retuning the frozen v1 candidate;
- treating H1/H2/H3/H4 as fresh holdouts;
- restoring broad adaptive L/T/M routing;
- adding an Architect/Verifier/Auditor by default;
- hiding missing runtime evidence behind prompt claims;
- weakening the controller merely to obtain COMPLETE.

The next evidence-producing action is one tiny **audit-mode live runtime smoke**.
