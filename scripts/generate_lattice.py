#!/usr/bin/env python3
"""Expand lattice vectors, fractional basis sites, and repeat counts into objects.

No bonds or coordination are inferred. Coincident positions are preserved by
default because distinct crystallographic sites must not be silently merged.
Standard-library only.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def finite_number(v: Any, name: str) -> float:
    if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(float(v)):
        raise ValueError(f"{name} must be a finite number")
    return float(v)


def vec3(v: Any, name: str) -> list[float]:
    if not isinstance(v, list) or len(v) != 3:
        raise ValueError(f"{name} must be three finite numbers")
    return [finite_number(x, f"{name}[{i}]") for i, x in enumerate(v)]


def compile_fragment(spec: dict[str, Any]) -> dict[str, Any]:
    vectors = spec.get("lattice_vectors")
    basis = spec.get("basis")
    repeats = spec.get("repeats")
    if not isinstance(vectors, list) or len(vectors) != 3:
        raise ValueError("lattice_vectors must contain three vectors")
    vectors = [vec3(v, f"lattice_vectors[{i}]") for i, v in enumerate(vectors)]
    if not isinstance(basis, list) or not basis:
        raise ValueError("basis must be a non-empty array")
    if (
        not isinstance(repeats, list)
        or len(repeats) != 3
        or any(not isinstance(n, int) or isinstance(n, bool) or n < 1 for n in repeats)
    ):
        raise ValueError("repeats must be three positive integers")

    origin = vec3(spec.get("origin", [0, 0, 0]), "origin")
    prefix = str(spec.get("id_prefix", "lattice")).strip()
    if not prefix:
        raise ValueError("id_prefix must not be empty")

    boundary_mode = spec.get("boundary_mode", "half_open")
    if boundary_mode not in {"half_open", "explicit"}:
        raise ValueError("boundary_mode must be half_open or explicit")

    deduplicate_positions = bool(spec.get("deduplicate_positions", False))
    tol = finite_number(spec.get("deduplicate_tolerance", 1e-8), "deduplicate_tolerance")
    if tol <= 0:
        raise ValueError("deduplicate_tolerance must be positive")

    max_objects_raw = spec.get("max_objects", 10000)
    if not isinstance(max_objects_raw, int) or isinstance(max_objects_raw, bool) or max_objects_raw < 1:
        raise ValueError("max_objects must be a positive integer")
    expected_objects = len(basis) * repeats[0] * repeats[1] * repeats[2]
    if expected_objects > max_objects_raw:
        raise ValueError(
            f"requested lattice may create {expected_objects} objects, exceeding max_objects={max_objects_raw}"
        )

    # Validate basis before generation so IDs and fractional coordinates fail early.
    normalized_basis: list[dict[str, Any]] = []
    basis_ids: set[str] = set()
    for bi, site in enumerate(basis):
        if not isinstance(site, dict):
            raise ValueError(f"basis[{bi}] must be an object")
        sid = str(site.get("id", f"site{bi}")).strip()
        if not sid:
            raise ValueError(f"basis[{bi}].id must not be empty")
        if sid in basis_ids:
            raise ValueError(f"duplicate basis id: {sid}")
        basis_ids.add(sid)
        frac = vec3(site.get("fractional"), f"basis[{bi}].fractional")
        if boundary_mode == "half_open" and any(x < -1e-12 or x >= 1 - 1e-12 for x in frac):
            raise ValueError(f"basis[{bi}].fractional must be in [0,1) for half_open mode")
        geometry = site.get("geometry", {})
        if not isinstance(geometry, dict):
            raise ValueError(f"basis[{bi}].geometry must be an object")
        normalized_basis.append({"source": site, "id": sid, "fractional": frac, "geometry": geometry})

    objects: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    first_id_at_position: dict[tuple[int, int, int], str] = {}
    coincident_positions: list[dict[str, Any]] = []
    dropped_duplicates: list[dict[str, Any]] = []

    for site_info in normalized_basis:
        site = site_info["source"]
        sid = site_info["id"]
        frac = site_info["fractional"]
        kind = site.get("kind", "atom")
        for i in range(repeats[0]):
            for j in range(repeats[1]):
                for k in range(repeats[2]):
                    coeff = [i + frac[0], j + frac[1], k + frac[2]]
                    pos = [origin[d] + sum(coeff[a] * vectors[a][d] for a in range(3)) for d in range(3)]
                    pos_key = tuple(round(x / tol) for x in pos)
                    obj_id = f"{prefix}.cell.{i:03d}.{j:03d}.{k:03d}.site.{sid}"
                    if obj_id in seen_ids:
                        raise ValueError(f"duplicate generated ID: {obj_id}")

                    coincident_with = first_id_at_position.get(pos_key)
                    if coincident_with is not None:
                        event = {
                            "position3d": [round(x, 8) for x in pos],
                            "existing_id": coincident_with,
                            "candidate_id": obj_id,
                        }
                        coincident_positions.append(event)
                        if deduplicate_positions:
                            dropped_duplicates.append(event)
                            continue
                    else:
                        first_id_at_position[pos_key] = obj_id

                    seen_ids.add(obj_id)
                    geom = dict(site_info["geometry"])
                    geom["position3d"] = [round(x, 8) for x in pos]
                    obj: dict[str, Any] = {
                        "id": obj_id,
                        "kind": kind,
                        "semantic_role": site.get("semantic_role", "lattice_site"),
                        "geometry": geom,
                        "provenance": {
                            "generator": "generate_lattice.py",
                            "basis_id": sid,
                            "cell_index": [i, j, k],
                            "fractional": frac,
                        },
                    }
                    if coincident_with is not None:
                        obj["provenance"]["coincident_with"] = coincident_with
                    for key in ("element", "appearance", "text", "occupancy", "site_label"):
                        if key in site:
                            obj[key] = site[key]
                    objects.append(obj)

    warnings: list[str] = []
    if coincident_positions and not deduplicate_positions:
        warnings.append(
            "Coincident positions were preserved because deduplicate_positions=false; inspect occupancy/site semantics."
        )
    if dropped_duplicates:
        warnings.append(
            "Coincident positions were removed by explicit deduplicate_positions=true; review dropped_duplicates before scientific use."
        )

    return {
        "generator": "lattice",
        "boundary_mode": boundary_mode,
        "position_deduplication": deduplicate_positions,
        "deduplicate_tolerance": tol,
        "lattice_vectors": vectors,
        "basis_count": len(normalized_basis),
        "repeats": repeats,
        "expected_object_count_before_optional_deduplication": expected_objects,
        "object_count": len(objects),
        "coincident_position_count": len(coincident_positions),
        "coincident_positions": coincident_positions,
        "dropped_duplicate_count": len(dropped_duplicates),
        "dropped_duplicates": dropped_duplicates,
        "objects": objects,
        "bonds_inferred": False,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = compile_fragment(json.loads(args.spec.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"lattice generation failed: {exc}", file=sys.stderr)
        return 1
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(args.output)
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
