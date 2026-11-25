"""Build the first 500 m and 2 km MuJoCo design scenes.

Only Python's standard library is needed to generate the XML files. These
scenes show geometry and named actors; control and emergency events are later
simulation steps, not connections to a real police service.
"""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SCENES = ROOT / "scenes"
LENGTHS_METERS = (500, 2000)


def element(parent: ET.Element, tag: str, **attrs: object) -> ET.Element:
    return ET.SubElement(parent, tag, {key: str(value) for key, value in attrs.items()})


def box(parent: ET.Element, name: str, pos: str, size: str, rgba: str) -> None:
    element(parent, "geom", name=name, type="box", pos=pos, size=size, rgba=rgba)


def make_scene(length: int) -> ET.ElementTree:
    root = ET.Element("mujoco", model=f"safe_walk_{length}m")
    element(root, "compiler", angle="radian")
    element(root, "option", timestep="0.02", gravity="0 0 -9.81")
    element(root, "statistic", center="10 0 0", extent="25")
    visual = element(root, "visual")
    element(visual, "global", offwidth="800", offheight="480")
    element(visual, "map", zfar=length + 100)
    world = element(root, "worldbody")
    element(world, "camera", name="start_camera", pos="7 -15 7", xyaxes="1 0 0 0 0.42 0.91")

    element(
        world,
        "light",
        name="night_ambient",
        directional="true",
        pos="0 0 50",
        dir="-0.2 0 -1",
        diffuse="0.22 0.24 0.32",
        ambient="0.07 0.08 0.12",
    )
    element(
        world,
        "geom",
        name="ground",
        type="plane",
        pos="0 0 -0.02",
        size=f"{length + 40} 30 0.1",
        rgba="0.10 0.14 0.13 1",
    )
    box(world, "pedestrian_path", f"{length / 2} 0 0.04", f"{length / 2} 1.5 0.04", "0.38 0.40 0.42 1")
    box(world, "road", f"{length / 2} -6 0.01", f"{length / 2} 3.5 0.01", "0.12 0.13 0.17 1")
    box(world, "curb", f"{length / 2} -1.7 0.12", f"{length / 2} 0.08 0.12", "0.75 0.75 0.65 1")

    # The origin is a transit stop or an arterial street. Homes may lie anywhere
    # along the route; the endpoint is a route boundary, not every user's home.
    box(world, "transit_stop", "-7 6 1.5", "4 1.5 1.5", "0.16 0.35 0.48 1")
    for index, x in enumerate((length / 4, length / 2, length * 3 / 4, length), start=1):
        box(world, f"residence_{index}", f"{x} 7 2", "3 2 2", "0.25 0.27 0.31 1")

    # Simple streetlight markers make the long route legible without pretending
    # to reproduce a real neighborhood or measured illumination.
    for x in range(0, length + 1, 100):
        element(
            world,
            "geom",
            name=f"lamp_post_{x}",
            type="cylinder",
            pos=f"{x} 2.6 2",
            size="0.07 2",
            rgba="0.28 0.29 0.32 1",
        )
        element(
            world,
            "geom",
            name=f"lamp_head_{x}",
            type="sphere",
            pos=f"{x} 2.6 4.05",
            size="0.18",
            rgba="0.9 0.82 0.45 1",
        )

    for index, x in enumerate((0, length // 2, length), start=1):
        element(
            world,
            "geom",
            name=f"call_button_{index}",
            type="box",
            pos=f"{x} 1.9 1.1",
            size="0.18 0.12 0.28",
            rgba="0.15 0.55 0.95 1",
        )
        element(
            world,
            "geom",
            name=f"emergency_button_{index}",
            type="box",
            pos=f"{x + 0.6} 1.9 1.1",
            size="0.18 0.12 0.28",
            rgba="0.9 0.12 0.10 1",
        )

    robot = element(world, "body", name="escort_robot", mocap="true", pos="5 -0.65 0.43")
    box(robot, "robot_chassis", "0 0 0", "0.38 0.32 0.16", "0.10 0.36 0.72 1")
    box(robot, "robot_beacon", "0 0 0.26", "0.15 0.15 0.10", "0.95 0.78 0.18 1")
    for side, y in (("left", 0.33), ("right", -0.33)):
        for end, x in (("front", 0.25), ("rear", -0.25)):
            element(
                robot,
                "geom",
                name=f"wheel_{end}_{side}",
                type="cylinder",
                pos=f"{x} {y} -0.21",
                quat="0.7071068 0.7071068 0 0",
                size="0.12 0.05",
                rgba="0.08 0.08 0.09 1",
            )

    person = element(world, "body", name="pedestrian", mocap="true", pos="10 0.65 0.08")
    element(person, "geom", name="pedestrian_body", type="capsule", pos="0 0 0.9", size="0.18 0.72", rgba="0.88 0.47 0.24 1")
    element(person, "geom", name="pedestrian_head", type="sphere", pos="0 0 1.76", size="0.16", rgba="0.93 0.76 0.58 1")

    element(world, "site", name="route_start", pos="0 0 0.12", size="0.35", rgba="0.1 0.9 0.2 1")
    element(world, "site", name="route_end", pos=f"{length} 0 0.12", size="0.35", rgba="0.9 0.8 0.1 1")
    ET.indent(root, space="  ")
    return ET.ElementTree(root)


def main() -> None:
    SCENES.mkdir(parents=True, exist_ok=True)
    for length in LENGTHS_METERS:
        output = SCENES / f"safe_walk_{length}m.xml"
        make_scene(length).write(output, encoding="utf-8", xml_declaration=True)
        print(output)


if __name__ == "__main__":
    main()
