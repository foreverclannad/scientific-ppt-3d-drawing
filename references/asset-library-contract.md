# Asset library contract

## 1. Principles

- Search before constructing a generic substitute.
- Never invent an asset ID.
- Keep provenance, license/permission, format, view, and editability explicit.
- Prefer semantic search plus deterministic filters.
- Keep style and scientific identity separate: the same device may have multiple approved views/styles.

## 2. Supported asset sources

- PowerPoint asset deck (`.pptx`) with named grouped shapes;
- SVG/EMF/WMF vector files;
- PNG/JPEG raster files;
- PDF/EPS/AI source files when a conversion path is available;
- calculation outputs or plots exported from scientific software.

## 3. Recommended PowerPoint asset deck naming

Name each reusable group:

```text
ASSET__<DOMAIN>__<CONCEPT>__<VIEW>__<VARIANT>
```

Examples:

```text
ASSET__CHEM__VSC_CONVERTER__FRONT__BLUE
ASSET__CHEM__MOLECULAR_ORBITAL__ISOSURFACE__SIGNED
ASSET__CS__GPU_STACK__ISOMETRIC__NEUTRAL
ASSET__MATERIALS__POROUS_CUBE__PERSPECTIVE__GRAY
```

Do not use a concept name that the source does not justify.

## 4. Minimum catalog record

See `schemas/asset.schema.json`. A record should include:

- `asset_id`;
- title and semantic tags;
- domain/category;
- file path or PowerPoint deck + slide + shape name;
- format and vector editability;
- view/orientation and aspect ratio;
- allowed recoloring/scaling;
- connection anchors when relevant;
- provenance and permission/license;
- optional scientific metadata such as molecule, orbital, isovalue, calculation source.

## 5. Search protocol

1. Query by semantic role and domain.
2. Filter by required view/orientation.
3. Prefer vector/editable assets.
4. Filter by style compatibility.
5. Verify file existence and permissions.
6. Render previews for the top candidates.
7. Select one and record the asset ID in the Scene.

A search result must never be treated as selected until the underlying file/shape can be opened.

## 6. Insertion protocol

- copy native grouped shapes from a library deck when exact PowerPoint editability matters;
- insert SVG/EMF as vector where supported;
- preserve aspect ratio unless the asset explicitly allows distortion;
- rename the inserted group with a scene semantic ID while retaining `source_asset_id` in metadata/manifest;
- align connectors to declared anchors;
- do not recolor assets whose scientific color convention is fixed.

## 7. Fallback policy

When no asset matches:

1. construct from native primitives if scientifically adequate;
2. ask for the missing asset if fidelity depends on it;
3. use a clearly labeled placeholder only during planning;
4. never silently substitute an unrelated icon.

## 8. Building the first catalog

Run:

```bash
python scripts/build_asset_index.py --root /path/to/assets --output /path/to/asset-catalog.json
```

The scanner creates conservative file-level records. It does not infer chemistry, meaning, license, or shape anchors. Enrich those fields manually or through a verified second-pass workflow.
