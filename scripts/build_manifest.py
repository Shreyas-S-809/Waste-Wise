#!/usr/bin/env python3
"""
WasteWise — Build Manifest Script
Builds a CSV manifest with filepath, original_class, mapped_class (Wet/Dry),
and source_dataset. Applies label mapping and excludes ambiguous classes.
"""

import os
import sys
import csv
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Dataset paths
# ---------------------------------------------------------------------------
TECHSASH_BASE = PROJECT_ROOT / "Datasets" / "Additional WetDry images" / "DATASET"
REALWASTE_BASE = PROJECT_ROOT / "Datasets" / "realwaste-main" / "RealWaste"
MANIFEST_DIR = PROJECT_ROOT / "datasets" / "manifests"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}

# ---------------------------------------------------------------------------
# Label mapping
# ---------------------------------------------------------------------------
LABEL_MAP = {
    # TechSash classes
    "O": "Wet",
    "R": "Dry",
    # RealWaste classes
    "Food Organics": "Wet",
    "Vegetation": "Wet",
    "Cardboard": "Dry",
    "Glass": "Dry",
    "Metal": "Dry",
    "Paper": "Dry",
    "Plastic": "Dry",
}

EXCLUDED_CLASSES = {"Textile Trash", "Miscellaneous Trash"}


def collect_and_map():
    """Collect images from both datasets, apply label mapping, exclude ambiguous."""
    records = []
    excluded_count = Counter()

    # TechSash
    for split in ["TRAIN", "TEST"]:
        split_dir = TECHSASH_BASE / split
        if not split_dir.exists():
            continue
        for class_dir in sorted(split_dir.iterdir()):
            if not class_dir.is_dir():
                continue
            original_class = class_dir.name
            if original_class in EXCLUDED_CLASSES:
                for fpath in class_dir.rglob("*"):
                    if fpath.is_file() and fpath.suffix.lower() in IMAGE_EXTENSIONS:
                        excluded_count[original_class] += 1
                continue
            mapped = LABEL_MAP.get(original_class)
            if mapped is None:
                print(f"  WARNING: Unknown TechSash class '{original_class}' — skipping.")
                continue
            for fpath in class_dir.rglob("*"):
                if fpath.is_file() and fpath.suffix.lower() in IMAGE_EXTENSIONS:
                    records.append({
                        "filepath": str(fpath),
                        "original_class": original_class,
                        "mapped_class": mapped,
                        "source_dataset": "TechSash",
                        "original_split": split,
                    })

    # RealWaste
    if REALWASTE_BASE.exists():
        for class_dir in sorted(REALWASTE_BASE.iterdir()):
            if not class_dir.is_dir():
                continue
            original_class = class_dir.name
            if original_class in EXCLUDED_CLASSES:
                for fpath in class_dir.rglob("*"):
                    if fpath.is_file() and fpath.suffix.lower() in IMAGE_EXTENSIONS:
                        excluded_count[original_class] += 1
                continue
            mapped = LABEL_MAP.get(original_class)
            if mapped is None:
                print(f"  WARNING: Unknown RealWaste class '{original_class}' — skipping.")
                continue
            for fpath in class_dir.rglob("*"):
                if fpath.is_file() and fpath.suffix.lower() in IMAGE_EXTENSIONS:
                    records.append({
                        "filepath": str(fpath),
                        "original_class": original_class,
                        "mapped_class": mapped,
                        "source_dataset": "RealWaste",
                        "original_split": "ALL",
                    })

    return records, excluded_count


def main():
    print("WasteWise — Building Image Manifest\n")

    records, excluded_count = collect_and_map()

    # Summary
    class_counts = Counter(r["mapped_class"] for r in records)
    source_counts = Counter(r["source_dataset"] for r in records)
    orig_counts = Counter(r["original_class"] for r in records)

    print(f"{'=' * 60}")
    print(f"  Manifest Summary")
    print(f"{'=' * 60}")
    print(f"  Total images (included): {len(records)}")
    print(f"\n  By mapped class:")
    for cls, cnt in sorted(class_counts.items()):
        print(f"    {cls:<10s}: {cnt:>6d}")
    print(f"\n  By source dataset:")
    for src, cnt in sorted(source_counts.items()):
        print(f"    {src:<15s}: {cnt:>6d}")
    print(f"\n  By original class:")
    for cls, cnt in sorted(orig_counts.items()):
        print(f"    {cls:<20s}: {cnt:>6d}")
    if excluded_count:
        print(f"\n  Excluded (ambiguous) classes:")
        for cls, cnt in sorted(excluded_count.items()):
            print(f"    {cls:<25s}: {cnt:>6d}")
    print(f"{'=' * 60}")

    # Save manifest
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = MANIFEST_DIR / "all_images.csv"
    fieldnames = ["filepath", "original_class", "mapped_class", "source_dataset", "original_split"]
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\nManifest saved to: {manifest_path}")
    print(f"Total records: {len(records)}")


if __name__ == "__main__":
    main()
