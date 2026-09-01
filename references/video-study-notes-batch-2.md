# Video study notes — batch 2

## Scope and evidence level

Source archive: `PPT3D科研绘图02.zip`.

- 7 videos;
- total duration approximately 01:56:53;
- visual sampling across each video, with targeted keyframes around demonstrations and final figures;
- visible slide text and PowerPoint operations reviewed;
- no source PPTX or independent asset library in this batch;
- no claim of a complete word-for-word audio transcript.

These notes record reusable methods rather than reproducing tutorial narration. Exact RGB values, bevel presets, control points, group trees, and hidden XML properties remain provisional until the matching source PPTX is analyzed.

## 3.9 Gradient sharpening

### Observed reusable idea

A single editable line or shape can display visually discrete color regions by placing differently colored gradient stops at the same or nearly the same position. Within each region, additional stops can preserve a smooth local highlight while the region boundary remains sharp.

### Generalized rule

- represent a hard boundary as an intentional stop pair;
- preserve stop order and duplicate positions;
- use an epsilon only as an adapter compatibility fallback;
- inspect the final render, because PowerPoint may normalize stops;
- do not assume a curved line maps stops by arc length;
- split a path when the transition location is scientifically meaningful.

### Confidence

High for the visual method; medium for exact API behavior until source PPTX/COM readback is available.

## 3.10 Cross-section

### Observed reusable idea

The visual success of a cross-section depends on both the exposed contour and the light/shadow relationship of the newly exposed face. The tutorial examples use layered shapes, fragments, rims, and controlled shading rather than one overlay.

### Generalized rule

- decompose the object into retained shell, section face, interior, rim, masks, and optional removed part;
- compute analytic intersections when geometry is data-bound;
- recognize that a plane–sphere intersection is a circle in 3D and only becomes elliptical under projection;
- keep section and exterior materials/light responses distinct but consistent with one scene light;
- treat PowerPoint construction as a projected composite, not full 3D mesh CSG.

### Confidence

High for the decomposition and lighting principle; medium for exact construction sequences without the source object tree.

## 3.11 Gradient center

### Observed reusable idea

The inner and outer regions of a radial/path gradient can be manipulated beyond the common centered presets, producing off-center, line-like, or elliptical highlights.

### Generalized rule

- express the focus as normalized inner/outer geometry rather than “move it left”;
- route through native controls when possible;
- otherwise expose a controlled Bridge-level DrawingML operation;
- save a copy, close, patch, reopen, inspect, and render;
- fail explicitly if PowerPoint repairs the file or returns to a default center.

### Confidence

High for the visual concept; medium for exact DrawingML values until source PPTX inspection/calibration.

## 4.3 Supramolecular inclusion

### Observed reusable idea

Several host families can be communicated by simplified envelopes using rings/rims, side panels, cavity shading, guest placement, and front/back occlusion.

### Generalized rule

- separate host back, sides, cavity, guest, and host front;
- establish occlusion before adding transparency;
- keep generic envelopes illustrative;
- use validated coordinates or source assets when exact molecular geometry matters;
- never infer binding interactions or energetics from the silhouette.

### Confidence

High for the visual grammar; low for chemistry-specific exactness without source molecular assets.

## 4.4 Crystal lattice

### Observed reusable idea

Complex crystal/material figures become manageable when built from a small motif/unit cell, repeated by controlled displacement and grouped into higher-order structures. Examples also combine atoms, bonds/rods, polyhedra, layers, and device-like compositions.

### Generalized rule

- define lattice vectors, basis, repeat ranges, and boundary convention;
- generate sites deterministically;
- deduplicate shared boundaries;
- do not infer bonds/coordination without an explicit rule;
- use data sources such as validated coordinates for scientific claims;
- apply object-budget/LOD strategies before expanding dense structures.

### Confidence

High for the unit-cell/motif workflow; medium for exact tutorial object parameters.

## 4.5 Cell membrane

### Observed reusable idea

A planar membrane can be built by repeating one lipid unit, while a curved membrane requires local reorientation of each repeated unit along the path.

### Generalized rule

- define a lipid template;
- generate two leaflets around a centerline;
- compute tangent and normal at each placement;
- orient paired units so tails face the bilayer interior;
- close circular seams without duplicating the endpoint;
- do not bend a flattened bitmap when individual orientation matters.

### Confidence

High for the path-frame method; illustrative for molecular counts and dimensions unless data are supplied.

## 4.6 2D planar drawing

### Observed reusable idea

The tutorial explicitly reduces polished 2D scientific icons to two construction layers: shape and style. Shapes come from primitives, edit points, freeforms, booleans, and composition; style comes from outlines, gradients, shadows, and highlights.

### Generalized rule

Add a third scientific layer: semantic connection/provenance. A visually attractive pathway is not scientifically valid unless edge direction/type and entity identity are supplied.

This grammar transfers directly to computer-system diagrams:

- pathway entities → modules/services/states;
- biochemical processes → computation/validation;
- transport → data transfer;
- inhibition → gate/reject;
- feedback → update/rollback loop.

### Confidence

High for the reusable drawing grammar; pathway content itself must remain source-driven.

## Cross-video synthesis

The second batch adds three capability families missing from v0.1:

1. **advanced gradient geometry** — hard boundaries and movable/anisotropic focus;
2. **editable section/composite geometry** — cutaway decomposition with lighting consistency;
3. **deterministic generators** — lattice motifs, membrane templates, and path-oriented repetition.

It also establishes a practical 2D branch for chemistry/biology/computer figures, preventing the Skill from forcing every task into 3D.

## Known limitations pending batch 3

- source PPT object names, grouping, and Z-order are unknown;
- exact color, transparency, line, bevel, material, and lighting values are not recoverable with confidence from video alone;
- custom plugins/macros used by the instructor have not been identified from source files;
- the gradient-center implementation needs source DrawingML calibration;
- chemistry/computer asset IDs and licenses are absent;
- no end-to-end PowerPoint MCP reproduction has been executed in this environment.

These limitations are intentionally preserved in the Skill as capability gaps rather than filled with invented constants.
