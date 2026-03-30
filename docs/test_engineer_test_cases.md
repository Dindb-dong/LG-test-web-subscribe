# Test Engineer Test Cases

Date: 2026-03-30
Role: Test Engineer
Scope: Requirement 1, Requirement 2, Requirement 3-A/3-B/3-C

## Automated Coverage Executed
- API list response validation for subscribers
- API list response validation for subscriber devices
- API success and not-found validation for device usage
- Service-layer regression tests for valid and invalid lookups
- Dashboard shell smoke test
- Health endpoint smoke test for CI/CD readiness

## Core Test Cases

### TC-REQ1-001 Initial Subscriber Auto Load
- Objective: 첫 페이지 진입 시 구독자 목록이 자동 조회되는지 확인
- Preconditions: 서버가 정상 기동됨
- Steps:
  1. 브라우저에서 `/` 접속
  2. 네트워크 탭에서 `/api/v1/subscribers` 호출 여부 확인
  3. 테이블 첫 행과 요약 카드 값 확인
- Expected Result:
  1. 최초 진입 시 별도 클릭 없이 API가 1회 호출됨
  2. 구독자 테이블이 자동 렌더링됨
  3. 요약 카드의 전체 구독자 수와 테이블 row 수가 일치함

### TC-REQ1-002 Subscriber Search By Name
- Objective: 이름 기준 실시간 검색 동작 확인
- Preconditions: 기본 구독자 목록이 노출된 상태
- Steps:
  1. 검색창에 `Kim` 입력
  2. 결과 row 수 확인
- Expected Result:
  1. 입력 즉시 결과가 갱신됨
  2. `Kim Minsoo`만 남고 나머지 row는 숨겨짐

### TC-REQ1-003 Subscriber Search By User ID
- Objective: 사용자 ID 기준 검색 가능 여부 확인
- Steps:
  1. 검색창에 `U003` 입력
- Expected Result:
  1. `U003` 사용자가 즉시 표시됨
  2. 검색 대상에 사용자 ID가 포함됨

### TC-REQ1-004 Subscriber Status Filter
- Objective: 상태 필터가 정확히 적용되는지 확인
- Steps:
  1. 상태 필터에서 `Paused` 선택
  2. 표시된 row의 상태 badge 확인
- Expected Result:
  1. `Paused` 상태 사용자만 남음
  2. badge 색상이 파란색 계열로 표시됨

### TC-REQ2-001 Device List Load On Subscriber Click
- Objective: 특정 구독자 선택 시 해당 사용자의 가전 목록이 조회되는지 확인
- Steps:
  1. `U001` row 클릭
  2. `/api/v1/subscribers/U001/devices` 호출 확인
- Expected Result:
  1. 해당 사용자 가전 2개가 표시됨
  2. Device ID, Type, Model, Location, Status 컬럼이 모두 표시됨

### TC-REQ2-002 Empty Device List
- Objective: 가전이 없는 사용자 처리 확인
- Steps:
  1. `U005` row 클릭
- Expected Result:
  1. 오류 없이 빈 목록 응답을 처리함
  2. `No registered devices.` 메시지가 표시됨

### TC-REQ2-003 Device Search And Filter
- Objective: 가전 목록이 모델명, 타입, 위치, 상태, ID 기준으로 실시간 검색되는지 확인
- Steps:
  1. `U003` 선택
  2. 가전 검색창에 `Office` 입력
  3. 상태 필터를 `Online`으로 설정
- Expected Result:
  1. `LG Whisen` 1건만 표시됨
  2. 필터 결과가 입력 즉시 반영됨

### TC-REQ2-004 Device Usage Detail Load
- Objective: 가전 선택 시 상세 사용 현황이 표시되는지 확인
- Steps:
  1. `U001` 선택
  2. `D001` 선택
  3. `/api/v1/devices/D001/usage` 호출 확인
- Expected Result:
  1. Device ID, Device Name, Power Status, Last Used, Total Usage Hours, Weekly Usage Count, Health Status, Remark가 표시됨
  2. 주간 사용량 Bar Chart가 렌더링됨

### TC-REQ2-005 Invalid Device API Regression
- Objective: 존재하지 않는 디바이스 요청 시 표준 에러 응답이 반환되는지 확인
- Steps:
  1. `/api/v1/devices/D999/usage` 호출
- Expected Result:
  1. HTTP 404 반환
  2. `error.code = NOT_FOUND` 구조 유지

### TC-REQ3-001 Badge Color Mapping
- Objective: 상태별 badge 색상 규칙이 요구사항과 일치하는지 확인
- Steps:
  1. Subscriber status와 Device status, Usage status를 각각 확인
- Expected Result:
  1. `Active / Online / Normal`은 초록
  2. `Paused / Standby`는 파랑
  3. `Expired / Error / Warning`은 빨강
  4. `Offline`은 회색

### TC-REQ3-002 CI Workflow Trigger
- Objective: GitHub Actions CI가 push, pull_request에서 자동 실행되도록 설정되었는지 확인
- Steps:
  1. `.github/workflows/ci.yml` 확인
  2. `on.push`, `on.pull_request` 확인
- Expected Result:
  1. push와 PR 모두에서 워크플로우가 실행되도록 정의됨
  2. build, lint, test, health, core API check 단계가 포함됨

### TC-REQ3-003 Render Deployment Readiness
- Objective: Render 연동을 위한 배포 설정이 준비되었는지 확인
- Steps:
  1. `render.yaml` 확인
  2. `/health` 엔드포인트 확인
- Expected Result:
  1. Docker 기반 웹 서비스 설정이 존재함
  2. healthCheckPath가 `/health`로 연결됨
  3. GitHub checks 통과 후 자동 배포를 위한 `autoDeployTrigger: checksPass`가 설정됨

## Execution Notes
- 자동 테스트는 `docker compose run --rm app uv run ruff format --check .`, `docker compose run --rm app uv run ruff check .`, `docker compose run --rm test` 기준으로 실행합니다.
- 브라우저 상호작용은 현재 수동 QA 케이스로 상세화했으며, 필요 시 이후 Playwright E2E로 확장할 수 있습니다.
