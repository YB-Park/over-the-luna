# Over the Luna — Next Harness Research Charter

> **Product first, experiments only to make a product decision.**  
> Status: research / not a release | Started: 2026-10-16 | Stable baseline: `main` v1.1.1

## Mission

이미 뛰어난 LLM의 능력을 더 잘 활용하는 **실용적인 VS Code / GitHub Copilot 하네스**를 만든다. Luna의 경제성을 기본으로 활용하되, Sol·Haiku·Sonnet 등 다른 모델의 가치가 확인되면 그 근거가 있는 작업에 선택적으로 사용한다. 목표는 최대 에이전트 수나 최소 토큰이 아니라 **완료된 작업의 유효한 품질, 예측 가능한 비용, 적은 사용자 마찰**이다.

> Luna-first, not Luna-only. Evidence-led, not experiment-led.

## Non-goals

- 프롬프트만으로 모델의 근본적인 지능이 크게 향상된다고 주장하지 않는다.
- 모델별 에이전트를 미리 늘리지 않는다. 새 역할에는 독립적인 효과에 대한 증명 책임이 있다.
- 실험 플랫폼 자체를 제품으로 만들지 않는다. 대형 벤치마크·자동 라우터는 필요해지기 전까지 만들지 않는다.
- 현재의 `main` 안정 계약을 연구 과정에서 바꾸지 않는다.
- 비용 상한 비율이나 최적 조합을 데이터 없이 미리 고정하지 않는다.
- 기존 VS Code/Copilot 권한·조직 정책·MCP 제한을 우회하지 않는다.

## Durable product constraints

1. **Parallelize thinking; serialize mutation.** 외부 상태 변경은 명시적 승인 및 단일 실행 책임 경계 안에서만 한다. read-only 리서치에는 불필요한 돌연변이 규칙을 강제하지 않는다.
2. **Main owns the work, not all the thinking.** Main의 모델이 항상 Luna여야 한다는 전제는 검증 가능한 가설로 둔다.
3. **Small tasks remain small.** 명확한 작업에 보조 에이전트를 자동으로 덧붙이지 않는다.
4. **Independent evidence, not self-confidence.** 성공 여부는 실질 수용 기준/테스트/출처로 판정한다. Reviewer의 PASS는 절대적 정답이 아니다.
5. **Cost = full trajectory.** 기본 토큰 단가가 아니라 완료까지의 재시도·도구·캐시·보조 호출·지연을 포함한다. Haiku의 비용 꼬리 위험을 별도 관찰한다.
6. **Human attention is a budget.** 지능을 더 쓰는 것과 상태 설명을 더 많이 표시하는 것은 다르다.
7. **Runtime observed > prompt declared.** 모델/effort/위임/도구 상속/승인은 Copilot Agent Host 실사용에서 확인한다.
8. **No automatic paid experiments.** AI Credits를 쓰는 작업은 사용자 승인 후 의도적인 일회성 트리거 또는 수동 실행만 허용하고 예산을 둔다. CLI의 AI Credits 한도는 소프트 한도라 청구 절대 상한을 보장하지 않는다. Secrets는 채팅·코드에 기록하지 않는다.

## Decision questions, in order

| ID | Decision needed | Minimal evidence | Status |
| --- | --- | --- | --- |
| D0 | 현재 인증·모델·도구·추론 설정이 Agent Host/Copilot CLI에서 실행되는가? | static pair, small authenticated smoke and runtime trace | STATIC PASS / paid not run |
| D1 | Native Copilot Agent 대비 GPT-6 Luna harness가 무엇을 개선하는가? | 동일 작업의 direct vs harness 비교 | PENDING |
| D2 | 어떤 일에 다른 모델/독립 검증이 값을 하는가? | 실패/고위험 작업만 소규모 paired ablation | PENDING |
| D3 | 고정 Luna Main보다 작업별 강한 Main이 이득인가? | 가치가 예상되는 작업의 직접 A/B | PENDING |
| D4 | Agent Host 중심 배포가 현재 Local 호환성보다 나은가? | plugin + MCP + subagent + reasoning-effort live gates | PENDING |

## Operating sequence (not a rigid calendar)

- **Phase 0 — no-credit preflight**: 기존 5.6 계약을 보존한 control과 GPT-6 Luna model-only candidate를 생성·diff 확인한다. 기존 validator도 통과시킨다. 이는 **실제 LLM 품질 시험이 아님**.
- **Phase 0b — manual runtime authorization**: GitHub Copilot 계정·모델 정책/토큰 문제를 해결한 후 소액·수동 smoke. 네 가지 모델 가용성, actual agent model/effort, subagent, MCP, permissions를 관찰한다. 실패하면 Phase 1을 시작하지 않는다.
- **Phase 1 — useful baseline**: native Copilot Agent vs Luna-6-only harness. 구현·리뷰·리서치·반복 작업의 소수 대표 사례. 적절한 validator/ground truth를 작업별로 적용한다.
- **Phase 2 — targeted ablation**: 발견된 약점에 대해서만 Haiku, Sol, Sonnet, reasoning effort, reviewer/architect 분리의 **한 변수씩** 추가한다. strong-first vs escalation도 필요할 때 비교한다.
- **Phase 3 — actual dogfood**: 코드 외 작업 포함. 사용성·권한·지연·작업당 총비용을 본 뒤 필요한 것만 제품에 남긴다.

## Run-level evidence minimum

Each meaningful run should record: date/runtime/version, task/acceptance, control vs candidate and *one changed variable*, actual model and reasoning effort **verified or unknown**, exact tool/agent invocations, cost or AI Credits **with source or unknown**, time, result checked externally, material failure, user intervention, and decision.

Do not treat a small sample's P95 as a stable estimate; capture surprising high-cost traces qualitatively until repetitions justify distributional metrics.

## Stop / simplify rules

- 의사결정이 달라질 근거가 없으면 실험하지 않는다.
- 런타임이 요청 모델을 실행하지 않았거나 policy/auth 오류가 나면 성능 점수로 채점하지 않는다.
- 작고 불확실한 품질 차이보다 단순한 구성을 우선한다. 강한 이점 또는 위험 감소가 있으면 비용 증가도 허용한다.
- 반복되는 통과만 확인되거나 충분히 결론을 내렸다면 중단하고 실제 사용에 투입한다.
- 새 역할/모델 경로가 뚜렷한 이점을 보이지 못하면 제거한다.
- 불변 조건 위반·예상 밖 원격 쓰기·비용 제어 실패는 즉시 중단한다.

## Decision log (append decisions, not a diary)

- **2026-10-16 — Start**: `main` v1.1.1 보존. 연구 브랜치에서 Phase 0 model-only 정적 비교를 준비한다. Premium Review 제거, multi-model routing, Agent Host-only 전환은 **아직 제품 결정이 아니다**.
- **2026-10-16 — Phase 0 PASS**: [no-credit model-only preflight](https://github.com/YB-Park/over-the-luna/actions/runs/38833915882) 와 [기존 plugin validator](https://github.com/YB-Park/over-the-luna/actions/runs/38833915766) 모두 통과. GPT-6가 실제 실행됐다는 의미는 아니다.
- **2026-10-16 — Copilot CLI P0b partial PASS**: [one-shot GPT-6 Luna request](https://github.com/YB-Park/over-the-luna/actions/runs/38836438484) used `GITHUB_TOKEN` with `copilot-requests: write`, returned the exact expected response. Auth/response PASS; observed model ID was unavailable in CLI JSONL, so that gate is INCONCLUSIVE. The first attempt with 2 credit cap failed at flag validation (CLI minimum 30); no inference occurred there. Copilot Agent Host and plugin runtime remain untested.
- **2026-10-16 — Known blocker**: 이전 `research/gpt6-luna-model-qualification`의 Copilot 인증 실험은 authentication/policy 오류로 실패했다. 모델 성능 실패가 아니다. 실제 유료 호출 전에 별도로 확인한다.

## Reference assets

- Stable contract: [DESIGN](DESIGN.md), [SMOKE_TEST](SMOKE_TEST.md).
- Existing model-only qualification: `research/gpt6-luna-model-qualification/experiments/gpt6_luna/`.
- Next experiment instructions: [experiments/next/README.md](../experiments/next/README.md).

**Release rule:** 연구 변경은 증거가 확보되고 사용자 경험에 가치가 확인되기 전에는 `main`에 병합하지 않는다.
