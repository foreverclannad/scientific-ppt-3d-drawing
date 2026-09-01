# QA checklist — v0.2

## 0. Reference reconstruction

- [ ] Reference path, SHA-256, pixel dimensions, source, and normalized regions are recorded.
- [ ] Slide aspect ratio matches the reference within 0.1%.
- [ ] No whole-slide reference bitmap is used as the final background.
- [ ] Native text, panels, lines, arrows, and basic geometry remain editable.
- [ ] External/cropped scientific assets record source, licence state, match reason, and editability limit.
- [ ] One target PPTX was kept open and edited in place; no revision-deck clutter remains.
- [ ] Full-image MAE <= 0.06, within-24 ratio >= 0.85, and tolerant edge F1 >= 0.88.
- [ ] Every critical region has tolerant edge F1 >= 0.85 and passes visual inspection.
- [ ] All readable text and scientific relationships match the reference; ambiguous content is unresolved rather than guessed.

## A. Scientific integrity

- [ ] Fidelity mode is declared.
- [ ] Data-bound coordinates, values, labels, topology, and pathway relations have sources.
- [ ] Illustrative components are identified as illustrative where ambiguity matters.
- [ ] No fabricated scientific values, bonds, states, crystal sites, interactions, or asset IDs.
- [ ] Orbital/density/field assets record source calculation, view, and convention.
- [ ] Decorative gradients do not imitate unreported data fields.

## B. Scene and object model

- [ ] Scene validates.
- [ ] Semantic IDs are unique.
- [ ] References and group members resolve.
- [ ] Object count is within budget.
- [ ] Native object types are used where appropriate.
- [ ] No whole-slide raster replacement.
- [ ] Source copies/checkpoints exist for destructive booleans, group flattening, or XML patches.

## C. 2D figures and pathways

- [ ] One dominant reading direction is clear.
- [ ] Shape recipes are separated from style recipes.
- [ ] Connector endpoints remain attached.
- [ ] Activation, inhibition, transport, association, feedback, data, and control semantics are distinguishable.
- [ ] Meaning is not carried by color alone.
- [ ] Shadows/highlights do not obscure topology or suggest data.

## D. Gradients

- [ ] Stop positions are ordered and within `[0,1]`.
- [ ] Intentional coincident/near-coincident hard pairs survive save/reopen.
- [ ] Epsilon is recorded when used.
- [ ] Curved-line boundaries are not assumed to follow arc length without validation.
- [ ] Inner/outer gradient geometry is explicit when non-default.
- [ ] Advanced center survives readback and render.
- [ ] DrawingML-patched deck reopens without repair.
- [ ] Highlight direction is coherent with the scene light.

## E. Cutaways and sections

- [ ] Outer shell, section face, rim, interior wall/cavity, and masks are distinct where needed.
- [ ] Data-bound intersections are computed, not eyeballed.
- [ ] Section face shading follows a coherent normal/light relation.
- [ ] Rim thickness is visually consistent.
- [ ] Removed pieces derive from the same geometry.
- [ ] No floating cap, broken seam, or impossible occlusion.

## F. Periodic structures

- [ ] Motif/unit cell/template is explicit.
- [ ] Translation/path parameters are recorded.
- [ ] Boundary deduplication convention is declared.
- [ ] Bonds/coordination are not inferred without permission.
- [ ] Dense structures use a justified level of detail.
- [ ] IDs are deterministic.

## G. Membranes

- [ ] Leaflets are generated from local tangent/normal frames.
- [ ] Leaflet separation is coherent.
- [ ] Curved/circular seams close correctly.
- [ ] Individual orientation is preserved when biologically meaningful.
- [ ] Thickness/count is labeled illustrative unless data-bound.

## H. 3D geometry and camera

- [ ] One camera and one light rig per scene.
- [ ] Projection choice does not distort quantitative comparison.
- [ ] Bevel/depth do not self-intersect.
- [ ] Camera-space depth order is correct.
- [ ] Over/under crossings are split when whole-object Z-order is insufficient.
- [ ] Transparency renders as intended.

## I. Layout and typography

- [ ] Labels are readable at final publication size.
- [ ] Text is 2D/horizontal unless surface attachment is justified.
- [ ] Units, symbols, capitalization, subscripts, and superscripts are consistent.
- [ ] No text/arrow overlap or slide-bound violation.
- [ ] Insets are linked unambiguously.
- [ ] Visual emphasis matches scientific hierarchy.

## J. File and export

- [ ] PPTX saves and reopens without repair.
- [ ] Reopened object tree matches expected IDs/counts.
- [ ] PNG/PDF preview matches the reopened slide.
- [ ] No stale render is used for approval.
- [ ] QA report records limitations and capability gaps.
