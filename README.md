# safe-walk-escort-robot
야간 보행자 및 우범지대, 통행량이 적은 구역의 안전을 담당하는 로봇 프로젝트
# 야간 보행자 동행 로봇

## 프로젝트 목표
일몰 무렵부터 일출 전까지, 어둡거나 인적이 드문 지정 보행 구간을 순찰하며 요청한 보행자와 동행하는 로봇을 설계한다.

## 이용 상황
지하철역, 버스정류장 또는 큰 대로에서 주거 구간으로 이동하는 야간 보행자를 대상으로 한다. 집이 순찰 경로 안에 있으면 집 앞까지, 경로 밖에 있으면 지정된 종료 지점까지 동행한다.

## 주요 기능
- 지정 보행 구간 왕복 순찰
- 스마트폰 또는 구간 내 호출 버튼을 통한 동행 요청
- 보행자와 동행하며 통행을 방해하지 않도록 이동
- 비상 버튼 작동 시 112와 운영 상황실에 동시에 긴급 신호 전달

## 현재 단계
문제 정의와 요구사항을 정리하고, 로봇 구조·안전 개념·시뮬레이션 장면을 설계 중이다. 기능과 효과는 아직 검증 전이다.

## 현재 작업물

- [D01 문제 정의서](docs/problem.md): 대표 사용자, 현재 귀가 흐름, 불편의 숫자와 근거, 로봇이 맡는 단계
- [D03 요구사항 명세](docs/requirements.md): 요구사항 계층, 수치 목표, 우선순위, 판정 방법
- [03 Design 초안](docs/design.md): 시스템 구조, 장면 구성, 안전 개념
- [MuJoCo 500m 장면](scenes/safe_walk_500m.xml), [2km 장면](scenes/safe_walk_2000m.xml): 첫 배치 장면 v0
- [판정 코드](src/judge.py)와 [판정 테스트](tests/test_judge.py)
- [로봇 형태 비교](docs/robot-form-options.md): 바퀴형·사족형·이족형 구상 이미지와 선택 기준

## 실행

```powershell
uv sync --group dev
uv run pytest -q tests
uv run python tools/build_scenes.py
uv run python -m mujoco.viewer --mjcf=scenes/safe_walk_500m.xml
```

2km 장면을 보려면 마지막 명령의 파일명을 `safe_walk_2000m.xml`로 바꾼다. 장면 v0는 도로·보행로·로봇·보행자·버튼의 배치를 보여준다. **로봇 형태는 아직 미정이며, XML의 4바퀴는 임시 외형이다.** 자율 주행과 실제 112 연동은 아직 구현되지 않았다.
