#!/usr/bin/env python3
"""Compile and validate advanced gradient recipes.

Input JSON may contain explicit `stops`, or `segments` with start/end colors.
It can also define focus geometry as center/size or explicit L/T/R/B percentages.
Standard-library only; it does not edit a PPTX.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def num(v: Any, name: str) -> float:
    if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(float(v)):
        raise ValueError(f'{name} must be a finite number')
    return float(v)


def rect_from_center(spec: dict[str, Any]) -> dict[str, float]:
    cx = num(spec.get('center_x'), 'center_x')
    cy = num(spec.get('center_y'), 'center_y')
    width = num(spec.get('width'), 'width')
    height = num(spec.get('height'), 'height')
    for name, value in [('center_x',cx),('center_y',cy),('width',width),('height',height)]:
        if not 0 <= value <= 1:
            raise ValueError(f'{name} must be in [0,1]')
    left_edge, right_edge = cx-width/2, cx+width/2
    top_edge, bottom_edge = cy-height/2, cy+height/2
    if left_edge < -1e-12 or right_edge > 1+1e-12 or top_edge < -1e-12 or bottom_edge > 1+1e-12:
        raise ValueError('focus rectangle must remain inside the unit gradient box')
    return {
        'left': round(left_edge*100, 6),
        'top': round(top_edge*100, 6),
        'right': round((1-right_edge)*100, 6),
        'bottom': round((1-bottom_edge)*100, 6),
    }


def validate_rect(rect: dict[str, Any], name: str) -> dict[str, float]:
    out = {}
    for key in ('left','top','right','bottom'):
        val = num(rect.get(key), f'{name}.{key}')
        if not 0 <= val <= 100:
            raise ValueError(f'{name}.{key} must be in [0,100]')
        out[key] = val
    if out['left'] + out['right'] > 100 + 1e-9:
        raise ValueError(f'{name}: left + right must be <= 100')
    if out['top'] + out['bottom'] > 100 + 1e-9:
        raise ValueError(f'{name}: top + bottom must be <= 100')
    return out


def compile_stops(spec: dict[str, Any]) -> tuple[list[dict[str, Any]], list[float]]:
    epsilon = num(spec.get('epsilon', 0.0001), 'epsilon')
    if not 0 <= epsilon <= 0.01:
        raise ValueError('epsilon must be in [0,0.01]')
    coincident = bool(spec.get('coincident_supported', True))
    boundaries: list[float] = []
    if isinstance(spec.get('stops'), list):
        stops = [dict(s) for s in spec['stops']]
    else:
        segments = spec.get('segments')
        if not isinstance(segments,list) or not segments:
            raise ValueError('provide stops or non-empty segments')
        stops = []
        previous_end = None
        for i, seg in enumerate(segments):
            if not isinstance(seg,dict):
                raise ValueError(f'segments[{i}] must be an object')
            start = num(seg.get('start'), f'segments[{i}].start')
            end = num(seg.get('end'), f'segments[{i}].end')
            if not 0 <= start <= end <= 1:
                raise ValueError(f'segments[{i}] range must satisfy 0 <= start <= end <= 1')
            if previous_end is not None and abs(start-previous_end) > 1e-9:
                raise ValueError('segments must be contiguous')
            c0 = seg.get('color_start', seg.get('color'))
            c1 = seg.get('color_end', seg.get('color'))
            if not isinstance(c0,str) or not isinstance(c1,str):
                raise ValueError(f'segments[{i}] requires color/color_start/color_end')
            if i == 0:
                stops.append({'position':start,'color':c0,'role':'segment_start'})
            elif stops:
                boundary = start
                boundaries.append(boundary)
                if coincident:
                    stops.append({'position':boundary,'color':c0,'role':'hard_boundary_right'})
                else:
                    stops[-1]['position'] = max(0.0, boundary-epsilon/2)
                    stops.append({'position':min(1.0,boundary+epsilon/2),'color':c0,'role':'hard_boundary_right'})
            stops.append({'position':end,'color':c1,'role':'segment_end'})
            previous_end = end
    normalized = []
    prev = -math.inf
    for i, stop in enumerate(stops):
        if not isinstance(stop,dict):
            raise ValueError(f'stops[{i}] must be an object')
        p = num(stop.get('position'), f'stops[{i}].position')
        if not 0 <= p <= 1:
            raise ValueError(f'stops[{i}].position must be in [0,1]')
        if p < prev - 1e-12:
            raise ValueError('stops must be sorted')
        prev = p
        color = stop.get('color')
        if not isinstance(color,str) or not color:
            raise ValueError(f'stops[{i}].color is required')
        item = dict(stop)
        item['position'] = round(p, 8)
        normalized.append(item)
    if not boundaries:
        positions = [s['position'] for s in normalized]
        boundaries = [positions[i] for i in range(len(positions)-1) if abs(positions[i+1]-positions[i]) <= max(epsilon,1e-12)]
    return normalized, boundaries


def compile_plan(spec: dict[str, Any]) -> dict[str, Any]:
    stops, boundaries = compile_stops(spec)
    geometry = spec.get('geometry') or {}
    if not isinstance(geometry,dict):
        raise ValueError('geometry must be an object')
    output_geometry: dict[str, Any] = {
        'type': geometry.get('type', spec.get('type','linear')),
        'rotate_with_shape': bool(geometry.get('rotate_with_shape', True)),
    }
    for key in ('inner_rect_pct','outer_rect_pct','fill_to_rect_pct'):
        if key in geometry:
            output_geometry[key] = validate_rect(geometry[key], key)
    for key in ('inner_focus','outer_focus'):
        if key in geometry:
            mapped = 'inner_rect_pct' if key == 'inner_focus' else 'outer_rect_pct'
            output_geometry[mapped] = rect_from_center(geometry[key])
    return {
        'type': spec.get('type','linear'),
        'transition_mode': spec.get('transition_mode','hard' if boundaries else 'continuous'),
        'hard_epsilon': num(spec.get('epsilon',0.0001),'epsilon'),
        'stops': stops,
        'hard_boundaries': sorted(set(round(float(v),8) for v in boundaries)),
        'geometry': output_geometry,
        'adapter_requirements': {
            'preserve_duplicate_stops': bool(boundaries),
            'readback_after_save': True,
            'advanced_drawingml_required': any(k in output_geometry for k in ('inner_rect_pct','outer_rect_pct','fill_to_rect_pct')),
        },
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('spec', type=Path)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding='utf-8'))
        plan = compile_plan(spec)
    except (OSError,json.JSONDecodeError,ValueError,TypeError) as exc:
        print(f'gradient planning failed: {exc}', file=sys.stderr)
        return 1
    payload = json.dumps(plan, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding='utf-8')
        print(args.output)
    else:
        print(payload,end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
