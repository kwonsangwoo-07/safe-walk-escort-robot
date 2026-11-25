"""Acceptance examples for D03. Keep these fixed when editing src/judge.py."""

import pytest

from judge import judge_calls, judge_emergency, judge_escort, judge_patrol, judge_response_log


@pytest.mark.parametrize("route_length_m", [500, 2000])
def test_t01_full_round_trip_is_success(route_length_m):
    route = [0, route_length_m / 2, route_length_m, route_length_m / 2, 0]
    assert judge_patrol(route_length_m, route, collisions=0, off_route_count=0)


def test_t02_exactly_one_meter_error_is_success():
    assert judge_patrol(500, [0, 251, 500, 250, 0], collisions=0, off_route_count=0)


def test_t02_missed_checkpoint_is_failure():
    assert not judge_patrol(500, [0, 250, 500, 0], collisions=0, off_route_count=0)


def test_t02_wrong_visit_order_is_failure():
    assert not judge_patrol(500, [0, 500, 250, 250, 0], collisions=0, off_route_count=0)


def test_t03_escort_stop_at_boundary_is_success():
    assert judge_escort(500, destination_m=400, stop_m=401)


@pytest.mark.parametrize("destination_m", [0, 125, 250, 375, 500])
def test_t03_five_different_destinations_are_success(destination_m):
    assert judge_escort(500, destination_m=destination_m, stop_m=destination_m)


def test_t03_escort_stops_too_early_is_failure():
    assert not judge_escort(500, destination_m=400, stop_m=398.9)


def test_t03_destination_outside_route_is_failure():
    assert not judge_escort(500, destination_m=600, stop_m=500)


@pytest.mark.parametrize("source", ["smartphone", "button"])
def test_t04_five_calls_from_each_source_are_accepted(source):
    assert judge_calls(source, accepted=[True] * 5)


def test_t04_unaccepted_call_is_failure():
    assert not judge_calls("smartphone", accepted=[True, True, False, True, True])


def test_t05_two_emergency_outputs_at_same_step_are_success():
    assert judge_emergency(True, police_steps=[100], center_steps=[100])


@pytest.mark.parametrize("step", [10, 100, 1000, 5000, 10000])
def test_t05_five_emergency_events_are_success(step):
    assert judge_emergency(True, police_steps=[step], center_steps=[step])


def test_t05_missing_police_output_is_failure():
    assert not judge_emergency(True, police_steps=[], center_steps=[100])


def test_t05_alerts_at_different_steps_are_failure():
    assert not judge_emergency(True, police_steps=[100], center_steps=[101])


def test_t05_duplicate_alert_is_failure():
    assert not judge_emergency(True, police_steps=[100, 100], center_steps=[100])


def test_t06_one_collision_is_failure():
    assert not judge_patrol(500, [0, 250, 500, 250, 0], collisions=1, off_route_count=0)


def test_t07_one_off_route_event_is_failure():
    assert not judge_patrol(500, [0, 250, 500, 250, 0], collisions=0, off_route_count=1)


def test_t08_response_time_recorded_for_both_lengths_and_occupancy_states():
    records = [
        {"route_length_m": length, "occupied": occupied, "arrival_s": 30.0}
        for length in (500, 2000)
        for occupied in (False, True)
    ]
    assert judge_response_log(records)


def test_t08_missing_occupied_case_is_failure():
    records = [
        {"route_length_m": length, "occupied": False, "arrival_s": 30.0}
        for length in (500, 2000)
    ]
    assert not judge_response_log(records)
