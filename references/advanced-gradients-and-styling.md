# Advanced gradients and scientific styling

## Purpose

Use these rules when a PowerPoint scientific figure needs segmented coloring, a sharp color boundary, an off-center highlight, a non-circular radial focus, or a controlled depth cue. The objective is to preserve editability without allowing decorative styling to masquerade as scientific data.

## 1. First classify the gradient

Before creating stops, assign one semantic role:

- `decorative_shading`: depth or material cue only;
- `categorical_segments`: visually distinct regions with discrete meaning;
- `ordered_progression`: qualitative direction without quantitative calibration;
- `data_encoding`: a numerical field with units, scale, provenance, and legend.

A decorative gradient must not be described as concentration, charge density, probability, temperature, or another measured/calculated quantity. A data-encoding gradient must be derived from supplied values and must include its scale.

## 2. Hard-transition gradients

### 2.1 Core construction

A hard transition is represented by two adjacent gradient stops at the same nominal position, with the left stop carrying the preceding color and the right stop carrying the following color.

Example:

```json
{
  "transition_mode": "hard",
  "stops": [
    {"position": 0.0, "color": "#315B9A"},
    {"position": 0.32, "color": "#547FC0"},
    {"position": 0.32, "color": "#4B9B73"},
    {"position": 0.66, "color": "#73B990"},
    {"position": 0.66, "color": "#C16F44"},
    {"position": 1.0, "color": "#E39A69"}
  ]
}
```

Do not deduplicate intentional equal-position pairs during cleanup or serialization.

### 2.2 Epsilon fallback

Some adapters may reject two stops at exactly the same position. In that case:

1. retain the semantic boundary value separately;
2. place the pair at `p - epsilon/2` and `p + epsilon/2`;
3. choose the smallest epsilon that survives save/reopen;
4. render at the final export dimensions;
5. reject the result if a visible soft band remains.

The Scene must record the epsilon used. Never let the adapter silently widen the transition.

### 2.3 Curved paths and rings

A gradient applied to a curved line or closed ring may be evaluated in object/bounding-box coordinates rather than by physical arc length. Therefore:

- do not assume a stop at 0.5 lies halfway along a curve;
- when boundary position has semantic meaning, split the path into separately named segments;
- keep segment endpoints data-bound when they represent a scientific transition;
- use one editable path only when approximate placement is acceptable and explicitly illustrative.

For repeated colored arcs, deterministic segment construction is preferred over manually placing many gradient stops.

## 3. Gradient-center geometry

### 3.1 Conceptual model

An advanced radial/path gradient can be described using two regions:

- an inner focal region, which controls where the highlight or source appears;
- an outer fill region, which controls how the gradient expands toward the shape boundary.

Represent these using normalized insets or rectangles rather than an ambiguous phrase such as “move the gradient center left.” A normalized rectangle uses:

```json
{
  "left": 18,
  "right": 52,
  "top": 28,
  "bottom": 42
}
```

The values are percentages/insets interpreted by the Bridge adapter. The exact mapping must be calibrated against a known PowerPoint file and verified after save/reopen.

### 3.2 Useful focus families

- **point-like focus**: narrow inner rectangle;
- **line-like focus**: narrow in one axis and extended in the other;
- **elliptical focus**: unequal horizontal and vertical extents;
- **off-center focus**: asymmetric left/right or top/bottom insets;
- **edge highlight**: focus moved toward a boundary, with restrained falloff.

These are styling primitives, not automatically physical light sources or measured fields.

### 3.3 Capability routing

Use the least invasive route:

1. native PowerPoint/COM gradient controls, when they reproduce the required geometry;
2. a Bridge-level high-level tool such as `ppt.set_gradient_geometry`;
3. a controlled DrawingML adapter owned by the Bridge, only when the object model cannot express the geometry.

Codex must not unzip and patch arbitrary PPTX XML ad hoc in each drawing task.

## 4. Safe DrawingML adapter workflow

When advanced geometry requires a file-level patch:

1. save a versioned copy;
2. close the target presentation in PowerPoint;
3. identify the target shape by stable semantic ID, not by transient XML order alone;
4. patch only the intended shape/fill fragment;
5. preserve namespaces, relationships, package integrity, and unrelated formatting;
6. reopen in PowerPoint;
7. inspect the target object's properties when readable;
8. export a preview;
9. compare against the requested focus and against an unpatched control;
10. roll back if PowerPoint repairs the file, discards the geometry, or changes unrelated objects.

The operation is unsuccessful unless both the object/package checks and the rendered result pass.

## 5. Scientific style rules

- Use one coherent light direction across objects that belong to one physical scene.
- Keep depth shading subordinate to the information hierarchy.
- Do not use high-contrast rainbow gradients without a scientific reason and legend.
- Avoid multiple unrelated highlight directions on adjacent objects.
- Use outline contrast to preserve boundaries after grayscale conversion.
- Test at intended print size; subtle gradients visible at 200% zoom may disappear in a paper figure.
- Keep labels and connectors independent of shaded shapes so they remain readable and editable.

## 6. Bridge data contract

A Bridge should accept a structured gradient recipe containing at least:

- gradient type;
- semantic role;
- ordered stops with stable IDs;
- transition mode and epsilon;
- angle/rotation behavior;
- inner and outer geometry;
- transparency policy;
- target shape semantic ID;
- expected verification properties.

It should return:

- actual stop positions after PowerPoint normalization;
- whether native COM or DrawingML was used;
- whether save/reopen preserved the result;
- a preview path;
- warnings about fallback/default-center behavior.

## 7. QA checklist

Reject or revise when any condition is true:

- an intentional stop pair was merged;
- a hard boundary became visibly soft;
- a curve boundary moved because of bounding-box mapping;
- the gradient center returned to the default center after reopen;
- shading implies an unreported physical field;
- adjacent objects use incompatible light directions;
- the slide can only reproduce the effect as a flattened bitmap;
- the Bridge cannot identify which object received the advanced geometry.
