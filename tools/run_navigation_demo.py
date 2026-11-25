"""Run a map-based MuJoCo position demo for the scoped milestone.

The mocap marker is moved in 1 m increments. MuJoCo provides the marker's
world position as a *virtual location input*, not a physical GPS receiver.
"""

from __future__ import annotations

import argparse
import json
import sys
from math import ceil, hypot
from pathlib import Path

import mujoco

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from navigation import canonical_edge, pedestrian_network, plan_route, route_distance  # noqa: E402


def run_demo(length_m: int, blocked: bool = False) -> dict[str, object]:
    positions, edges = pedestrian_network(length_m)
    closed = {canonical_edge("middle", "goal")} if blocked else set()
    route = plan_route(positions, edges, "start", "goal", closed)
    model = mujoco.MjModel.from_xml_path(str(ROOT / "scenes" / f"safe_walk_{length_m}m.xml"))
    data = mujoco.MjData(model)
    robot_id = model.body("escort_robot").id
    mocap_id = int(model.body_mocapid[robot_id])
    if mocap_id < 0:
        raise RuntimeError("The scene robot must be a mocap marker.")

    snapshots = 0
    max_location_error_m = 0.0
    off_path_snapshots = 0
    for origin, destination in zip(route, route[1:]):
        start = positions[origin]
        end = positions[destination]
        distance = hypot(end[0] - start[0], end[1] - start[1])
        steps = max(1, ceil(distance))
        for index in range(steps + 1):
            fraction = index / steps
            target_x = start[0] + fraction * (end[0] - start[0])
            target_y = start[1] + fraction * (end[1] - start[1])
            data.mocap_pos[mocap_id] = (target_x, target_y, 0.43)
            mujoco.mj_forward(model, data)
            # Simulation world coordinates stand in for a perfect location feed.
            virtual_gps = data.body("escort_robot").xpos
            error = hypot(float(virtual_gps[0]) - target_x, float(virtual_gps[1]) - target_y)
            max_location_error_m = max(max_location_error_m, error)
            if abs(float(virtual_gps[1])) > 1.12:  # path half-width 1.5 m minus 0.38 m chassis half-width
                off_path_snapshots += 1
            snapshots += 1

    actual_goal = data.body("escort_robot").xpos
    goal_error_m = hypot(float(actual_goal[0]) - positions["goal"][0], float(actual_goal[1]) - positions["goal"][1])
    passed = goal_error_m <= 1.0 and max_location_error_m <= 1.0 and off_path_snapshots == 0
    return {
        "scenario_m": length_m,
        "blocked_link": blocked,
        "route": route,
        "route_distance_m": round(route_distance(positions, route), 2),
        "position_snapshots": snapshots,
        "max_virtual_location_error_m": round(max_location_error_m, 4),
        "goal_error_m": round(goal_error_m, 4),
        "off_path_snapshots": off_path_snapshots,
        "passed": passed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, choices=(500, 2000), default=500)
    parser.add_argument("--blocked", action="store_true", help="Close the direct middle-to-goal link.")
    args = parser.parse_args()
    result = run_demo(args.length, args.blocked)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
