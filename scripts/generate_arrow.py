#!/usr/bin/env python3
"""Compile one of thirteen editable scientific-arrow templates into Scene objects.

Taxonomy derived from the course: five line arrows, four planar arrows, and four
3D arrows. Templates describe geometry and semantics; the PowerPoint bridge
creates native lines/freeforms/shapes rather than SmartArt or flattened images.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

TEMPLATES: dict[str, dict[str, Any]] = {
    # Five line-arrow families
    "line.straight": {"category": "line", "description": "Straight causal/data/material flow"},
    "line.bezier_wave": {"category": "line", "description": "Curved or wave-like transport/propagation"},
    "line.circular": {"category": "line", "description": "Circular feedback or cycle"},
    "line.stream_bundle": {"category": "line", "description": "Multiple converging/diverging streams"},
    "line.segmented_loop": {"category": "line", "description": "Segmented loop with explicit stages"},
    # Four planar-arrow families
    "planar.block": {"category": "planar", "description": "Filled block arrow for major direction"},
    "planar.curved_ribbon": {"category": "planar", "description": "Curved filled ribbon arrow"},
    "planar.folded_turn": {"category": "planar", "description": "Bent/folded turn arrow"},
    "planar.segmented_cycle": {"category": "planar", "description": "Repeated planar cycle segments"},
    # Four 3D-arrow families
    "3d.extruded_flat": {"category": "3d", "description": "Flat arrow with editable extrusion"},
    "3d.upright_depth": {"category": "3d", "description": "Arrow oriented into/out of depth"},
    "3d.curved_extruded": {"category": "3d", "description": "Curved extruded arrow"},
    "3d.segmented_cycle": {"category": "3d", "description": "Repeated 3D cycle segments"},
}

SEMANTICS = {
    "forward": {"tail": "none", "head": "triangle", "dash": "solid"},
    "activation": {"tail": "none", "head": "triangle", "dash": "solid"},
    "inhibition": {"tail": "none", "head": "bar", "dash": "solid"},
    "feedback": {"tail": "none", "head": "triangle", "dash": "solid"},
    "rollback": {"tail": "none", "head": "triangle", "dash": "dash"},
    "optional": {"tail": "none", "head": "triangle", "dash": "dash"},
    "bidirectional": {"tail": "triangle", "head": "triangle", "dash": "solid"},
    "association": {"tail": "none", "head": "oval", "dash": "solid"},
}


def _rot(point: tuple[float, float], angle_deg: float) -> list[float]:
    a = math.radians(angle_deg)
    c, s = math.cos(a), math.sin(a)
    return [point[0] * c - point[1] * s, point[0] * s + point[1] * c]


def _translate(points: list[list[float]], x: float, y: float) -> list[list[float]]:
    return [[px + x, py + y, 0.0] for px, py in points]


def _arc_points(radius: float, start_deg: float, end_deg: float, count: int) -> list[list[float]]:
    if count < 3:
        raise ValueError("arc count must be >= 3")
    return [
        [radius * math.cos(math.radians(start_deg + (end_deg - start_deg) * i / (count - 1))),
         radius * math.sin(math.radians(start_deg + (end_deg - start_deg) * i / (count - 1)))]
        for i in range(count)
    ]


def list_templates() -> list[dict[str, str]]:
    return [{"id": key, **value} for key, value in TEMPLATES.items()]


def compile_fragment(spec: dict[str, Any]) -> dict[str, Any]:
    template = spec.get("template")
    if template not in TEMPLATES:
        raise ValueError(f"unsupported arrow template: {template!r}")
    category = TEMPLATES[template]["category"]
    semantic = spec.get("semantic", "forward")
    if semantic not in SEMANTICS:
        raise ValueError(f"unsupported semantic: {semantic!r}")
    origin = spec.get("origin", [0.0, 0.0])
    if not (isinstance(origin, list) and len(origin) == 2 and all(isinstance(v, (int, float)) for v in origin)):
        raise ValueError("origin must be [x,y]")
    length = float(spec.get("length", 120.0))
    width = float(spec.get("width", 18.0))
    angle = float(spec.get("angle_deg", 0.0))
    if length <= 0 or width <= 0:
        raise ValueError("length and width must be positive")
    color = spec.get("color", "#315A8A")
    base_id = spec.get("id", template.replace(".", "_"))
    objects: list[dict[str, Any]] = []
    app = {"fill": color, "line": color, "arrow": SEMANTICS[semantic], "semantic": semantic}

    if template == "line.straight":
        pts = [[0.0, 0.0], [length, 0.0]]
        kind = "connector"
    elif template == "line.bezier_wave":
        samples = int(spec.get("samples", 40))
        amplitude = float(spec.get("amplitude", width * 1.5))
        cycles = float(spec.get("cycles", 1.25))
        pts = [[length * i / (samples - 1), amplitude * math.sin(2 * math.pi * cycles * i / (samples - 1))] for i in range(samples)]
        kind = "polyline"
    elif template == "line.circular":
        pts = _arc_points(length / 2, -35, 290, int(spec.get("samples", 48)))
        kind = "polyline"
    elif template == "line.stream_bundle":
        count = int(spec.get("count", 3))
        if count < 2:
            raise ValueError("stream_bundle count must be >= 2")
        for i in range(count):
            offset = (i - (count - 1) / 2) * width
            local = [[0.0, offset], [length * 0.55, offset * 0.35], [length, 0.0]]
            local = [_rot(tuple(p), angle) for p in local]
            objects.append({
                "id": f"{base_id}.stream.{i+1:02d}", "kind": "polyline", "semantic_role": semantic,
                "geometry": {"points3d": _translate(local, float(origin[0]), float(origin[1])), "line_width_pt": max(1.2, width * 0.12)},
                "appearance": app,
            })
        return {"template": template, "category": category, "object_count": len(objects), "objects": objects}
    elif template == "line.segmented_loop":
        segments = int(spec.get("segments", 4))
        if segments < 2:
            raise ValueError("segmented_loop segments must be >= 2")
        for i in range(segments):
            start = -25 + i * 360 / segments
            end = start + 0.72 * 360 / segments
            local = _arc_points(length / 2, start, end, max(7, int(spec.get("samples_per_segment", 10))))
            local = [_rot(tuple(p), angle) for p in local]
            objects.append({
                "id": f"{base_id}.segment.{i+1:02d}", "kind": "polyline", "semantic_role": semantic,
                "geometry": {"points3d": _translate(local, float(origin[0]), float(origin[1])), "line_width_pt": max(1.2, width * 0.12)},
                "appearance": app,
            })
        return {"template": template, "category": category, "object_count": len(objects), "objects": objects}
    elif template in {"planar.block", "3d.extruded_flat", "3d.upright_depth"}:
        head = min(length * 0.38, width * 2.2)
        shaft = width * 0.52
        local2 = [[0, -shaft / 2], [length - head, -shaft / 2], [length - head, -width], [length, 0], [length - head, width], [length - head, shaft / 2], [0, shaft / 2]]
        pts = local2
        kind = "freeform"
    elif template in {"planar.curved_ribbon", "3d.curved_extruded"}:
        outer = _arc_points(length / 2, -60, 155, 30)
        inner = list(reversed(_arc_points(length / 2 - width, -48, 142, 30)))
        pts = outer + inner
        kind = "freeform"
    elif template == "planar.folded_turn":
        h = length * 0.55
        pts = [[0, -width / 2], [h, -width / 2], [h, -length * 0.32], [length, 0], [h, length * 0.32], [h, width / 2], [0, width / 2]]
        kind = "freeform"
    elif template in {"planar.segmented_cycle", "3d.segmented_cycle"}:
        segments = int(spec.get("segments", 4))
        if segments < 2:
            raise ValueError("cycle segments must be >= 2")
        for i in range(segments):
            start = -35 + i * 360 / segments
            end = start + 0.70 * 360 / segments
            outer = _arc_points(length / 2, start, end, 12)
            inner = list(reversed(_arc_points(length / 2 - width, start + 6, end - 8, 10)))
            local = outer + inner
            local = [_rot(tuple(p), angle) for p in local]
            appearance = dict(app)
            if category == "3d":
                appearance.update({"depth_pt": max(4.0, width * 0.45), "bevel": "angle", "material": "plastic", "light_rig": "three_point_top"})
            objects.append({
                "id": f"{base_id}.segment.{i+1:02d}", "kind": "arrow", "semantic_role": semantic,
                "geometry": {"points3d": _translate(local, float(origin[0]), float(origin[1])), "closed": True},
                "appearance": appearance,
            })
        return {"template": template, "category": category, "object_count": len(objects), "objects": objects}
    else:  # defensive
        raise AssertionError(template)

    local = [_rot(tuple(p), angle) for p in pts]
    appearance = dict(app)
    if category == "3d":
        appearance.update({
            "depth_pt": max(4.0, width * 0.55),
            "bevel": "angle" if template != "3d.upright_depth" else "round",
            "material": "plastic",
            "light_rig": "three_point_top",
            "rotation_deg": {"x": 20 if template == "3d.upright_depth" else 8, "y": -18, "z": angle},
        })
    objects.append({
        "id": base_id,
        "kind": "arrow" if category != "line" else kind,
        "semantic_role": semantic,
        "geometry": {
            "points3d": _translate(local, float(origin[0]), float(origin[1])),
            "closed": category != "line",
            "line_width_pt": max(1.2, width * 0.12),
        },
        "appearance": appearance,
        "provenance": {"template": template, "taxonomy": "5-line/4-planar/4-3d"},
    })
    return {"template": template, "category": category, "object_count": len(objects), "objects": objects}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", type=Path)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.list:
        print(json.dumps({"templates": list_templates()}, ensure_ascii=False, indent=2))
        return 0
    if args.spec is None:
        parser.error("spec is required unless --list is used")
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    result = compile_fragment(spec)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
