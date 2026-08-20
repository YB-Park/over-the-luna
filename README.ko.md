# Over the Luna 🌙

[English](README.md) · **한국어**

> **Luna는 많이 쓰고, 비싼 판단은 정말 값어치를 할 때만 쓴다.**

**Over the Luna는 GitHub Copilot 안에서 동작하는 VS Code 네이티브 GPT-5.6 Luna 코딩 하네스다.** 하나의 Main Luna가 실제 구현을 계속 소유하고, 계획·저장소 조사·반대 검토·리서치·복구·리뷰처럼 독립 context가 값어치를 하는 곳에 짧은 Luna leaf를 사용한다.

**v1.1이 현재 stable contract다.** investigation/assurance 경계를 분리하고, 개발자가 선택한 VS Code tool 환경을 보존하는 ambient Main, sealed Architect handback, artifact-first Reviewer, 그리고 Claude Sonnet 5 기반의 단일 **Premium Review**를 제공한다.

VS Code Agent Plugins 자체는 아직 Preview 기능이므로 플랫폼 동작은 프로젝트와 독립적으로 바뀔 수 있다.

## 설치

### 요구사항

- GitHub Copilot이 활성화된 최신 VS Code.
- 조직 정책에서 Agent Plugins가 허용되어 있어야 한다 (`chat.plugins.enabled`).
- Copilot 모델 정책에서 **GPT-5.6 Luna**를 사용할 수 있어야 한다.
- **Claude Sonnet 5**는 선택 사항이며 사용자가 Premium Review를 직접 선택할 때만 사용한다.

### Git에서 바로 설치

1. VS Code Command Palette를 연다.
2. **`Chat: Install Plugin From Source`**를 실행한다.
3. 다음 URL을 입력한다.

   ```text
   https://github.com/YB-Park/over-the-luna
   ```

4. 필요하면 VS Code를 Reload한다.
5. Copilot Chat에서 **Over the Luna**를 선택한다.

## v1.1 구조

```text
                              You
                               │
                               ▼
                        Over the Luna
                        GPT-5.6 Luna
                   Main implementation owner
                               │
                 investigation + assurance
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
  Luna Planner           Luna Architect          Luna Skeptic
 요구사항/제약              repo evidence           반대 검토
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
                                 │
                                 ▼
                         Premium Review
                       Claude Sonnet 5
                          HUMAN CLICK
```

필요할 때 사용할 수 있는 별도 evidence lane도 있다.

- **Luna Researcher** — 최신 공식 문서, specification, release note 같은 public evidence를 조사한다.
- **Luna Tool Worker** — 개발자가 이미 설정한 VS Code MCP / extension tool을 bounded context에서 사용한다.

## Routing = investigation + assurance

v1.1은 **얼마나 조사해야 하는지**와 **변경 후 얼마나 강하게 검증해야 하는지**를 분리한다.

### Investigation

- **SIMPLE** — bounded local orientation 뒤 구현 위치와 계약이 명확하다. Main이 직접 처리한다.
- **STANDARD** — 알려지지 않은 repository contract, dependency, broad semantic pattern을 찾아야 한다. Main이 넓게 self-scouting하기 전에 **Luna Architect**에게 disposable discovery를 맡긴다.
- **DEEP** — 서로 독립적인 불확실성이나 중요한 cross-cutting risk가 여러 개일 때 최대 세 개의 서로 다른 초기 Luna advisory call을 사용할 수 있다.

Architect가 충분한 evidence를 반환하면 구현과 검증에 필요한 전체 `MUTATION_TARGETS` work set도 함께 반환한다. Main은 `Boundary sealed — work set: ...`을 출력하고 mutation 전에 넓은 repository discovery를 다시 반복하지 않는다.

### Assurance

- **NONE** — 직접 assertion으로 검증되는, 정말 mechanical하고 locally bounded한 변경에만 사용한다.
- **REVIEW** — 일반적인 semantic change는 focused validation 뒤 정확히 한 번의 named **Luna Reviewer** pass를 사용한다.
- **RISK** — auth/security, concurrency/idempotency, transaction, migration, persistence/data integrity, rollback, 중요한 public contract는 최소 한 번의 post-change named Luna Reviewer를 요구한다.

Reviewer는 현재 unified diff, acceptance criteria, validation evidence를 받는다. 실제 repository mutation은 끝까지 Main만 수행하며 Reviewer finding의 채택 여부도 Main이 판단한다.

## Agent 구성

| Agent | Model | Visible | Tool boundary | Purpose |
|---|---|---:|---|---|
| **Over the Luna** | GPT-5.6 Luna | ✅ | VS Code selected tool 유지 | Main worker + coordinator |
| Luna Planner | GPT-5.6 Luna | ❌ | no tools | acceptance / constraints |
| Luna Architect | GPT-5.6 Luna | ❌ | read/search | repository evidence + sealed work set |
| Luna Skeptic | GPT-5.6 Luna | ❌ | read/search | 중요한 가정 반박 |
| Luna Researcher | GPT-5.6 Luna | ❌ | read/search/web | 최신 public evidence |
| Luna Tool Worker | GPT-5.6 Luna | ❌ | selected tool 상속 | bounded MCP / extension evidence |
| Luna Recovery | GPT-5.6 Luna | ❌ | read/search | failure-anchored diagnosis |
| Luna Reviewer | GPT-5.6 Luna | ❌ | read/search | artifact-first independent review |
| **Premium Review** | Claude Sonnet 5 | ✅ | read/search | 사람이 선택하는 different-model judgment |

모든 automatic leaf는 non-recursive (`agents: []`)다. 일반적인 user-selectable agent UI에는 **Over the Luna**와 **Premium Review**만 보이는 것이 의도된 동작이다.

## VS Code tool 환경 보존

Over the Luna는 MCP 서버를 설치하거나 소유하지 않는다. Main은 고정 `tools` 목록을 선언하지 않아서 개발자가 선택한 built-in/MCP/extension tool 환경을 VS Code가 계속 소유하도록 한다. Luna Tool Worker도 isolation이 값어치를 할 때 같은 ambient 경로를 사용한다.

반면 read-only leaf는 좁은 explicit tool list를 사용하므로 임의의 mutation-capable integration을 상속하지 않는다.

Tool이 보인다고 mutation 권한이 생기는 것은 아니다. message 전송, ticket/database 변경, push, deploy, PR 생성, cloud resource 변경 같은 external mutation은 그 side effect를 사용자가 명시적으로 요청해야 한다.

상세 계약과 troubleshooting은 [`docs/MCP.md`](docs/MCP.md)를 참고한다.

## Premium Review

Premium inference는 model menu가 아니라 하나의 눈에 보이는 human decision이다.

- backing model: **Claude Sonnet 5**.
- handoff: 정확히 하나의 **Premium Review**.
- `send: false`: prompt는 채워지지만 사용자가 전송하기 전에는 premium request가 실행되지 않는다.
- Premium Review는 read/search only이며 다른 agent에 delegate하지 않는다.
- handoff와 Premium Review agent는 사용자의 마지막 substantive request 언어를 유지한다. code, path, command, verdict label은 그대로 유지한다.
- premium model을 사용할 수 없으면 요청한 premium judgment가 실행된 것처럼 조용히 대체하지 않고 그 사실을 드러내야 한다.

## 설계 원칙

> **Parallelize thinking; serialize mutation.**

> **Main Luna owns the work, not all of the thinking.**

목표는 최소 token이나 최대 agent 수가 아니다. 독립 context가 잘못된 방향의 구현을 줄이거나, 넓은 disposable discovery를 Main 밖으로 격리하거나, 구체적인 실패를 진단하거나, 완성된 artifact를 독립 검증할 때 저렴한 Luna inference를 추가로 사용한다.

## 범위와 한계

Over the Luna는 orchestration layer이지 security boundary가 아니다. VS Code trust, approval, sandboxing, organization policy, 그리고 개발자가 설정한 tool environment에 의존한다. GitHub Copilot feature/model policy를 우회하거나 개발자에게 허용된 model catalog 밖의 모델을 가져오지 않는다.

Automatic core는 의도적으로 **GPT-5.6 Luna only**다. Luna를 사용할 수 없으면 다른 automatic model로 조용히 대체하지 않는다.

## 문서

- [`docs/DESIGN.md`](docs/DESIGN.md) — v1.1 architecture와 invariant.
- [`docs/MCP.md`](docs/MCP.md) — MCP/extension-tool 계약.
- [`docs/SMOKE_TEST.md`](docs/SMOKE_TEST.md) — runtime release check.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution / architecture rule.
- [`CHANGELOG.md`](CHANGELOG.md) — release history.

## 라이선스

MIT. [`LICENSE`](LICENSE)를 참고한다.

Over the Luna는 community project이며 GitHub, Microsoft, OpenAI의 공식 제품이 아니다.
