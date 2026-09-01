# Reference-image reconstruction

Use this route whenever a user supplies an image to reproduce in PowerPoint. Fidelity to that image overrides the free-generation guidance elsewhere in this Skill.

## 1. Establish the contract

- Hash the original file with SHA-256 and record its pixel dimensions and source.
- Use one image per slide. If the aspect ratio is within 0.1% of 16:9, use a 16:9 canvas; otherwise set the slide to the reference ratio.
- Map pixels to PowerPoint points with `ppt_x = pixel_x / image_width * slide_width` and the equivalent formula for Y, width, and height.
- Do not beautify, paraphrase, simplify, rearrange, or replace a scientifically meaningful relationship.
- Mark unreadable text or ambiguous science as unresolved. A sourced local crop may preserve an independent ambiguous object; never invent its content.

## 2. Build the region inventory

Store every region under `reference.regions` with:

- stable `id`;
- normalized `bbox_norm: [x, y, width, height]`;
- `priority`: `critical`, `major`, or `decorative`;
- recognized text and content type;
- route: `native_ppt`, `catalog_asset`, `external_tool`, or `reference_crop`;
- source asset ID/path and editability when relevant;
- review status and unresolved notes.

Cover the canvas, panels, text blocks, separators, arrows, plots, scientific objects, decorations, and background. Regions may overlap when a critical object sits inside a larger panel.

## 3. Select the reconstruction route

- Native PowerPoint: text, boxes, lines, arrows, basic charts, legends, and simple geometric symbols.
- Catalog asset: call `ppt_list_assets`, inspect the top 5–10 previews, and select by identity first, then view, silhouette, proportion, colour, line style, and clarity.
- External tool: ChemDraw for validated 2D chemistry; Chem3D, PyMOL, or VESTA for an appropriate validated scientific render. Retain the source structure/data and method.
- Reference crop: only an independent object that cannot be reconstructed reliably. Crop tightly; record that it is not object-level editable.

For every raster route, set provenance fields `raster_reason`, `atomic_raster_unit`, `contains_reconstructable_content`, and `decomposition_note`. Use native `table` and `chart` Scene objects when the reference contains editable data displays and the values are known.

Never use the complete reference image as the slide background or cover reconstructed native content with it.

## 4. Draw visibly in one file

Compile one complete Scene, then execute stages against one target path:

```text
ppt_set_focus_policy("foreground")
→ ppt_apply_scene(objects=[], keep_open=true)
→ ppt_append_scene(framework IDs, keep_open=true)
→ ppt_append_scene(text and line IDs, keep_open=true)
→ ppt_append_scene(arrows and chart IDs, keep_open=true)
→ ppt_append_scene(scientific asset IDs, keep_open=true)
→ ppt_append_scene(detail IDs, keep_open=true)
→ ppt_patch_scene(in_place=true, keep_open=true)
→ ppt_audit_figure
```

Each append batch is transactional: all requested IDs and dependencies must validate before PowerPoint changes. Use append only for new IDs and patch only for existing IDs. Save after each stage so the user can inspect the live window without accumulating version files.

Separate the passes: Designer records regions/routes; Drawer appends; Reviewer only inspects, audits, and compares; Corrector applies targeted patches. The same Codex instance may perform all four, but review evidence must precede correction.

## 5. Visual difference loop

Render at the exact reference pixel size and run:

```powershell
python scripts/compare_reference.py --reference <reference.png> --candidate <render.png> --scene <scene.json> --output-dir <acceptance-dir>
```

The script writes `reference-compare.json`, `reference-overlay.png`, and `reference-diff.png`. Default completion targets are:

- aspect-ratio error <= 0.1%;
- normalized full-image MAE <= 0.06;
- pixels whose maximum channel difference is <= 24: at least 85%;
- edge F1 with 2-pixel tolerance: at least 0.88;
- every critical region edge F1: at least 0.85.

Use the region scores to patch the worst critical region first. Numeric success is necessary but not sufficient: verify every readable word, number, symbol, scientific relationship, panel, arrow, asset, font, line width, colour, spacing, and Z-order. Do not claim completion while a critical mismatch or unresolved scientific ambiguity remains.
