#!/usr/bin/env python3
"""Project Scene 3D coordinates to PowerPoint page coordinates and depth order.

Conventions:
- scene coordinates are right-handed;
- rotations are applied Rx, then Ry, then Rz;
- page Y points down, so projected scene Y is negated;
- larger rotated Z is nearer to the viewer;
- z_order_back_to_front is sorted from smaller to larger rotated Z.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


def matmul3(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def matvec3(m: list[list[float]], v: Iterable[float]) -> tuple[float, float, float]:
    x, y, z = [float(n) for n in v]
    return (
        m[0][0]*x + m[0][1]*y + m[0][2]*z,
        m[1][0]*x + m[1][1]*y + m[1][2]*z,
        m[2][0]*x + m[2][1]*y + m[2][2]*z,
    )


def rotation_matrix(rotation_deg: dict[str, float]) -> list[list[float]]:
    x = math.radians(float(rotation_deg.get('x', 0)))
    y = math.radians(float(rotation_deg.get('y', 0)))
    z = math.radians(float(rotation_deg.get('z', 0)))
    cx, sx = math.cos(x), math.sin(x)
    cy, sy = math.cos(y), math.sin(y)
    cz, sz = math.cos(z), math.sin(z)
    rx = [[1,0,0],[0,cx,-sx],[0,sx,cx]]
    ry = [[cy,0,sy],[0,1,0],[-sy,0,cy]]
    rz = [[cz,-sz,0],[sz,cz,0],[0,0,1]]
    return matmul3(rz, matmul3(ry, rx))


def project_point(point: Iterable[float], camera: dict[str, Any], rot: list[list[float]]) -> dict[str, float]:
    x, y, z = matvec3(rot, point)
    ox, oy = [float(v) for v in camera['origin_pt']]
    scale = float(camera.get('scale', 1.0))
    if camera.get('projection') == 'perspective':
        distance = float(camera['distance'])
        focal = float(camera['focal_length'])
        denom = distance - z
        if denom <= 1e-6:
            raise ValueError(f'point is on/behind the camera plane after rotation: z={z:.6f}, distance={distance:.6f}')
        perspective_scale = focal / denom
    else:
        perspective_scale = 1.0
    total_scale = scale * perspective_scale
    return {
        'page_x_pt': ox + x * total_scale,
        'page_y_pt': oy - y * total_scale,
        'camera_x': x,
        'camera_y': y,
        'camera_z': z,
        'projected_scale': total_scale,
    }


def object_center3d(obj: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> list[float] | None:
    geom = obj.get('geometry') or {}
    if isinstance(geom.get('position3d'), list):
        return [float(v) for v in geom['position3d']]
    if isinstance(geom.get('center3d'), list):
        return [float(v) for v in geom['center3d']]
    points = geom.get('points3d')
    if isinstance(points, list) and points:
        return [sum(float(p[i]) for p in points)/len(points) for i in range(3)]
    if obj.get('kind') in {'bond','connector','pathway_edge'}:
        a = by_id.get(str(obj.get('from')))
        b = by_id.get(str(obj.get('to')))
        if a and b:
            pa = (a.get('geometry') or {}).get('position3d')
            pb = (b.get('geometry') or {}).get('position3d')
            if isinstance(pa, list) and isinstance(pb, list):
                return [(float(pa[i])+float(pb[i]))/2 for i in range(3)]
    return None


def compile_plan(scene: dict[str, Any]) -> dict[str, Any]:
    camera = scene['camera']
    rot = rotation_matrix(camera.get('rotation_deg', {}))
    objects = scene.get('objects', [])
    by_id = {obj['id']: obj for obj in objects if isinstance(obj, dict) and isinstance(obj.get('id'), str)}
    projected = []
    for obj in objects:
        if not isinstance(obj, dict) or not isinstance(obj.get('id'), str):
            continue
        center = object_center3d(obj, by_id)
        if center is None:
            continue
        p = project_point(center, camera, rot)
        record: dict[str, Any] = {
            'id': obj['id'],
            'kind': obj.get('kind'),
            'source_center3d': center,
            **p,
        }
        if obj.get('kind') in {'bond','connector','pathway_edge'}:
            a = by_id.get(str(obj.get('from')))
            b = by_id.get(str(obj.get('to')))
            if a and b:
                pa = (a.get('geometry') or {}).get('position3d')
                pb = (b.get('geometry') or {}).get('position3d')
                if isinstance(pa, list) and isinstance(pb, list):
                    p1 = project_point(pa, camera, rot)
                    p2 = project_point(pb, camera, rot)
                    record['endpoint_1'] = p1
                    record['endpoint_2'] = p2
                    dx = p2['page_x_pt'] - p1['page_x_pt']
                    dy = p2['page_y_pt'] - p1['page_y_pt']
                    record['screen_length_pt'] = math.hypot(dx, dy)
                    record['screen_angle_deg'] = math.degrees(math.atan2(dy, dx))
        projected.append(record)
    order = [r['id'] for r in sorted(projected, key=lambda r: (r['camera_z'], r['id']))]
    for rank, obj_id in enumerate(order):
        for record in projected:
            if record['id'] == obj_id:
                record['z_rank_back_to_front'] = rank
                break
    return {
        'scene_id': scene.get('scene_id'),
        'camera': camera,
        'rotation_matrix': rot,
        'convention': 'larger camera_z is nearer; order is back-to-front',
        'objects': projected,
        'z_order_back_to_front': order,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        scene = json.loads(args.scene.read_text(encoding='utf-8'))
        plan = compile_plan(scene)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f'projection failed: {exc}', file=sys.stderr)
        return 1
    payload = json.dumps(plan, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding='utf-8')
        print(args.output)
    else:
        print(payload, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
