# Human-in-the-loop Form Workflow + Loop Engineering Demo

채용 플랫폼의 실제 계정이나 데이터를 건드리지 않고, **문서 → 구조화된 payload → 화면 구조 확인 → 입력 계획 → 값 검증 → 사람 최종 확인** 흐름을 재현하는 공개용 데모입니다. 여기에 **정상 실행과 반복 실패 분석을 분리하는 Loop Engineer 계층**을 추가했습니다.

이 저장소는 실제 지원 자동화 코드를 공개한 것이 아닙니다. 공개 저장소에는 가짜 데이터와 로컬 가짜 입력 화면만 포함합니다. 저장·지원·삭제는 자동화하지 않습니다.

## 데모 실행

Python 3.10+만 필요합니다.

```bash
python scripts/run_demo.py
python scripts/run_loop_demo.py
python -m unittest discover -s tests -v
```

브라우저에서 `demo/index.html`을 열면 동일한 흐름을 직접 확인할 수 있습니다.

1. `examples/payload.sample.json`을 읽습니다.
2. `examples/form_snapshot.sample.json`의 필드와 payload를 매핑합니다.
3. 입력 계획과 민감 동작 차단 결과를 출력합니다.
4. 로컬 화면에 값만 채우고, 화면의 값이 payload와 일치하는지 확인합니다.
5. 저장·지원 버튼은 비활성화되어 있으며 사용자가 직접 확인해야 합니다.

Loop Engineering 데모는 정상 PASS를 수집하지 않습니다. `WARN/REVISE/FAIL`, 사용자의 PASS 이의 제기, 모델 간 판정 충돌, 반복 수정만 관찰 후보로 만들고, 검토된 결정 없이 실행 하네스의 규칙을 자동 변경하지 않습니다.

## 구조

```text
src/form_workflow.py       # payload/snapshot 검증과 입력 계획
src/loop_engineer.py       # 이상 신호 선별·중복 제거·검토 분류
scripts/run_demo.py        # 의존성 없는 재현용 CLI
scripts/run_loop_demo.py   # 정상 PASS와 disputed PASS 비교
demo/index.html            # 외부 사이트가 아닌 로컬 가짜 입력 화면
examples/                  # 가짜 회사·가짜 지원자 데이터
tests/                     # 실행 계약과 Loop 포착 경계 테스트
docs/                      # 아키텍처·안전 정책·Loop Engineering 설명
```

## 공개 범위

포함한 것은 공개 검토에 필요한 일반화된 구조뿐입니다.

- payload 생성·검증의 순수 로직
- Form Snapshot의 필드 계약 예시
- selector mapping과 dry-run 계획
- 입력 후 값 검증
- 정상 PASS와 이상 신호를 분리하는 관찰 정책
- 사용자 이의 제기와 반복 수정의 일반화된 inbox record
- 중복 제거와 `ONE_OFF/PATTERN/EXPECTED/INSUFFICIENT_EVIDENCE` 분류
- 가짜 데이터와 재현 가능한 테스트

포함하지 않은 것:

- 실제 채용 플랫폼 URL, 회사명, 지원자 정보
- 실제 payload, form snapshot, 실행 로그
- 실제 사용자 이의 제기, 모델 대화, 실패 이력
- 쿠키·세션·브라우저 프로필·비밀번호·OTP
- 로컬 플랫폼용 selector 파일이나 private endpoint 호출
- 저장·지원 버튼 자동 클릭 코드

## 설계 원칙

- 화면 구조를 먼저 확인하지 못하면 입력하지 않습니다.
- 필드가 없거나 중복으로 매칭되면 입력 계획을 중단합니다.
- 자동화 결과를 제출 성공으로 해석하지 않습니다.
- 입력 후 값 검증과 사람의 최종 검수를 분리합니다.
- 검사 PASS를 그 검사가 확인하지 않은 의미·근거의 PASS로 확대하지 않습니다.
- 반복 실패가 생겨도 즉시 규칙을 추가하지 않고 바깥 Loop에서 원인과 회귀 영향을 확인합니다.
- Loop 관찰은 규칙 변경 권한이 아니며, 검토된 결정 전에는 하네스를 수정하지 않습니다.
- 실제 업무에서 얻은 수치나 회사 자산은 이 공개 데모의 근거로 사용하지 않습니다.

## 면접에서 보여줄 수 있는 것

이 데모는 “AI가 대신 지원했다”가 아니라, 비정형 문서를 작업 단위로 정규화하고, 실행 전 화면 계약을 확인하며, 실패 시 멈추는 **Human-in-the-loop Workflow**를 보여줍니다. 또한 테스트를 통과하는 것과 실제 사용 품질이 같은지 의심하고, 반복 실패만 외부 관찰 루프로 보내 최소 수정과 회귀 검증을 거치는 **Harness Engineering → Loop Engineering 확장**을 재현합니다.

자세한 설계는 [아키텍처](docs/ARCHITECTURE.md), [안전 정책](docs/SAFETY_POLICY.md), [Loop Engineering](docs/LOOP_ENGINEERING.md)에서 확인할 수 있습니다.
