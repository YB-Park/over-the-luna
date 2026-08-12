# Over the Luna 🌙

[English](README.md) · **한국어**

> **Luna는 많이 쓰고, 비싼 판단은 정말 값어치를 할 때만 쓴다.**

GPT-5.6 Luna는 agent harness의 경제성을 바꿔놓는다. 충분히 저렴하기 때문에 계획, 저장소 분석, 반대 검토, 실패 복구, 리서치, 리뷰 같은 독립적인 판단을 여러 번 수행하면서도 매 턴 premium 모델을 상시 배치할 필요가 없다. **Over the Luna는 이 저렴한 test-time compute를 적극적으로 활용하되, 실제 구현의 책임과 mutable context는 하나의 Main Luna가 계속 소유하도록 설계했다.**

Over the Luna는 **GitHub Copilot을 위한 VS Code 네이티브 Luna-only 코딩 하네스**다. 의도적으로 얇다. 별도 daemon도, 두 번째 editor UI도, 번들 MCP 서버도, 몰래 호출되는 premium 모델도, 같은 코드를 서로 고치는 agent swarm도 없다. 단순한 작업은 그대로 단순하게 처리하고, 복잡한 작업은 필요한 순간에만 작은 Luna context들을 열어 독립적인 증거를 수집한 뒤 같은 Main Luna에게 짧게 돌려준다.

Luna가 더 강한 두 번째 판단이 실제로 위험을 줄일 수 있다고 판단하면 **Claude Sonnet 5** 또는 **Claude Opus 4.8** 리뷰를 제안할 수 있다. 두 모델은 절대 자동 실행되지 않고, 개발자가 눈에 보이는 handoff를 직접 선택해야 한다.

**Over the Luna 1.0은 이 하네스의 안정적인 설계 계약을 정의한다.** 다만 VS Code Agent Plugins 자체는 아직 Preview 기능이므로 플랫폼 동작은 앞으로도 바뀔 수 있다.

> 모델 가격은 바뀔 수 있다. 비용 판단 전에는 GitHub의 최신 [Copilot 모델 가격](https://docs.github.com/ko/copilot/reference/copilot-billing/models-and-pricing)을 확인하는 것을 권장한다.

---

## 설치

### 요구사항

- GitHub Copilot이 활성화된 최신 VS Code.
- 조직 정책에서 Agent Plugins가 허용되어 있어야 한다 (`chat.plugins.enabled`).
- Copilot 모델 정책에서 **GPT-5.6 Luna**를 사용할 수 있어야 한다.
- **Claude Sonnet 5**, **Claude Opus 4.8**은 선택 사항이며 수동 premium review handoff에서만 사용한다.

### Git에서 바로 설치

1. VS Code Command Palette를 연다.
2. **`Chat: Install Plugin From Source`**를 실행한다.
3. 다음 URL을 입력한다.

   ```text
   https://github.com/YB-Park/over-the-luna
   ```

4. 필요하면 VS Code를 Reload한다.
5. Copilot Chat에서 **Over the Luna**를 선택한다.

VS Code는 Agent Plugin을 Git repository에서 직접 설치할 수 있다. 자세한 내용은 공식 [Agent Plugins 문서](https://code.visualstudio.com/docs/agent-customization/agent-plugins)를 참고한다.

---

## 어떻게 동작하나

자동 core는 **GPT-5.6 Luna only**다. 사용자가 선택하는 **Over the Luna** 자체가 Main Worker이자 Coordinator다.

```text
                              You
                               │
                               ▼
                        Over the Luna
                        GPT-5.6 Luna
                  main worker + coordinator
                               │
                 locality / uncertainty / risk
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
  Luna Planner           Luna Architect          Luna Skeptic
 요구사항/계약             repo evidence           반대 검토
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               │
                        compact evidence
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

필요할 때 사용할 수 있는 별도 evidence lane도 두 개 있다.

- **Luna Researcher** — 최신 공식 문서, specification, release note처럼 버전에 따라 달라지는 외부 사실을 조사한다.
- **Luna Tool Worker** — 사용자가 이미 설정해 둔 VS Code MCP / extension tool을 한정된 범위에서 사용한다.

### SIMPLE — Main Luna 직접 실행

가까운 기존 패턴이 명확한 로컬 변경은 그대로 직접 처리한다.

```text
Mode: SIMPLE — direct Luna
```

Main Luna가 주변 context를 확인하고, 수정하고, 검증하고, 보고한다. Planner나 Reviewer가 존재한다는 이유만으로 호출하지 않는다.

### STANDARD — 필요한 read-only 작업만 격리

독립적인 관점 하나나 둘이 실제로 도움이 될 때 STANDARD가 된다. 여기에는 불확실성뿐 아니라 **context pollution**도 포함된다. 코드 변경 자체는 단순해도 올바른 패턴을 찾기 위해 repository를 넓게 탐색해야 한다면 Luna Architect를 사용하는 편이 낫다.

```text
Mode: STANDARD — Luna Architect
```

Main Luna는 mutable implementation context를 유지한다. Architect는 clean context에서 넓게 탐색하고, 실제 구현 방향을 바꾸는 file/symbol evidence만 짧게 반환한다.

### DEEP — 값어치가 있는 곳에 Luna compute를 더 사용

서로 독립적인 불확실성이나 risk boundary가 여러 개라면 초기 advisory call을 최대 세 개까지, 가능하면 병렬로 사용한다.

```text
Mode: DEEP — Luna Planner ∥ Luna Architect ∥ Luna Skeptic
```

Planner는 acceptance와 constraint를 정리한다. Architect는 실제 repository 구조에 근거를 둔다. Skeptic은 중요한 가정을 반박해본다. 세 결과는 압축된 뒤 Main Luna가 구현을 시작한다.

### Recovery — 실패 증거를 바탕으로 진단

Luna Recovery는 막연한 self-reflection 용도가 아니다. 의미 있는 수정 시도 뒤에도 focused test가 실패하거나, 실제 repository 동작이 현재 계획과 충돌하는 등 **구체적인 failure evidence**가 있을 때만 사용한다. Recovery는 bounded diagnosis와 next attempt 하나를 반환하고 실제 수정은 Main Luna가 수행한다.

### Review — 독립적이고 rubric 기반

아주 작은 mechanical change는 별도 reviewer 없이 끝날 수 있다. 하지만 **non-trivial completed change에는 Luna Reviewer 한 번**을 사용하고, correctness, regression, security, concurrency, data integrity, migration safety처럼 구체적인 rubric을 준다. DEEP/high-risk 작업은 서로 다른 rubric일 때만 reviewer를 최대 두 번 사용할 수 있다.

### Premium judgment — 사람이 직접 선택

architecture, auth/security, concurrency, transactionality, migration, data integrity, public contract처럼 판단 비용이 큰 영역이거나 미묘한 불확실성이 남으면 Luna가 다음을 반환할 수 있다.

```text
RECOMMEND_SONNET: <specific reason>
```

정말 높은 위험도의 판단이면:

```text
RECOMMEND_OPUS: <specific reason>
```

추천 문구가 나와도 premium 모델이 자동 실행되지는 않는다. VS Code에 handoff가 나타나고 실제 실행 여부는 개발자가 결정한다.

---

## 구조를 한 문장으로

> **Parallelize thinking; serialize mutation.**

그리고 그에 붙는 두 번째 원칙은:

> **Main Luna owns the work, not all of the thinking.**

Main Luna가 유일한 자동 repository mutation owner다. Council agent들은 같은 branch를 서로 고치는 자율적인 팀원이 아니라, 서로 다른 관점에서 독립 증거를 가져오는 짧은 수명의 leaf context다.

---

## 왜 이런 구조인가

아래 연구가 GPT-5.6 Luna 자체의 성능이나 Over the Luna가 최적의 하네스라는 사실을 증명하는 것은 아니다. 우리는 이 결과를 설계 결정의 근거로 사용하고 실제 VS Code runtime behavior와 함께 검증한다.

### 싼 inference는 알고리즘 자체를 바꿀 수 있다

추론 비용이 충분히 낮으면 planning이나 verification을 한 번 더 독립적으로 수행하는 multi-pass 전략 자체가 현실적인 선택지가 된다. [Scaling Test-time Compute for LLM Agents](https://arxiv.org/abs/2506.12928)는 추가 compute가 agent 성능을 개선할 수 있음을 보이면서 동시에 **언제**, **어떻게** compute를 쓰는지가 중요하다고 보고한다. 그래서 Over the Luna는 항상 fan-out하지 않고 SIMPLE / STANDARD / DEEP으로 budget을 조절한다.

### agent가 많다고 자동으로 좋아지는 것은 아니다

OpenAI의 [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)는 multi-agent 복잡도를 추가하기 전에 single agent의 capability를 충분히 활용할 것을 권한다. [TeamBench](https://arxiv.org/abs/2605.07073)도 팀이나 verifier가 오히려 성능을 해치는 경우를 보고한다. 그래서 Main Luna가 직접 구현하고, 추가 호출에는 반드시 구체적인 이유가 있어야 한다.

### 코딩에서는 competing writer보다 context isolation이 더 중요하다

Anthropic의 [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)은 breadth-first parallel research의 장점을 보여주지만 coordination/token cost가 커지고 coding은 독립적으로 병렬화할 수 있는 일이 상대적으로 적다고 설명한다. VS Code도 subagent를 독립 context에서 집중적으로 일한 뒤 main agent에게 결과를 반환하는 구조로 설명한다 ([VS Code Subagents](https://code.visualstudio.com/docs/agents/subagents)). 그래서 Over the Luna는 competing code mutation이 아니라 read-only 사고를 병렬화한다.

### context는 계속 전달하기보다 압축한다

Microsoft의 [SWE-Edit](https://www.microsoft.com/en-us/research/publication/swe-edit-rethinking-code-editing-for-efficient-swe-agent/)과 [CORPGEN](https://www.microsoft.com/en-us/research/blog/corpgen-advances-ai-agents-for-real-work/)은 역할/context 분리와 통제된 context 전달의 가치를 보여준다. Council agent는 내부에서는 넓게 탐색할 수 있지만 Main Luna에게는 짧은 evidence만 반환한다.

### 실패는 blind retry보다 diagnosis를 먼저 한다

Microsoft의 [PROBE](https://www.microsoft.com/en-us/research/publication/debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents/)는 evidence → diagnosis → bounded recovery 형태를 뒷받침한다. Luna Recovery도 같은 방향으로 동작하며 retry budget은 제한된다.

### verification에는 구체적인 관점이 필요하다

막연한 "전체적으로 꼼꼼히 봐" 리뷰는 쉽게 과신할 수 있다. Microsoft의 [AgentLens](https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/)는 성공 결과 뒤에도 나쁜 agent trajectory가 숨어 있을 수 있음을 보여준다. 그래서 Over the Luna는 명시적인 reviewer rubric을 사용하고 premium judgment는 사람에게 노출한다.

---

## Agent 구성

| Agent | Model | Visible | Tool boundary | Purpose |
|---|---|---:|---|---|
| **Over the Luna** | GPT-5.6 Luna | ✅ | active selection 상속 | main worker + coordinator |
| Luna Planner | GPT-5.6 Luna | ❌ | no tools | acceptance / work contract |
| Luna Architect | GPT-5.6 Luna | ❌ | read/search | repository structure / impact |
| Luna Skeptic | GPT-5.6 Luna | ❌ | read/search | 중요한 가정 반박 |
| Luna Researcher | GPT-5.6 Luna | ❌ | read/search/web | 최신 public evidence |
| Luna Tool Worker | GPT-5.6 Luna | ❌ | active selection 상속 | bounded MCP / extension evidence |
| Luna Recovery | GPT-5.6 Luna | ❌ | read/search | failure diagnosis |
| Luna Reviewer | GPT-5.6 Luna | ❌ | read/search | independent rubric review |
| **Sonnet Reviewer** | Claude Sonnet 5 | ✅ | read/search | manual premium second opinion |
| **Opus Critical Reviewer** | Claude Opus 4.8 | ✅ | read/search/web | manual highest-stakes review |

모든 automatic subagent는 leaf node (`agents: []`)다. Sonnet과 Opus는 manual-only profile이며 automatic core가 호출하지 않는다.

---

## MCP와 extension tool

Over the Luna는 MCP 서버를 설치하거나 소유하지 않는다. Main Luna와 Luna Tool Worker는 개발자가 현재 선택한 VS Code tool environment를 보존하고, strict council/review role은 좁은 explicit tool list를 사용한다.

Tool이 보인다고 mutation 권한이 생기는 것은 아니다. 요청을 수행하는 데 명백히 필요한 external read는 추론할 수 있지만 **external mutation은 절대 추론하지 않는다.** ticket 수정, message 전송, push, deploy, database 변경, PR 생성, cloud resource 변경은 해당 side effect를 사용자가 명시적으로 요청해야 한다.

상세 계약과 troubleshooting은 [`docs/MCP.md`](docs/MCP.md)를 참고한다.

---

## Thinking effort

Over the Luna는 `.agent.md`에 문서화되지 않은 per-agent reasoning-effort field를 넣지 않는다. reasoning/thinking 설정은 VS Code/model control이 담당한다. 대신 하네스는 실제로 관찰 가능한 작업 구조를 제어한다.

- advisory fan-out
- context-isolation trigger
- compact output contract
- one mutation owner
- evidence-triggered recovery
- reviewer count와 rubric
- explicit stop condition과 human premium gate

---

## 범위와 한계

Over the Luna는 orchestration layer이지 security boundary가 아니다. VS Code의 trust, approval, sandboxing, organization policy, 그리고 개발자가 설정한 tool environment에 의존한다. Agent Plugins는 현재 Preview 기능이므로 VS Code/Copilot 업데이트에 따라 runtime behavior가 달라질 수 있다.

Automatic core는 의도적으로 **GPT-5.6 Luna**에 최적화되어 있다. 조직에서 Luna를 사용할 수 없다면 다른 모델로 조용히 자동 대체하지 않는다.

---

## 문서

- [`docs/DESIGN.md`](docs/DESIGN.md) — 현재 architecture와 invariant.
- [`docs/MCP.md`](docs/MCP.md) — MCP/extension-tool 계약.
- [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) — runtime release check.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution / architecture rule.
- [`CHANGELOG.md`](CHANGELOG.md) — release history.

## 라이선스

MIT. [`LICENSE`](LICENSE)를 참고한다.

Over the Luna는 community project이며 GitHub, Microsoft, OpenAI의 공식 제품이 아니다.
