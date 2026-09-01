# Source-PPT inspection and reuse

## What was learned from the supplied course decks

The course archive contains both knowledge/reference slides and editable construction-source slides. They are not interchangeable.

- Knowledge-check decks primarily encode rules and should be treated as `reference_only`.
- Construction decks contain native shapes, groups, freeforms, gradients, and 3D properties that may be copied after inspection.
- Some decks mix editable shapes with raster reference images.
- Default object names are common and must be replaced with semantic IDs.

The complete course folder contains 29 decks and 51 slides. Open XML inspection found 1,238 objects, 41 groups, 229 custom geometries, 403 3D-bearing objects, 31 gradients, 82 pictures, and 92 connectors. PowerPoint COM opened and rendered all 51 slides read-only with no errors; source hashes were unchanged. These counts describe the supplied archive, not a universal style prescription.

## Reuse procedure

1. Find the drawing goal in `course-task-goal-index.md`, then locate the candidate deck and slide in `course-deck-map.md`.
2. Open or inspect the source deck read-only.
3. Enumerate slide objects, groups, pictures, freeform nodes, fills, 3D properties, and Z-order.
4. Reject full-slide pictures/screenshots as editable assets.
5. Copy selected shapes/groups to a versioned target presentation.
6. Assign semantic names and provenance immediately.
7. Reapply the destination camera/style only when this does not corrupt geometry.
8. Render, save, close, reopen, and inspect the target.

## High-value source categories

- laboratory apparatus and glassware;
- mechanical/articulated components;
- supramolecular envelope recipes;
- colour exercises;
- bevel/material/light examples;
- boolean/freeform construction exercises.

The Skill packages a catalog and small preview contact sheets, not the original course PPTX files.

The 25-deck JSON catalog predates the complete 29-deck review. Use the two Markdown course indexes above as the authoritative routing layer; keep the JSON only for legacy machine lookups.
