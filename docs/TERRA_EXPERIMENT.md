# Terra Deep Judgment Experiment

Status: **experimental branch only**  
Branch: `experiment/terra-deep-judgment`  
Stable baseline: `main` at `814a069df188d28a564c4b05fbc441c2e3092d3d`

This experiment asks one narrow question:

> Does one human-selected GPT-5.6 Terra judgment checkpoint, fed by cheap Luna evidence contexts, prevent enough consequential wrong-direction work to justify adding a second pre-change intelligence tier to Over the Luna?

It does **not** ask whether Terra is generally better than Luna.

## Candidate architecture

```text
User
  |
  | rare, human-selected consequential uncertainty
  v
Deep Judgment — GPT-5.6 Terra
  |  tools: agent only
  |
  +--> Luna Planner
  +--> Luna Architect
  +--> Luna Skeptic
  +--> Luna Researcher
  |
  | compact evidence + one judgment
  v
human-click handoff (send:false)
  |
  v
Over the Luna — GPT-5.6 Luna
  |
  v
existing v1.1 mutation / validation / review path
```

Structural constraints:

- Terra cannot directly read/search/edit/execute the repository.
- Terra cannot call MCP/extension tools or perform external side effects.
- Terra may invoke at most three named Luna evidence leaves.
- Terra never delegates implementation.
- Main Luna remains the sole repository mutation owner after handoff.
- Existing Premium Review remains unchanged and is excluded from Phase 1 so the experiment isolates the pre-change judgment effect.

## Hypotheses

### H1 — positive-value hypothesis

For tasks with competing causal models, cross-cutting invariants, conflicting evidence, or high downstream rework leverage, Deep Judgment produces a materially better decision contract than the Luna-only baseline.

### H2 — selectivity hypothesis

For large-but-straightforward, broad-discovery-only, or locally bounded tasks, Deep Judgment should identify that Terra was not justified rather than manufacture premium work.

### H3 — context-economy hypothesis

The candidate gets most repository evidence through Luna leaves and does not need Terra to ingest broad repository context directly.

### H4 — continuity hypothesis

A Terra decision can be handed to Main Luna without breaking v1.1 mutation ownership, sealed discovery, validation, or artifact-first assurance.

## Cost discipline

Quality is primary, but spend must remain interpretable.

Phase 0 and Phase 1 deliberately avoid implementation. This tests the expensive architectural hypothesis before paying for duplicate end-to-end coding runs.

Per Deep Judgment run:

- one Terra parent trajectory;
- at most three Luna leaf calls;
- zero premium review;
- zero implementation;
- fresh chat;
- stop as soon as the required output contract is complete.

Do not add more samples merely to make a weak result look convincing.

## Phase 0 — structural smoke

Run once before any comparison.

Expected:

1. **Deep Judgment** is visible and shows GPT-5.6 Terra.
2. Its available tool surface is only the subagent/`agent` tool.
3. It can invoke only Luna Planner, Luna Architect, Luna Skeptic, and Luna Researcher.
4. A delegated leaf runs with GPT-5.6 Luna.
5. Terra does not directly read/search the workspace.
6. The **Implement with Over the Luna** handoff is visible and remains `send:false`.
7. The handoff targets Over the Luna / GPT-5.6 Luna.
8. No repository mutation occurs before the human handoff.

Fail the experiment immediately if any structural boundary cannot be enforced in the real VS Code/Copilot runtime.

## Phase 1 — decision-only historical replay

Use fresh chats and disposable worktrees. The agent must not see later commits, current README/CHANGELOG, or this experiment document from the future state.

For each positive case, run:

- **A / baseline:** stable Over the Luna behavior against the historical workspace; request analysis/decision only, no implementation.
- **B / candidate:** Deep Judgment against an identical historical workspace; no implementation.

Randomize A/B order per case. Do not continue one arm's chat into the other.

### Case P1 — ambient tool inheritance failure

Historical workspace:

`8af8e03230808bc0baf73793727c2dad1964cd94`  
(the parent of the accepted v0.6 correction)

Prompt:

> VS Code에서 사용자가 선택해 둔 MCP/extension tools가 harness의 worker까지 자연스럽게 유지되어야 한다. 그런데 현재 구조에서는 tool wiring과 coordinator/worker 경계가 실제 VS Code 동작과 어긋날 가능성이 있다. 현재 repo와 필요한 최신 VS Code custom-agent/subagent 동작을 근거로 구조적 원인을 판단하고, 어떤 역할이 tools를 명시해야 하고 어떤 역할이 생략해야 하는지 결정해줘. coordinator가 사용자 환경 도구를 직접 실행하는 구조는 피하고 싶다. 구현은 하지 말고 결정과 근거, 위험만 정리해줘.

Reference outcome, hidden from the agent:

- accepted v0.6 commit `bf042ebee3b9e07ddbaf29cdf6e7ee6053b1cca4`;
- ambient roles preserve selected-tool inheritance by omitting fixed tools;
- strict roles keep explicit narrow tool lists;
- coordinator direct environment execution is treated as a harness violation.

### Case P2 — specialist routing simplification

Historical workspace:

`bf042ebee3b9e07ddbaf29cdf6e7ee6053b1cca4`  
(the parent of the accepted v0.7 simplification)

Prompt:

> Luna의 비용/능력 프로필이 좋아진 상황에서 현재 dedicated worker routing이 정말 복잡도를 벌어들이는지 다시 판단하고 싶다. mechanical/multi-file 작업을 전용 모델로 보내는 구조와 Luna를 기본 implementation owner로 두는 구조를 비교해서, 어떤 branch를 유지/삭제/승격 전용으로 둘지 결정해줘. 모델 다양성 자체는 목표가 아니다. 구현은 하지 말고 architecture decision과 제거 가능한 complexity를 명확히 해줘.

Reference outcome, hidden from the agent:

- accepted v0.7 commit `e6ae7d85537a6b0cdfc1e90533dba61ba6460410`;
- dedicated MAI worker removed;
- Luna becomes the default owner for mechanical and coherent multi-file implementation;
- Kimi remains observable escalation-only rather than an initial route.

### Case P3 — always-on premium coordinator

Historical workspace:

`e6ae7d85537a6b0cdfc1e90533dba61ba6460410`  
(the parent of the accepted v0.8 Luna Council change)

Prompt:

> 현재 Over the Luna는 Sonnet coordinator가 항상 control plane을 잡고 Luna worker들을 라우팅한다. Luna의 비용/능력과 harness overhead를 다시 고려했을 때 이 always-on premium coordinator가 여전히 자기 비용과 복잡도를 벌어들이는지 판단해줘. Main implementation continuity, independent context isolation, review, human-visible premium escalation을 모두 고려해서 automatic core의 모델/ownership 구조를 결정해줘. 구현은 하지 말아줘.

Reference outcome, hidden from the agent:

- accepted v0.8 commit `607539f4fbdb9275bfff04f325d704f9c5d29a17`;
- always-on Sonnet coordinator removed;
- Luna-only automatic core introduced;
- Main Luna owns implementation;
- compact Luna Council leaves provide isolated thinking;
- premium models stay manual and visible.

## Phase 1 negative controls

These are **candidate-only** runs. They test whether Deep Judgment manufactures a reason to spend Terra.

### Case N1 — exact mechanical change

Prompt:

> `plugin.json`의 description에서 오타 한 단어만 정확히 교체하고 같은 문자열을 확인하면 되는 작업이라고 가정하자. 다른 behavior나 contract는 바뀌지 않는다. 이 작업에 Deep Judgment가 필요한지 판단해줘. 구현은 하지 마.

Expected: `VERDICT: NOT_JUSTIFIED`, ideally with zero leaf calls.

### Case N2 — broad discovery without consequential synthesis

Prompt:

> repo에서 Premium Review의 response-language continuity가 어디에서 정의되고 검증되는지 찾아서 경로와 contract만 알려줘. 변경은 하지 않는다. 여러 competing architecture decision은 없다. Deep Judgment를 쓰는 것이 정당한지도 같이 판단해줘.

Expected: `VERDICT: NOT_JUSTIFIED`. A single Luna Architect/Researcher evidence call is tolerable only if the runtime requires evidence before rejecting the premium route; repeated evidence gathering is a failure.

## Blinded scoring

Score baseline and candidate outputs without looking at which arm produced them.

Each positive case is 0–2 on each axis:

1. **Decision correctness** — matches the consequential direction later accepted in the repository.
2. **Repository/runtime grounding** — distinguishes repository fact, platform fact, and inference.
3. **Alternative discrimination** — rejects the most plausible wrong path for a concrete reason.
4. **Execution usefulness** — produces constraints that downstream Main could actually implement without inventing the key decision again.
5. **Scope discipline** — avoids unrelated redesign, implementation, and generic premium-model ceremony.

Maximum: 10 per case.

Also record:

- number of Luna leaf calls;
- whether Terra attempted any direct environment tool;
- total tool calls;
- elapsed time;
- displayed token/credit/request usage if VS Code exposes it;
- whether the decision changed after specialist evidence;
- unresolved facts;
- human intervention beyond the fixed prompt.

Do not infer token usage when the product does not expose it.

## Phase 1 gate

Proceed to end-to-end Phase 2 only if all are true:

- candidate beats baseline on at least **2 of 3** positive historical cases;
- candidate has **no material decision regression** on the remaining positive case;
- both negative controls return `NOT_JUSTIFIED`;
- no structural tool/model boundary violation occurs;
- Terra evidence gathering stays within the three-leaf budget;
- at least one winning case shows a concrete improvement in causal/architectural discrimination, not merely longer prose.

If these conditions fail, stop. Do not tune prompts indefinitely in the same experiment.

## Phase 2 — held-out end-to-end test

Only after Phase 1 passes.

Choose two real, consequential tasks not used to design this prompt:

- one hard root-cause/debugging task with competing hypotheses;
- one cross-cutting architecture or concurrency/data-integrity task.

Run baseline and candidate from identical clean repository states.

Candidate path:

`Deep Judgment -> human handoff -> Over the Luna -> existing validation/review`

Primary measures:

- final correctness;
- wrong-direction edits before convergence;
- repair/rework count;
- Recovery count;
- Reviewer actionable findings;
- Boundary reopen count;
- plan-to-implementation contradiction;
- total model/tool cost when visible;
- elapsed time.

The candidate is interesting only if the Terra checkpoint changes a consequential decision or materially reduces downstream rework/risk. A prettier plan is not a win.

## Promotion / kill rule

This branch is not a release candidate.

Evidence for promotion requires:

- structural runtime boundaries hold;
- positive Phase 1 result;
- at least one held-out end-to-end case where Deep Judgment prevents or materially reduces consequential rework;
- no evidence that users would need to select it for ordinary STANDARD/DEEP work;
- total cost remains acceptable relative to the rework/risk actually avoided.

Kill or redesign the branch if:

- Terra mostly repeats Luna conclusions;
- the value comes from extra context rather than better judgment;
- handoff loses critical context and Main must rediscover the decision;
- the premium checkpoint becomes a generic “hard task” route;
- tool/model boundaries cannot be enforced reliably;
- the experiment needs repeated prompt tuning to manufacture a win.

## Copilot usage note

Record actual premium requests/tokens/credits from the GitHub/VS Code surfaces available to the tester. This repository cannot query the developer's private Copilot billing balance itself, and the experiment must not assume unlimited quota.
