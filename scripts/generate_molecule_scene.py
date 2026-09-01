#!/usr/bin/env python3
"""Compile XYZ or MOL V2000 data into a scientific PowerPoint Scene.

The default is conservative: XYZ input does not create bonds unless --infer-bonds
is supplied. MOL V2000 bond records are preserved. Generated atom/bond objects
remain PowerPoint-native candidates; large biomolecules and volumetric surfaces
should use validated external assets instead.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ELEMENT_STYLE: dict[str, dict[str, Any]] = {
    "H": {"color": "#FFFFFF", "radius": 0.31},
    "C": {"color": "#3A3A3A", "radius": 0.76},
    "N": {"color": "#3155D9", "radius": 0.71},
    "O": {"color": "#E53935", "radius": 0.66},
    "F": {"color": "#64D65A", "radius": 0.57},
    "P": {"color": "#F49A36", "radius": 1.07},
    "S": {"color": "#F2CE3D", "radius": 1.05},
    "Cl": {"color": "#36B44A", "radius": 1.02},
    "Ti": {"color": "#A0A0A0", "radius": 1.60},
}
DEFAULT_STYLE = {"color": "#A8A8A8", "radius": 0.90}


@dataclass(frozen=True)
class Atom:
    index: int
    element: str
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Bond:
    a: int
    b: int
    order: int = 1
    provenance: str = "source"


def _normalise_element(value: str) -> str:
    value = re.sub(r"[^A-Za-z]", "", value.strip())
    if not value:
        raise ValueError("empty/invalid element symbol")
    return value[0].upper() + value[1:].lower()


def parse_xyz(path: Path) -> tuple[list[Atom], list[Bond], str]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines:
        raise ValueError("empty XYZ file")
    try:
        count = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError("XYZ first line must be an atom count") from exc
    if len(lines) < count + 2:
        raise ValueError(f"XYZ declares {count} atoms but contains too few lines")
    comment = lines[1].strip()
    atoms: list[Atom] = []
    for i, line in enumerate(lines[2 : 2 + count], start=1):
        fields = line.split()
        if len(fields) < 4:
            raise ValueError(f"XYZ atom line {i + 2} has fewer than four fields")
        element = _normalise_element(fields[0])
        try:
            x, y, z = map(float, fields[1:4])
        except ValueError as exc:
            raise ValueError(f"invalid coordinate on XYZ atom line {i + 2}") from exc
        if not all(math.isfinite(v) for v in (x, y, z)):
            raise ValueError(f"non-finite coordinate on XYZ atom line {i + 2}")
        atoms.append(Atom(i, element, x, y, z))
    return atoms, [], comment


def parse_mol_v2000(path: Path) -> tuple[list[Atom], list[Bond], str]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if any("V3000" in line for line in lines[:12]):
        raise ValueError("MOL V3000 is not supported by this lightweight parser")
    if len(lines) < 4:
        raise ValueError("MOL file is too short")
    counts = lines[3]
    try:
        atom_count = int(counts[0:3])
        bond_count = int(counts[3:6])
    except ValueError as exc:
        # tolerate whitespace-delimited counts written by some exporters
        fields = counts.split()
        if len(fields) < 2:
            raise ValueError("cannot parse MOL V2000 counts line") from exc
        atom_count, bond_count = int(fields[0]), int(fields[1])
    if len(lines) < 4 + atom_count + bond_count:
        raise ValueError("MOL file is truncated")
    atoms: list[Atom] = []
    for i, line in enumerate(lines[4 : 4 + atom_count], start=1):
        try:
            x = float(line[0:10])
            y = float(line[10:20])
            z = float(line[20:30])
            element = _normalise_element(line[31:34])
        except (ValueError, IndexError):
            fields = line.split()
            if len(fields) < 4:
                raise ValueError(f"cannot parse MOL atom line {i + 4}")
            x, y, z = map(float, fields[:3])
            element = _normalise_element(fields[3])
        atoms.append(Atom(i, element, x, y, z))
    bonds: list[Bond] = []
    start = 4 + atom_count
    for i, line in enumerate(lines[start : start + bond_count], start=1):
        try:
            a, b, order = int(line[0:3]), int(line[3:6]), int(line[6:9])
        except ValueError:
            fields = line.split()
            if len(fields) < 3:
                raise ValueError(f"cannot parse MOL bond line {start + i}")
            a, b, order = map(int, fields[:3])
        if not (1 <= a <= atom_count and 1 <= b <= atom_count):
            raise ValueError(f"MOL bond {i} references an invalid atom")
        bonds.append(Bond(a, b, max(1, order), "mol_v2000"))
    title = lines[0].strip() or path.stem
    return atoms, bonds, title


def infer_bonds(atoms: Iterable[Atom], scale: float = 1.20, minimum_distance: float = 0.20) -> list[Bond]:
    atom_list = list(atoms)
    if scale <= 0:
        raise ValueError("bond inference scale must be positive")
    result: list[Bond] = []
    for i, a in enumerate(atom_list):
        ra = float(ELEMENT_STYLE.get(a.element, DEFAULT_STYLE)["radius"])
        for b in atom_list[i + 1 :]:
            rb = float(ELEMENT_STYLE.get(b.element, DEFAULT_STYLE)["radius"])
            distance = math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))
            threshold = scale * (ra + rb)
            if minimum_distance <= distance <= threshold:
                result.append(Bond(a.index, b.index, 1, "distance_inferred"))
    return result


def compile_scene(
    source: Path,
    *,
    input_format: str = "auto",
    infer_xyz_bonds: bool = False,
    scene_id: str | None = None,
    title: str | None = None,
    coordinate_scale: float = 32.0,
    radius_scale: float = 8.0,
) -> dict[str, Any]:
    source = source.resolve()
    fmt = input_format.lower()
    if fmt == "auto":
        fmt = "xyz" if source.suffix.lower() == ".xyz" else "mol" if source.suffix.lower() in {".mol", ".sdf"} else ""
    if fmt == "xyz":
        atoms, bonds, source_title = parse_xyz(source)
        if infer_xyz_bonds:
            bonds = infer_bonds(atoms)
    elif fmt == "mol":
        atoms, bonds, source_title = parse_mol_v2000(source)
    else:
        raise ValueError("input_format must be auto, xyz, or mol")
    if coordinate_scale <= 0 or radius_scale <= 0:
        raise ValueError("coordinate_scale and radius_scale must be positive")
    sid = scene_id or re.sub(r"[^A-Za-z0-9._-]+", "-", source.stem).strip("-") or "molecule"
    objects: list[dict[str, Any]] = []
    for atom in atoms:
        style = ELEMENT_STYLE.get(atom.element, DEFAULT_STYLE)
        objects.append(
            {
                "id": f"{sid}.atom.{atom.index:04d}",
                "kind": "atom",
                "element": atom.element,
                "semantic_role": "molecular_atom",
                "geometry": {
                    "position3d": [atom.x * coordinate_scale, atom.y * coordinate_scale, atom.z * coordinate_scale],
                    "radius_pt": max(2.0, float(style["radius"]) * radius_scale),
                },
                "appearance": {"fill": style["color"], "material": "plastic", "bevel": "round"},
                "provenance": {"source_atom_index": atom.index, "source_file": str(source)},
            }
        )
    for i, bond in enumerate(bonds, start=1):
        objects.append(
            {
                "id": f"{sid}.bond.{i:04d}",
                "kind": "bond",
                "semantic_role": "molecular_bond",
                "from": f"{sid}.atom.{bond.a:04d}",
                "to": f"{sid}.atom.{bond.b:04d}",
                "geometry": {"radius_pt": 2.2, "bond_order": bond.order},
                "appearance": {"fill": "#B9B9B9", "material": "plastic", "line_cap": "round"},
                "provenance": {"bond_source": bond.provenance},
            }
        )
    objects.append(
        {
            "id": f"{sid}.label",
            "kind": "text",
            "semantic_role": "figure_title",
            "text": title or source_title or source.stem,
            "geometry": {"position3d": [0.0, -110.0, 0.0]},
        }
    )
    assumptions: list[str] = [
        "Element colours and display radii are illustration style tokens, not measured atomic radii."
    ]
    if fmt == "xyz" and not infer_xyz_bonds:
        assumptions.append("No bonds were generated because XYZ does not carry bond topology and inference was not authorized.")
    if fmt == "xyz" and infer_xyz_bonds:
        assumptions.append("Bonds were inferred from covalent-radius distance thresholds and must be reviewed.")
    return {
        "schema_version": "1.0",
        "scene_id": sid,
        "title": title or source_title or source.stem,
        "domain": "computational_chemistry",
        "representation": "3d",
        "abstraction": {
            "target_claim": "Show molecular geometry and supplied connectivity as an editable ball-and-stick model.",
            "essential_information": ["atomic identity", "3D coordinates", "declared bond topology"],
            "omitted_information": ["electron density", "thermal motion", "unreported stereochemical annotations"],
        },
        "fidelity": {
            "mode": "data_bound",
            "source_data": [{"id": "molecular_source", "type": fmt, "path": str(source), "units": "angstrom"}],
            "assumptions": assumptions,
        },
        "canvas": {"width_pt": 960, "height_pt": 540, "margin_pt": 30, "background": "#FFFFFF"},
        "camera": {
            "projection": "orthographic",
            "rotation_deg": {"x": 18, "y": -24, "z": 0},
            "origin_pt": [480, 270],
            "scale": 1.0,
        },
        "style_ref": "styles/default-scientific-3d.style.json",
        "object_budget": max(200, len(objects) + 20),
        "objects": objects,
        "constraints": [
            "preserve_source_coordinates",
            "do_not_infer_bonds_without_authorization",
            "semantic_object_names",
            "single_camera_and_light_rig",
        ],
        "outputs": {
            "pptx": f"artifacts/{sid}.pptx",
            "preview_png": f"artifacts/{sid}.png",
            "scene_copy": f"artifacts/{sid}.scene.json",
            "object_manifest": f"artifacts/{sid}.objects.json",
            "qa_report": f"artifacts/{sid}.qa.json",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--format", choices=["auto", "xyz", "mol"], default="auto")
    parser.add_argument("--infer-bonds", action="store_true", help="Infer XYZ bonds by distance; never enabled by default")
    parser.add_argument("--scene-id")
    parser.add_argument("--title")
    parser.add_argument("--coordinate-scale", type=float, default=32.0)
    parser.add_argument("--radius-scale", type=float, default=8.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scene = compile_scene(
        args.source,
        input_format=args.format,
        infer_xyz_bonds=args.infer_bonds,
        scene_id=args.scene_id,
        title=args.title,
        coordinate_scale=args.coordinate_scale,
        radius_scale=args.radius_scale,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scene, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(args.output), "objects": len(scene["objects"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
