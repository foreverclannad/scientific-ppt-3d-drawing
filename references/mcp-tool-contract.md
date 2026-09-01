# Bundled PowerPoint MCP contract — Scientific Bridge v1.4

The final package includes `ppt-codex-bridge` v1.4. Use the exact tools below when it is installed. Do not substitute computer use, UI automation, macros, or an unrelated PPTX generator.

## 1. Required runtime sequence

```text
ppt_health_check
→ ppt_set_focus_policy("foreground" for visible drawing; "preserve" for background work)
→ ppt_get_capabilities
→ generate/validate/expand Scene
→ ppt_plan_scene
→ ppt_apply_scene(keep_open=true)
→ ppt_append_scene for each reconstruction stage
→ ppt_inspect_slide
→ ppt_validate_geometry
→ ppt_audit_figure
→ ppt_render_slide
→ visual review
→ ppt_patch_scene when needed
→ final render/export
```

`ppt_apply_scene` establishes the one target deck. `ppt_append_scene` adds new semantic IDs to that same visible slide, and `ppt_patch_scene` modifies existing IDs in place.

## 2. Exact bundled tools

### Connection and inspection

| Tool | Purpose |
|---|---|
| `ppt_health_check` | Verify Windows, PowerPoint COM, process, user and session health. |
| `ppt_set_focus_policy` | Keep visible drawing in front or restore the user's previous foreground window after each call. |
| `ppt_get_capabilities` | Return supported operations, limits and explicit gaps. |
| `ppt_list_presentations` | Read-only list of open presentations. |
| `ppt_create_smoke_deck` | Create the four-object native PowerPoint acceptance deck. |
| `ppt_inspect_slide` | Return semantic IDs, bounds, text, groups, connectors, fill/gradient and 3D properties. |
| `ppt_release` | Release references; quit only a safely owned PowerPoint instance. |

### Scene execution

| Tool | Purpose |
|---|---|
| `ppt_plan_scene` | Validate and compile Scene JSON without starting PowerPoint. |
| `ppt_apply_scene` | Create editable native objects, save PPTX, render PNG, export PDF and write Scene/plan/object/QA manifests. |
| `ppt_append_scene` | Compile the complete Scene but append only requested IDs to the same saved slide, with dependency preflight and rollback. |
| `ppt_patch_scene` | Apply versioned semantic-ID changes: text, move, resize, rotate, style, delete, front/back, native align and distribute. |
| `ppt_validate_geometry` | Detect off-slide, tiny and unattached objects and return the object tree. |
| `ppt_audit_figure` | Detect duplicate IDs/names, text overflow, connector crossings and incomplete raster editability declarations. |
| `ppt_render_slide` | Render through PowerPoint, not screen capture. |
| `ppt_export_presentation` | Export a presentation under `artifacts/` to PDF. |

### Assets and source PowerPoint decks

| Tool | Purpose |
|---|---|
| `ppt_list_assets` | Search approved asset roots. |
| `ppt_inspect_source_slide` | Inspect a source PPT object tree before copying. |
| `ppt_copy_source_shapes` | Copy only explicitly named native shapes/groups into a versioned target copy. |

### Gradient round trip

| Tool | Purpose |
|---|---|
| `ppt_get_gradient_stops` | Read actual stored fill/line gradient stops. |
| `ppt_set_gradient_stops` | Set ordinary stops on a versioned copy, render and return the stored values. |

## 3. Tool input conventions

### `ppt_plan_scene`

```json
{
  "scene_json": "{...}",
  "allow_partial": false,
  "include_plan": false
}
```

Use `allow_partial=false` for final figures. A high-level object such as `lattice`, `membrane`, `cutaway`, `molecule`, `wire_sphere` or `em_wave` must first be expanded by the Skill's deterministic generator script. Placeholders are only acceptable in a declared capability-board diagnostic.

### `ppt_apply_scene`

```json
{
  "scene_json": "{...}",
  "output_directory": "artifacts/project-name",
  "base_name": "figure_01",
  "overwrite": false,
  "keep_open": true,
  "export_pdf": true,
  "allow_partial": false,
  "dry_run": false
}
```

Successful output contains:

- `.pptx`;
- `.png`;
- optional `.pdf`;
- `.scene.json`;
- `.plan.json`;
- `.objects.json`;
- `.qa.json`.

Scene objects with `kind: "table"` use `table.rows` plus optional header/style/cell overrides. Objects with `kind: "chart"` use `chart.categories`, numeric `chart.series`, and a supported native chart type. Both remain editable PowerPoint objects.

### `ppt_append_scene`

```json
{
  "presentation_path": "artifacts/project-name/figure_01.pptx",
  "scene_json": "{...complete scene...}",
  "object_ids": ["panel.input", "title.input", "arrow.input_to_route"],
  "slide_index": 1,
  "keep_open": true
}
```

Every requested ID must exist in the compiled Scene and not yet exist on the slide. Connector endpoints and group members must exist already or be included in the same batch. Any invalid ID or dependency aborts before writing.

### `ppt_patch_scene`

```json
{
  "presentation_path": "artifacts/project-name/figure_01.pptx",
  "patch_json": "{\"operations\":[...]}",
  "output_directory": "artifacts/project-name",
  "base_name": "ignored_for_in_place",
  "overwrite": false,
  "keep_open": true,
  "in_place": true
}
```

Supported operations:

```json
{"op":"set_text","id":"label.method","text":"Validated method"}
{"op":"move","id":"node.validation","dx_pt":12,"dy_pt":-4}
{"op":"resize","id":"panel.main","width_pt":410,"height_pt":230}
{"op":"rotate","id":"arrow.energy","rotation_deg":18}
{"op":"set_appearance","id":"node.accepted","appearance":{"fill":"#DDEFE5"}}
{"op":"bring_to_front","id":"rim.front"}
{"op":"send_to_back","id":"glass.back"}
{"op":"delete","id":"temporary.guide"}
{"op":"align","ids":["node.a","node.b"],"alignment":"left","relative_to":"selection"}
{"op":"distribute","ids":["node.a","node.b","node.c"],"direction":"horizontal","relative_to":"selection"}
```

Reference-reconstruction patches use the same saved PPTX with `in_place=true`; free-generation workflows may still request a new copy.

## 4. Object semantics

Every meaningful native object created by the bundled Bridge receives:

- PowerPoint shape name `SPPT__<sanitised semantic ID>`;
- `scientific_id` tag containing the complete Scene ID;
- `scene_id`, `kind` and `semantic_role` tags;
- compact provenance in Alternative Text.

Use the tag value as the authoritative ID. The visible PowerPoint shape name is a safe transport name and may be sanitised.

## 5. Source-PPT policy

1. Search `references/course-source-ppt-catalog.json` and `ppt_list_assets`.
2. Check `reuse_class` before opening a deck.
3. Call `ppt_inspect_source_slide`.
4. Distinguish native shapes, groups, custom geometry, pictures and external 3D models.
5. Call `ppt_copy_source_shapes` only with explicit source shape names.
6. Rename and record provenance immediately after import.
7. Render and inspect the target copy.

The Bridge uses PowerPoint's COM object-copy operation for cross-presentation reuse. It does not click the UI, but the result still requires inspection because Office may alter fonts, themes or grouping.

## 6. Implemented and deferred capabilities

### Implemented in v1.4

- single-STA PowerPoint COM worker;
- safe attach/start and user-session checks;
- native shapes, text, lines, attached connectors and freeforms;
- editable atoms/bonds, arrows, waves and ordinary apparatus components after Scene expansion;
- semantic names/tags/provenance;
- ordinary gradient stops, including epsilon fallback for coincident stops;
- common depth, Z, material, bevel, light-direction and X/Y rotation properties;
- camera-space/source-order Z sequencing;
- approved asset-root search and explicit source-PPT object reuse;
- PPTX/PNG/PDF plus object and QA manifests;
- versioned semantic patching.
- visible-from-start Scene creation and transactional staged append in one PPTX.
- editable native tables/charts and native ShapeRange alignment/distribution.
- selectable foreground-preservation policy and structural/editability audit.

### Explicit capability gaps

- advanced off-centre gradient geometry requiring DrawingML edits;
- arbitrary Boolean merge operations;
- full editable-node round trip for every PowerPoint freeform;
- native import/manipulation of external 3D model formats;
- automatic Bridge-side expansion of all high-level scientific generators;
- visual-semantic judgement of the exported image.

When a requested result depends on one of these gaps, expand with Skill scripts, use a validated external vector/raster scientific asset, or return a capability-gap report. Never fall back to GUI automation.

## 7. Safety and transaction rules

- All output writes stay under the Bridge `artifacts/` root.
- Asset reads stay under `assets/` or roots explicitly configured by `PPT_MCP_SOURCE_ROOTS`.
- Existing files are rejected unless `overwrite=true`.
- In-place append and patch are allowed only for writable `.pptx` files under `artifacts/`; invalid batches roll back to the last saved state.
- The Bridge does not close or quit user-owned/unsaved presentations.
- All COM operations are serialised in one STA thread.
- STDIO protocol output is never mixed with ordinary stdout logging.
- Large or scientific-data-bound scenes are planned before write.
- A successful COM return is not the completion gate; inspect and render afterward.
