# Over the Luna Next 🌙 — v2.0.0-rc.1

[English](README.md) · **한국어**

**출시 후보(RC)이지 안정 버전은 아니야.** 이번 패키지는 **Over the Luna Next Main 하나**만 제공해. 의무 Council, Premium Review UI, 모델별 에이전트, 별도 API 브리지, MCP 번들, 유료 모델 자동 호출은 없어. **모델·도구·승인 권한은 VS Code Host가 관리**해.

## 안정판을 그대로 둔 채 설치하기

기본 `main`은 계속 **v1.1.1 안정판**이야. 저장소 기본 URL로 설치하면 RC가 아니라 안정판일 수 있어.

1. `release/next-v2.0.0-rc1` 브랜치의 성공한 [RC Actions](https://github.com/YB-Park/over-the-luna/actions/workflows/validate.yml?query=branch%3Arelease%2Fnext-v2.0.0-rc1)에서 `over-the-luna-next-v2.0.0-rc.1` artifact를 받아 내부 ZIP을 풀어 줘. 또는 해당 브랜치를 별도로 체크아웃하고 그 루트를 플러그인 폴더로 사용해.
2. VS Code **사용자 설정(JSON)**에서 `chat.plugins.enabled`가 허용되었는지 확인하고, 기존 설정을 지우지 말고 `chat.pluginLocations`에 RC 디렉터리의 절대 경로를 추가해.

   ```json
   {"chat.pluginLocations": {"/RC/압축을/푼/절대/경로": true}}
   ```

3. 같은 플러그인 ID가 중복되지 않도록 기존 연구용 `over-the-luna-next` 플러그인 경로는 잠시 비활성화해. **안정판 v1.1.1은 삭제하지 마.**
4. 필요한 경우 VS Code를 다시 열고 **Over the Luna Next**를 선택해. 모델은 선택기에서 고르면 돼. GPT-6 Luna는 기본 가설일 뿐 고정하지 않았어.

작업 중 실제 diff와 테스트를 검증하고, 중요한 위험에만 독립 검토를 고려해. **프롬프트 자체는 보안 샌드박스가 아니며**, 조직의 도구·MCP·권한 정책을 우회하지 않아. 사내 코드와 채팅 기록을 여기로 옮길 필요도 없어.

## 업데이트 및 롤백

v1.1.1의 Council·의무 Reviewer·Premium UI를 제거한 **호환성이 크게 바뀌는 버전**이야. 문제가 생기면 `chat.pluginLocations`에서 RC 경로만 비활성화하고 기존 **Over the Luna** 또는 기본 Copilot Agent를 선택하면 돼.

실험 근거는 [연구 브랜치](https://github.com/YB-Park/over-the-luna/tree/research/next-harness-foundation)와 [Draft PR #18](https://github.com/YB-Park/over-the-luna/pull/18)에 있어. **Next가 native Agent보다 우월하다는 증거는 아직 없어.** [출시 체크리스트](docs/RELEASE_CHECKLIST.md)를 확인해. CI는 **정적 검증과 패키징만** 실행하며 유료 모델을 호출하지 않아.
