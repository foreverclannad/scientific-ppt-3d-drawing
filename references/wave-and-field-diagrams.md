# Wave and field diagrams

## Wire sphere

Generate latitude and longitude curves from a common sphere equation. Split front/back curve segments by the declared view direction. Use Z-order, transparency, or dashing to reveal occlusion. Do not place unrelated ellipses by eye.

Use `scripts/generate_wire_sphere.py`.

## Electromagnetic wave

A scientific EM-wave schematic must declare:

- propagation axis;
- electric-field axis;
- magnetic-field axis;
- amplitude, wavelength/cycle count, phase, and sampling;
- whether amplitudes are illustrative or data-bound.

The electric and magnetic components must remain orthogonal. Use separate polylines and sampled vectors. Hard gradient boundaries or split paths may simulate front/back crossings, but they must not alter the underlying field data.

Use `scripts/generate_em_wave.py`.

## BCC unit cell

A body-centred cubic explanatory cell has eight corner sites and one body-centre site. Corner clipping is a visual construction; each corner contributes one eighth to the unit cell and the centre contributes one. Use validated lattice constants/elements when the cell is data-bound.

Use `scripts/generate_bcc_cell.py`.
