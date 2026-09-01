#!/usr/bin/env python3
"""Compute an analytic plane-sphere intersection for an editable cutaway plan."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def vec3(v: Any, name: str) -> tuple[float,float,float]:
    if not isinstance(v,list) or len(v) != 3:
        raise ValueError(f'{name} must be [x,y,z]')
    vals = tuple(float(x) for x in v)
    if not all(math.isfinite(x) for x in vals):
        raise ValueError(f'{name} must contain finite values')
    return vals


def dot(a,b): return sum(a[i]*b[i] for i in range(3))
def sub(a,b): return tuple(a[i]-b[i] for i in range(3))
def add(a,b): return tuple(a[i]+b[i] for i in range(3))
def mul(a,s): return tuple(a[i]*s for i in range(3))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a,a))
def unit(a):
    n = norm(a)
    if n <= 1e-12: raise ValueError('zero-length vector')
    return mul(a,1/n)


def compile_plan(spec: dict[str, Any]) -> dict[str, Any]:
    sphere = spec.get('sphere')
    plane = spec.get('plane')
    if not isinstance(sphere,dict) or not isinstance(plane,dict):
        raise ValueError('spec requires sphere and plane objects')
    center = vec3(sphere.get('center'), 'sphere.center')
    radius = float(sphere.get('radius'))
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError('sphere.radius must be positive')
    point = vec3(plane.get('point'), 'plane.point')
    normal = unit(vec3(plane.get('normal'), 'plane.normal'))
    signed_distance = dot(sub(center,point), normal)
    if abs(signed_distance) > radius + 1e-9:
        raise ValueError('plane does not intersect the sphere')
    cap_center = sub(center, mul(normal,signed_distance))
    cap_radius = math.sqrt(max(0.0, radius*radius-signed_distance*signed_distance))
    helper = (1.0,0.0,0.0) if abs(normal[0]) < 0.9 else (0.0,1.0,0.0)
    u = unit(cross(normal,helper))
    v = unit(cross(normal,u))
    samples = int(spec.get('samples',64))
    if samples < 8 or samples > 2048:
        raise ValueError('samples must be in [8,2048]')
    points = []
    for i in range(samples):
        t = 2*math.pi*i/samples
        p = add(cap_center, add(mul(u,cap_radius*math.cos(t)), mul(v,cap_radius*math.sin(t))))
        points.append([round(x,8) for x in p])
    return {
        'sphere_center':[round(x,8) for x in center],
        'sphere_radius':radius,
        'plane_point':[round(x,8) for x in point],
        'plane_normal':[round(x,8) for x in normal],
        'signed_distance':round(signed_distance,8),
        'cap_center':[round(x,8) for x in cap_center],
        'cap_radius':round(cap_radius,8),
        'basis_u':[round(x,8) for x in u],
        'basis_v':[round(x,8) for x in v],
        'cap_points3d':points,
        'semantic_parts':['retained_shell','section_face','rim','interior_wall_or_cavity','optional_removed_piece'],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('spec',type=Path)
    p.add_argument('--output',type=Path)
    args = p.parse_args()
    try:
        plan = compile_plan(json.loads(args.spec.read_text(encoding='utf-8')))
    except (OSError,json.JSONDecodeError,ValueError,TypeError,KeyError) as exc:
        print(f'cutaway planning failed: {exc}', file=sys.stderr)
        return 1
    payload = json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding='utf-8')
        print(args.output)
    else:
        print(payload,end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
