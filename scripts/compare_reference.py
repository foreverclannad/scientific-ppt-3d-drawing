#!/usr/bin/env python3
"""Compare a PowerPoint render with a reference image, globally and by Scene region."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

THRESHOLDS = {
    "aspect_ratio_error_max": 0.001,
    "normalized_mae_max": 0.06,
    "within_24_ratio_min": 0.85,
    "edge_f1_tolerance_2px_min": 0.88,
    "critical_region_edge_f1_min": 0.85,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge_mask(image: Image.Image) -> np.ndarray:
    edges = np.asarray(image.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.uint8) >= 32
    edges[[0, -1], :] = False
    edges[:, [0, -1]] = False
    return edges


def dilate(mask: np.ndarray, tolerance: int) -> np.ndarray:
    if tolerance <= 0:
        return mask
    image = Image.fromarray(mask.astype(np.uint8) * 255)
    return np.asarray(image.filter(ImageFilter.MaxFilter(2 * tolerance + 1))) > 0


def tolerant_edge_f1(reference: Image.Image, candidate: Image.Image, tolerance: int = 2) -> float:
    ref = edge_mask(reference)
    cand = edge_mask(candidate)
    ref_count = int(ref.sum())
    cand_count = int(cand.sum())
    if not ref_count and not cand_count:
        return 1.0
    if not ref_count or not cand_count:
        return 0.0
    precision = float((cand & dilate(ref, tolerance)).sum()) / cand_count
    recall = float((ref & dilate(cand, tolerance)).sum()) / ref_count
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def image_metrics(reference: Image.Image, candidate: Image.Image) -> dict[str, float]:
    ref = np.asarray(reference.convert("RGB"), dtype=np.int16)
    cand = np.asarray(candidate.convert("RGB"), dtype=np.int16)
    difference = np.abs(ref - cand)
    return {
        "normalized_mae": float(difference.mean() / 255.0),
        "within_24_ratio": float((difference.max(axis=2) <= 24).mean()),
        "edge_f1_tolerance_2px": tolerant_edge_f1(reference, candidate, 2),
    }


def crop_region(image: Image.Image, bbox: list[float]) -> Image.Image:
    width, height = image.size
    x, y, region_width, region_height = bbox
    left = max(0, min(width - 1, round(x * width)))
    top = max(0, min(height - 1, round(y * height)))
    right = max(left + 1, min(width, round((x + region_width) * width)))
    bottom = max(top + 1, min(height, round((y + region_height) * height)))
    return image.crop((left, top, right, bottom))


def compare(reference: Image.Image, candidate: Image.Image, regions: list[dict[str, Any]]) -> dict[str, Any]:
    ref_ratio = reference.width / reference.height
    candidate_ratio = candidate.width / candidate.height
    aspect_error = abs(candidate_ratio / ref_ratio - 1.0)
    resized = candidate.convert("RGB").resize(reference.size, Image.Resampling.LANCZOS)
    global_metrics = image_metrics(reference, resized)
    global_metrics["aspect_ratio_error"] = aspect_error
    region_results = []
    for region in regions:
        ref_crop = crop_region(reference, region["bbox_norm"])
        cand_crop = crop_region(resized, region["bbox_norm"])
        metrics = image_metrics(ref_crop, cand_crop)
        region_results.append(
            {
                "id": region["id"],
                "priority": region.get("priority", "major"),
                "bbox_norm": region["bbox_norm"],
                **metrics,
                "passed": region.get("priority") != "critical"
                or metrics["edge_f1_tolerance_2px"]
                >= THRESHOLDS["critical_region_edge_f1_min"],
            }
        )
    passed = (
        aspect_error <= THRESHOLDS["aspect_ratio_error_max"]
        and global_metrics["normalized_mae"] <= THRESHOLDS["normalized_mae_max"]
        and global_metrics["within_24_ratio"] >= THRESHOLDS["within_24_ratio_min"]
        and global_metrics["edge_f1_tolerance_2px"]
        >= THRESHOLDS["edge_f1_tolerance_2px_min"]
        and all(region["passed"] for region in region_results)
    )
    return {
        "passed": passed,
        "reference_size_px": list(reference.size),
        "candidate_size_px": list(candidate.size),
        "thresholds": THRESHOLDS,
        "global": global_metrics,
        "regions": region_results,
    }


def self_test() -> None:
    reference = Image.new("RGB", (160, 90), "white")
    draw = ImageDraw.Draw(reference)
    draw.rectangle((20, 18, 140, 72), outline="navy", width=3)
    draw.line((35, 45, 125, 45), fill="red", width=3)
    regions = [{"id": "critical", "priority": "critical", "bbox_norm": [0.1, 0.1, 0.8, 0.8]}]
    assert compare(reference, reference.copy(), regions)["passed"]
    same_ratio_resample = reference.resize((320, 180)).resize(reference.size)
    assert compare(reference, same_ratio_resample, regions)["passed"]
    scores = []
    for shift in (1, 2, 3):
        moved = Image.new("RGB", reference.size, "white")
        moved.paste(reference.crop((0, 0, reference.width - shift, reference.height)), (shift, 0))
        scores.append(compare(reference, moved, regions)["global"]["edge_f1_tolerance_2px"])
    assert scores[0] >= scores[1] >= scores[2]
    changed = Image.new("RGB", reference.size, (200, 200, 200))
    assert not compare(reference, changed, regions)["passed"]
    wrong_aspect = reference.resize((160, 100))
    assert not compare(reference, wrong_aspect, regions)["passed"]
    print("compare_reference self-test: OK")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--scene", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not all((args.reference, args.candidate, args.scene, args.output_dir)):
        parser.error("--reference, --candidate, --scene, and --output-dir are required")

    scene = json.loads(args.scene.read_text(encoding="utf-8"))
    reference_contract = scene.get("reference") or {}
    if scene.get("workflow_mode") != "reference_reconstruction":
        raise SystemExit("Scene workflow_mode must be reference_reconstruction")
    actual_hash = sha256(args.reference)
    if actual_hash.casefold() != str(reference_contract.get("sha256") or "").casefold():
        raise SystemExit("Reference SHA-256 does not match the Scene")
    reference = Image.open(args.reference).convert("RGB")
    expected_size = (
        int(reference_contract.get("width_px", 0)),
        int(reference_contract.get("height_px", 0)),
    )
    if reference.size != expected_size:
        raise SystemExit(f"Reference size {reference.size} does not match Scene {expected_size}")
    candidate = Image.open(args.candidate).convert("RGB")
    result = compare(reference, candidate, list(reference_contract.get("regions") or []))
    result.update(
        {
            "reference_path": str(args.reference.resolve()),
            "candidate_path": str(args.candidate.resolve()),
            "scene_path": str(args.scene.resolve()),
            "reference_sha256": actual_hash,
        }
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    resized = candidate.resize(reference.size, Image.Resampling.LANCZOS)
    Image.blend(reference, resized, 0.5).save(args.output_dir / "reference-overlay.png")
    difference = np.abs(
        np.asarray(reference, dtype=np.int16) - np.asarray(resized, dtype=np.int16)
    )
    Image.fromarray(np.clip(difference * 4, 0, 255).astype(np.uint8)).save(
        args.output_dir / "reference-diff.png"
    )
    (args.output_dir / "reference-compare.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
