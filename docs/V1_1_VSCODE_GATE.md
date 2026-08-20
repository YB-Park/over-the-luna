# Over the Luna v1.1 — real VS Code runtime gate

Branch: `rc/v1.1-vscode-gate`  
Status: **integration candidate for manual authenticated VS Code validation; not a release**

This branch deliberately places the evidence-backed v1.1 RC2 contracts in the real `agents/` directory while keeping `plugin.json` at `1.0.0`.

The goal is to answer the remaining questions that Copilot CLI/static tests cannot prove: actual Agent Plugin discovery, selected-tool inheritance, subagent/debug behavior, and visible premium handoff semantics.

## Before testing

- Use this branch, not `main` and not the broad research PR branch.
- Install/load the repository as an Agent Plugin through the normal VS Code / GitHub Copilot path used for development.
- Use an authenticated Copilot session.
- Keep OTel/debug content capture off unless a specific observation requires content.
- Record VS Code version, GitHub Copilot extension/runtime version, plan/policy context, and whether Autopilot is enabled.
- Do not change `plugin.json` to `1.1.0` for this gate.

Expected visible custom agents in this gate layout include:

- `Over the Luna`
- `Luna Architect`
- `Luna Reviewer`
- `Premium Review`

The old normal-menu `Sonnet Reviewer` and `Opus Critical Reviewer` agents are intentionally absent from this gate branch.

## Gate A1 — plugin discovery and exact agent identity

Verify in the actual agent picker/runtime:

1. the plugin loads without parse/fallback errors;
2. `Over the Luna` resolves to this plugin's agent, not a similarly named global/custom agent;
3. the listed Luna leaves are discoverable with the exact expected names;
4. `Premium Review` is discoverable with that exact name;
5. no stale `Review with Sonnet` / `Critical review with Opus` handoff menu appears from this plugin.

**Pass evidence:** screenshot/notes of the loaded agent names plus Agent Debug identity if available.

## Gate A2 — mechanical boundary: SIMPLE + NONE

Use a tiny repository change with all of these properties:

- exact target already named or locatable by one narrow term;
- exact scalar/default/text/metadata substitution;
- no control-flow/validation/identity/data-shape/compatibility change;
- one direct existing assertion validates the requested value.

Expected behavior:

- route line: `Mode: SIMPLE ... | Assurance: NONE`;
- no Architect;
- no Reviewer;
- Main performs the edit and validation;
- final report says review was intentionally skipped because the mechanical threshold was satisfied.

**Fail if:** the task buys Reviewer ceremony merely because a file changed.

## Gate A3 — local semantic boundary: SIMPLE + REVIEW

Use a named local behavioral change where the implementation neighborhood and one visible helper are already clear.

Expected behavior:

- route remains `SIMPLE`;
- assurance is `REVIEW`;
- no investigative Architect by default;
- Main is the only mutation owner;
- after focused validation, Main collects the current unified diff;
- exactly one named `Luna Reviewer` runs;
- Reviewer prompt contains `BEGIN_UNIFIED_DIFF`, `END_UNIFIED_DIFF`, concrete `diff --git` headers, `@@` hunks, and every changed path;
- if Main accepts a finding, Main repairs/revalidates without recursively buying a second normal Reviewer.

**Fail if:** SIMPLE suppresses assurance, a built-in/generic reviewer substitutes for `Luna Reviewer`, or normal REVIEW loops.

## Gate A4 — broad semantic discovery: STANDARD + REVIEW

Use a task that explicitly requires discovering an unknown repository contract or dependency, for example “find and reuse the established identity/normalization contract” without naming its symbol/path.

Expected behavior:

1. Main uses only the bounded local-orientation allowance before recognizing the unknown contract;
2. route becomes `STANDARD` before broad Main scouting;
3. `Luna Architect` runs once for the broad evidence question;
4. Architect returns:
   - `DECISION`
   - `EVIDENCE`
   - `RELATIONSHIPS`
   - `MUTATION_TARGETS`
   - `UNRESOLVED`;
5. Main prints `Boundary sealed — work set: ...` before another repository action;
6. Main's first repository action after seal is a concrete file read inside the work set;
7. until mutation begins, Main does not replay broad `glob`/`rg`, directory views, `find`, `tree`, `git ls-files`, `git grep`, recursive grep/listing, or equivalent inventory;
8. Main owns mutation;
9. final artifact gets exactly one normal Reviewer.

Inspect Agent Debug / OTel specifically for the handback boundary, not merely for the fact that Architect was invoked.

**Fail if:** Main rehydrates the broad repository evidence after Architect or another worker mutates.

## Gate A5 — consequential boundary: RISK

Use a small but real concurrency/idempotency, auth/security, transaction, migration, persistence/data-integrity, rollback, or important public-contract task.

Expected behavior:

- assurance explicitly says `RISK`;
- pre-change Architect/Skeptic may run only for a real independent risk question;
- after the meaningful final patch and focused validation, at least one **named `Luna Reviewer`** runs with the concrete artifact;
- a second post-change Reviewer is not automatic: Main must first name one distinct consequential residual risk/rubric;
- Main remains the only mutation owner.

**Fail if:** high-risk work completes without final independent Luna assurance or review count grows merely because the first review found something.

## Gate A6 — selected built-in / MCP / extension tool inheritance

This is one of the most important real-runtime-only gates.

Main intentionally has **no fixed `tools` field**. Configure at least one harmless selected MCP or extension tool alongside normal built-in tools, then start `Over the Luna`.

Verify:

- Main can see/use the developer-selected tool according to VS Code policy;
- the missing `tools` field does not erase the active selected-tool map;
- `agent/runSubagent` remains available when the runtime supports Council delegation;
- explicit leaf contracts stay restrictive: `Luna Architect` and `Luna Reviewer` do not inherit mutation-capable ambient tools;
- a read-capable leaf does not suddenly receive shell/edit/MCP side effects merely because Main can use them.

Use a harmless read-only MCP/extension action for this check. Do not infer an external side effect merely to prove tool inheritance.

**Fail if:** Main loses selected tools, leaves inherit dangerous ambient tools, or the plugin requires a fixed `tools` list to function.

## Gate A7 — single Premium Review UI and human spend boundary

Produce or reuse a completed change with a **specific consequential residual uncertainty** after Luna validation/review.

Expected behavior:

1. Over the Luna exposes **one** handoff: `Premium Review`;
2. selecting it targets the exact custom agent `Premium Review`;
3. the handoff prompt is prefilled but not sent automatically;
4. `send: false` remains a real human confirmation/spend boundary, including when Autopilot is enabled;
5. the selected backing model is Claude Sonnet 5 when available;
6. if that model is unavailable under the current plan/client/policy, VS Code makes the unavailability/fallback behavior visible enough that the product does not silently pretend the user received the requested premium judgment.

Do **not** accept a silent different-model fallback as a passing premium review. The CLI premium experiment demonstrated that unavailable Opus selection could fall back to Sonnet when expressed through custom-agent frontmatter, so model identity must be observed rather than assumed.

**Fail if:** premium auto-runs, two model-routing choices reappear, or an unavailable model is silently substituted with no product-visible signal.

## Gate A8 — Agent Debug / OTel sanity

For at least one SIMPLE+REVIEW and one STANDARD+REVIEW session, capture enough debug/OTel metadata to verify:

- Main vs leaf agent identities;
- subagent invocation count;
- model identity;
- tool ownership;
- Reviewer count;
- route markers;
- no competing leaf mutation.

The repository analyzer now keys ancestry by `(trace_id, span_id)` and has a cross-trace collision regression. Prefer using the repository scripts for exported trace summaries so the same metric definitions are used as the automated research.

## Exit criterion

Gate A passes only when actual VS Code behavior supports all product-critical claims:

- mechanical work remains low-ceremony;
- local semantic work can be `SIMPLE + REVIEW`;
- broad unknown discovery is genuinely isolated and sealed;
- RISK receives final independent assurance;
- Main is the sole mutation owner;
- selected-tool inheritance behaves as intended;
- leaves remain restricted;
- one `Premium Review` handoff is exact-name, human initiated, and model behavior is not silently misrepresented.

If any point contradicts the RC contract, fix the contract/runtime assumption **on this RC branch** and repeat the smallest failing gate before productizing or bumping the version.

## After Gate A passes

Then, and only then:

1. treat the RC2 + Architect v3 + Reviewer RC + single Premium Review shape as the v1.1 product contract;
2. update README / README.ko / DESIGN / SMOKE_TEST / CONTRIBUTING and tool-selection guidance;
3. decide which research artifacts/workflows remain after release;
4. run packaged-plugin clean-install smoke tests;
5. bump version/changelog to `1.1.0` and prepare the release integration into `main`.
