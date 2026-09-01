#!/usr/bin/env python3
"""Run cross-batch scientific PPT Skill v1.0 regression checks."""
from __future__ import annotations
import argparse,importlib.util,json,math,tempfile,sys
from pathlib import Path

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Cannot load module {name} from {path}')
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--skill-root',type=Path,required=True); ns=ap.parse_args()
    root=ns.skill_root.resolve(); failures=[]; results=[]
    validator=load('validator',root/'scripts/validate_scene.py'); projector=load('projector',root/'scripts/project_3d.py')
    gradients=load('gradients',root/'scripts/plan_gradient.py'); cutaways=load('cutaways',root/'scripts/plan_cutaway.py')
    lattices=load('lattices',root/'scripts/generate_lattice.py'); membranes=load('membranes',root/'scripts/generate_membrane.py')
    arrows=load('arrows',root/'scripts/generate_arrow.py'); bcc=load('bcc',root/'scripts/generate_bcc_cell.py')
    wire=load('wire',root/'scripts/generate_wire_sphere.py'); em=load('em',root/'scripts/generate_em_wave.py')
    palettes=load('palettes',root/'scripts/validate_palette.py'); molecules=load('molecules',root/'scripts/generate_molecule_scene.py')
    cases=json.loads((root/'evals/eval-cases.json').read_text(encoding='utf-8'))['cases']
    for case in cases:
        path=(root/'evals'/case['scene']).resolve(); scene=json.loads(path.read_text(encoding='utf-8')); errs=validator.validate(scene)
        if errs: failures.extend(f"{case['id']}: {e}" for e in errs)
        count=len(scene.get('objects',[])); exp=case.get('expected',{}).get('object_count')
        if exp is not None and count!=exp: failures.append(f"{case['id']}: object_count={count}, expected={exp}")
        if case.get('expected',{}).get('projection_required'):
            plan=projector.compile_plan(scene)
            if not plan['objects']: failures.append(f"{case['id']}: projection produced no objects")
            if len(plan['z_order_back_to_front'])!=len({r['id'] for r in plan['objects']}): failures.append(f"{case['id']}: incomplete z-order")
        results.append({'id':case['id'],'ok':not errs,'object_count':count})
    checks={}
    # Existing v0.2 algorithms.
    gp=gradients.compile_plan(json.loads((root/'examples/gradient-plan.spec.json').read_text(encoding='utf-8')))
    checks['hard_gradient']=bool(gp['hard_boundaries'])
    cp=cutaways.compile_plan(json.loads((root/'examples/cutaway-plan.spec.json').read_text(encoding='utf-8')))
    checks['cutaway']=len(cp['cap_points3d'])==48
    lp=lattices.compile_fragment(json.loads((root/'examples/lattice-generator.spec.json').read_text(encoding='utf-8')))
    checks['lattice']=lp['object_count']==24 and lp.get('bonds_inferred') is False
    mp=membranes.compile_fragment(json.loads((root/'examples/membrane-generator.spec.json').read_text(encoding='utf-8')))
    checks['membrane']=mp['object_count']==32
    # Third-batch algorithms.
    checks['arrow_taxonomy']=len(arrows.list_templates())==13 and {x['category'] for x in arrows.list_templates()}=={'line','planar','3d'}
    af=arrows.compile_fragment(json.loads((root/'examples/arrow-generator.spec.json').read_text(encoding='utf-8')))
    checks['arrow_fragment']=af['object_count']>=1
    bf=bcc.compile_fragment(json.loads((root/'examples/bcc-generator.spec.json').read_text(encoding='utf-8')))
    checks['bcc']=bf['site_count']==9 and abs(bf['effective_atom_count']-2.0)<1e-12 and bf['object_count']==21
    wf=wire.compile_fragment(json.loads((root/'examples/wire-sphere-generator.spec.json').read_text(encoding='utf-8')))
    vis={o['provenance']['visibility'] for o in wf['objects']}; checks['wire_sphere']=vis=={'front','back'} and wf['object_count']>9
    ef=em.compile_fragment(json.loads((root/'examples/em-wave-generator.spec.json').read_text(encoding='utf-8')))
    checks['em_wave']=ef['orthogonal_components'] and ef['electric_axis']=='y' and ef['magnetic_axis']=='z' and ef['object_count']==33
    pr=palettes.analyse(json.loads((root/'examples/palette-v1.json').read_text(encoding='utf-8')))
    checks['palette']=pr['ok'] and not pr['errors']
    with tempfile.TemporaryDirectory() as td:
        xyz=Path(td)/'water.xyz'; xyz.write_text('3\nwater\nO 0 0 0\nH 0.9572 0 0\nH -0.239 0.927 0\n',encoding='utf-8')
        ms=molecules.compile_scene(xyz,input_format='xyz',infer_xyz_bonds=False,scene_id='water-no-bonds')
        ms2=molecules.compile_scene(xyz,input_format='xyz',infer_xyz_bonds=True,scene_id='water-inferred')
        checks['molecule_conservative']=sum(o['kind']=='bond' for o in ms['objects'])==0 and sum(o['kind']=='bond' for o in ms2['objects'])>=2
        if validator.validate(ms) or validator.validate(ms2): checks['molecule_conservative']=False
    for name,ok in checks.items():
        if not ok: failures.append(f'algorithm check failed: {name}')
    skill=(root/'SKILL.md').read_text(encoding='utf-8')
    for phrase in ['明确主张 → 抽象 → 拆 → 绘 → 变 → 组 → 调 → 验','five line-arrow families','Construct molecular models','Never use computer use']:
        if phrase not in skill: failures.append(f'SKILL.md missing phrase: {phrase}')
    required=['abstraction-and-fidelity.md','arrow-taxonomy.md','color-system-and-palettes.md','labware-and-apparatus.md','molecular-model-workflows.md','source-ppt-lessons.md','wave-and-field-diagrams.md','course-source-ppt-catalog.json']
    for f in required:
        if not (root/'references'/f).exists(): failures.append(f'missing reference: {f}')
    payload={'ok':not failures,'case_count':len(cases),'cases':results,'algorithm_checks':checks,'failures':failures}
    print(json.dumps(payload,ensure_ascii=False,indent=2)); return 1 if failures else 0
if __name__=='__main__': raise SystemExit(main())
