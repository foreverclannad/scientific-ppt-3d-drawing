# Scientific arrow taxonomy

The final course lesson organizes 13 arrow constructions into five line arrows, four planar arrows, and four 3D arrows. The Skill uses these as construction families rather than fixed decorative assets.

## Five line-arrow families

1. `line.straight` — causal/data/material flow, force, vector, transfer.
2. `line.bezier_wave` — curved transport, propagation, nonlocal relation, wave-like path.
3. `line.circular` — feedback or continuous cycle.
4. `line.stream_bundle` — convergence, divergence, multiple streams.
5. `line.segmented_loop` — staged cycle or multiple named transitions.

## Four planar-arrow families

1. `planar.block` — dominant direction or large transfer.
2. `planar.curved_ribbon` — curved transfer with visible width.
3. `planar.folded_turn` — sharp redirection or routing.
4. `planar.segmented_cycle` — repeated process stages.

## Four 3D-arrow families

1. `3d.extruded_flat` — a planar arrow with depth.
2. `3d.upright_depth` — direction into/out of scene depth.
3. `3d.curved_extruded` — spatially curved process/rotation.
4. `3d.segmented_cycle` — volumetric cycle segments.

## Semantic rules

- activation/forward: filled triangular head;
- inhibition/rejection: bar or blunt termination plus label;
- bidirectional exchange: heads at both ends;
- association: converging lines or small terminal marker;
- feedback: loop routed back to an earlier node;
- rollback: dashed reverse path with explicit label;
- optional/putative: dashed path and label.

Do not use colour alone. Avoid decorative 3D arrows in logical workflows. Circular arrows with distinct stages should be repeated segments, not a single SmartArt cycle. Use `scripts/generate_arrow.py` for deterministic fragments.
