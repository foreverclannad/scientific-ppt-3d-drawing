---
name: scientific-ppt-3d-drawing
description: Reconstruct reference images as high-fidelity editable PowerPoint scientific figures, or create 2D, 2.5D, and 3D figures when no reference is supplied, through a structured PowerPoint MCP/COM toolchain. Use for reference-to-PPT replication, chemistry and quantum-chemistry schematics, molecules, crystals, laboratory apparatus, scientific workflows, arrows, computer architectures, cutaways, layered devices, and publication-ready research figures. Do not use for GUI/computer-use clicking, numerical chart generation, or photorealistic rendering.
---

# Scientific PowerPoint Drawing v1.2

## Mission

When a reference image is supplied, reconstruct it faithfully as an editable PowerPoint figure. Use free generation only when the user explicitly requests it or supplies no reference. Use a PowerPoint MCP/COM bridge as the execution layer and a structured Scene JSON as the source of truth. Preserve scientific fidelity, semantic object names, deterministic geometry, editability, and reproducible exports.

The governing design principle learned from the course is:

> Scientific drawing exists to communicate, not to imitate reality. Remove information noise and strengthen the information required to support the scientific claim.

## Non-negotiable constraints

1. Never use computer use, screen coordinates, mouse/keyboard simulation, `pyautogui`, `pywinauto`, AutoHotkey, or ribbon clicking as the execution route.
2. Do not flatten the complete figure into one bitmap. Keep text, arrows, nodes, paths, apparatus parts, atoms, bonds, and geometry editable whenever PowerPoint can represent them.
3. Do not fabricate coordinates, bonds, energies, states, labels, orbital shapes, densities, crystal sites, pathway relations, tensor dimensions, units, benchmarks, or asset IDs.
4. Treat PowerPoint as a composition, vector-construction, and annotation engine. Import validated scientific assets for orbitals, electron density, ESP, numerical fields, complex meshes, proteins, and plots.
5. Use one explicit camera and one coherent light rig per 3D scene unless an inset explicitly declares a different view.
6. Assign stable semantic IDs to every meaningful object. Do not leave final objects with names such as `Oval 17`, `椭圆 9`, or `组合 23`.
7. Keep one target PPTX for a reconstruction session. Use `keep_open=true` and in-place append/patch operations; never create a revision deck for each correction.
8. Render and inspect after each material stage. Save–close–reopen only when a file-format operation requires it or for the final integrity check.
9. Never claim that advanced gradient geometry, cutaways, source-PPT copying, or native 3D construction succeeded unless object inspection and the rendered result confirm it.
10. A visually plausible result is not automatically scientifically correct. Record provenance and assumptions.

## Required inputs

Collect or infer only when scientifically safe:

- target scientific claim and intended audience;
- entities, topology, relations, coordinates, values, units, and labels;
- data-bound, illustrative, or hybrid status of each component;
- output size, formats, editability, and publication requirements;
- fonts, journal style, and semantic colour policy;
- available PowerPoint MCP tools;
- available source PPT decks, asset catalogs, SVG/EMF/PNG assets, XYZ/MOL/CIF data, plots, and orbital/density images.

When a material scientific input is missing, ask for it or mark the component `illustrative`. Do not silently substitute invented data.

## Output contract

Produce when tools permit:

- editable `.pptx`;
- rendered `.png` for review;
- optional `.pdf` and vector exports;
- final Scene JSON;
- object manifest with semantic IDs, object types, source/provenance, bounds, group path, and Z-order;
- QA report and unresolved limitations;
- capability-gap report when the Bridge cannot execute a required operation.

## Default reference-reconstruction route

If the user provides a reference image, set `workflow_mode: "reference_reconstruction"` and read `references/reference-reconstruction.md` before using the general construction workflow below.

1. Hash and measure the reference, preserve its aspect ratio, and inventory normalized regions `[x, y, width, height]`.
2. Reproduce the reference rather than improving, simplifying, rewriting, or rearranging it. Unreadable or scientifically ambiguous content stays unresolved; do not guess.
3. Use native PowerPoint text, panels, lines, arrows, and basic geometry. Use a bounded SVG, EMF, or transparent PNG only for an independent scientific object that cannot be reliably rebuilt. Never use the whole reference as the final slide background.
4. Draw into one visible deck in this order: canvas/framework → text/basic lines → arrows/charts → scientific assets → small details → difference corrections.
5. Set `ppt_set_focus_policy("foreground")`, create the blank target with `ppt_apply_scene(keep_open=true)`, append each stage with `ppt_append_scene(keep_open=true)`, and correct existing IDs with `ppt_patch_scene(in_place=true, keep_open=true)`. Use `preserve` only for unattended/background work.
6. Search the V5 catalog only when an external object is needed. Inspect 5–10 preview candidates and rank scientific identity, view, silhouette, proportion, palette, line style, and clarity. Record `asset_id`, variant, source, licence state, and match reason.
7. Compare every material render with `scripts/compare_reference.py`, then run `ppt_audit_figure`; finish only when image metrics, structural/editability audit, and region-by-region human checks pass.

Use four explicit passes even when one agent performs all of them: Designer inventories regions and routes; Drawer appends native objects/assets; Reviewer inspects, audits, and compares without editing; Corrector applies only evidence-backed semantic-ID patches. Do not let the drawing pass self-approve.

## Core workflow: 明确主张 → 抽象 → 拆 → 绘 → 变 → 组 → 调 → 验

### 0. Discover and map the execution tools

1. List available PowerPoint MCP tools.
2. Read `references/mcp-tool-contract.md`.
3. When the bundled Bridge v1.4 is present, use `ppt_health_check` → `ppt_set_focus_policy` → `ppt_get_capabilities` → `ppt_plan_scene` → `ppt_apply_scene(keep_open=true)` as the default path. In reconstruction mode, use `ppt_append_scene` for staged additions and `ppt_patch_scene(in_place=true, keep_open=true)`, `ppt_validate_geometry`, `ppt_audit_figure`, and `ppt_render_slide` for the correction loop.
4. Expand high-level generator objects with the Skill scripts before `ppt_apply_scene`; final execution uses `allow_partial=false`.
5. Map actual tools to abstract capabilities.
6. Run health check and read-only presentation/slide inspection.
7. Record capability tiers: Core, Advanced DrawingML, Source-PPT/Asset, and Scientific Generators.
8. If an essential capability is missing, do not switch to GUI automation. Produce the Scene, deterministic plans, and a capability-gap report.

### 1. State the scientific claim and information hierarchy

Before drawing, write:

- `target_claim`: what the reader should understand;
- `essential_information`: elements that must survive abstraction;
- `supporting_information`: useful but subordinate elements;
- `omitted_information`: detail intentionally removed;
- `risk_of_misinterpretation`: visual shortcuts that could imply a false scientific relation.

Read `references/abstraction-and-fidelity.md`.

### 2. Classify fidelity

Set `fidelity.mode`:

- `data_bound`: geometry, labels, values, or topology must follow supplied data;
- `illustrative`: the figure explains a concept and is not quantitative;
- `hybrid`: some components are data-bound and others illustrative.

Record source data and assumptions in the Scene. Object-level provenance may narrow the status of individual components.

### 3. Select the representation route

When the request resembles a course construction task, read `references/course-task-goal-index.md` first and use `references/course-deck-map.md` to locate the exact source slide. Course teaching-slide layout is not a publication template.

Choose the least complex route that preserves meaning:

- **2D** — pathways, algorithms, energy levels, causal/data/control flow, equations, labels, legends;
- **2.5D composite** — labware, transparent vessels, cutaways, host–guest envelopes, stitched faces, layered devices;
- **3D** — molecules, crystal geometry, spatial stacking, orientation, waves/fields when spatial orthogonality matters;
- **external scientific asset + PPT annotation** — orbitals, density/ESP fields, complex meshes, proteins, numerical plots;
- **mixed** — a clean 2D logical flow plus one spatial/scientific inset.

Do not use 3D merely for decoration. Read `references/figure-grammar.md`.

### 4. Decompose the target — 拆

Break the figure into semantic components:

- primitives, shells, faces, cut faces, rims, spouts, layers, atoms, bonds, rods, rings, arrows, ribbons;
- native tables and charts when their values are supplied;
- labels, equations, legends, callouts, dimensions;
- causal, energy, material, electron, data, and control flows;
- repeated arrays, lattices, membranes, latitude/longitude curves, wave samples, path-distributed micro-elements;
- host, guest, cavity, masks, front/back components;
- external assets such as orbital isosurfaces, plots, device silhouettes, or validated molecular renderings.

Separate scientific identity from visual styling.

### 5. Create and validate a Scene

1. Start from `schemas/scene.schema.json` and a relevant example.
2. New scenes use `schema_version: "1.0"`; legacy 0.1/0.2 scenes remain accepted.
3. Use stable IDs and explicit units.
4. Put the abstraction statement under `abstraction`.
5. Put scientific provenance under `fidelity.source_data` and object-level `provenance`.
6. Declare camera, palette/style, constraints, outputs, and object budget.
7. Run:

```bash
python scripts/validate_scene.py path/to/scene.json
python scripts/project_3d.py path/to/scene.json --output path/to/projection-plan.json
```

Resolve validation errors before writing to PowerPoint.

### 6. Resolve source PPTs and assets

1. Search an approved asset catalog before drawing a generic replacement.
2. Read `references/asset-library-contract.md`, `references/course-task-goal-index.md`, and `references/source-ppt-lessons.md`.
3. Source PPTX files are not automatically asset libraries. Inspect the actual object tree.
4. Copy only editable native shapes/groups with verified bounds, group structure, fill/line/3D properties, and source slide.
5. Treat screenshots, full-slide pictures, and knowledge-check pages as `reference_only`.
6. Rename imported objects immediately with semantic IDs.
7. Prefer PowerPoint-native groups, SVG, or EMF. Use PNG only when raster data are intrinsic or no vector/native source exists.
8. Never invent an asset ID or claim a missing source object was used.
9. Every raster asset must declare `raster_reason`, `atomic_raster_unit`, `contains_reconstructable_content`, and `decomposition_note` in object provenance; a large raster without these fields fails the final audit.

Use `references/course-deck-map.md` as the authoritative complete course map. `references/course-source-ppt-catalog.json` remains a legacy 25-deck machine catalog. The original course PPTX files are deliberately not bundled into this Skill.

### 7. Draw accurate 2D bases — 绘

Build all correct 2D contours before applying depth or bevel:

- primitives and connectors;
- sparse freeform/Bezier paths;
- edit-point modification;
- boolean union/intersect/subtract/fragment;
- deterministic duplication and distribution;
- explicit front/back fragments for occlusion;
- semantic grouping.

Preserve source copies before destructive merge operations. Use round line caps for tubes, bonds, and waves; flat caps for ribbons and cut faces. Keep labels horizontal unless an oriented label materially improves interpretation.

### 8. Apply colour as a semantic system

Read `references/color-system-and-palettes.md`.

1. Assign hue by semantic role or category, not decoration.
2. Use saturation and lightness to establish hierarchy.
3. Keep neutrals for context and reserve strong accents for the core claim.
4. Prefer coherent analogous/warm/cool systems; use complementary contrast deliberately and sparingly.
5. Avoid indiscriminate rainbow palettes.
6. Do not rely on colour alone for state, direction, or acceptance/rejection.
7. Check text contrast and grayscale separability.
8. A gradient used as scientific data encoding requires scale, units, legend, and provenance.

Run `scripts/validate_palette.py` for a palette specification.

### 9. Choose and construct arrows by meaning

Read `references/arrow-taxonomy.md`.

The final course taxonomy contains:

- **five line-arrow families** — straight, curved/wave, circular, stream bundle, segmented loop;
- **four planar-arrow families** — block, curved ribbon, folded turn, segmented cycle;
- **four 3D-arrow families** — flat extruded, depth/upright, curved extruded, segmented 3D cycle.

Rules:

1. Select scientific semantics first: forward/activation, inhibition, association, bidirectional exchange, transport, feedback, rollback, or optional/putative.
2. Use line arrows for logical or field/vector relations; filled planar arrows for dominant material/energy direction; 3D arrows only when depth/orientation adds information.
3. Construct circular arrows as deterministic repeated segments when distinct stages matter.
4. Do not depend on SmartArt.
5. Do not use colour as the sole semantic channel.

Use `scripts/generate_arrow.py` for deterministic arrow fragments.

### 10. Apply gradients and material recipes

Read `references/advanced-gradients-and-styling.md`.

#### Hard-transition gradients

- Use coincident or intentionally near-coincident stops with different colours for a hard boundary.
- Record `transition_mode: hard`, boundary position, and epsilon.
- Preserve stop order; do not deduplicate intentional pairs.
- A gradient on a curved line is not assumed to follow arc length. Split the path at semantic boundaries when exact placement matters.

#### Off-centre/path-gradient geometry

- Record inner/outer gradient rectangles or equivalent geometry.
- Use native COM APIs when sufficient.
- When COM cannot express the geometry, call a Bridge-level transactional DrawingML tool; do not ad-hoc edit ZIP/XML in each drawing task.
- Save/close the target copy before patching, reopen, inspect, and render.
- If PowerPoint repairs the file or returns to the default gradient centre, mark the operation failed.

#### Material/light discipline

Course source PPTs predominantly use coherent front orthographic cameras with `plastic`, `metal`, or `clear` materials and three-point/soft/contrasting top light rigs. Treat these as recipe families, not universal defaults. Keep one scene light direction and adapt surface lightness consistently.

### 11. Construct labware and apparatus as layered 2.5D composites

Read `references/labware-and-apparatus.md`.

For test tubes, beakers, flasks, syringes, pipettes, electrodes, and similar apparatus:

1. Separate outer glass shell, inner liquid, meniscus/top ellipse, rim, spout, base, graduation marks, and labels.
2. Create back shell/rim parts before liquid and front shell/rim parts after liquid.
3. Establish Z-order before adding transparency.
4. Use custom freeform profiles and edit points for beaker mouths, spouts, tapered walls, and rounded bottoms.
5. Apply `clear` material and controlled transparency only after geometry and occlusion are correct.
6. Keep fluid level and meniscus scientifically plausible; do not imply a measurement that was not supplied.
7. Treat course parameter tables as reproducible style recipes, not universal dimensions.

### 12. Construct cutaways as editable composites

Read `references/cutaway-and-cross-section.md`.

A cutaway consists of:

- retained outer body;
- exposed section face;
- interior wall/cavity;
- rim/edge thickness;
- foreground/background masks or fragments;
- optional removed piece.

Compute data-bound intersections deterministically. A plane–sphere intersection is a 3D circle that may project as an ellipse; do not draw an arbitrary ellipse by eye. Use `scripts/plan_cutaway.py` where applicable.

### 13. Generate lattices, wire spheres, waves, and repeated structures

Read `references/periodic-structures-and-membranes.md` and `references/wave-and-field-diagrams.md`.

#### Lattice/crystal route

- Use lattice vectors, basis sites, fractional coordinates, repeat ranges, and boundary policy.
- Preserve distinct crystallographic sites even if coincident unless explicit positional deduplication is requested.
- Do not infer bonds/coordination without an authorized rule.
- Use CIF/POSCAR/validated coordinates for data-bound crystals.
- For BCC explanatory cells, corner-site fractions are 1/8 and the body-centre site contributes 1; do not confuse visual clipping with occupancy.

Use `scripts/generate_lattice.py` or `scripts/generate_bcc_cell.py`.

#### Latitude/longitude sphere route

- Generate latitude and longitude curves parametrically.
- Split front/back curves by view direction and use Z-order/transparency/dash deliberately.
- Do not fake a sphere by placing unrelated ellipses without shared geometry.

Use `scripts/generate_wire_sphere.py`.

#### Electromagnetic-wave route

- Declare propagation direction and two orthogonal field axes.
- Keep electric and magnetic components orthogonal and phase relationship explicit.
- Use sampled vectors and separate polylines.
- Apply hard-stop/path segmentation only as an occlusion device, not as fabricated field data.

Use `scripts/generate_em_wave.py`.

#### Membrane/path route

- Define one unit, a path/surface, and local tangent/normal frames.
- Place repeated units deterministically; close circular seams.
- Treat counts and thicknesses as illustrative unless data-bound.

Use `scripts/generate_membrane.py`.

### 14. Construct molecular models through the correct route

Read `references/molecular-model-workflows.md`.

For 2D chemical structures and structural formulae, use ChemDraw first when it is installed and usable. Supply validated CDX/CDXML, MOL/SDF, or SMILES-derived structure data, export SVG or EMF, preserve its aspect ratio, and import it as a scientific asset. Do not manually reconstruct a complex chemical formula with PowerPoint primitives unless ChemDraw is unavailable or the user explicitly requires native atom/bond objects.

For polished small-molecule 3D images, prefer `ChemDraw -> MOL/SDF -> Chem3D -> transparent PNG -> PowerPoint` when a trusted, unmodified Chem3D installation is available. Generate or optimize coordinates in Chem3D with the method recorded, keep the source structure beside the render, and disclose that the imported image is not atom/bond-level editable. Use PowerPoint only for composition and annotation. Never execute a Chem3D binary whose Authenticode status is not `Valid`.

Choose one of three routes:

1. **PowerPoint-native editable ball-and-stick** — parse XYZ/MOL/SDF, preserve coordinates and declared bonds, create semantic atom/bond objects, and perform camera-space depth sorting.
2. **External interactive 3D model** — suitable for rotation/presentation but normally not object-level editable in PowerPoint; explicitly report this limitation.
3. **Validated external scientific render** — preferred for large biomolecules, proteins, orbitals, densities, ESPs, and complex surfaces; retain native PPT labels and annotations.

Rules:

- XYZ does not contain bond topology. Do not infer bonds unless explicitly authorized.
- MOL/SDF bond records may be preserved.
- Element colours and display radii are visual tokens, not measured observables.
- An optional ThreeD/ChemOffice/MolView workflow may be used when available, but the Skill must not depend on proprietary add-ins.
- Imported 3D models that can rotate but cannot be decomposed into editable PowerPoint objects are not equivalent to native ball-and-stick models.

Use `scripts/generate_molecule_scene.py`.

### 15. Host–guest and membrane routes

For host–guest figures, keep host back, guest, host front, rim, cavity, and masks separate. Correct order is:

> host back → guest → host front → occlusion fragments → transparency

Generic pillar/cup/barrel/cavity templates are illustrative envelopes, not atomistically exact structures. Read `references/supramolecular-host-guest.md`.

### 16. Convert selected geometry to 3D — 变

Apply only required properties:

- depth/extrusion;
- top/bottom bevel;
- Z offset/distance from ground;
- local rotation;
- material/light token;
- fill, gradient, transparency, or texture.

Read `references/powerpoint-3d-operations.md`.

Keep bevel dimensions bounded to prevent clipping. Distinguish page, selection-box, object-local, and camera coordinates. Calibrate the Bridge adapter rather than assuming UI X/Y rotation semantics.

### 17. Group and establish spatial relationships — 组

1. Group by semantic unit, not convenience alone.
2. Preserve meaningful child IDs and source provenance.
3. Use distance-from-ground or explicit 3D coordinates for spatial separation.
4. Recompute camera-space depth and apply back-to-front Z-order.
5. For crossing curves, waves, arrows, or woven structures, split at crossings and assign deliberate front/back fragments.
6. Do not use arbitrary PowerPoint layer order as a substitute for geometry.

### 18. Adjust, render, and validate — 调 → 验

1. Apply one camera, palette, light rig, and typography system.
2. Run geometric QA: bounds, overlaps, connector attachment, group integrity, Z-order, object budget.
3. Use native `align`/`distribute` patch operations for repeated layouts instead of hand-tuning each coordinate.
4. Render the slide at review resolution.
5. Inspect scientific hierarchy, legibility, occlusion, colour, and unnecessary detail.
6. Run `ppt_audit_figure`; treat hard findings as blockers, not advisory notes.
7. Patch by semantic object ID; avoid global rebuilds for local defects.
8. Render at least once more after corrections.
9. Save–close–reopen and inspect advanced gradients/source-copied shapes when relevant.
10. Export final PPTX/PNG/PDF and object/QA manifests.

Read `references/qa-checklist.md`.

## Domain-specific minimums

### Computational and quantum chemistry

- Require coordinates/topology or label the model illustrative.
- Keep orbital/density/ESP surfaces external and scientifically sourced.
- Preserve state labels, occupancy, spin, symmetry, units, and provenance.
- Use 2D for energy/state logic and 3D only for geometry/spatial orbitals.

### Computer science

- Keep logic/data/control flow 2D by default.
- Distinguish data flow, control flow, feedback, rollback, acceptance, and rejection.
- Use 3D only for real spatial hierarchy such as hardware, memory, tensor, or chip stacking.

### Laboratory and materials science

- Separate transparent shell, contents, cut face, and foreground rim.
- Use repeated/periodic generators rather than hand duplication.
- Distinguish illustrative texture from measured spatial distribution.

## Completion gate

Do not report completion until all applicable items are true:

- Scene and source data validated;
- abstraction statement recorded;
- all significant objects have semantic IDs;
- source PPT objects classified and inspected before copying;
- labels and arrows remain editable;
- geometry and Z-order checks pass;
- structural/editability audit has no hard findings;
- no material scientific value was invented;
- at least two renders reviewed for a nontrivial figure;
- PPTX opens without repair warning;
- exported image matches the PowerPoint layout;
- unresolved capability gaps and rasterized components are disclosed.
