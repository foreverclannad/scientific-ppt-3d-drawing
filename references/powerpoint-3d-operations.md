# PowerPoint 3D operations and deterministic construction rules

## 1. Coordinate frames

Maintain four explicit frames:

1. **scene coordinates** — scientific XYZ supplied or defined by the Scene;
2. **page coordinates** — PowerPoint slide X/Y in points;
3. **object-local coordinates** — coordinates relative to a shape or group;
4. **camera coordinates** — coordinates after scene rotation, used for projection and depth sorting.

PowerPoint UI operations may act around the selected object's bounding box or local axes. The tutorial distinguishes page, selection-box, and object coordinate systems and demonstrates counterintuitive X/Y visual behavior. Therefore the adapter must calibrate the mapping rather than hard-code intuition.

Recommended adapter test:

- create an asymmetric triad labeled +X/+Y/+Z;
- apply one rotation at a time;
- render;
- record the API-to-scene mapping for the installed PowerPoint version and tool implementation.

## 2. Depth/extrusion

Use extrusion for real thickness or a diagrammatic solid.

- circle + depth → cylinder-like solid;
- rectangle + depth → prism;
- custom closed freeform + depth → custom extruded body.

Do not use large depth to imitate a sphere. Depth extends from the 2D face; define whether the face represents the front, center plane, or back in the Scene.

## 3. Bevel

Use bevel to shape front/back surfaces.

Typical constructions:

- sphere: circle/ellipse, round bevel approaching radius, negligible depth;
- capsule: ellipse/rounded profile with controlled depth and round ends;
- cylinder: circle + depth, small or zero end bevel;
- torus: ring profile + round bevel;
- cone/truncated cone: suitable bevel preset and constrained depth;
- raised frame/button: rectangle/ring + shallow bevel.

Constraints:

- bevel width <= half the smallest base dimension;
- bevel height/depth must not invert or self-intersect the body;
- preview after any large bevel change;
- keep a 2D source copy before destructive conversion.

## 4. Boolean operations

Supported conceptual operations:

- union;
- combine/xor-like combination;
- fragment;
- intersect;
- subtract.

Rules:

1. Duplicate source geometry before destructive merge.
2. Pass the primary shape explicitly; result formatting should be deterministic.
3. Preserve selection order for subtract.
4. Name the result semantically and archive/delete temporary sources deliberately.
5. Prefer boolean construction before 3D formatting.

Applications:

- rings and hollow shells;
- windows and channels;
- porous panels;
- cutaway views;
- segmented over/under crossings;
- custom arrow and ribbon profiles.

## 5. Freeforms and edit points

Use sparse points at changes in curvature, tangent, or topology.

Vertex behavior:

- smooth: aligned handles and continuous tangent;
- straight: collinear handles with independent lengths;
- corner: independent handles and discontinuous tangent.

Rules:

- do not trace every pixel;
- parameterize repeated curves;
- keep source/control points in the Scene;
- round caps and joins for tubes, loops, and bonds;
- flat caps for ribbons and strips;
- make arrowheads from explicit geometry when built-in arrows cannot express the required 3D form.

## 6. Grouping and distance from ground

`distance_from_ground` represents the object's local Z position in the Scene adapter.

For each object:

```text
scene_position = (x, y, z)
page_position = project(camera_rotation * scene_position)
distance_from_ground = adapter_scale_z(z_local)
```

When PowerPoint's native grouped 3D behavior is used:

- align parts in 2D page coordinates;
- assign Z offsets;
- group compatible parts;
- apply shared rotation, material, and light;
- inspect whether the group changes local reference frames.

Do not assume 2D layer order equals 3D visibility.

## 7. Path distribution (“integration method”)

Represent a path as a parametric function or sampled polyline.

For sample `i` among `N`:

```text
t_i = t_min + i * (t_max - t_min) / (N - 1)
p_i = path(t_i)
tangent_i = normalize(path(t_i + ε) - path(t_i - ε))
```

Place each copy at `p_i` and orient it from `tangent_i` when needed.

### Helix

```text
x(t) = cx + r cos(t)
y(t) = cy + r sin(t)
z(t) = z0 + pitch * t / (2π)
```

Parameters:

- turns;
- samples per turn;
- radius;
- pitch;
- phase;
- start/end margins;
- bond or crossbar cadence.

The tutorial's DNA-like example visibly uses 20 steps per 360° period and a 400 pt period height, yielding 20 pt axial steps. Store this as an example, not a universal molecular constant.

### Wave/ribbon

```text
x(t) = x0 + t
y(t) = y0 + A sin(ωt + φ)
z(t) = z0 + B cos(ωt + φ)
```

### Semantic naming

Use:

```text
helix.segment.0000
helix.segment.0001
helix.crossbar.0000
```

Do not depend on mutable PowerPoint group numbers.

## 8. Perspective and face stitching

Use stitching when:

- each face has a directional texture/pattern;
- a single extruded face produces unacceptable side mapping;
- a porous/lattice solid must show separate face motifs;
- exact face-level editing is required.

Workflow:

1. create and name each face;
2. apply face-specific perspective/rotation;
3. align shared corners and seams;
4. resolve overlap order;
5. group only after seam validation;
6. preserve face IDs (`cube.face.front`, etc.).

## 9. Camera-space depth sorting

For each object center or segment midpoint:

1. apply scene rotation;
2. compute camera-space depth `z_cam`;
3. sort far-to-near;
4. set PowerPoint Z-order from back to front.

The visible lesson rule is: objects nearer the viewer must be higher in the layer stack. The demonstrated operation assumes one group, an applied 3D rotation, and no nested groups.

For transparency, order alone may not guarantee ideal compositing; inspect the render and split geometry if needed.

## 10. Interlocking and woven topology

Whole-object Z-order cannot express a ring that is in front at one crossing and behind at another.

Use one of:

- split paths at crossings and alternate segment order;
- fragment shapes using masks/booleans;
- apply small alternating Z offsets to separate ribbons;
- use validated pre-rendered vector assets for extreme complexity.

For a weave, define crossing parity:

```text
over = (row_index + column_index) mod 2 == 0
z_offset = +d if over else -d
```

Then project and sort.

## 11. Texture and gradients

- Use a separate top/side face when texture continuity is important.
- Use gradient stops deliberately; avoid many arbitrary stops.
- Keep transparency compatible with depth sorting and background.
- Record whether a gradient is `shading` or `data_encoding`.
- For data encoding, include scale, units, and legend.

## 12. Object budgets and performance

Suggested starting budgets:

- normal schematic: <= 150 objects;
- molecule/crystal: <= 500 objects;
- dense helix/weave/porous construction: preview <= 800; final only as needed;
- above 1,000 objects: require batching, checkpoint saves, and explicit justification.

Use coarse sampling first. Increase object count only if the final target size reveals a meaningful difference.
