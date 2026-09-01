#!/usr/bin/env python3
"""Generate paired leaflet placements along a planar, wave, or circular centerline.

For line/wave paths, the default "outer" side is the left normal of path
traversal. For circular paths, the default is radial outward, independent of
clockwise/counter-clockwise traversal.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def finite(v: Any, name: str) -> float:
    if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(float(v)):
        raise ValueError(f"{name} must be finite")
    return float(v)


def vec2(v: Any, name: str) -> tuple[float, float]:
    if not isinstance(v, list) or len(v) != 2:
        raise ValueError(f"{name} must be [x,y]")
    return finite(v[0], f"{name}.x"), finite(v[1], f"{name}.y")


def normalize(x: float, y: float) -> tuple[float, float]:
    magnitude = math.hypot(x, y)
    if magnitude <= 1e-12:
        raise ValueError("zero path tangent")
    return x / magnitude, y / magnitude


def sample_path(path: dict[str, Any], u: float) -> tuple[float, float, float, float]:
    ptype = path.get("type", "line")
    if ptype == "line":
        x0, y0 = vec2(path.get("start", [0, 0]), "start")
        x1, y1 = vec2(path.get("end", [100, 0]), "end")
        if math.hypot(x1 - x0, y1 - y0) <= 1e-12:
            raise ValueError("line start and end must differ")
        return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, x1 - x0, y1 - y0
    if ptype == "wave":
        x0 = finite(path.get("x_start", 0), "x_start")
        x1 = finite(path.get("x_end", 100), "x_end")
        if abs(x1 - x0) <= 1e-12:
            raise ValueError("x_start and x_end must differ")
        base = finite(path.get("base_y", 0), "base_y")
        amplitude = finite(path.get("amplitude", 20), "amplitude")
        cycles = finite(path.get("cycles", 1), "cycles")
        phase = math.radians(finite(path.get("phase_deg", 0), "phase_deg"))
        x = x0 + (x1 - x0) * u
        theta = 2 * math.pi * cycles * u + phase
        y = base + amplitude * math.sin(theta)
        dx_du = x1 - x0
        dy_du = amplitude * math.cos(theta) * 2 * math.pi * cycles
        return x, y, dx_du, dy_du
    if ptype == "circle":
        cx, cy = vec2(path.get("center", [0, 0]), "center")
        radius = finite(path.get("radius"), "radius")
        if radius <= 0:
            raise ValueError("radius must be positive")
        start = math.radians(finite(path.get("start_deg", 0), "start_deg"))
        end = math.radians(finite(path.get("end_deg", 360), "end_deg"))
        if abs(end - start) <= 1e-12:
            raise ValueError("circle angular span must be non-zero")
        angle = start + (end - start) * u
        return (
            cx + radius * math.cos(angle),
            cy + radius * math.sin(angle),
            -radius * math.sin(angle) * (end - start),
            radius * math.cos(angle) * (end - start),
        )
    raise ValueError(f"unsupported path.type: {ptype!r}")


def circle_is_closed(path: dict[str, Any]) -> bool:
    span = abs(finite(path.get("end_deg", 360), "end_deg") - finite(path.get("start_deg", 0), "start_deg"))
    turns = span / 360.0
    return abs(turns - round(turns)) <= 1e-9 and round(turns) >= 1


def outer_normal(
    *,
    path: dict[str, Any],
    x: float,
    y: float,
    tx: float,
    ty: float,
    outer_side: str,
) -> tuple[float, float]:
    if outer_side == "left":
        return -ty, tx
    if outer_side == "right":
        return ty, -tx
    if outer_side == "radial_outward":
        if path.get("type") != "circle":
            raise ValueError("outer_side=radial_outward is only valid for circle paths")
        cx, cy = vec2(path.get("center", [0, 0]), "center")
        return normalize(x - cx, y - cy)
    raise ValueError("outer_side must be left, right, or radial_outward")


def compile_fragment(spec: dict[str, Any]) -> dict[str, Any]:
    path = spec.get("path")
    if not isinstance(path, dict):
        raise ValueError("path must be an object")
    ptype = path.get("type", "line")

    count = spec.get("count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 2 or count > 5000:
        raise ValueError("count must be an integer in [2,5000]")
    max_objects = spec.get("max_objects", 10000)
    if not isinstance(max_objects, int) or isinstance(max_objects, bool) or max_objects < 1:
        raise ValueError("max_objects must be a positive integer")
    if 2 * count > max_objects:
        raise ValueError(f"requested membrane creates {2 * count} objects, exceeding max_objects={max_objects}")

    separation = finite(spec.get("leaflet_separation", 18), "leaflet_separation")
    if separation <= 0:
        raise ValueError("leaflet_separation must be positive")
    prefix = str(spec.get("id_prefix", "membrane")).strip()
    if not prefix:
        raise ValueError("id_prefix must not be empty")
    z = finite(spec.get("z", 0), "z")

    default_closed = ptype == "circle" and circle_is_closed(path)
    closed = bool(spec.get("closed", default_closed))
    if closed and ptype != "circle":
        raise ValueError("closed=true is currently supported only for circle paths")
    if closed and not circle_is_closed(path):
        raise ValueError("closed circle paths require an angular span equal to an integer number of full turns")

    default_outer_side = "radial_outward" if ptype == "circle" else "left"
    outer_side = str(spec.get("outer_side", default_outer_side))

    placements: list[dict[str, Any]] = []
    denominator = count if closed else count - 1
    for i in range(count):
        u = i / denominator
        x, y, tx, ty = sample_path(path, u)
        tx, ty = normalize(tx, ty)
        nx, ny = outer_normal(path=path, x=x, y=y, tx=tx, ty=ty, outer_side=outer_side)
        nx, ny = normalize(nx, ny)
        for leaflet, sign in (("outer", 1), ("inner", -1)):
            px = x + sign * separation / 2 * nx
            py = y + sign * separation / 2 * ny
            local_nx, local_ny = sign * nx, sign * ny
            normal_angle = math.degrees(math.atan2(local_ny, local_nx))
            placements.append(
                {
                    "id": f"{prefix}.{leaflet}.{i:04d}",
                    "kind": "lipid",
                    "semantic_role": f"{leaflet}_leaflet_unit",
                    "geometry": {
                        "position3d": [round(px, 8), round(py, 8), round(z, 8)],
                        "centerline_position2d": [round(x, 8), round(y, 8)],
                        "tangent2d": [round(tx, 8), round(ty, 8)],
                        "normal2d": [round(local_nx, 8), round(local_ny, 8)],
                        "orientation_deg": round(normal_angle, 8),
                    },
                    "provenance": {
                        "generator": "generate_membrane.py",
                        "sample_index": i,
                        "u": round(u, 8),
                        "leaflet": leaflet,
                        "outer_side_convention": outer_side,
                    },
                }
            )

    warnings: list[str] = []
    if ptype in {"line", "wave"}:
        warnings.append(
            f"For {ptype} paths, outer/inner are defined by outer_side={outer_side}; they are not absolute biological compartments."
        )
    if ptype == "circle" and not closed:
        warnings.append("The circular path is an open arc; inspect endpoint spacing and labels.")

    return {
        "generator": "membrane",
        "path": path,
        "count_per_leaflet": count,
        "leaflet_separation": separation,
        "closed": closed,
        "outer_side": outer_side,
        "object_count": len(placements),
        "objects": placements,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = compile_fragment(json.loads(args.spec.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError, TypeError, IndexError) as exc:
        print(f"membrane generation failed: {exc}", file=sys.stderr)
        return 1
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(args.output)
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
