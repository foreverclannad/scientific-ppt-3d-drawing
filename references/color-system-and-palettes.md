# Colour system and palette rules

## Course-derived design logic

Colour problems commonly appear as dark/dull, glaring, monotonous, or conflicting figures. Repair them by controlling hue, saturation, and lightness separately rather than changing random RGB values.

## Semantic palette structure

Use named roles rather than anonymous colours:

- `background`, `text`, `muted_text`, `outline`;
- `primary` for the central mechanism or object;
- `secondary` for supporting structure;
- `accent1..3` for categorical distinctions;
- `success`, `warning`, `rejection`, `uncertain` only when those semantics exist.

Hue should usually encode category; saturation and lightness encode hierarchy. Neutral greys reduce competition. Strong saturation should be reserved for the focal claim.

## Harmony options

- **analogous/adjacent** — coherent scientific systems and layered structures;
- **warm or cool family** — unified apparatus/material scenes;
- **complementary** — deliberate contrast between two competing states or pathways;
- **split-complementary** — up to three distinguishable roles without rainbow clutter.

Do not use a full spectrum merely because many objects exist.

## Accessibility and print

- Normal text should aim for at least 4.5:1 contrast against its background.
- Critical states must differ by shape, line pattern, label, or symbol in addition to hue.
- Check lightness separation in grayscale.
- Avoid very light transparent fills behind small text.
- Validate the palette with `scripts/validate_palette.py`.

## Gradients

Gradients may model form, transparency, depth, or emphasis. A gradient that encodes a measured field requires a legend, scale, units, and provenance. Decorative gradients must not resemble unreported heat maps or density fields.
