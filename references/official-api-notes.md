# PowerPoint / DrawingML adapter notes

This file records implementation boundaries rather than promising that every property is exposed identically through every automation layer.

## PowerPoint object model

The Windows PowerPoint object model provides application, presentation, slide, shape, text, line, grouping, Z-order, export, fill, line, and 3D-format objects. The Bridge should wrap these in stable high-level MCP tools rather than exposing the full COM surface directly.

## Freeforms and booleans

Freeform nodes and merge operations are sensitive to source order, primary shape, local coordinates, and formatting inheritance. Preserve source shapes until the result validates.

## Path-gradient geometry

DrawingML represents path-gradient details separately from ordinary stop lists. Advanced inner/outer focus geometry may require controlled package-level XML changes when the installed automation API cannot set it.

Safe sequence:

1. save a copy;
2. close the copy in PowerPoint;
3. patch only the identified shape's gradient geometry;
4. reopen;
5. read back properties;
6. render;
7. reject any repair warning or silent fallback.

Do not patch a file while PowerPoint holds a stale open object model for that same copy.

## Version calibration

The Bridge should run a calibration deck for:

- rotation-axis mapping;
- material/light presets;
- gradient stop roundtrip;
- coincident-stop behavior;
- path-gradient center persistence;
- shape export formats;
- nested group and Z-order behavior.

Store the observed capability profile with the PowerPoint version and Bridge version.
