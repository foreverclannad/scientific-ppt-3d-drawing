#!/usr/bin/env python3
"""Conservative validator for Scientific PowerPoint Scene JSON v0.1/v0.2/v1.0."""
from __future__ import annotations
import argparse,json,math,re,sys
from pathlib import Path
from typing import Any

ALLOWED_VERSIONS={'0.1','0.2','1.0'}
ALLOWED_KINDS={'primitive','atom','bond','text','connector','group','asset','energy_level','panel','array','path_distribution','polyline','freeform','annotation','gradient_shape','cutaway','section_face','host_guest','lattice','unit_cell','polyhedron','membrane','lipid','pathway_node','pathway_edge','surface','arrow','labware','apparatus_part','molecule','wire_sphere','em_wave','wave_field','field_vector','external_3d_model'}
ALLOWED_DOMAINS={'general_science','computational_chemistry','quantum_chemistry','supramolecular_chemistry','crystallography','materials_science','biochemistry','cell_biology','computer_science','power_systems','multidisciplinary'}
ID_RE=re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]+$')

def is_number(v:Any)->bool:
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(float(v))
def vec(v:Any,n:int)->bool:
    return isinstance(v,list) and len(v)==n and all(is_number(x) for x in v)
def load_json(path:Path)->dict[str,Any]:
    data=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,dict): raise ValueError('scene root must be an object')
    return data

def validate_gradient(g:Any,prefix:str,errors:list[str])->None:
    if not isinstance(g,dict): errors.append(f'{prefix} must be an object'); return
    stops=g.get('stops')
    if stops is not None:
        if not isinstance(stops,list) or len(stops)<2: errors.append(f'{prefix}.stops needs at least two entries'); return
        prev=-1.0
        positions=[]
        for i,s in enumerate(stops):
            if not isinstance(s,dict): errors.append(f'{prefix}.stops[{i}] must be an object'); continue
            pos=s.get('position')
            if not is_number(pos) or not 0<=float(pos)<=1: errors.append(f'{prefix}.stops[{i}].position must be in [0,1]'); continue
            if float(pos)<prev: errors.append(f'{prefix}.stops must be sorted')
            prev=float(pos); positions.append(float(pos))
        if g.get('transition_mode')=='hard':
            eps=float(g.get('hard_epsilon',0.002))
            if not any(abs(b-a)<=eps+1e-12 for a,b in zip(positions,positions[1:])):
                errors.append(f'{prefix}: hard transition requires a coincident/near-coincident stop pair')

def validate(scene:dict[str,Any])->list[str]:
    errors=[]
    for key in ['schema_version','scene_id','title','domain','fidelity','canvas','camera','objects','constraints','outputs']:
        if key not in scene: errors.append(f'missing required field: {key}')
    version=scene.get('schema_version')
    if version not in ALLOWED_VERSIONS: errors.append('schema_version must be 0.1, 0.2, or 1.0')
    if not isinstance(scene.get('scene_id'),str) or not ID_RE.fullmatch(scene.get('scene_id','')): errors.append('scene_id must be a stable identifier')
    if scene.get('domain') not in ALLOWED_DOMAINS: errors.append(f"unsupported domain: {scene.get('domain')!r}")
    if scene.get('representation') is not None and scene.get('representation') not in {'2d','2.5d','3d','external_asset_composite','mixed'}: errors.append('invalid representation')
    if version=='1.0':
        abstraction=scene.get('abstraction')
        if not isinstance(abstraction,dict): errors.append('v1.0 requires abstraction object')
        else:
            if not isinstance(abstraction.get('target_claim'),str) or not abstraction.get('target_claim','').strip(): errors.append('abstraction.target_claim is required')
            for k in ('essential_information','omitted_information'):
                if not isinstance(abstraction.get(k),list): errors.append(f'abstraction.{k} must be an array')
    fidelity=scene.get('fidelity')
    if not isinstance(fidelity,dict): errors.append('fidelity must be an object')
    else:
        mode=fidelity.get('mode')
        if mode not in {'data_bound','illustrative','hybrid'}: errors.append('invalid fidelity.mode')
        sources=fidelity.get('source_data')
        if not isinstance(sources,list): errors.append('fidelity.source_data must be an array')
        elif mode=='data_bound' and not sources: errors.append('data_bound scenes require source_data')
        if not isinstance(fidelity.get('assumptions'),list): errors.append('fidelity.assumptions must be an array')
    canvas=scene.get('canvas')
    if not isinstance(canvas,dict): errors.append('canvas must be an object')
    else:
        for k in ('width_pt','height_pt'):
            if not is_number(canvas.get(k)) or float(canvas[k])<=0: errors.append(f'canvas.{k} must be positive')
        if not is_number(canvas.get('margin_pt')) or float(canvas.get('margin_pt',-1))<0: errors.append('canvas.margin_pt must be non-negative')
    camera=scene.get('camera')
    if not isinstance(camera,dict): errors.append('camera must be an object')
    else:
        if camera.get('projection') not in {'orthographic','perspective'}: errors.append('invalid camera.projection')
        r=camera.get('rotation_deg')
        if not isinstance(r,dict) or any(not is_number(r.get(k)) for k in ('x','y','z')): errors.append('camera.rotation_deg needs finite x/y/z')
        if not vec(camera.get('origin_pt'),2): errors.append('camera.origin_pt must be [x,y]')
        if not is_number(camera.get('scale')) or float(camera.get('scale',0))<=0: errors.append('camera.scale must be positive')
        if camera.get('projection')=='perspective' and (not is_number(camera.get('distance')) or not is_number(camera.get('focal_length'))): errors.append('perspective camera requires distance and focal_length')
    objects=scene.get('objects')
    if not isinstance(objects,list): errors.append('objects must be an array'); objects=[]
    budget=scene.get('object_budget')
    if budget is not None and (not isinstance(budget,int) or budget<1): errors.append('object_budget must be a positive integer')
    elif isinstance(budget,int) and len(objects)>budget: errors.append(f'object count {len(objects)} exceeds object_budget {budget}')
    ids=set(); by_id={}
    for i,obj in enumerate(objects):
        pre=f'objects[{i}]'
        if not isinstance(obj,dict): errors.append(f'{pre} must be an object'); continue
        oid=obj.get('id')
        if not isinstance(oid,str) or not ID_RE.fullmatch(oid): errors.append(f'{pre}.id invalid'); continue
        if oid in ids: errors.append(f'duplicate object id: {oid}')
        ids.add(oid); by_id[oid]=obj
        if obj.get('kind') not in ALLOWED_KINDS: errors.append(f"{pre}.kind unsupported: {obj.get('kind')!r}")
        geom=obj.get('geometry',{})
        if geom is not None and not isinstance(geom,dict): errors.append(f'{pre}.geometry must be an object'); geom={}
        if isinstance(geom,dict):
            for k in ('position3d','center3d','start3d','end3d'):
                if geom.get(k) is not None and not vec(geom[k],3): errors.append(f'{pre}.geometry.{k} must be [x,y,z]')
            pts=geom.get('points3d')
            if pts is not None and (not isinstance(pts,list) or len(pts)<2 or any(not vec(p,3) for p in pts)): errors.append(f'{pre}.geometry.points3d invalid')
        app=obj.get('appearance')
        if app is not None and not isinstance(app,dict): errors.append(f'{pre}.appearance must be an object')
        if isinstance(app,dict) and isinstance(app.get('gradient'),dict): validate_gradient(app['gradient'],f'{pre}.appearance.gradient',errors)
        if isinstance(obj.get('gradient_spec'),dict): validate_gradient(obj['gradient_spec'],f'{pre}.gradient_spec',errors)
        if obj.get('kind')=='asset' and not (obj.get('source_asset_id') or obj.get('asset_query') or (isinstance(geom,dict) and geom.get('path'))): errors.append(f'{pre}: asset needs source_asset_id, asset_query, or geometry.path')
        if obj.get('kind')=='external_3d_model' and not isinstance(obj.get('provenance'),dict): errors.append(f'{pre}: external_3d_model requires provenance')
    for oid,obj in by_id.items():
        for k in ('from','to','target','parent','host_id','guest_id'):
            ref=obj.get(k)
            if ref is not None and ref not in ids: errors.append(f'{oid}.{k} references missing object {ref!r}')
        for k in ('children','members','host_ids'):
            refs=obj.get(k)
            if refs is not None:
                if not isinstance(refs,list): errors.append(f'{oid}.{k} must be an array')
                else:
                    for ref in refs:
                        if ref not in ids: errors.append(f'{oid}.{k} references missing object {ref!r}')
    if not isinstance(scene.get('constraints'),list): errors.append('constraints must be an array')
    outputs=scene.get('outputs')
    if not isinstance(outputs,dict): errors.append('outputs must be an object')
    else:
        for k in ('pptx','preview_png'):
            if not isinstance(outputs.get(k),str) or not outputs.get(k): errors.append(f'outputs.{k} required')
    return errors

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('scene',type=Path); ap.add_argument('--json',action='store_true')
    ns=ap.parse_args()
    try: scene=load_json(ns.scene); errors=validate(scene)
    except (OSError,ValueError,json.JSONDecodeError) as exc: errors=[str(exc)]
    payload={'ok':not errors,'scene':str(ns.scene),'errors':errors}
    if ns.json: print(json.dumps(payload,ensure_ascii=False,indent=2))
    elif errors:
        for e in errors: print(e,file=sys.stderr)
    else: print(f'OK: {ns.scene}')
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
