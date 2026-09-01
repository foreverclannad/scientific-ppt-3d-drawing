#!/usr/bin/env python3
"""Generate an editable body-centred-cubic unit-cell Scene fragment."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any

CORNERS=[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)]
EDGES=[(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7)]

def compile_fragment(spec: dict[str,Any]) -> dict[str,Any]:
    prefix=str(spec.get('id_prefix','bcc')); a=float(spec.get('lattice_constant',120.0)); origin=[float(v) for v in spec.get('origin',[0,0,0])]
    if a<=0 or len(origin)!=3: raise ValueError('lattice_constant must be positive and origin must have three coordinates')
    corner_element=str(spec.get('corner_element','A')); center_element=str(spec.get('center_element',corner_element))
    radius=float(spec.get('radius_pt',13.0)); color_corner=spec.get('corner_color','#7AA7D9'); color_center=spec.get('center_color','#D98A4A')
    objects=[]
    for i,c in enumerate(CORNERS):
        pos=[origin[j]+a*c[j] for j in range(3)]
        objects.append({'id':f'{prefix}.corner.{i+1:02d}','kind':'atom','element':corner_element,'semantic_role':'bcc_corner_site','geometry':{'position3d':pos,'fractional':list(c),'radius_pt':radius,'unit_cell_fraction':0.125},'appearance':{'fill':color_corner,'material':'plastic','bevel':'round'},'provenance':{'generator':'bcc','site':'corner'}})
    objects.append({'id':f'{prefix}.body_center','kind':'atom','element':center_element,'semantic_role':'bcc_body_center_site','geometry':{'position3d':[origin[j]+a*0.5 for j in range(3)],'fractional':[0.5,0.5,0.5],'radius_pt':radius,'unit_cell_fraction':1.0},'appearance':{'fill':color_center,'material':'plastic','bevel':'round'},'provenance':{'generator':'bcc','site':'body_center'}})
    if spec.get('include_edges',True):
        for i,(u,v) in enumerate(EDGES,1):
            objects.append({'id':f'{prefix}.edge.{i:02d}','kind':'connector','semantic_role':'unit_cell_edge','from':f'{prefix}.corner.{u+1:02d}','to':f'{prefix}.corner.{v+1:02d}','appearance':{'line':'#65717E','line_width_pt':1.2,'transparency':0.2}})
    return {'generator':'bcc_unit_cell','lattice_constant':a,'site_count':9,'corner_site_count':8,'body_center_site_count':1,'effective_atom_count':2.0,'object_count':len(objects),'objects':objects}

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('spec',type=Path); ap.add_argument('--output',type=Path)
    ns=ap.parse_args(); result=compile_fragment(json.loads(ns.spec.read_text(encoding='utf-8'))); text=json.dumps(result,ensure_ascii=False,indent=2)
    if ns.output: ns.output.parent.mkdir(parents=True,exist_ok=True); ns.output.write_text(text,encoding='utf-8')
    else: print(text)
    return 0
if __name__=='__main__': raise SystemExit(main())
