# Human-in-the-loop Form Workflow Demo

채용 플랫폼의 실제 계정이나 데이터를 건드리지 않고, **문서 → 구조화된 payload → 화면 구조 확인 → 입력 계획 → 값 검증 → 사람 최종 확인** 흐름을 재현하는 공개용 데모입니다.

이 저장소는 실제 지원 자동화 코드를 공개한 것이 아닙니다. 공개 저장소에는 가짜 데이터와 로컬 가짜 입력 화면만 포함합니다. 저장·지원·삭제는 자동화하지 않습니다.

## 데모 실행

Python 3.10+만 필요합니다.

```bash
python scripts/run_demo.py
python -m unittest discover -s tests -v
```

브라우저에서 `demo/index.html`을 열면 동일한 흐름을 직접 확인할 수 있습니다.

1. `examples/payload.sample.json`을 읽습니다.
2. `examples/form_snapshot.sample.json`의 필드와 payload를 매핑합니다.
3. 입력 계획과 민감 동작 차단 결과를 출력합니다.
4. 로컬 화면에 값만 채우고, 화면의 값이 payload와 일치하는지 확인합니다.
5. 저장·지원 버튼은 비활성화되어 있으며 사용자가 직접 확인해야 합니다.

## 구조

```text
src/form_workflow.py       # payload/snapshot 검증과 입력 계획
scripts/run_demo.py        # 의존성 없는 재현용 CLI
demo/index.html            # 외부 사이트가 아닌 로컬 가짜 입력 화면
examples/                  # 가짜 회사·가짜 지원자 데이터
tests/                     # 중복 필드, 누락 필드, 검증 실패 테스트
docs/                      # 아키텍처와 안전 정책
```

## 공개 범위

포함한 것은 공개 검토에 필요한 일반화된 구조뿐입니다.

- payload 생성·검증의 순수 로직
- Form Snapshot의 필드 계약 예시
- selector mapping과 dry-run 계획
- 입력 후 값 검증
- 가짜 데이터와 재현 가능한 테스트

포함하지 않은 것:

- 실제 채용 플랫폼 URL, 회사명, 지원자 정보
- 실제 payload, form snapshot, 실행 로그
- 쿠키·세션·브라우저 프로필·비밀번호·OTP
- 로컬 플랫폼용 selector 파일이나 private endpoint 호출
- 저장·지원 버튼 자동 클릭 코드

## 설계 원칙

- 화면 구조를 먼저 확인하지 못하면 입력하지 않습니다.
- 필드가 없거나 중복으로 매칭되면 입력 계획을 중단합니다.
- 자동화 결과를 제출 성공으로 해석하지 않습니다.
- 입력 후 값 검증과 사람의 최종 검수를 분리합니다.
- 실제 업무에서 얻은 수치나 회사 자산은 이 공개 데모의 근거로 사용하지 않습니다.

## 면접에서 보여줄 수 있는 것

이 데모는 “AI가 대신 지원했다”가 아니라, 비정형 문서를 작업 단위로 정규화하고, 실행 전 화면 계약을 확인하며, 실패 시 멈추는 **Human-in-the-loop Workflow**를 보여줍니다. 실제 플랫폼 어댑터와 인증 정보는 공개하지 않고도 이 설계·안전 경계를 재현할 수 있습니다.
