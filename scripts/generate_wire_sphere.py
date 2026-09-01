#!/usr/bin/env python3
"""Generate editable latitude/longitude wire-sphere paths for PowerPoint."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _unit(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x*x for x in v))
    if n <= 1e-12:
        raise ValueError("view_direction must be non-zero")
    return [x/n for x in v]


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x*y for x,y in zip(a,b))


def _split_visibility(points: list[list[float]], view: list[float], center: list[float]) -> list[tuple[str,list[list[float]]]]:
    # Positive dot means closer to a camera looking toward the origin from +view.
    if len(points) < 2:
        return []
    labels=["front" if _dot([p[i]-center[i] for i in range(3)],view)>=0 else "back" for p in points]
    chunks: list[tuple[str,list[list[float]]]]=[]
    current=labels[0]; chunk=[points[0]]
    for label,point in zip(labels[1:],points[1:]):
        if label != current:
            chunk.append(point)
            if len(chunk)>=2: chunks.append((current,chunk))
            current=label; chunk=[chunk[-1],point]
        else:
            chunk.append(point)
    if len(chunk)>=2: chunks.append((current,chunk))
    return chunks


def compile_fragment(spec: dict[str,Any]) -> dict[str,Any]:
    radius=float(spec.get("radius",100.0))
    latitudes=int(spec.get("latitudes",7))
    longitudes=int(spec.get("longitudes",12))
    samples=int(spec.get("samples_per_curve",72))
    center=[float(x) for x in spec.get("center",[0.0,0.0,0.0])]
    view=_unit([float(x) for x in spec.get("view_direction",[0.0,0.0,1.0])])
    prefix=str(spec.get("id_prefix","wire_sphere"))
    if radius<=0 or latitudes<1 or longitudes<2 or samples<12 or len(center)!=3:
        raise ValueError("invalid wire-sphere parameters")
    objects=[]
    def add_curve(curve_id: str, points: list[list[float]], family: str):
        for j,(vis,chunk) in enumerate(_split_visibility(points,view,center),start=1):
            objects.append({
                "id":f"{prefix}.{curve_id}.{vis}.{j:02d}","kind":"polyline",
                "semantic_role":f"wire_sphere_{family}_{vis}",
                "geometry":{"points3d":chunk,"line_width_pt":1.25},
                "appearance":{"line":"#5F6F82","transparency":0.0 if vis=="front" else 0.62,"dash":"solid" if vis=="front" else "dash"},
                "provenance":{"generator":"wire_sphere","family":family,"visibility":vis},
            })
    for i in range(1,latitudes+1):
        phi=-math.pi/2 + i*math.pi/(latitudes+1)
        z=radius*math.sin(phi); rr=radius*math.cos(phi)
        points=[]
        for k in range(samples+1):
            t=2*math.pi*k/samples
            points.append([center[0]+rr*math.cos(t),center[1]+rr*math.sin(t),center[2]+z])
        add_curve(f"lat.{i:02d}",points,"latitude")
    for i in range(longitudes):
        lam=2*math.pi*i/longitudes
        points=[]
        for k in range(samples+1):
            phi=-math.pi/2+math.pi*k/samples
            rr=radius*math.cos(phi); z=radius*math.sin(phi)
            points.append([center[0]+rr*math.cos(lam),center[1]+rr*math.sin(lam),center[2]+z])
        add_curve(f"lon.{i:02d}",points,"longitude")
    return {"generator":"wire_sphere","radius":radius,"latitude_count":latitudes,"longitude_count":longitudes,"object_count":len(objects),"objects":objects}


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("spec",type=Path); ap.add_argument("--output",type=Path)
    ns=ap.parse_args(); result=compile_fragment(json.loads(ns.spec.read_text(encoding="utf-8")))
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if ns.output:
        ns.output.parent.mkdir(parents=True,exist_ok=True); ns.output.write_text(text,encoding="utf-8")
    else: print(text)
    return 0
if __name__=="__main__": raise SystemExit(main())
