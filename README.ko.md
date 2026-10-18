# Over the Luna Next — RC2 역할 배치 연구 🌙

[English](README.md)

**안정 버전이 아니야.** 기존 v1.1.1에서 수많은 실험으로
도출한 Council의 가치를 다시 중심에 놓고, 역할과 모델을
**언제 배치하는 게 실제로 이득인지** 개선하는 연구 후보야.
[전체 설계 및 타 하네스 조사](docs/ROLE_TOPOLOGY.md).

**Main 1개 + 조건부 보조 에이전트 7개**를 정의했어.

- **Architect (Luna):** 넓은 저장소 탐색과 컨텍스트 격리
- **Reviewer (Luna):** 실제 코드 diff와 테스트를 바탕으로 독립 검토
- **Skeptic (Luna):** 구현 전에 중요한 가정을 반박
- **Researcher (Luna):** 공식 문서/최신 API 조사
- **Recovery (Luna):** 실제 오류 발생 이후에만 진단
- **Sol Specialist (GPT-6.1 Sol):** 필요할 때 강한 독립 판단
- **Sonnet Specialist (Claude Sonnet 5.5):** 강한 판단의 대체 모델

**일반 작업은 Main 혼자 처리해.** 어려운 작업에서 필요한
역할만 호출하는 구조이므로, 파일이 8개라고 매번 8번 호출하는
것은 아니야. **Claude Haiku 5.5도 Main 모델로 직접 선택 가능**해.
단, Haiku 자동 라우팅의 경제성을 아직 입증하지 않았기 때문에
근거 없이 고정하지는 않았어.

**Planner와 Tool Worker를 보류한 이유:** 전자의 `tools: []`
도구 권한 변환 위험과 후자의 광범위한 MCP 도구 상속 문제는
정식으로 해소되지 않았어. 이 역할들의 가치까지 부정한 게
아니고, 안전하게 운영하는 방식을 먼저 결정한다는 뜻이야.

## 설치·원복

무과금 Actions를 통과한 브랜치의 ZIP을 사용하거나,
`research/next-role-topology`를 별도 복제하여 그 루트를
`chat.pluginLocations`에 등록하면 돼. 중복된 Next 플러그인
경로는 비활성화하되 안정판 v1.1.1은 그대로 둬.

**사내 코드나 로그를 외부로 옮길 필요 없어.** 새 보조 에이전트의
실제 모델, 권한, 서브에이전트 실행 경로는 별도의 통합 검증이
필요하고, 현재 정적 검사만으로는 증명되지 않아.
외부 공급자 전송은 회사 정책과 사용자 허용을 따르고,
프롬프트 자체를 샌드박스로 여기지 마.

문제가 있으면 RC2의 `chat.pluginLocations` 항목만 끄고
기존 안정판/RC1/native Copilot을 선택해.
**`main`·RC1은 변경하지 않았어.**

## 실제 역할 위임 확인은 Host에서만

독립 Copilot SDK 서버에서는 등록된 Architect를 실행하려다가 `custom_agent_prompt` Host 상호작용 미지원으로 실패했어. 이건 모델이나 Council의 실패를 뜻하지 않아. [공개 코드 기반 최소 Host 확인 절차](docs/HOST_DELEGATION_GATE.md)를 마련했지만, **반복적인 사내 테스트나 코드·로그 반출은 요구하지 않아.** 실제 Host에서 이름이 확인된 보조 에이전트의 **완료된 반환 증거**가 있어야 협업이 검증됐다고 인정할 거야.
