# 개발 범위와 단계별 완료 기준

## 이번에 완성할 범위

첫 개발 단계는 **지정된 보행로에서 길을 찾고, 위치를 확인하고, 통행할 수 없는 연결을 피해 목적지에 도착하는 시뮬레이션 시연**입니다. 500 m와 2,000 m는 지역별 실제 거리를 대표하기 위한 시험 조건입니다. 막힌 구간은 시험 시나리오가 미리 알려줍니다.

로봇은 현재 MuJoCo의 **mocap 표지**입니다. 시연 코드는 표지를 경로 위에서 옮기며 MuJoCo 세계 좌표를 가상 위치값으로 다시 읽습니다. 따라서 위치 처리와 경로 전환을 확인할 수 있지만, 바퀴 구동·실제 GPS·장애물 센서·실시간 자율 주행의 완성으로 해석하지 않습니다.

## 고장 위치를 찾기 위한 단계

| 단계 | 작업 | 실행·합격 기준 | 실패 시 먼저 확인할 부분 |
| --- | --- | --- | --- |
| 1. 장면 | 500 m와 2,000 m XML 생성·로딩 | 두 장면이 MuJoCo에서 열립니다. | `tools/build_scenes.py`, `scenes/` |
| 2. 경로 | 보행 연결만 사용해 최단 경로 탐색 | 정상·차단·경로 없음 시험이 통과합니다. | `src/navigation.py` |
| 3. 위치 | MuJoCo 표지 좌표를 가상 위치값으로 읽기 | 위치 기록이 유한하고 목표 지점 오차가 1 m 이하입니다. | `tools/run_navigation_demo.py` |
| 4. 통합 | 정상·차단 × 500 m·2,000 m | 네 조건 모두 `passed: true`입니다. | 단계 1→3 결과 순서대로 확인 |

## 직접 실행

저장소 최상위 폴더에서 실행합니다.

```powershell
uv sync --group dev
uv run python tools/build_scenes.py
uv run pytest -q tests/test_navigation.py
uv run python tools/run_navigation_demo.py --length 500
uv run python tools/run_navigation_demo.py --length 500 --blocked
uv run python tools/run_navigation_demo.py --length 2000
uv run python tools/run_navigation_demo.py --length 2000 --blocked
```

`--blocked`는 중간 지점에서 끝 지점으로 가는 직접 연결을 닫고, 같은 보행로 안의 다른 연결로 우회하도록 합니다. 현재 차단 여부는 **미리 제공된 정보**이며 로봇이 스스로 감지한 결과가 아닙니다. 출력의 `route`, `goal_error_m`, `off_path_snapshots`, `passed`를 함께 확인합니다.

## 전체 프로젝트와의 관계

| 단계 | 목표 | 지금 상태 |
| --- | --- | --- |
| A. 이동 핵심 시연 | 지도에 표시된 보행 연결 탐색, 가상 위치 확인, 차단 구간 우회, 도착 | 이번 개발 범위 |
| B. 동적 이동 | 실제 구동 모델, 센서 기반 장애물 발견, 사람과의 간격, 충돌·정지 시험 | 후속 범위 |
| C. 동행 서비스 | 사용자 호출, 보행자 위치 파악, 동행 시작·종료, 대기·배차 | 후속 범위 |
| D. 현장 연동 | 실제 GPS·지도, 스마트폰·버튼, 운영 상황실, 긴급 신고 절차, 현장 안전 검증 | 후속 범위 |

**이번 제출의 완료는 A 단계의 네 시나리오가 재현 가능한 상태**를 의미합니다. 전체 로봇의 완성은 B~D 단계까지 별도의 검증을 마친 뒤 판단합니다. 기능을 추가할 때에는 먼저 해당 단계의 합격 기준과 실패 사례를 만들고 다음 단계로 넘어갑니다.
