# Phase 3 update plan — final videos, source PPTX, and asset library

## Objective

Phase 3 will convert the current method-level Skill into a calibrated PowerPoint automation workflow grounded in the final tutorial videos, matching source PPTX files, and chemistry/computer asset libraries. It must preserve backward compatibility with Scene 0.2 unless evidence justifies a schema migration.

## 1. Intake and inventory

For every supplied archive:

1. create a file manifest with hashes, sizes, formats, and folder structure;
2. map each video to its matching PPTX, final slide, and asset folder;
3. identify fonts, themes, slide sizes, macros/add-ins, linked files, and external dependencies;
4. classify assets by domain, scientific fidelity, editability, view, orientation, license, and recolor policy;
5. retain source files read-only and work on copies.

Do not infer that similarly named files are linked; verify through slide content/object IDs.

## 2. Source PPTX object-tree extraction

Use PowerPoint COM/Open XML inspection to record, per relevant slide:

- shape ID, name, type, bounds, rotation, flip, Z-order;
- group hierarchy and child order;
- text, font, size, alignment, spacing, and language;
- fill type, color stops, transparency, angle, and advanced gradient geometry;
- line, cap, join, dash, arrowhead, and connector attachment;
- freeform node/control-point geometry;
- 3D depth, bevel, contour, material, lighting, camera, and distance from ground;
- crop, transparency, and source path for pictures/SVG/EMF;
- merge/fragment results where inferable;
- slide/master/theme dependencies.

Store normalized JSON snapshots and a rendered preview for each source slide.

## 3. DrawingML calibration

Build controlled fixtures for advanced gradient-center operations:

1. create a known native shape in PowerPoint;
2. apply the tutorial effect in a source PPTX;
3. compare relevant DrawingML fragments;
4. identify the minimum stable patch;
5. implement it behind a high-level Bridge tool;
6. verify save/reopen/readback/render;
7. add rollback and package-integrity tests;
8. document unsupported Office versions.

Never expose raw arbitrary XML mutation as the normal Codex tool.

## 4. Asset catalog construction

Create a machine-readable catalog and contact sheets. Each asset entry should include:

- stable `asset_id`;
- source file and source slide/group;
- domain/category and semantic roles;
- scientific scope and fidelity status;
- file type and editability;
- aspect ratio and recommended scale range;
- view/orientation and connection anchors;
- color/recolor policy;
- license/usage restrictions;
- preview path;
- dependencies such as fonts or linked images;
- known compatibility issues.

For PPTX libraries, name reusable groups with deterministic prefixes and preserve group internals.

## 5. Chemistry-specific expansion

Prioritize:

- atom/bond and ball-and-stick style calibration;
- crystal/unit-cell/polyhedron examples tied to real coordinates;
- supramolecular host–guest source groups;
- reaction/energy/pathway schematics;
- membranes, layered materials, porous structures, and interfaces;
- external orbital/density/ESP asset integration;
- chemical typography, subscripts, charges, state labels, and legends.

Hard rule: source PPT decorative molecular icons remain illustrative unless linked to validated structural data.

## 6. Computer-science-specific expansion

Prioritize:

- architecture, data-flow, control-flow, pipeline, and feedback-loop templates;
- algorithm/POMDP/QUBO states, actions, observations, validation, acceptance/rejection, and rollback;
- neural-network/graph/tensor/hardware visual components;
- semantic connector styles and anchor rules;
- consistent treatment of modules, datasets, models, services, storage, and physical devices;
- optional 3D only for spatial topology, tensors, hardware stacks, or deployment layers.

Use source PPT examples to calibrate spacing, arrows, grouping, and typography, not to hard-code a single project vocabulary.

## 7. Bridge capability expansion

Implement and test, in order:

### Base read/write

- inspect presentation/slide/object tree;
- create native shapes, text, connectors, freeforms, groups;
- set style/3D properties;
- save, reopen, render, export.

### Level 1 batch operations

- `ppt.apply_scene` and `ppt.patch_scene`;
- deterministic arrays and path distributions;
- semantic alignment/distribution;
- depth sorting and path splitting;
- copy named group from a PPT asset library;
- validate geometry and object manifest.

### Level 2 calibrated operations

- advanced gradient geometry;
- safe DrawingML adapter;
- source-group cloning with theme/style normalization;
- shape-node read/write where COM coverage is insufficient;
- structured readback for verification.

No capability may fall back to GUI clicking.

## 8. Evaluation design

### 8.1 Reproduction tests

Select representative source figures and compare:

- semantic object coverage;
- object count/group hierarchy;
- geometry and alignment;
- color/line/material tokens;
- gradient stops/centers;
- occlusion/Z-order;
- final render at publication size.

A reproduction need not be pixel-identical when the source uses unstable manual offsets, but deviations must be explained.

### 8.2 Generalization tests

Use unseen tasks in the same grammar:

- a new molecule/crystal/material schematic;
- a new host–guest inclusion layout;
- a new quantum-chemistry workflow;
- a new algorithm/control architecture;
- a hybrid figure combining a validated scientific asset with native PPT annotation.

The Skill must choose the correct route and not copy source-specific labels or asset IDs blindly.

### 8.3 Regression tests

Retain all v0.2 examples and algorithm checks. Add source-PPT readback fixtures, asset-catalog tests, package-integrity tests, and MCP smoke tests.

## 9. Schema migration criteria

Move from Scene 0.2 only when source analysis demonstrates a missing concept that cannot be represented without ambiguity. Potential additions:

- calibrated PowerPoint style tokens;
- source-PPT group references;
- explicit DrawingML gradient geometry;
- per-object connector anchors;
- reusable template/motif definitions;
- provenance links to source slide/shape IDs;
- render-comparison tolerances.

Provide a migration script and keep legacy examples passing.

## 10. Completion criteria for Phase 3

Phase 3 is complete only when:

- final videos and matching PPTX are mapped;
- source object trees and relevant DrawingML are extracted;
- asset catalog/search/preview works;
- at least several chemistry and computer source figures are reproduced through MCP/COM;
- all outputs remain editable as intended;
- save/reopen/render verification passes;
- generalization tests pass on unseen tasks;
- limitations and version-specific behavior are documented;
- no computer-use fallback is required.
