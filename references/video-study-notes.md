# Video study notes and provenance

## Evidence basis

Version 0.1 was derived from:

- interval visual sampling across the complete 03:18:47 duration;
- targeted key-frame review around slides with explicit rules and formulas;
- visible slide text;
- visible PowerPoint construction operations and before/after results.

The source videos contain audio but no embedded subtitle stream. A complete speech-to-text transcript was not available in the working environment. Therefore:

- rules explicitly visible on slides are marked **high confidence**;
- repeated construction behavior is marked **medium-to-high confidence**;
- automation adaptations are marked **derived engineering rules**;
- audio-only nuances may be added in the second learning pass.

## Rule extraction by lesson

### 2.1 — Depth and rotation

Observed:

- A 2D profile becomes a 3D object by adding depth/extrusion.
- Circle + depth yields a cylinder-like body; rectangle/square + depth yields a prism.
- The front-face profile and depth should be designed separately.
- Layered structures are built as separate components, then aligned and given one coherent view.

Skill rules:

- construct accurate 2D bases before styling;
- use shared camera parameters across one scene;
- use depth only where the object has meaningful thickness.

Confidence: medium-to-high.

### 2.2 — Three coordinate systems

Explicit slides near approximately 03:08 and 04:54 distinguish:

- page coordinates;
- selection-box coordinates;
- object coordinates.

The tutorial demonstrates that the visual interpretation of UI X/Y rotation values can appear swapped relative to the intended local object axes. This is best understood as a coordinate-frame mapping issue, not as permission to hard-code one global axis swap.

Skill rules:

- define a scene coordinate frame;
- make the MCP adapter responsible for mapping scene axes to PowerPoint API fields;
- render a calibration object and verify orientation;
- do not mix page, selection-box, and object-local coordinates.

Confidence: high for the three-frame distinction; derived engineering rule for adapter calibration.

### 2.3 — Boolean operations

Explicit operation set:

- union;
- combine;
- fragment;
- intersect;
- subtract.

Explicit slide rule: the result inherits formatting from the first/primary selected object. Subtract is selection-order sensitive.

Applications observed: rings, hollow shells, windows, fragmented surfaces, and porous/lattice-like profiles.

Skill rules:

- pass an explicit primary shape;
- duplicate sources before destructive operations;
- perform boolean construction in 2D, then apply 3D.

Confidence: high.

### 2.4 — Materials and lighting

Observed presets include balanced/three-point-like lighting, stronger directional modes, warm/neutral/cool tones, matte/plastic/metal, and translucent/clear effects.

Skill rules:

- perceived form is a joint function of material and light;
- apply one light rig per scene;
- select material by scientific semantics, not decoration;
- avoid uncontrolled gloss and contrast.

Confidence: medium-to-high.

### 2.5 — Textures and gradients

Observed:

- built-in and image textures;
- linear, radial, rectangular, and path gradients;
- stop positions, transparency, brightness, angle/direction;
- texture distortion on extruded side faces.

Skill rules:

- separate top/side faces or stitch faces when texture orientation matters;
- use gradients for controlled shading or declared data semantics;
- never allow decorative gradients to imply a physical field accidentally.

Confidence: high for features, derived rule for scientific semantics.

### 2.6 — Curves and line editing

Observed line controls:

- color/transparency/width/dash/compound;
- cap and join types;
- arrowheads.

Explicit vertex types:

- smooth;
- straight;
- corner.

Observed applications include ribbons, helices, arrows, protein-like traces, and silhouette tracing.

Skill rules:

- use sparse meaningful nodes;
- use round caps/joins for tubes and loops;
- duplicate/flip aligned curve segments for periodic structures;
- preserve a parameterized source curve.

Confidence: high.

### 2.7 — Bevels

Observed applications:

- sphere from circle/ellipse with round bevel and minimal depth;
- cylinder from circle + depth;
- torus from ring + round bevel;
- cones, truncated cones, capsules, frames, rods, membranes, proteins, and crystal/polyhedral motifs.

Skill rules:

- bound bevel width/height by base dimensions;
- distinguish depth from bevel;
- use low-complexity primitives before freeforms.

Confidence: medium-to-high.

### 2.8 — Grouping and distance from ground

Explicit principle: after 3D grouping, original 2D layer order is not equivalent to true 3D spatial relation. `Distance from ground` acts as the object's Z coordinate within the group.

Observed molecular example: atoms and bonds are assigned different Z values, grouped, and rotated together.

Skill rules:

- map scientific XYZ coordinates to scene XYZ;
- use PowerPoint Z/distance-from-ground through the adapter;
- derive bonds from coordinate endpoints;
- apply shared camera and light after grouping.

Confidence: high.

### 2.9 — General drawing mindset

Explicit workflow:

> 拆 → 绘 → 变 → 组 → 调

Observed transparent-cylinder/cage example decomposes the object into rings, circles, cylinders, transparency, grouping, and final adjustment. The lesson also states that PowerPoint does not natively generate arrays as a parametric modeling program would.

Skill rules:

- make the workflow the runtime backbone;
- generate arrays through code/formulas;
- keep one source object and deterministic replicas.

Confidence: high.

### 3.6 — Perspective and stitching

Observed:

- perspective placement of repeated motifs;
- assembling separately patterned faces into a cube;
- separate face treatment avoids invalid side-texture behavior from one extruded object.

Skill rules:

- use face-specific perspective for patterned solids;
- calibrate seams and corner intersections;
- preserve face IDs for later edits.

Confidence: medium-to-high.

### 3.7 — Integration/path distribution

Observed:

- distribute repeated micro-elements along a path;
- form helices, waves, loops, polymer-like chains, and DNA-like structures;
- explicit example: one 360° period with total height 400 pt, 20 steps, 20 pt per step, with half-step end margins;
- periodic bond placement uses deterministic index formulas.

Skill rules:

- replace manual group-number formulas with semantic IDs and loops;
- store count, step, phase, pitch, amplitude, and tangent orientation;
- use formulas, not repeated manual alignment.

Confidence: high for visible parameterization; derived engineering rule for semantic IDs.

### 3.8 — Integration 2 and depth sorting

Observed:

- 3D arrow, helix, woven structures, chemical bonds, and interlocking rings;
- warning that high object count can make PowerPoint slow;
- explicit rule around approximately 12:02–13:30: reorder layer positions according to current distance from the viewer; nearer objects should be higher in the layer stack;
- stated constraints for the demonstrated reorder operation: same group, group has 3D rotation, no nested groups;
- coordinate-mapping concept for converting object-relative coordinates into Z/scene placement.

Skill rules:

- compute camera-space depth and set Z-order back-to-front;
- flatten nested groups before sort when required;
- split geometry at crossings for true over/under topology;
- batch operations, enforce object budgets, and checkpoint saves.

Confidence: high for explicit reorder rule/constraints; derived engineering rule for camera projection.

## Source limitations to revisit in phase 2

1. Extract audio transcription or receive subtitles to capture verbal caveats.
2. Add source PPTX to inspect exact RGB, material presets, bevel values, group trees, and naming.
3. Add the actual asset library and build a verified catalog.
4. Reproduce selected examples end-to-end through the PowerPoint MCP bridge.
5. Compare generated PPT renders against tutorial targets and record tolerances.
