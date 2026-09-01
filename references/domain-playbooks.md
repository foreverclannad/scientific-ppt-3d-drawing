# Domain playbooks

## A. Computational and supramolecular chemistry

### A1. Molecules and ball-and-stick scenes

Data-bound inputs:

- atom IDs/elements;
- XYZ coordinates and units;
- explicit bond endpoints and any encoded bond order;
- optional radius/color policy;
- view intent.

Workflow:

1. normalize coordinates around a declared origin;
2. rotate only through a declared view transform;
3. project atom centers;
4. create spheres from circles/ellipses + round bevel;
5. create bonds from endpoints, shortened to meet sphere surfaces;
6. use one material/light rig;
7. camera-depth sort;
8. keep labels/legend 2D.

Do not infer bonds, charge, spin, or bond order unless explicitly authorized by a stated heuristic.

### A2. Host–guest and molecular-container figures

Use `references/supramolecular-host-guest.md`.

- keep host envelope, cavity, rims, panels, guest, and masks separate;
- use generic pillar/cup/barrel/toroidal templates only as illustrative envelopes;
- use supplied coordinates or validated molecular assets when geometry is scientifically material;
- avoid implying atomistic exactness through glossy 3D styling.

### A3. Crystals, lattices, and coordination polyhedra

- define lattice vectors and basis sites;
- convert fractional to Cartesian coordinates deterministically;
- use a half-open boundary convention or explicit deduplication;
- do not infer bonds/coordination without a declared rule;
- use transparency carefully for polyhedra;
- label crystallographic axes/directions when relevant;
- use CIF/POSCAR/validated coordinate sources for data-bound structures.

### A4. Layered devices and materials

Use explicit layer thickness and Z offsets for electrodes, electrolytes, membranes, interfaces, semiconductor stacks, adsorption layers, porous electrodes, composites, and cable/converter conceptual layers. Transparency is justified only when internal structure must remain visible.

### A5. Reaction paths and workflows

Use 2D process grammar for geometry progression, state transitions, optimization, evaluation, feedback, and rollback. Use 3D only for selected molecular snapshots or validated surface assets.

## B. Quantum chemistry

### B1. Energy levels and transitions

Native PowerPoint is suitable for levels, state labels, occupation arrows, transitions, couplings, avoided crossings, and active-space workflows.

- quantitative spacing requires real energies, units, and reference zero;
- distinguish allowed/forbidden/proposed/observed relations;
- do not let decorative spacing or gradients imply quantitative data.

### B2. Orbitals and fields

Do not reconstruct validated orbital/density/ESP isosurfaces from arbitrary PPT blobs. Generate them in trusted scientific software, catalog view/isovalue/sign convention/source calculation, and import as vector or controlled high-resolution raster. Keep labels and panel structure native.

A conceptual orbital icon must be labeled schematic.

### B3. Active-space and multireference workflows

Use distinct 2D states for evidence, belief/state update, proposal, physical evaluation, accept/reject/rollback, and iteration. Do not hard-code molecule-specific orbital numbers in generic templates.

## C. Biological/chemical pathways and membranes

### C1. Pathway illustrations

Use `references/biological-and-2d-symbols.md`.

- create symbols from shape recipes and style tokens;
- establish compartments before reactions;
- use connector semantics for activation, inhibition, transport, association, information flow, and putative relations;
- data-bound pathway entities/edges require a source;
- do not fabricate biological interactions.

### C2. Membranes

Use one lipid unit and generate paired leaflets from a centerline tangent/normal frame. Planar patches, waves, arcs, and vesicles must preserve local orientation and leaflet separation. Counts/thicknesses are illustrative unless supplied by data.

## D. Computer science

### D1. Architecture and data flow

- use native rounded rectangles and attached connectors;
- group by subsystem/layer;
- distinguish control, data, synchronous/asynchronous, optional, and feedback paths;
- keep one primary reading direction;
- use 3D only for hardware stacks, tensors, memory cubes, or physical deployment.

### D2. Algorithms, POMDPs, and optimization loops

Use explicit stages for observation, state/belief update, action/policy, optimization/proposal, evaluation, accept/reject/rollback, and termination. Logic remains 2D; physical scientific objects may appear as insets.

### D3. Neural networks and graph structures

Generate nodes/edges from data. Avoid complete all-to-all clutter unless topology is the message. Label dimensions and transformations. Use deterministic arrays.

### D4. Tensors, chips, and layered computing systems

Use prisms for tensor/memory blocks, label dimensions outside, and prefer orthographic/weak perspective for comparison. Cutaways/transparency must reveal meaningful internal structure.

## E. Cross-domain selection guide

| Figure need | Preferred construction |
|---|---|
| causal/process logic | 2D semantic block/pathway diagram |
| irregular scientific icon | editable shape + style recipe |
| physical stacking | 3D/2.5D layers with Z offsets |
| molecule | coordinate-driven spheres and bonds |
| crystal | lattice vectors + basis + deterministic replication |
| host–guest | editable envelope panels/rims + independent guest |
| cut surface/cavity | projected composite cutaway |
| membrane/vesicle | centerline/surface tangent-normal generator |
| energy/state relation | 2D levels + validated orbital assets |
| helix/polymer | path distribution |
| porous patterned solid | stitched faces or generated holes |
| braided/interlocking topology | split paths + alternating depth |
| numerical field/plot | external scientific plot + native annotation |
