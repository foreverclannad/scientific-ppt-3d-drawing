# Supramolecular host–guest illustrations

## Purpose

Use this reference to construct editable conceptual inclusion diagrams for pillar-like, cup-like, barrel-like, ring-like, and cavity-forming hosts. The method is suitable for explaining encapsulation, threading, inclusion, recognition, or transport. It is not a substitute for atomistically accurate molecular geometry.

## 1. Scientific fidelity split

Choose one:

- **illustrative envelope**: a simplified host cavity and guest communicate topology only;
- **hybrid**: a schematic envelope is combined with a validated molecular/structure asset;
- **data-bound molecular model**: coordinates, bonds, and conformation are supplied and rendered from those data.

Without coordinates or a validated source asset, generic pillar/cup/barrel shapes must be labeled illustrative. Do not identify exact stereochemistry, cavity dimensions, binding mode, or orientation from a stylized envelope alone.

## 2. Semantic decomposition

A robust host–guest Scene separates:

- back panel or back rim;
- side faces/walls;
- cavity/lumen;
- guest object;
- front panel or front rim;
- top/bottom openings;
- optional substituents/portals;
- masks used to establish inclusion;
- arrows, labels, interaction marks, and annotations.

Recommended object IDs:

```text
host.back
host.side.left
host.side.right
host.rim.back
host.cavity
 guest.core
host.rim.front
host.mask.front
```

Keep the guest independent so it can be moved, recolored, or replaced without rebuilding the host.

## 3. Occlusion before transparency

Correct inclusion is primarily an ordering problem:

1. draw the back portion of the host;
2. draw the guest;
3. draw the front portion of the host;
4. apply masks/fragments where the guest crosses an opening;
5. only then add restrained transparency.

A fully transparent host placed over the guest often looks like overlap rather than encapsulation. Front/back fragments should remain separately inspectable.

## 4. Generic host families

These are visual envelope families, not exact molecular templates:

- **pillar/ring stack**: parallel front/back rings connected by side panels;
- **cup/cone**: wider opening and tapered body;
- **barrel/portal**: constricted openings with a rounded central cavity;
- **cylindrical cavity**: neutral envelope for generic inclusion;
- **threaded ring**: guest axis passes through a ring or channel.

Do not hard-code a particular named host's chemistry into the generic geometry. Use source PPT assets or validated molecular models for chemistry-specific depictions.

## 5. Construction recipes

### 5.1 Pillar/ring envelope

- create back ring/opening;
- add side walls or repeated pillar motifs;
- add cavity shading as a separate shape;
- insert guest at the intended depth;
- add front ring/opening;
- use consistent highlights and one scene light.

### 5.2 Cup/cone envelope

- construct outer and inner profiles;
- use booleans for a hollow opening;
- create a visible rim;
- keep front lip separate for occlusion;
- align the guest with the declared cavity axis.

### 5.3 Barrel/portal envelope

- use separate back portal, body, cavity, and front portal;
- avoid extreme transparency that erases the body thickness;
- use side shading to communicate the narrower portal and wider cavity.

## 6. Interactions and annotations

Only show hydrogen bonding, π interactions, electrostatics, coordination, or hydrophobic effects when supplied or explicitly requested as an illustrative hypothesis. Use distinct connector styles and a legend. Do not infer binding energy, stoichiometry, or interaction network from visual proximity.

For association/dissociation diagrams:

- keep reactant/product states aligned;
- preserve host/guest scale unless a declared zoom is used;
- use a clear reaction/process arrow;
- place thermodynamic/kinetic values only from validated sources;
- distinguish “conceptual recognition” from a calculated structure.

## 7. Asset policy

Prefer, in order:

1. a source PPTX group with editable host components;
2. an approved SVG/EMF envelope;
3. a validated molecular rendering combined with native PPT masks/labels;
4. a generic native-shape envelope marked illustrative.

Never invent an asset ID or claim an exact host family solely because a generic silhouette resembles it.

## 8. QA checklist

Reject or revise when:

- the guest is merely overlaid rather than convincingly inside the cavity;
- front/back host elements are not separable;
- transparency hides the wall/rim thickness;
- an illustrative envelope is presented as an atomistically accurate conformation;
- interaction lines are unsupported;
- scale or orientation changes between states without disclosure;
- the host cannot be edited without flattening the full figure;
- labels overlap the cavity or obscure the inclusion relation.
