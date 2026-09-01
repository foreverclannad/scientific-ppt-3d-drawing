# Molecular-model workflows

## Default 2D chemical-structure route — ChemDraw

Use ChemDraw first for 2D structural formulae when it is installed and usable. Use native PowerPoint atom/bond construction only when ChemDraw is unavailable or object-level PowerPoint editability is explicitly required.

1. Require validated CDX/CDXML, MOL/SDF, or SMILES-derived structure data. Do not infer a complex structure from a screenshot.
2. Prefer MOL/SDF or CDXML for automation because they preserve explicit atoms, bonds, charges, and available stereochemistry. Verify SMILES conversion before use.
3. Keep ChemDraw visible when the user wants to watch the drawing process. Automate through its document/COM interfaces, not screen-coordinate clicking.
4. On the verified ChemDraw 20 workflow, open the visible application first and attach with `GetActiveObject("ChemDraw.Application")`; direct creation of a new COM instance may return `0x80040112`. `Documents.Open()` accepts MOL, and `SaveAs(<path>.svg)` exports SVG. Treat this as a tested compatibility recipe, not a universal version guarantee.
5. Inspect the ChemDraw document before export: confirm atom and bond counts, bond orders, charges, stereochemistry, and any enhanced-stereo labels such as `abs` or `&1`. Remove a label only when the source does not require it.
6. Export SVG by default. Retain the original ChemDraw or MOL/SDF source beside the project for future chemical editing.
7. Preserve the SVG `width`, `height`, or `viewBox` ratio exactly when placing it in PowerPoint. Never stretch a molecule to fill a frame.
8. For the bundled Bridge, declare the SVG as `kind: "asset"` with `appearance: {"fill":"none","outline":"none","transparency":0}` so PowerPoint does not recolour it with the Bridge's default picture fill.
9. If `ppt_patch_scene` cannot add an asset to an existing deck, create a minimal staging PPTX, inspect its object names, then use `ppt_copy_source_shapes(..., in_place=true, keep_open=true)` to copy the SVG into the open target presentation.
10. Render the complete target slide, not only the isolated molecule. Check colour, aspect ratio, label legibility, clipping, cover masks, and Z-order before acceptance.

An imported SVG is a high-quality vector object but is not equivalent to atom/bond-level PowerPoint editability. Keep surrounding labels and annotations native, and report this limitation.

## Default 3D small-molecule render route — Chem3D

Use this route for attractive ball-and-stick or space-filling images of small molecules. It is an external-render route; PowerPoint remains responsible for labels, arrows, captions, and page composition.

1. Verify the Chem3D executable before launch. Require Authenticode status `Valid`; do not run `HashMismatch`, unsigned, or otherwise modified binaries.
2. Start from a validated ChemDraw structure and export MOL or SDF so atom identity, bonds, charges, and stereochemistry are explicit.
3. Open the structure in visible Chem3D. Confirm atom count, bond topology, formal charge, stereochemistry, and whether the input contains real 3D coordinates.
4. If 3D coordinates are absent, generate a conformer and run an appropriate built-in geometry optimization. Record the force field or method and do not imply quantum-chemical accuracy.
5. Choose the representation by purpose: ball-and-stick for connectivity, space-filling for steric volume, ribbon/cartoon for proteins in a biomolecular tool, and surfaces/orbitals in a quantum-chemistry viewer.
6. Use a restrained element palette, neutral lighting, readable bond thickness, a deliberate camera angle, and a transparent or plain background. Avoid glossy decorative effects that obscure connectivity.
7. Export a high-resolution transparent PNG when supported. Keep the MOL/SDF and any native Chem3D document beside the image as provenance.
8. Import the PNG without stretching, keep all explanatory text native in PowerPoint, render the complete slide, and inspect at full-slide scale.

If a trusted Chem3D installation is unavailable, use Avogadro for small-molecule conformers/renders. Use PyMOL or ChimeraX for proteins and complexes, GaussView/IQmol or Multiwfn+VMD for orbitals and density/ESP surfaces, and VESTA or Mercury for crystals and periodic materials.

For 2.5D structural formulae, stay in ChemDraw and use wedge/dash bonds or perspective sparingly; do not generate a true 3D render merely to decorate a flat scheme.

## Route A — native editable PowerPoint model

Use for small and medium molecular structures when object-level editability matters.

1. Read validated XYZ, MOL, or SDF data.
2. Preserve atomic coordinates.
3. Preserve bond records from MOL/SDF.
4. Do not infer XYZ bonds unless explicitly authorized.
5. Generate one semantic atom object and one bond object per declared bond.
6. Project coordinates through one camera and depth-sort in camera space.
7. Use round bevels for atoms and round-ended cylinders/lines for bonds.

Use `scripts/generate_molecule_scene.py`.

## Route B — interactive external 3D model

PowerPoint may display and rotate an imported 3D model, but it is generally not decomposable into editable atom/bond shapes. Treat this as an interactive presentation asset, not as a native editable model. Record the limitation in the manifest.

## Route C — external scientific render

Use for proteins, large biomolecules, orbital isosurfaces, electron density, ESP, complex meshes, and publication-quality molecular surfaces. Generate the science in appropriate software, export SVG/EMF or high-resolution transparent PNG, then keep PowerPoint annotations native.

## Other optional software routes

MolView, Avogadro, and the ThreeD add-in can assist molecule acquisition, conversion, or 3D rendering when ChemDraw does not cover the required representation. Course evidence shows version-dependent behaviour and that imported 3D models may not be editable. The Skill must verify actual editability after import and retain a non-proprietary fallback.

## Scientific guardrails

- element colours and display radii are visual tokens;
- inferred bonds must be marked as inferred;
- bond order, charge, spin, state, and stereochemistry must come from source data;
- do not replace a validated orbital/density surface with a generic PowerPoint blob.
