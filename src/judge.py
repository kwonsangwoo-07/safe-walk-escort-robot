"""Small, deterministic acceptance checks for the D03 simulation records.

These functions judge reported results. They do not drive a robot, detect a
crime, send a real 112 report, or prove that the MuJoCo scene meets a target.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import isfinite


POSITION_TOLERANCE_M = 1.0
CALL_SOURCES = {"smartphone", "button"}
SCENARIO_LENGTHS_M = (500, 2000)


def judge_patrol(
    route_length_m: float,
    visited_m: Sequence[float],
    *,
    collisions: int,
    off_route_count: int,
) -> bool:
    """R-01, R-06, R-07: five ordered checkpoints and no safety violations."""
    if not isfinite(route_length_m) or route_length_m <= 0:
        return False
    if collisions != 0 or off_route_count != 0:
        return False
    expected = (0, route_length_m / 2, route_length_m, route_length_m / 2, 0)
    if len(visited_m) != len(expected):
        return False
    return all(
        isfinite(actual)
        and 0 <= actual <= route_length_m
        and abs(actual - target) <= POSITION_TOLERANCE_M
        for actual, target in zip(visited_m, expected)
    )


def judge_escort(route_length_m: float, *, destination_m: float, stop_m: float) -> bool:
    """R-02: escort ends within 1 m of a destination inside the route."""
    return (
        isfinite(route_length_m)
        and route_length_m > 0
        and isfinite(destination_m)
        and isfinite(stop_m)
        and 0 <= destination_m <= route_length_m
        and 0 <= stop_m <= route_length_m
        and abs(stop_m - destination_m) <= POSITION_TOLERANCE_M
    )


def judge_calls(source: str, *, accepted: Sequence[bool]) -> bool:
    """R-03, R-04: all five calls of one allowed source were accepted."""
    return source in CALL_SOURCES and len(accepted) == 5 and all(value is True for value in accepted)


def judge_emergency(
    pressed: bool,
    *,
    police_steps: Sequence[int],
    center_steps: Sequence[int],
) -> bool:
    """R-05: one event creates one record per destination in the same step."""
    if not pressed:
        return len(police_steps) == 0 and len(center_steps) == 0
    return (
        len(police_steps) == 1
        and len(center_steps) == 1
        and type(police_steps[0]) is int
        and type(center_steps[0]) is int
        and police_steps[0] >= 0
        and police_steps[0] == center_steps[0]
    )


def judge_response_log(records: Sequence[Mapping[str, object]]) -> bool:
    """R-08: both route lengths have free and occupied response records."""
    required = {(length, occupied) for length in SCENARIO_LENGTHS_M for occupied in (False, True)}
    observed = set()
    for record in records:
        length = record.get("route_length_m")
        occupied = record.get("occupied")
        arrival_s = record.get("arrival_s")
        if type(length) is not int or type(occupied) is not bool:
            return False
        if not isinstance(arrival_s, (int, float)) or not isfinite(arrival_s) or arrival_s < 0:
            return False
        observed.add((length, occupied))
    return required <= observed
