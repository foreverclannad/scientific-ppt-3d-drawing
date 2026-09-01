#!/usr/bin/env python3
"""Index source PPTX decks by inspecting Open XML object structure.

No Office installation is required. The index is conservative: it distinguishes
knowledge/reference decks from construction-source decks and never claims that a
slide image is an editable asset without checking native shape counts.
"""
from __future__ import annotations
import argparse,json,re,zipfile
from collections import Counter
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS={
 'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
 'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
}
def _slides(names:list[str])->list[str]:
    def key(n):
        m=re.search(r'slide(\d+)\.xml$',n); return int(m.group(1)) if m else 10**9
    return sorted([n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=key)
def inspect(path:Path)->dict[str,Any]:
    metrics=Counter(); geometries=Counter(); fills=Counter(); texts=[]
    with zipfile.ZipFile(path) as z:
        names=z.namelist(); slide_names=_slides(names)
        for sname in slide_names:
            root=ET.fromstring(z.read(sname))
            groups=len(root.findall('.//p:grpSp',NS))
            # `shapes` follows the course catalog's object-tree convention and includes group objects.
            metrics['shapes']+=len(root.findall('.//p:sp',NS))+len(root.findall('.//p:pic',NS))+len(root.findall('.//p:graphicFrame',NS))+len(root.findall('.//p:cxnSp',NS))+groups
            metrics['groups']+=groups; metrics['pictures']+=len(root.findall('.//p:pic',NS)); metrics['connectors']+=len(root.findall('.//p:cxnSp',NS))
            # Count direct shape properties only.  Descendant-wide queries double-count properties through groups
            # and include line/text gradients that are not part of the catalog's shape-fill metric.
            metrics['custom_geometries']+=len(root.findall('.//p:sp/p:spPr/a:custGeom',NS)); metrics['gradients']+=len(root.findall('.//p:sp/p:spPr/a:gradFill',NS))
            metrics['three_d_shapes']+=len(root.findall('.//p:sp/p:spPr/a:sp3d',NS))
            for g in root.findall('.//a:prstGeom',NS): geometries[g.get('prst','unknown')]+=1
            for tag in ('solidFill','noFill','gradFill','pattFill','blipFill'):
                fills[tag]+=len(root.findall(f'.//a:{tag}',NS))
            texts.extend(t.text for t in root.findall('.//a:t',NS) if t.text)
    name=path.name
    if '知识点自查' in name: role='knowledge_reference'; reuse='reference_only'
    elif any(k in name for k in ('绘制素材','跟着做','作业')): role='construction_source'; reuse='editable_source' if metrics['pictures']<=max(2,metrics['shapes']//4) else 'mixed'
    else: role='mixed'; reuse='mixed'
    return {'file_name':name,'size_bytes':path.stat().st_size,'slide_count':len(slide_names),'source_role':role,'reuse_class':reuse,'metrics':dict(metrics),'geometry':dict(geometries),'fill':dict(fills),'text_preview':' '.join(texts)[:600]}
def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',type=Path,required=True); ap.add_argument('--output',type=Path,required=True)
    ns=ap.parse_args(); root=ns.root.resolve(); files=sorted(root.rglob('*.pptx'))
    decks=[]; aggregate=Counter()
    for p in files:
        try: d=inspect(p); decks.append(d); aggregate.update(d['metrics'])
        except (zipfile.BadZipFile,ET.ParseError,OSError,ValueError) as exc: decks.append({'file_name':p.name,'error':str(exc)})
    result={'catalog_version':'1.0','root':str(root),'deck_count':len(files),'aggregate':dict(aggregate),'decks':decks}
    ns.output.parent.mkdir(parents=True,exist_ok=True); ns.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'ok':True,'deck_count':len(files),'output':str(ns.output)},ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
