#!/usr/bin/env python3
"""Generate two orthogonal sinusoidal field components and a propagation axis."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from typing import Any


def compile_fragment(spec: dict[str,Any]) -> dict[str,Any]:
    prefix=str(spec.get("id_prefix","em_wave")); length=float(spec.get("length",240.0))
    amp_e=float(spec.get("electric_amplitude",42.0)); amp_b=float(spec.get("magnetic_amplitude",32.0))
    cycles=float(spec.get("cycles",2.0)); phase=float(spec.get("phase_deg",0.0)); samples=int(spec.get("samples",121))
    arrow_count=int(spec.get("arrow_count",9)); origin=[float(v) for v in spec.get("origin",[0,0,0])]
    if length<=0 or amp_e<=0 or amp_b<=0 or cycles<=0 or samples<9 or arrow_count<2 or len(origin)!=3:
        raise ValueError("invalid electromagnetic-wave parameters")
    ph=math.radians(phase); epts=[]; bpts=[]; axis=[]
    for i in range(samples):
        u=i/(samples-1); x=origin[0]+length*u; s=math.sin(2*math.pi*cycles*u+ph)
        axis.append([x,origin[1],origin[2]])
        epts.append([x,origin[1]+amp_e*s,origin[2]])
        bpts.append([x,origin[1],origin[2]+amp_b*s])
    objects=[
      {"id":f"{prefix}.axis","kind":"polyline","semantic_role":"propagation_axis","geometry":{"points3d":axis,"line_width_pt":1.5},"appearance":{"line":"#444444","arrow":{"head":"triangle"}}},
      {"id":f"{prefix}.electric","kind":"wave_field","semantic_role":"electric_field","geometry":{"points3d":epts,"axis":"y","phase_deg":phase},"appearance":{"line":spec.get("electric_color","#D94A4A"),"line_width_pt":2.4}},
      {"id":f"{prefix}.magnetic","kind":"wave_field","semantic_role":"magnetic_field","geometry":{"points3d":bpts,"axis":"z","phase_deg":phase},"appearance":{"line":spec.get("magnetic_color","#315A8A"),"line_width_pt":2.4}},
    ]
    for i in range(arrow_count):
        u=(i+0.5)/arrow_count; x=origin[0]+length*u; s=math.sin(2*math.pi*cycles*u+ph)
        objects.extend([
          {"id":f"{prefix}.E.vector.{i:02d}","kind":"connector","semantic_role":"electric_field_vector","from":f"{prefix}.axis.anchor.E.{i:02d}","to":f"{prefix}.E.tip.{i:02d}","geometry":{"start3d":[x,origin[1],origin[2]],"end3d":[x,origin[1]+amp_e*s,origin[2]]},"appearance":{"line":spec.get("electric_color","#D94A4A"),"arrow":{"head":"triangle"}}},
          {"id":f"{prefix}.B.vector.{i:02d}","kind":"connector","semantic_role":"magnetic_field_vector","from":f"{prefix}.axis.anchor.B.{i:02d}","to":f"{prefix}.B.tip.{i:02d}","geometry":{"start3d":[x,origin[1],origin[2]],"end3d":[x,origin[1],origin[2]+amp_b*s]},"appearance":{"line":spec.get("magnetic_color","#315A8A"),"arrow":{"head":"triangle"}}},
          {"id":f"{prefix}.axis.anchor.E.{i:02d}","kind":"annotation","geometry":{"position3d":[x,origin[1],origin[2]]},"appearance":{"hidden":True}},
          {"id":f"{prefix}.E.tip.{i:02d}","kind":"annotation","geometry":{"position3d":[x,origin[1]+amp_e*s,origin[2]]},"appearance":{"hidden":True}},
          {"id":f"{prefix}.axis.anchor.B.{i:02d}","kind":"annotation","geometry":{"position3d":[x,origin[1],origin[2]]},"appearance":{"hidden":True}},
          {"id":f"{prefix}.B.tip.{i:02d}","kind":"annotation","geometry":{"position3d":[x,origin[1],origin[2]+amp_b*s]},"appearance":{"hidden":True}},
        ])
    return {"generator":"electromagnetic_wave","orthogonal_components":True,"propagation_axis":"x","electric_axis":"y","magnetic_axis":"z","sample_count":samples,"object_count":len(objects),"objects":objects}

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("spec",type=Path); ap.add_argument("--output",type=Path)
    ns=ap.parse_args(); result=compile_fragment(json.loads(ns.spec.read_text(encoding="utf-8"))); text=json.dumps(result,ensure_ascii=False,indent=2)
    if ns.output: ns.output.parent.mkdir(parents=True,exist_ok=True); ns.output.write_text(text,encoding="utf-8")
    else: print(text)
    return 0
if __name__=="__main__": raise SystemExit(main())
