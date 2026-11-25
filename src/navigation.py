"""Small pedestrian-route planner for the first simulation milestone.

The graph describes known pedestrian links. A blocked link is supplied by the
scenario; this module does not detect obstacles from a camera or lidar.
"""

from __future__ import annotations

from heapq import heappop, heappush
from math import hypot, isfinite

Point = tuple[float, float]
Edge = tuple[str, str]


def pedestrian_network(length_m: int) -> tuple[dict[str, Point], set[Edge]]:
    """Two narrow corridor lines with crossings at the midpoint and endpoint."""
    if length_m not in (500, 2000):
        raise ValueError("The first milestone supports 500 m and 2,000 m scenes.")
    positions = {
        "start": (0.0, -0.65),
        "middle": (length_m / 2, -0.65),
        "goal": (float(length_m), -0.65),
        "detour_middle": (length_m / 2, 0.65),
        "detour_goal": (float(length_m), 0.65),
    }
    edges = {
        ("start", "middle"),
        ("middle", "goal"),
        ("middle", "detour_middle"),
        ("detour_middle", "detour_goal"),
        ("detour_goal", "goal"),
    }
    return positions, edges


def canonical_edge(a: str, b: str) -> Edge:
    return tuple(sorted((a, b)))


def plan_route(
    positions: dict[str, Point],
    pedestrian_edges: set[Edge],
    start: str,
    goal: str,
    blocked_edges: set[Edge] | None = None,
) -> list[str]:
    """Return the shortest route over open pedestrian links, or raise ValueError."""
    if start not in positions or goal not in positions:
        raise ValueError("Start and goal must be pedestrian graph nodes.")
    blocked = {canonical_edge(*edge) for edge in (blocked_edges or set())}
    adjacency: dict[str, list[tuple[str, float]]] = {node: [] for node in positions}
    for a, b in pedestrian_edges:
        if a not in positions or b not in positions:
            raise ValueError("Pedestrian edge refers to an unknown node.")
        if canonical_edge(a, b) in blocked:
            continue
        distance = hypot(positions[a][0] - positions[b][0], positions[a][1] - positions[b][1])
        if not isfinite(distance) or distance <= 0:
            raise ValueError("Pedestrian edge must have a positive finite length.")
        adjacency[a].append((b, distance))
        adjacency[b].append((a, distance))

    queue = [(0.0, start)]
    costs = {start: 0.0}
    previous: dict[str, str] = {}
    while queue:
        cost, node = heappop(queue)
        if cost > costs[node]:
            continue
        if node == goal:
            route = [goal]
            while route[-1] != start:
                route.append(previous[route[-1]])
            return list(reversed(route))
        for neighbor, distance in adjacency[node]:
            next_cost = cost + distance
            if next_cost < costs.get(neighbor, float("inf")):
                costs[neighbor] = next_cost
                previous[neighbor] = node
                heappush(queue, (next_cost, neighbor))
    raise ValueError("No traversable pedestrian route reaches the goal.")


def route_distance(positions: dict[str, Point], route: list[str]) -> float:
    return sum(hypot(positions[a][0] - positions[b][0], positions[a][1] - positions[b][1]) for a, b in zip(route, route[1:]))
