# Over the Luna 🌙

[English](README.md) · **한국어**

> **Luna는 많이 쓰고, 비싼 판단은 정말 값어치를 할 때만 쓴다.**

GPT-5.6 Luna는 꽤 특이한 모델이다. GitHub는 Luna를 GPT-5.6 패밀리의 lightweight·cost-efficient·lowest-cost 모델로 소개하고 있는데, 실제 agentic coding에서는 그 가격표만 보고 예상하기 어려울 만큼 많은 일을 해낸다. 이 가격 구조는 하네스의 경제성을 바꾼다. 모든 라우팅 판단에 비싼 모델을 상시 사용하기보다, **추가적인 독립 사고가 실제로 도움이 되는 지점—계획, 저장소 분석, 반대 검토, 실패 복구, 리서치, 리뷰—에 저렴한 Luna compute를 더 쓰고**, 실제 구현의 맥락과 책임은 하나의 Main Luna가 계속 들고 가는 방식이 가능해진다.

Over the Luna는 **GitHub Copilot을 위한 VS Code 네이티브 Luna-only 코딩 하네스**다. 의도적으로 얇다. 별도 daemon도, 두 번째 에디터 UI도, 번들 MCP 서버도, 몰래 호출되는 premium 모델도, 같은 코드를 서로 고치는 agent swarm도 없다. 단순한 일은 Luna 하나가 바로 처리한다. 복잡한 일은 필요한 순간에만 작은 Luna context들을 병렬 또는 독립적으로 열어 증거를 수집하고, 그 결과를 짧게 압축해 같은 Main Luna에게 돌려준다. 정말 더 강한 판단이 필요하다고 Luna가 판단하면 Sonnet 또는 Opus 리뷰를 제안할 수 있지만, premium 모델은 **사용자가 직접 handoff를 실행해야만** 동작한다.

이 프로젝트의 출발점은 한 문장으로 정리된다. **Luna는 test-time compute 자체를 설계 재료로 써볼 수 있을 만큼 싸다.** 어려운 문제라면 서로 다른 Luna에게 독립적으로 몇 번 더 생각시켜 볼 수 있다. 다만 agent가 늘어날수록 latency, context 전달, coordination failure도 함께 늘어나므로 무조건 많이 부르는 방식은 택하지 않는다.

> 모델 가격은 바뀔 수 있다. 최신 정보는 GitHub의 [Copilot 모델 가격](https://docs.github.com/ko/copilot/reference/copilot-billing/models-and-pricing)과 [GPT-5.6 Copilot 공개 공지](https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot/)를 참고한다.

---

## 설치

### 요구사항

- GitHub Copilot이 활성화된 최신 VS Code.
- 조직 정책에서 Agent Plugins가 허용되어 있어야 한다 (`chat.plugins.enabled`).
- Copilot 모델 정책에서 **GPT-5.6 Luna**를 사용할 수 있어야 한다.
- **Claude Sonnet 5**, **Claude Opus 4.8**은 선택 사항이다. 자동 core에서는 쓰지 않고 수동 premium review handoff에서만 사용한다.

### Git에서 바로 설치

1. VS Code Command Palette를 연다.
2. **`Chat: Install Plugin From Source`**를 실행한다.
3. 다음 URL을 붙여넣는다.

   ```text
   https://github.com/YB-Park/over-the-luna
   ```

4. 필요하면 VS Code를 Reload한다.
5. Copilot Chat에서 **Over the Luna**를 선택한다.

VS Code Agent Plugins는 현재 Preview 기능이다. 공식 문서는 [Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins)를 참고한다.

---

## 실제로 어떻게 동작하나

자동 core는 **Luna only**다. 사용자가 선택하는 **Over the Luna** 자체가 Main Worker이자 Coordinator다. 파일을 읽고 수정하고, 명령을 실행하고, 검증하고, 현재 구현 맥락을 유지하면서 "여기서 별도의 독립 Luna 관점이 실제로 도움이 되는가"를 판단한다.

```text
                              You
                               │
                               ▼
                        Over the Luna
                        GPT-5.6 Luna
                  main worker + coordinator
                               │
                    complexity / uncertainty
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
  Luna Planner           Luna Architect          Luna Skeptic
 요구사항/계약             repo evidence           반대 검토
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               │
                       compact Work Contract
                               │
                               ▼
                          Main Luna
                    edit / execute / validate
                               │
                  failure? ────┴──── review?
                      │                  │
                Luna Recovery      Luna Reviewer
                      │                  │
                      └──────────┬───────┘
                                 ▼
                         Main Luna reports
                                 │
                     premium judgment useful?
                         │                 │
                         ▼                 ▼
                  Review with Sonnet   Critical with Opus
                     HUMAN CLICK          HUMAN CLICK
```

필요할 때 쓸 수 있는 별도 evidence lane도 두 개 있다.

- **Luna Researcher** — 최신 공식 문서, specification, release note, 버전에 따라 달라지는 외부 사실을 조사한다.
- **Luna Tool Worker** — 사용자가 이미 설정해 둔 VS Code MCP / extension tool을 한정된 범위에서 사용한다.

### 아주 단순한 작업

명확한 로컬 변경은 그냥 단순하게 끝내야 한다.

```text
Mode: SIMPLE — direct Luna
```

Main Luna가 가까운 기존 패턴을 확인하고, 수정하고, 필요한 검증을 수행하고 보고한다. **Planner가 있다는 이유로 Planner를 부르지 않고, Reviewer가 있다는 이유로 Reviewer를 붙이지 않는다.**

### 보통 수준의 기능 작업

구현 방향은 대체로 명확하지만 repository 구조나 contract 하나가 불분명하다면 그 불확실성만 떼어낸다.

```text
Mode: STANDARD — Luna Architect
```

Architect는 clean context에서 저장소를 읽고, 구현에 영향을 주는 기존 패턴·dependency path·constraint·risk만 짧게 반환한다. 코드를 실제로 고치는 책임은 계속 Main Luna에게 있다.

### 잘못 시작하면 비용이 큰 복잡한 작업

서로 독립적인 불확실성이 여러 개라면 Luna compute를 더 쓸 수 있다.

```text
Mode: DEEP — Luna Planner ∥ Luna Architect ∥ Luna Skeptic
```

- Planner는 사용자 요청을 acceptance criteria와 decision point로 정리한다.
- Architect는 실제 repository 구조와 기존 pattern을 확인한다.
- Skeptic은 현재 방향이 틀렸다고 가정하고 숨은 가정·반례·edge case를 찾는다.

세 결과는 짧은 Work Contract로 압축되어 Main Luna에게 돌아온다. **세 agent가 같은 기능을 각자 구현하는 구조가 아니다.** mutation은 Main Luna 한 번만 수행한다.

### 검증에 실패했을 때

실패했다고 같은 trajectory에서 무작정 "한번 더" 하지 않는다. Main Luna는 실패한 테스트, diagnostics, 실제 관찰 결과, 현재 구현 상태처럼 **구체적인 failure evidence**를 Luna Recovery에게 넘길 수 있다. Recovery는 원인을 별도 context에서 진단하고 다음 bounded attempt 하나를 제안한다. 실제 수정은 Main Luna가 한다.

### 더 강한 모델이 값어치를 할 수 있을 때

Luna는 스스로 "여기서는 Luna만으로 충분하지 않을 수 있다"고 말할 수 있다.

architecture, auth/security, concurrency, transactionality, migration, data integrity, public contract처럼 판단 비용이 큰 영역이거나 미묘한 불확실성이 남으면 Main Luna 또는 Luna Reviewer가 다음을 반환할 수 있다.

```text
RECOMMEND_SONNET: <specific reason>
```

정말 높은 위험도의 판단이면:

```text
RECOMMEND_OPUS: <specific reason>
```

이 문구가 나와도 premium 모델이 자동 실행되지는 않는다. VS Code에 **사람이 볼 수 있는 handoff**가 나타나고, 실제 실행 여부는 개발자가 결정한다.

---

## 구조를 한 문장으로

> **Parallelize thinking; serialize mutation.**

Main Luna가 유일한 자동 repository mutation owner다. Council agent들은 같은 branch를 서로 고치는 자율적인 팀원이 아니라, 서로 다른 관점에서 독립 증거를 가져오는 짧은 수명의 leaf context다.

이게 Over the Luna의 가장 중요한 설계 제약이다.

---

## 우리가 이런 구조를 선택한 이유

아래 연구와 엔지니어링 사례가 GPT-5.6 Luna 자체의 성능을 증명하거나 Over the Luna가 최적의 하네스라는 것을 증명하는 것은 아니다. 우리는 이 결과들을 **orchestration architecture를 결정하기 위한 근거**로 사용했고, 실제 VS Code runtime test와 함께 검증한다. 어떤 역할이 실효성을 증명하지 못하면 다시 지우기 쉽도록 설계한다.

### 1. 싼 inference는 알고리즘 자체를 바꿀 수 있다

GitHub는 Luna를 GPT-5.6 패밀리의 lightweight·cost-efficient·lowest-cost variant로 설명한다. 우리는 이걸 단순 billing 정보로만 보지 않는다. 충분히 낮은 inference cost라면 planning이나 verification을 한 번 더 독립적으로 수행하는 multi-pass 전략 자체가 현실적인 선택지가 된다.

[Scaling Test-time Compute for LLM Agents](https://arxiv.org/abs/2506.12928)는 agent에도 추가 test-time compute가 성능 향상에 도움이 될 수 있음을 보이면서, 동시에 **언제 reflection을 할지**, rollout을 어떻게 다양화할지가 중요하다고 보고한다. 그래서 우리는 "항상 fan-out" 대신 SIMPLE / STANDARD / DEEP budget을 둔다.

### 2. agent가 많다고 자동으로 좋아지는 건 아니다

OpenAI의 [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)는 multi-agent 복잡도를 추가하기 전에 single agent의 capability를 충분히 활용할 것을 권한다. [TeamBench](https://arxiv.org/abs/2605.07073)에서도 single agent가 이미 잘하는 문제에서는 팀 구조가 오히려 성능을 해칠 수 있고, verifier가 존재한다고 자동으로 신뢰할 수 있는 것은 아니라는 결과가 나왔다.

그래서 **기본값은 Main Luna 직접 실행**이다. 별도 Luna context는 실제로 떼어낼 만한 불확실성이 있을 때만 쓴다.

### 3. 코딩은 병렬 리서치와 다르다

Anthropic의 [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)은 breadth-first research에서 큰 효과를 보였지만, token 사용량도 크게 증가했고 coding은 여러 agent가 동일한 상태와 dependency를 공유해야 해서 research보다 병렬화하기 어렵다고 명시한다.

그래서 우리는 parallel coding을 하지 않는다. 대신 **read-only 사고는 병렬화하고 mutation은 직렬화**한다.

### 4. 불필요한 상태를 떼어낼 수 있다면 context isolation은 가치가 있다

VS Code도 subagent를 독립 context에서 집중적으로 일한 뒤 main agent에게 결과만 반환하는 구조로 설명한다 ([VS Code Subagents](https://code.visualstudio.com/docs/agents/subagents)). Microsoft의 [SWE-Edit](https://www.microsoft.com/en-us/research/publication/swe-edit-rethinking-code-editing-for-efficient-swe-agent/)은 code inspection과 edit execution을 분리해 평가에서 resolved rate를 높이면서 inference cost를 줄였다고 보고한다.

그래서 Planner, Architect, Researcher, Tool Worker, Recovery, Reviewer는 clean context를 쓰되 **실제 구현 thread는 Main Luna가 계속 유지**한다.

### 5. context는 계속 전달하기보다 압축해야 한다

Anthropic은 subagent의 중요한 역할을 넓게 탐색한 정보를 lead agent가 쓸 수 있는 형태로 압축하는 것으로 설명한다. Microsoft의 [CORPGEN](https://www.microsoft.com/en-us/research/blog/corpgen-advances-ai-agents-for-real-work/)도 isolated subagents, hierarchical planning, adaptive summarization으로 context interference와 memory growth를 줄인다.

우리 규칙은 다음과 같다.

> **Leaf 안에서는 넓게 생각하고, Main Luna에게는 좁게 말한다.**

다섯 줄이면 Main Luna의 결정을 바꿀 수 있는데 Council agent가 장문의 에세이를 반환한다면 좋은 delegation이 아니다.

### 6. 관리 compute는 파일 수가 아니라 불확실성에 따라 늘린다

Anthropic은 단순 질의에도 orchestrator가 과도하게 agent를 띄우는 문제를 막기 위해 query complexity에 따른 명시적 effort rule을 두었다고 설명한다. Test-time scaling 연구도 compute budget을 어디에 배분하느냐가 중요하다고 본다.

그래서 Over the Luna는 다음 budget을 사용한다.

| Mode | 기본 추가 Luna 호출 | 언제 쓰나 |
|---|---:|---|
| **SIMPLE** | 0 | 방향이 명확하고 로컬한 작업 |
| **STANDARD** | 1–2 | 독립적인 불확실성 1~2개가 실제로 중요할 때 |
| **DEEP** | 최대 3개의 초기 호출 | 서로 다른 불확실성이 여러 개이고 잘못된 방향의 비용이 클 때 |

10개 파일의 기계적인 변경은 SIMPLE일 수 있고, 2개 파일만 건드리는 concurrency 변경은 DEEP일 수 있다.

### 7. 실패는 끈기로 덮지 않고 증거로 복구한다

Microsoft의 [PROBE](https://www.microsoft.com/en-us/research/publication/debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents/)는 runtime evidence, diagnosis, bounded recovery guidance를 분리한다. 관찰된 실패를 먼저 진단한 뒤 제한된 다음 시도를 만드는 방식이 무작정 retry하는 것보다 우리가 원하는 패턴에 가깝다.

그래서 Luna Recovery는 Main Luna가 그냥 불안하다는 이유로 호출할 수 없다. 구체적인 failure evidence가 있어야 하고 recovery loop도 제한한다.

### 8. reviewer라는 이름만으로 안전해지지는 않는다

[TeamBench](https://arxiv.org/abs/2605.07073)는 verifier가 deterministic grader에서 실패한 결과를 승인하는 경우가 있음을 보였고, Microsoft의 [AgentLens](https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/)는 최종 테스트를 통과한 coding trajectory 안에도 blind retry, regression cycle, verification 누락 같은 Lucky Pass가 존재할 수 있음을 보여준다.

그래서 Reviewer에게 "전체적으로 꼼꼼히 봐"라고 하지 않는다. Main Luna가 correctness, regression, security, data integrity, concurrency처럼 **구체적인 rubric**을 지정한다. DEEP에서 리뷰를 두 번 하더라도 서로 다른 rubric일 때만 의미가 있다.

### 9. 이미 아는 workflow rule은 명시적으로 적는다

Microsoft의 [Conductor](https://opensource.microsoft.com/blog/2026/05/14/conductor-deterministic-orchestration-for-multi-agent-ai-workflows/)는 이미 구조가 알려진 workflow에서 orchestrator LLM이 매번 routing을 다시 발견하게 하면 cost, latency, unpredictability가 추가될 수 있다고 지적한다.

Over the Luna는 별도 workflow engine을 만들지 않고 VS Code native custom agents 안에 머문다. 대신 같은 원칙을 빌린다. **budget, role boundary, stop condition, premium gate는 명시적이고 inspectable해야 한다.**

### 10. premium judgment는 인간이 결정한다

모든 요청 위에 Sonnet을 상시 coordinator로 둘 수도 있고, Luna가 원할 때 몰래 premium 모델을 부르게 만들 수도 있었다. 둘 다 선택하지 않았다.

VS Code는 user-visible agent handoff를 지원하고, subagent가 parent보다 높은 cost tier의 모델을 요청할 때 제약을 둔다 ([VS Code Subagents](https://code.visualstudio.com/docs/agents/subagents)). 우리는 그 제약을 제품 철학으로 사용한다. **Luna는 더 비싼 판단이 필요하다고 제안할 수 있지만, 실제 비용을 지불할지는 사람이 정한다.**

### 11. 사용자의 VS Code를 대체하지 않는다

이 플러그인은 Jira, Confluence, database, browser, cloud, 사내 MCP를 번들하지 않는다. 사용자가 이미 만든 VS Code tool environment 위에서 동작하고, trust, approval, credential, sandbox, organization policy는 원래 있던 위치에 그대로 둔다.

Over the Luna를 설치한다는 건 두 번째 tool ecosystem을 설치한다는 뜻이 아니라 **기존 VS Code 위에 orchestration을 하나 추가한다는 뜻**이어야 한다.

자세한 내용은 [`docs/MCP.md`](docs/MCP.md)를 참고한다.

---

## 우리가 일부러 만들지 않은 것

**상시 premium coordinator 없음.** 이전 버전은 Sonnet이 모든 요청의 router/synthesizer였다. 잘 동작했지만 Luna가 control plane까지 감당할 만큼 저렴하다면 매 turn premium token을 쓰는 구조는 정당화하기 어려웠다. 지금 Sonnet은 선택적인 second opinion이다.

**parallel implementation swarm 없음.** 독립 planning과 review는 병렬화할 수 있지만 coupled code mutation은 그렇지 않다. conflicting edit, 중복 탐색, inconsistent state를 막기 위해 implementation owner는 한 명이다.

**깊은 manager hierarchy 없음.** Planner가 Architect를 호출하지 않고 Architect가 또 다른 manager를 부르지 않는다. Council은 전부 leaf다. 정보는 여러 중간 관리자를 거치는 전화게임 대신 Main Luna를 중심으로 한 shallow star topology로 흐른다.

**고정된 'deep ceremony' 없음.** 파일 수가 많거나 작업 설명이 길다는 이유만으로 Council을 소집하지 않는다. 추가 호출 하나마다 서로 다른 불확실성을 담당해야 한다.

**무한 self-reflection 없음.** Recovery는 failure-triggered + bounded, Review는 rubric-driven + bounded다. 안전하게 수렴하지 못하면 blocker를 사용자에게 드러낸다.

**숨은 model diversity 없음.** Kimi, MAI, Haiku, Sonnet, Opus는 automatic core에 참여하지 않는다. 모델 목록에 존재한다는 이유만으로 역할을 만들어주지 않는다. 별도 모델 route는 Luna보다 나은 이유를 증명해야 한다.

---

## Agent 구성

| Agent | Model | 사용자에게 보임 | Tool boundary | 역할 |
|---|---|---:|---|---|
| **Over the Luna** | GPT-5.6 Luna | ✅ | 현재 selected tools 상속 | main worker + coordinator |
| Luna Planner | GPT-5.6 Luna | ❌ | tools 없음 | acceptance / work contract |
| Luna Architect | GPT-5.6 Luna | ❌ | read/search | repository 구조 / 영향도 |
| Luna Skeptic | GPT-5.6 Luna | ❌ | read/search | 가정 공격 / 반례 탐색 |
| Luna Researcher | GPT-5.6 Luna | ❌ | read/search/web | 최신 공개 근거 |
| Luna Tool Worker | GPT-5.6 Luna | ❌ | 현재 selected tools 상속 | MCP / extension evidence |
| Luna Recovery | GPT-5.6 Luna | ❌ | read/search | 실패 진단 |
| Luna Reviewer | GPT-5.6 Luna | ❌ | read/search | 독립 rubric review |
| **Sonnet Reviewer** | Claude Sonnet 5 | ✅ | read/search | 수동 premium second opinion |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | read/search/web | 수동 최고위험 review |

모든 automatic subagent는 leaf node(`agents: []`)다. Sonnet과 Opus는 manual-only profile이며 automatic core가 직접 호출하지 않는다.

---

## MCP와 extension tools

Over the Luna는 사용자의 MCP 설정을 소유하지 않는다.

Main Luna와 Luna Tool Worker는 사용자의 현재 VS Code selected-tool environment를 유지하도록 구성되어 있어서 MCP / extension tool 이름을 하네스에 하드코딩하지 않아도 기존 도구를 사용할 수 있다. 외부에서 읽어 온 내용은 evidence로 취급하고 개발자의 지시를 덮는 instruction으로 취급하지 않는다.

외부 side effect는 추론하지 않는다. 티켓을 읽는다고 업데이트 권한까지 받은 것이 아니다. 코드를 구현했다고 push, deploy, message 전송, PR 생성, database write, cloud resource 변경까지 허용된 것도 아니다. 그런 동작은 사용자가 명시적으로 요청했을 때만 한다.

실제 runtime contract와 smoke test는 [`docs/MCP.md`](docs/MCP.md)를 참고한다.

---

## Thinking effort

Over the Luna는 `.agent.md`에 존재하지 않는 per-agent reasoning-effort 설정이 있는 척하지 않는다. 현재 VS Code custom agent 구성은 model, tools, agents, instructions, handoff 같은 역할과 capability를 정의하고, 모델의 reasoning/thinking 설정은 별도로 관리된다.

대신 하네스가 실제로 관찰하고 통제할 수 있는 것을 제어한다.

- subagent 호출 수
- fan-out 폭
- 각 호출의 scope와 역할
- compact return contract
- validation / recovery budget
- review rubric
- stop condition

그래서 Luna subagent 하나가 오래 걸린다고 자동으로 버그인 것도 아니다. 독립 agent는 fresh repository context를 다시 읽고, 도구를 사용하고, evidence를 검증하고, 자체 reasoning loop를 수행할 수 있다. 목표는 무조건 가장 짧은 latency가 아니라 **coordination overhead는 제한하면서 실제로 가치 있는 추가 작업을 수행하는 것**이다.

---

## 검증과 배포 원칙

모든 push와 pull request에서 `scripts/validate_plugin.py`가 실행된다.

Static CI는 Luna-only automatic core, 정확한 role/tool boundary, leaf Council, manual premium profile, selected-tool inheritance, MCP 미번들, 폐기한 worker 재도입 방지 같은 구조적 invariant를 검사한다.

하지만 static CI는 orchestration이 실제로 도움이 되는지 증명할 수 없다. 배포 전에는 [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md)를 실제 VS Code 환경에서 실행하고 다음을 본다.

- first-pass correctness
- wall-clock time
- 보이는 경우 input/output token 또는 AI credit
- Council 호출 수
- Council output이 실제로 Main Luna의 결정을 바꿨는지
- recovery loop와 blind retry
- 실제로 가치 있었던 review finding
- Sonnet / Opus 제안을 실제로 받아들일 가치가 있었는지

latency만 늘리고 Main Luna의 결정을 거의 바꾸지 못하는 Council role은 삭제 후보다.

---

## 현재 상태

현재 architecture: **v0.8.0 — Luna Council**.

이 프로젝트는 빠르게 변하는 VS Code / Copilot agent surface 위에 올라간 젊은 하네스다. 문서나 우리의 가정보다 **실제 runtime behavior가 우선**한다. VS Code 업데이트나 사용자 실측이 설계를 반박하면 설계를 바꾼다.

관련 문서:

- [`docs/DESIGN.md`](docs/DESIGN.md) — architecture와 invariant
- [`docs/MCP.md`](docs/MCP.md) — MCP / ambient tool contract
- [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) — runtime release gate
- [`CHANGELOG.md`](CHANGELOG.md) — 구조가 왜 계속 바뀌었는지
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rule

---

## 설계에 참고한 연구 / 엔지니어링 자료

- GitHub — [GPT-5.6 Sol, Terra, and Luna in GitHub Copilot](https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot/)
- GitHub — [GitHub Copilot 모델 및 가격](https://docs.github.com/ko/copilot/reference/copilot-billing/models-and-pricing)
- VS Code — [Subagents in Visual Studio Code](https://code.visualstudio.com/docs/agents/subagents)
- VS Code — [Custom agents in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- Anthropic — [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- OpenAI — [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- Microsoft Research — [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](https://www.microsoft.com/en-us/research/publication/swe-edit-rethinking-code-editing-for-efficient-swe-agent/)
- Microsoft Research — [CORPGEN advances AI agents for real work](https://www.microsoft.com/en-us/research/blog/corpgen-advances-ai-agents-for-real-work/)
- Microsoft Research — [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](https://www.microsoft.com/en-us/research/publication/debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents/)
- Microsoft Research — [AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation](https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/)
- Microsoft Open Source — [Conductor: Deterministic orchestration for multi-agent AI workflows](https://opensource.microsoft.com/blog/2026/05/14/conductor-deterministic-orchestration-for-multi-agent-ai-workflows/)
- Zhu et al. — [Scaling Test-time Compute for LLM Agents](https://arxiv.org/abs/2506.12928)
- Kim et al. — [TeamBench: Evaluating Agent Coordination under Enforced Role Separation](https://arxiv.org/abs/2605.07073)

---

## License

MIT
