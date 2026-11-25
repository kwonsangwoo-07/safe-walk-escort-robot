# 야간 보행자 동행 로봇

## 프로젝트 목표
일몰 무렵부터 일출 전까지, 어둡거나 인적이 드문 지정 보행 구간을 순찰하며 요청한 보행자와 동행하는 로봇을 설계합니다.

## 이용 상황
지하철역, 버스정류장 또는 큰 대로에서 주거 구간으로 이동하는 야간 보행자를 대상으로 합니다. 집이 순찰 경로 안에 있으면 집 앞까지, 경로 밖에 있으면 지정된 종료 지점까지 동행합니다.

## 전체 서비스 구상
- 지정 보행 구간 왕복 순찰
- 스마트폰 또는 구간 내 호출 버튼을 통한 동행 요청
- 보행자와 동행하며 통행을 방해하지 않도록 이동
- 비상 버튼 작동 시 112와 운영 상황실에 동시에 긴급 신호 전달

## 현재 개발 범위
이번 단계는 **보행 경로 탐색, 통행 불가 연결 회피, MuJoCo 가상 위치 확인과 목표 지점 도착**입니다. 스마트폰·호출 버튼·112·상황실 연동은 후속 단계입니다. [개발 범위와 완료 기준](docs/development-scope.md)에 이번 단계와 전체 로봇의 완료 기준을 구분했습니다.

## 현재 작업물

- [D01 문제 정의서](docs/problem.md): 대표 사용자, 현재 귀가 흐름, 불편의 숫자와 근거, 로봇이 맡는 단계
- [D03 요구사항 명세](docs/requirements.md): 요구사항 계층, 수치 목표, 우선순위, 판정 방법
- [개발 범위와 완료 기준](docs/development-scope.md): 이번 단계의 합격 조건과 단계별 확인 방법
- [03 Design 초안](docs/design.md): 시스템 구조, 장면 구성, 안전 개념
- [MuJoCo 500m 장면](scenes/safe_walk_500m.xml), [2km 장면](scenes/safe_walk_2000m.xml): 첫 배치 장면 v0
- [판정 코드](src/judge.py)와 [판정 테스트](tests/test_judge.py)
- [경로 탐색](src/navigation.py), [MuJoCo 이동 시연](tools/run_navigation_demo.py), [핵심 기능 테스트](tests/test_navigation.py)
- [로봇 형태 비교](docs/robot-form-options.md): 바퀴형·사족형·이족형 구상 이미지와 선택 기준

## 실행

```powershell
uv sync --group dev
uv run pytest -q tests
uv run python tools/build_scenes.py
uv run pytest -q tests/test_navigation.py
uv run python tools/run_navigation_demo.py --length 500
uv run python tools/run_navigation_demo.py --length 500 --blocked
uv run python tools/run_navigation_demo.py --length 2000
uv run python tools/run_navigation_demo.py --length 2000 --blocked
uv run python -m mujoco.viewer --mjcf=scenes/safe_walk_500m.xml
```

2km 장면을 보려면 마지막 명령의 파일명을 `safe_walk_2000m.xml`로 바꿉니다. `--blocked`는 통행 불가 연결을 미리 알려주는 시험 조건입니다. 시연 결과의 `passed`는 경로·위치·도착의 **1차 시뮬레이션 판정**이며 실제 GPS, 장애물 자동 감지, 바퀴 구동, 충돌 안전을 입증하지 않습니다. 로봇 형태는 아직 미정이며 XML의 4바퀴는 임시 외형입니다.
