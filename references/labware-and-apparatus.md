# Labware and apparatus construction

## Layer model

Transparent laboratory objects are 2.5D composites. Typical semantic parts are:

1. back glass shell;
2. inner liquid/body;
3. meniscus or top liquid ellipse;
4. back rim;
5. front rim and foreground shell;
6. spout, base, neck, plunger, electrode, or tool-specific components;
7. graduation marks and labels.

Build geometry and Z-order before transparency.

## Test tube

- use a tapered or parallel outer shell with rounded lower end;
- represent liquid as a separate inner shape with a top meniscus;
- retain a visible front rim and subtle rear rim;
- use controlled transparency rather than no fill;
- avoid a perfectly flat liquid surface when the drawing implies a meniscus.

## Beaker

- use a custom freeform profile for tapered walls and spout;
- separate rear lip, front lip, liquid, and front wall;
- keep the mouth ellipse consistent with perspective;
- do not use one transparent cylinder as the entire beaker;
- graduation marks should follow the front face and remain editable.

## Other apparatus

Course source decks include editable or mixed recipes for lenses, electrodes, syringes, round-bottom flasks, micropipettes, beakers, and a mechanical arm. Parameters such as depth, bevel, material, transparency, and line width are style recipes, not scientific dimensions.

## Source reuse

Use `course-source-ppt-catalog.json` to find candidate source decks. Inspect objects before copying, copy only native groups/shapes, preserve source provenance, and rename default object names immediately.
