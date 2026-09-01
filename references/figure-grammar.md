# Scientific figure grammar

## 1. Use 3D to encode, not decorate

Use 3D when the scientific message depends on:

- layer order or thickness;
- spatial arrangement;
- orientation;
- enclosure or porosity;
- topology such as interlocking or weaving;
- a camera view that reveals otherwise hidden relations.

Prefer 2D when the message is sequence, hierarchy, comparison, or numerical relationship. A workflow diagram with unnecessary perspective is harder to read and less reproducible.

## 2. Visual hierarchy

A figure should have one clear primary path or object. Use three visual levels:

1. primary mechanism or structure;
2. supporting components and arrows;
3. annotations, units, and provenance.

Do not give all elements equal contrast. Avoid noisy shadows, excessive gradients, rainbow palettes, or multiple unrelated light directions.

## 3. Layout

- Keep a defined safe margin around the slide.
- Use a dominant left-to-right or top-to-bottom reading direction.
- Avoid connector crossings; when unavoidable, use bridges, routing, or spatial separation.
- Align repeated components mathematically.
- Use optical correction only after geometric alignment, and record it as an explicit offset.
- Keep insets visually subordinate and connect them to the source region unambiguously.

## 4. Camera and projection

- Use orthographic or weak perspective for technical structures unless depth perception needs stronger perspective.
- Use one camera per scene.
- Avoid a view that hides important atoms, layers, labels, or connectors.
- Test front, isometric-like, and low-angle views before choosing one.
- Preserve enough separation in camera depth to make occlusion unambiguous.

## 5. Materials and light

- Neutral balanced light is the default.
- Material is a semantic token, not a cosmetic preset.
- Use translucent layers only when seeing through them is scientifically useful.
- Do not use metallic materials for biological or nonmetallic objects merely for visual appeal.
- Keep highlights below text and edge contrast.

## 6. Color

- Use a small semantic palette.
- Keep element/species colors consistent across one figure and related figures.
- Reserve the strongest accent for the principal mechanism or state change.
- Ensure meaning is not carried by color alone; pair with labels, shapes, patterns, or line styles.
- Avoid gradients that resemble measured fields unless they encode one.

## 7. Typography

- Use one main sans-serif family for labels unless the paper style requires otherwise.
- Use a math-capable font or imported vector equation for equations.
- Keep text 2D and horizontal by default.
- Use consistent capitalization, symbols, subscripts, superscripts, and units.
- Design for the final publication size, not only the full-screen slide.

## 8. Arrows and lines

- Use arrow semantics consistently: causality, material flow, energy flow, data flow, or transition.
- Do not let decorative arrows overlap nodes or labels.
- Use round caps/joins for smooth tubes and bonds.
- Use connectors attached to anchors for movable block diagrams.
- Use explicit direction and labels for bidirectional or conditional relations.

## 9. Scientific provenance

Every data-bound component should be traceable to:

- input coordinates or table;
- a calculation output;
- an external plot or image;
- a verified material-library asset;
- an explicit assumption.

Use `fidelity.source_data` and object-level `provenance` fields.

## 10. Anti-patterns

Reject or revise:

- an entire slide inserted as one generated image;
- decorative 3D that reduces readability;
- inconsistent camera angles or light directions;
- fabricated molecular geometry or energy values;
- default PowerPoint object names;
- hand-spaced arrays;
- uncontrolled nested groups;
- booleans without saved source copies;
- unreadable labels placed on oblique surfaces;
- perspective so strong that dimensions appear misleading;
- visual style that mimics advertising rather than a scientific figure.
