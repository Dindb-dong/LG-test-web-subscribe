# PROJECT CURRENT STATUS

Date: 2026-03-30

## Summary
- 구독 사용자, 사용자별 가전 목록, 가전 상세 사용 현황을 제공하는 FastAPI 기반 운영 대시보드가 구현되었습니다.
- 프론트는 토스 스타일의 단일 페이지 대시보드로 재구성되었고, Lucide 아이콘과 주간 사용량 Bar Chart를 포함합니다.
- GitHub Actions 기반 CI와 Render 배포용 설정 파일이 추가되어 요구사항 3의 자동 검증 및 CD 준비 상태를 갖췄습니다.
- 주간 사용량 차트는 고정 높이 컨테이너와 무애니메이션 설정으로 안정화되어 과도한 세로 확장과 렌더링 지연을 줄였습니다.

## Current Behavior
1. `/` 진입 시 구독자 목록을 `/api/v1/subscribers`에서 자동 조회합니다.
2. 구독자 목록은 이름, 구독 플랜, 상태, 사용자 ID 기준으로 실시간 검색되며 상태 필터를 지원합니다.
3. 특정 구독자를 선택하면 `/api/v1/subscribers/{user_id}/devices`로 가전 목록을 조회합니다.
4. 가전 목록은 타입, 모델명, 위치, 상태, 가전 ID 기준으로 실시간 검색되며 상태 필터를 지원합니다.
5. 특정 가전을 선택하면 `/api/v1/devices/{device_id}/usage`로 상세 사용 현황과 주간 사용량 차트를 표시합니다.
6. 상태 값은 요구사항 3-A 기준에 맞춰 Badge 색상으로 통일 표현됩니다.

## Architecture And Flow Notes
1. API는 `app/api/v1/` 아래에 버전 라우터로 분리되었고, 서비스 계층은 `app/services/subscription_service.py`에서 더미 데이터를 조회합니다.
2. 응답 스키마는 `app/schemas/`에 정리되어 있으며, 목록 응답은 `data`, `total`, `page`, `page_size` 형식을 따릅니다.
3. 에러 응답은 `error.code`, `error.message`, `error.details` 구조로 통일되었습니다.
4. 프론트는 정적 `HTML + CSS + JS` 조합이며, 실시간 검색/필터는 클라이언트 측에서 즉시 반영됩니다.

## Operational Notes
1. Docker 실행 기준 파일은 `compose.yaml`, `Dockerfile`, `pyproject.toml`입니다.
2. CI는 `.github/workflows/ci.yml`에서 `docker compose build`, `ruff`, `pytest`, `health`, 주요 API 확인 순으로 검증합니다.
3. Render 배포는 `render.yaml`과 `/health` 헬스체크를 기준으로 연결되도록 준비했습니다.

## Limitations And Follow-Up
1. 현재 데이터는 `app/data/dummy_data.py`의 메모리 기반 더미 데이터이며 실제 DB 연동은 아직 없습니다.
2. 프론트 상호작용은 수동 QA 케이스 문서와 API 자동 테스트로 보완되어 있으며, 브라우저 E2E 자동화는 아직 추가하지 않았습니다.
