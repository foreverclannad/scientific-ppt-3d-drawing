#!/usr/bin/env python3
"""Create a conservative first-pass asset catalog from a local material library.

The scanner does not infer scientific meaning, license, or correctness. It only
creates deterministic file-level records that can be enriched later.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SUPPORTED = {'.pptx','.pptm','.svg','.emf','.wmf','.png','.jpg','.jpeg','.tif','.tiff','.pdf','.eps','.ai'}
VECTOR = {'.svg','.emf','.wmf','.eps','.ai','.pdf'}
RASTER = {'.png','.jpg','.jpeg','.tif','.tiff'}
POWERPOINT = {'.pptx','.pptm'}


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', value)
    return value.strip('-') or 'asset'


def editability(ext: str) -> str:
    if ext in POWERPOINT:
        return 'native_powerpoint'
    if ext in VECTOR:
        return 'vector'
    if ext in RASTER:
        return 'raster'
    return 'unknown'


def record(root: Path, path: Path) -> dict:
    rel = path.relative_to(root).as_posix()
    digest = hashlib.sha1(rel.encode('utf-8')).hexdigest()[:10]
    tags = []
    for part in path.relative_to(root).parts:
        if part == path.name:
            part = path.stem
        for token in re.split(r'[\s_\-.,()\[\]{}]+', part):
            token = token.strip()
            if token and token.lower() not in {t.lower() for t in tags}:
                tags.append(token)
    ext = path.suffix.lower()
    return {
        'asset_id': f'{slug(path.stem)}-{digest}',
        'title': path.stem,
        'relative_path': rel,
        'format': ext.lstrip('.'),
        'semantic_tags': tags,
        'domain': [],
        'category': 'unclassified',
        'editability': editability(ext),
        'view': 'unknown',
        'orientation': 'unknown',
        'aspect_ratio': None,
        'recolor_policy': 'unknown',
        'anchors': {},
        'scientific_metadata': {},
        'size_bytes': path.stat().st_size,
        'provenance': {
            'source': 'local_asset_library_scan',
            'license_or_permission': 'unknown — must be verified',
            'notes': 'Auto-indexed from file path only; semantic review required.'
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--include-hidden', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f'asset root is not a directory: {root}', file=sys.stderr)
        return 1
    paths = []
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        rel_parts = path.relative_to(root).parts
        if not args.include_hidden and any(part.startswith('.') for part in rel_parts):
            continue
        paths.append(path)
    paths.sort(key=lambda p: p.relative_to(root).as_posix().lower())
    catalog = {
        'catalog_version':'0.1',
        'root':str(root),
        'generated_by':'build_asset_index.py',
        'review_status':'unreviewed',
        'assets':[record(root, p) for p in paths]
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'output':str(args.output),'asset_count':len(paths)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
