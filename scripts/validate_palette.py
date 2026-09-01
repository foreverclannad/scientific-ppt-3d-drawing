#!/usr/bin/env python3
"""Validate semantic scientific-figure palettes using HSL and contrast checks."""
from __future__ import annotations
import argparse,colorsys,json,re
from pathlib import Path
from typing import Any
HEX_RE=re.compile(r'^#?([0-9A-Fa-f]{6})$')

def rgb(hex_color:str)->tuple[float,float,float]:
    m=HEX_RE.match(hex_color.strip())
    if not m: raise ValueError(f'invalid six-digit colour: {hex_color!r}')
    h=m.group(1); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def luminance(c:str)->float:
    vals=[]
    for x in rgb(c): vals.append(x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4)
    return 0.2126*vals[0]+0.7152*vals[1]+0.0722*vals[2]
def contrast(a:str,b:str)->float:
    x,y=sorted([luminance(a),luminance(b)],reverse=True); return (x+0.05)/(y+0.05)
def analyse(spec:dict[str,Any])->dict[str,Any]:
    colors=spec.get('colors',spec)
    if not isinstance(colors,dict): raise ValueError('palette must be an object or contain a colors object')
    info={}; errors=[]; warnings=[]
    for role,value in colors.items():
        if not isinstance(value,str): errors.append(f'{role}: colour must be a string'); continue
        try:
            r,g,b=rgb(value); h,l,s=colorsys.rgb_to_hls(r,g,b)
        except ValueError as e: errors.append(f'{role}: {e}'); continue
        info[role]={'hex':'#'+HEX_RE.match(value.strip()).group(1).upper(),'hue_deg':round(h*360,2),'saturation':round(s,4),'lightness':round(l,4),'relative_luminance':round(luminance(value),6)}
    background=colors.get('background','#FFFFFF') if isinstance(colors,dict) else '#FFFFFF'
    for role in ('text','muted_text','label'):
        if role in colors and role in info and 'background' in info:
            ratio=contrast(colors[role],background); info[role]['contrast_on_background']=round(ratio,3)
            if ratio<4.5: warnings.append(f'{role}: contrast {ratio:.2f}:1 is below 4.5:1 for normal text')
    accents=[k for k in colors if k.startswith('accent') or k in {'primary','secondary','highlight','warning','success'}]
    max_accents=int(spec.get('max_accents',3)) if isinstance(spec,dict) else 3
    if len(accents)>max_accents: warnings.append(f'{len(accents)} accent/semantic colours exceed requested maximum {max_accents}')
    # lightness distances give a conservative grayscale-separability warning
    accent_info=[(k,info[k]['lightness']) for k in accents if k in info]
    for i,(ka,la) in enumerate(accent_info):
        for kb,lb in accent_info[i+1:]:
            if abs(la-lb)<0.06: warnings.append(f'{ka} and {kb} have similar lightness; do not rely on colour alone')
    return {'ok':not errors,'errors':errors,'warnings':sorted(set(warnings)),'colors':info,'accent_roles':accents}
def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('palette',type=Path); ap.add_argument('--output',type=Path); ap.add_argument('--strict',action='store_true')
    ns=ap.parse_args(); report=analyse(json.loads(ns.palette.read_text(encoding='utf-8'))); text=json.dumps(report,ensure_ascii=False,indent=2)
    if ns.output: ns.output.parent.mkdir(parents=True,exist_ok=True); ns.output.write_text(text,encoding='utf-8')
    else: print(text)
    return 1 if report['errors'] or (ns.strict and report['warnings']) else 0
if __name__=='__main__': raise SystemExit(main())
