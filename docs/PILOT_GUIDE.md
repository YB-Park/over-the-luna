# Over the Luna Next RC2 — 제한적 실사용 파일럿

> **파일럿 후보이지 안정판 출시는 아닙니다.** main v1.1.1과 RC1은 그대로 보존합니다.
> 실제 VS Code Host가 RC2 역할 8개를 읽는 것은 확인했지만, 명명된 Architect/Reviewer의 성공적 실행은 아직 검증하지 못했습니다.

## 지금 사용 가능한 범위

- **PILOT DIRECT:** Copilot Host에서 Over the Luna Next Main을 선택해 허가된 프로젝트의 낮은 위험도 작업을 수행합니다. 정확한 요구사항, 변경 diff, 실행한 테스트를 확인하며, 필요하면 즉시 기본 Copilot/기존 안정판으로 돌아갑니다.
- **PILOT COUNCIL EXPERIMENTAL:** 실제로 하위 역할 호출이 **완료**되고 별도 증거가 반환될 때만 그 역할의 기여를 인정합니다. 에이전트 등록, 호출 시도 또는 Main의 자기 보고는 독립 검증이 아닙니다.
- 승인된 사내 작업에 쓰는 경우에도 조직의 플러그인·모델·도구·데이터 정책을 우선합니다. 승인되지 않은 외부 공급자, BYOK, 프롬프트/로그 외부 전송을 금지합니다.

## 설치 (사용자가 직접, 원복 가능)

1. 공개 저장소 `YB-Park/over-the-luna`의 **research/next-role-topology** 브랜치에서 최신 성공한 **Validate Next role topology (no model calls)** GitHub Actions를 열어 `over-the-luna-next-rc2-topology` 아티팩트를 받습니다. 아티팩트 안의 `over-the-luna-next-rc2-topology.zip`을 별도 폴더에 풉니다. 압축 해제 폴더의 **루트**에 `plugin.json`과 `agents/`가 있어야 합니다. 이 배포는 공개 안정 릴리스가 아닙니다.
2. 가능하면 같은 연구 커밋의 `scripts/pilot_archive.py`로 ZIP을 사전 검사합니다: `python scripts/pilot_archive.py --archive /path/to/over-the-luna-next-rc2-topology.zip`. 성공은 **패키지 무결성·범위**만 뜻하며, 실제 모델 사용 권한까지 보장하지 않습니다.
3. VS Code의 **User settings.json**에서 플러그인 지원이 허용된 경우 아래처럼 등록합니다. 경로는 압축을 푼 폴더의 **절대 경로**로 바꿉니다. 기존 설정값을 보존하고 객체 키만 추가하세요.

```json
{
  "chat.plugins.enabled": true,
  "chat.pluginLocations": {
    "/ABSOLUTE/PATH/over-the-luna-next-rc2": true
  }
}
```

4. 기존 RC1 등 **같은 `over-the-luna-next` 플러그인 ID의 중복 경로만** 비활성화하고 안정판 v1.1.1은 제거하지 않습니다. Copilot에 정상 로그인됐는지 확인한 뒤, **Copilot harness**의 새 세션에서 `Over the Luna Next`와 사용 승인된 Main 모델을 선택합니다. Local harness의 `runSubagent`와 혼동하지 마세요.
5. 모델·도구·플러그인 설정이 조직 정책으로 잠겨 있거나 선택 메뉴에 없다면 설정을 우회하지 말고 파일럿을 중단합니다. 활성화만으로 호스트 권한·모델 사용을 검증했다고 볼 수 없습니다.

공식 설정 가이드: https://code.visualstudio.com/docs/agent-customization/agent-plugins 및 https://code.visualstudio.com/docs/agents/reference/ai-settings

## 30분 내 최초 사용 결정 — 직접 확인할 수 있는 증거

| 단계 | 실제 작업 | 합격 또는 판정 |
| --- | --- | --- |
| A: 설치 | `Over the Luna Next`를 Copilot harness에서 선택 | 플러그인 인식. **실행 성공은 아직 아님** |
| B: 직접 처리 | 공개 샘플/승인된 낮은 위험 작업에서 작은 수정 또는 코드 설명 | Main 실제 응답, 변경 diff 및 관련 테스트 확인 → `PILOT_DIRECT_OK` |
| C: 복잡한 조사 | 공개 저장소에서 2개 이상의 모듈 사이의 실제 계약을 조사하도록 요청 | Next Architect의 **별도 작업 완료·반환 근거**가 있을 때만 `PILOT_HANDOFF_OK`; 그렇지 않으면 `NAMED_DELEGATION_UNAVAILABLE` |
| D: 변경 후 검토 | 실제 의미 있는 수정과 테스트 결과가 있을 때 Next Reviewer에게 검토 요청 | **실제 diff + 독립 완료 결과**가 있으면 `PILOT_REVIEW_OK`; 없으면 `REVIEW_UNVERIFIED` |

**절대로 하지 말 것:** 성공한 서브에이전트가 없는데 리뷰가 끝났다고 말하기, 검증되지 않은 권한 제한을 보안 장벽으로 취급하기, 단순 동작을 확인하려고 Sol/Sonnet을 자동 호출하기, 회사 소스·로그·민감 정보를 공개 Actions로 옮기기.

## 위험도와 출시 판단 (완벽주의 대신 엄격한 구분)

**단계 1 — 개인/소수 사용자 opt-in 파일럿:** 패키지 검사와 실제 Copilot Main 직접 수행에 성공하고, 철회/원복이 가능하면 낮은 위험도에 한해 시작할 수 있습니다. 독립 Council 협업은 성공하기 전까지 **미검증 기능**입니다. 중요한 인증, 데이터 이전, 배포, 고객 정보, 보안 변경에는 검증되지 않은 독립 검토를 대체품으로 쓰지 않습니다.

**단계 2 — 제한적 실무 베타 결정:** 승인된 환경에서 (a) Main 직접 처리, (b) 실제 Architect 증거 반환, (c) 실제 diff에 대한 Reviewer 완료를 각각 관찰하고, **세 가지 이상의 의미 있는 실사용 과제**에서 요구사항·테스트·권한 위반 여부를 기록합니다. 중대한 권한/데이터 위반이 하나라도 있으면 베타를 확대하지 않습니다. 일부 사소한 사용성 이슈는 기록하고 후속 개선할 수 있습니다.

**단계 3 — 공개 안정판 후보:** 실무 베타의 심각한 차단 문제 해결, 주요 실패·복구 시나리오 검증, 사용 정책·비용·업그레이드·원복 문서화, 보호된 브랜치에 대한 별도 출시 승인. **100% 완벽이나 모든 모델 조합 벤치마크는 조건이 아닙니다.**

## 사용 후기: 외부 반출 없이 로컬에서만 기록

과제마다 `직접/Architect/Reviewer 사용`, `실제 반환 여부`, `변경 요구사항 충족`, `테스트`, `재작업 여부`, `추가 비용 체감`, `미검증 위험`만 로컬에 적으면 충분합니다. 코드, 전체 대화, 디프, 인증 키, 사내 경로, 로그를 이 연구 저장소에 올릴 필요가 없습니다. 필요하면 `PILOT_DIRECT_OK`, `PILOT_HANDOFF_OK`, `PILOT_REVIEW_OK`, `BLOCKED`, `REVIEW_UNVERIFIED` 같은 상태 단어만 자발적으로 공유할 수 있습니다.

## 즉시 원복

User `chat.pluginLocations`에서 해당 파일럿 절대 경로의 값을 `false`로 바꾸거나 항목을 삭제하고, 에이전트를 기본 Copilot 또는 기존 안정판으로 전환합니다. 플러그인 전역 스위치 `chat.plugins.enabled`는 기존에 쓰던 다른 플러그인이 있다면 건드리지 않습니다. 기존 코드 변경은 별도로 Git diff를 확인하고 수동으로 유지·폐기합니다. **플러그인을 끄는 것만으로 코드 변경이 자동 취소되지는 않습니다.**

**제한:** P16 실제 Host 8/8 등록은 성공, P17 첫 턴에서 `chat/error` 발생, P18 임시 GitHub Actions Host 모델 카탈로그는 0개. 이 결과는 로그인된 사용자의 VS Code 사용 가능성을 부정하지도, Council 정상 동작을 증명하지도 않습니다.
