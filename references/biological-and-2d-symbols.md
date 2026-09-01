# Biological, chemical, and computer 2D symbol grammar

## Purpose

This reference converts the second-batch “shape + style” method into a reusable 2D scientific drawing grammar. It applies to cell-signaling pathways, chemical process diagrams, mechanism overviews, algorithms, control loops, computer architectures, data flows, and mixed biological/computational figures.

The full rule is:

> Shape + style + explicit semantic connection + scientific provenance.

## 1. Representation units

Each visible item must be one of:

- **entity**: molecule, protein, cell compartment, service, module, database, state, dataset;
- **process**: reaction, transformation, computation, validation, transport;
- **container**: membrane, organelle, subsystem, trust boundary, computational stage;
- **connector**: causal, transport, data, control, feedback, inhibition, association;
- **annotation**: label, value, condition, uncertainty, source, legend;
- **decorative support**: shading/highlight that carries no scientific meaning.

Stable semantic IDs must encode the role rather than the PowerPoint shape type.

## 2. Shape construction hierarchy

Use the simplest editable construction that communicates the entity:

1. native primitives;
2. modified native shapes/edit points;
3. sparse freeform/Bezier paths;
4. boolean combinations;
5. grouped sub-symbols;
6. approved vector asset when a custom silhouette is important.

Avoid excessive nodes. A symbol should remain easy to recolor, resize, and inspect.

## 3. Style hierarchy

Use style to reinforce, not replace, semantics:

- outline establishes boundary and grouping;
- fill distinguishes entity classes or states;
- gradient/highlight supplies restrained depth cue;
- shadow separates overlapping layers, not every object;
- transparency communicates enclosure/overlap only when ordering is already correct;
- texture is reserved for scientifically meaningful or carefully controlled material cues.

Do not encode an important distinction using color alone. Combine color with shape, line style, label, or icon.

## 4. Connector vocabulary

Every edge should declare a semantic type. Suggested visual mapping:

- `activation` / forward process: solid arrow;
- `inhibition`: line ending in a bar;
- `association`: converging connector or bracketed grouping;
- `dissociation`: diverging connector;
- `transport`: arrow crossing a declared boundary;
- `feedback`: return arrow with clear origin and destination;
- `rollback`: return path labeled as rollback/rejection;
- `optional_or_putative`: dashed connector with legend;
- `data_flow`: solid/dashed style defined by the architecture legend;
- `control_flow`: visually distinct from data flow;
- `bidirectional`: double-headed only when genuinely reciprocal.

Use attached connectors and stable anchors. Do not use a simple arrow where the scientific relation is inhibition, binding, or uncertainty.

## 5. Biological/chemical pathway rules

- Do not invent pathway members, order, localization, activation state, or interaction direction.
- Keep compartments and membranes explicit when localization matters.
- A transport edge must visibly cross the relevant boundary.
- Use repeated entity style for the same species across the figure.
- Distinguish molecule/protein/complex/process nodes when the distinction is material.
- Use labels for phosphorylation, cleavage, conformational change, or state transitions rather than relying on color alone.
- Mark hypotheses or incomplete evidence with a defined uncertain style.
- Counts, sizes, and spatial placement are illustrative unless data-bound.

## 6. Cell and membrane symbols

A stylized cell/organelle may be constructed from native/freeform outlines, inner gradients, highlights, and compartment layers. Keep:

- membrane/outline;
- lumen/cytosol;
- organelles or compartments;
- receptors/channels;
- labels and connector anchors

as separate objects. Do not flatten a pathway into the cell artwork.

For repeated membrane units, use the deterministic membrane workflow rather than decorative brushes or manual duplication.

## 7. Computer-science mapping

The same grammar maps cleanly to computing diagrams:

| Scientific pathway role | Computer-system analogue |
|---|---|
| molecule/protein/entity | service, model, dataset, state, module |
| biochemical process | computation, transformation, validation |
| membrane/compartment | subsystem, process boundary, security zone |
| activation | trigger/call/forward transition |
| inhibition | block/reject/gate |
| transport | data transfer/message passing |
| feedback | evaluation/update loop |
| uncertain pathway | optional/experimental branch |

Additional rules:

- distinguish data flow from control flow;
- show rollback, rejected candidates, or validation failures with unambiguous return paths;
- preserve temporal/causal direction;
- use 3D only for meaningful physical stacking, hardware, tensors, or deployment topology;
- do not turn ordinary algorithm boxes into decorative extrusions.

## 8. Layout grammar

- choose one dominant reading direction;
- place the main causal/data path on the strongest axis;
- keep branches orthogonal or gently curved and minimize crossings;
- align related nodes and use consistent spacing;
- put conditions/edge labels near the relevant connector without touching it;
- use containers/background regions only when they express hierarchy or location;
- reserve saturated color for emphasis or state changes;
- keep legends close to the symbols they decode.

When a connector must cross another, use a bridge/gap or reroute; do not create an ambiguous intersection.

## 9. Scene and Bridge requirements

A pathway Scene should contain:

- node IDs, labels, kinds, and states;
- edge IDs, source, target, semantic type, and direction;
- compartment/container membership;
- style tokens;
- provenance for data-bound relations;
- anchors and routing constraints;
- legend requirements;
- uncertainty/optional status.

The Bridge should support native text, shapes, groups, attached connectors, edit points/freeforms, booleans, alignment/distribution, Z-order, and object-tree inspection.

## 10. QA checklist

Reject or revise when:

- an edge relation is unsupported or directionally ambiguous;
- activation and inhibition use the same visual ending;
- data and control flow cannot be distinguished;
- the main reading direction is unclear;
- connector crossings imply false interactions;
- color is the only carrier of a critical distinction;
- labels overlap nodes or arrows;
- compartments are decorative rather than meaningful;
- a 2D logic diagram was made unnecessarily 3D;
- objects have default names or cannot be independently edited.
