# Cutaways and cross-sections

## Purpose

Use this reference for spheres, particles, capsules, porous bodies, layered devices, polyhedra, cells, materials, and other figures that reveal an interior. The central rule is:

> A convincing scientific cutaway is the combination of correct section geometry and coherent lighting on newly exposed surfaces.

A dark overlay or arbitrary ellipse is not a valid generic cutaway method.

## 1. Representation choice

Choose one route before construction:

- **projected 2.5D composite**: editable PowerPoint shell fragments, section face, rims, and masks;
- **analytic primitive cutaway**: intersection computed from a known sphere/cylinder/plane model, then represented in PowerPoint;
- **external validated mesh**: complex morphology or data-derived geometry rendered externally, with labels and annotations in PowerPoint.

PowerPoint booleans operate on projected shapes. They are not a general-purpose three-dimensional CSG engine.

## 2. Semantic decomposition

A cutaway Scene should name the following independently when applicable:

- `outer_shell_retained`;
- `outer_shell_back` and `outer_shell_front` when occlusion requires fragments;
- `section_face`;
- `interior_wall` or `cavity`;
- `rim_outer` and `rim_inner`;
- `removed_piece`;
- `foreground_mask` and `background_mask`;
- embedded inclusions, pores, layers, or labels.

Keep a non-destructive source copy before fragmenting or merging.

## 3. Plane–sphere intersection

For a sphere centered at `c`, radius `R`, and a plane defined by point `p0` and unit normal `n`:

1. signed distance from sphere center to plane:

```text
d = dot(c - p0, n)
```

2. an intersection exists when `|d| <= R`;
3. circle center:

```text
q = c - d n
```

4. intersection-circle radius:

```text
r = sqrt(R^2 - d^2)
```

5. choose orthonormal vectors `u` and `v` perpendicular to `n`;
6. sample:

```text
x(theta) = q + r [u cos(theta) + v sin(theta)]
```

The three-dimensional intersection is a circle. Under an oblique camera it may project as an ellipse. Use `scripts/plan_cutaway.py` for this analytic plan rather than drawing by eye.

## 4. General section workflow

1. Declare the body and section plane/surface.
2. Determine whether geometry is data-bound or illustrative.
3. Compute or construct the intersection contour.
4. Create the retained shell/body fragments.
5. Create a separate section face bounded by the contour.
6. Add interior walls or layer bands if thickness is visible.
7. Add rims/edges so the cut does not look like a transparent overlay.
8. Establish back-to-front order before applying transparency.
9. Apply shading using the normal of each exposed surface.
10. Render and inspect seams, thickness, and occlusion.

## 5. Lighting and material logic

The section face and curved exterior generally have different surface normals. With a common scene light vector `L`, use a consistent qualitative rule based on `max(0, dot(N, L))`, plus controlled ambient light. PowerPoint does not need physically exact rendering, but it must preserve these relations:

- faces oriented toward the light should not be darker than comparable faces oriented away from it without explanation;
- interior surfaces are usually lower contrast and slightly darker, but not uniformly black;
- the rim should be distinguishable from both shell and section face;
- transparent shells still require correct front/back layering;
- porous interiors need enough contrast to separate pores from the section plane.

Do not assign each component an unrelated highlight merely to make it look “3D.”

## 6. Common cutaway families

### 6.1 Spherical/particle cutaway

Use shell fragments plus an analytic circular section. If the object is hollow, add an inner contour and annular section band. For a core–shell particle, represent each radius separately and maintain concentric provenance.

### 6.2 Layered slab/device

Use stacked section bands with explicit thicknesses. Data-bound thickness must use supplied values or a declared visual scale. Connectors and labels remain 2D.

### 6.3 Porous solid

Separate pore geometry that intersects the section from pores hidden behind the retained shell. Avoid placing every pore as an arbitrary full circle on top of the face. Use masks/fragments or an external validated section image when morphology is material.

### 6.4 Polyhedron

Compute or derive the clipped face polygon where possible. A projected ellipse is inappropriate. Keep original face IDs and section edges distinct.

### 6.5 Biological cell/organelle

Treat membranes, lumen, nucleus, organelles, and cut surfaces as separate semantic layers. Unless data are supplied, dimensions and organelle counts are illustrative.

## 7. PowerPoint construction constraints

- Use semantic object names before booleans.
- Record the primary shape and merge operation order.
- Prefer fragment/intersect/subtract operations on duplicated source shapes.
- Preserve a source group outside the visible slide or in a source slide when allowed.
- Use a Bridge batch call for shell/cap/rim creation to avoid many fragile round trips.
- Reopen and inspect after destructive merges.
- Do not flatten the entire cutaway to a bitmap solely to hide seam errors.

## 8. Scene fields

A `cutaway` object should declare at least:

- body type and source geometry;
- section plane/surface;
- retained/removed side;
- thickness model;
- generated contour or reference to it;
- component semantic IDs;
- light/material tokens;
- fidelity status and source;
- expected object count and verification checks.

## 9. QA checklist

Reject or revise when:

- the displayed contour is inconsistent with the declared section plane;
- a plane–sphere section was drawn as an arbitrary ellipse without projection logic;
- shell, section face, and interior cannot be inspected as separate objects;
- the rim thickness changes unintentionally around the cut;
- front/back transparency order is wrong;
- lighting contradicts the common scene light;
- a data-derived interior has been replaced by decorative texture;
- the removed part still occludes the revealed interior;
- PowerPoint reopens with repaired shapes or missing fragments.
