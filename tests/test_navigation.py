"""Acceptance checks for route selection and the scoped MuJoCo demo."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from run_navigation_demo import run_demo  # noqa: E402
from navigation import canonical_edge, pedestrian_network, plan_route  # noqa: E402


@pytest.mark.parametrize("length", [500, 2000])
def test_normal_route_uses_direct_pedestrian_link(length):
    positions, edges = pedestrian_network(length)
    assert plan_route(positions, edges, "start", "goal") == ["start", "middle", "goal"]


@pytest.mark.parametrize("length", [500, 2000])
def test_blocked_direct_link_uses_open_detour(length):
    positions, edges = pedestrian_network(length)
    route = plan_route(positions, edges, "start", "goal", {canonical_edge("middle", "goal")})
    assert route == ["start", "middle", "detour_middle", "detour_goal", "goal"]


def test_no_route_fails_explicitly():
    positions, edges = pedestrian_network(500)
    with pytest.raises(ValueError, match="No traversable"):
        plan_route(positions, edges, "start", "goal", {canonical_edge("start", "middle")})


@pytest.mark.parametrize("length,blocked", [(500, False), (500, True), (2000, False), (2000, True)])
def test_mujoco_virtual_location_reaches_goal(length, blocked):
    result = run_demo(length, blocked)
    assert result["passed"]
    assert result["goal_error_m"] <= 1.0
    assert result["off_path_snapshots"] == 0
    assert ("detour_middle" in result["route"]) is blocked
