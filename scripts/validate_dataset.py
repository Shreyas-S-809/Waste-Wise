#!/usr/bin/env python3
"""
WasteWise — Dataset Validation Script
Validates all images are readable, checks minimum dimensions (32x32),
filters corrupt/invalid images, and saves a valid image list.
"""

import os
import sys
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

# ---------------------------------------------------------------------------
TECHSASH_BASE = PROJECT_ROOT / "Datasets" / "Additional WetDry images" / "DATASET"
REALWASTE_BASE = PROJECT_ROOT / "Datasets" / "realwaste-main" / "RealWaste"
MANIFEST_DIR = PROJECT_ROOT / "datasets" / "manifests"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
MIN_WIDTH = 32
MIN_HEIGHT = 32


def collect_image_paths():
    """Collect all image paths from both datasets."""
    paths = []

    # TechSash
    for split in ["TRAIN", "TEST"]:
        split_dir = TECHSASH_BASE / split
        if not split_dir.exists():
            continue
        for class_dir in sorted(split_dir.iterdir()):
            if not class_dir.is_dir():
                continue
            for fpath in class_dir.rglob("*"):
                if fpath.is_file() and fpath.suffix.lower() in IMAGE_EXTENSIONS:
                    paths.append(("TechSash", split, class_dir.name, fpath))

    # RealWaste
    if REALWASTE_BASE.exists():
        for class_dir in sorted(REALWASTE_BASE.iterdir()):
            if not class_dir.is_dir():
                continue
            for fpath in class_dir.rglob("*"):
                if fpath.is_file() and fpath.suffix.lower() in IMAGE_EXTENSIONS:
                    paths.append(("RealWaste", "ALL", class_dir.name, fpath))

    return paths


def validate_image(fpath):
    """
    Validate a single image.
    Returns (is_valid, width, height, error_message).
    """
    try:
        with Image.open(fpath) as img:
            img.verify()
        # Re-open after verify
        with Image.open(fpath) as img:
            w, h = img.size
            if w < MIN_WIDTH or h < MIN_HEIGHT:
                return False, w, h, f"Too small ({w}x{h}), minimum is {MIN_WIDTH}x{MIN_HEIGHT}"
            return True, w, h, None
    except Exception as e:
        return False, 0, 0, str(e)


def main():
    print("WasteWise — Dataset Validation\n")

    image_records = collect_image_paths()
    total = len(image_records)
    print(f"Found {total} image files to validate.\n")

    valid_images = []
    invalid_images = []
    corrupt_images = []

    for i, (dataset, split, class_name, fpath) in enumerate(image_records):
        is_valid, w, h, err = validate_image(fpath)
        if is_valid:
            valid_images.append({
                "filepath": str(fpath),
                "dataset": dataset,
                "split": split,
                "class": class_name,
                "width": w,
                "height": h,
            })
        else:
            entry = {
                "filepath": str(fpath),
                "dataset": dataset,
                "split": split,
                "class": class_name,
                "error": err,
            }
            if "Too small" in (err or ""):
                invalid_images.append(entry)
            else:
                corrupt_images.append(entry)

        # Progress every 5000 images
        if (i + 1) % 5000 == 0 or (i + 1) == total:
            print(f"  Validated {i + 1}/{total} images...")

    # Report
    print(f"\n{'=' * 60}")
    print(f"  Validation Results")
    print(f"{'=' * 60}")
    print(f"  Total images scanned : {total}")
    print(f"  Valid images         : {len(valid_images)}")
    print(f"  Too-small images     : {len(invalid_images)}")
    print(f"  Corrupt images       : {len(corrupt_images)}")
    print(f"{'=' * 60}")

    if corrupt_images:
        print(f"\nCorrupt files ({len(corrupt_images)}):")
        for entry in corrupt_images[:20]:
            print(f"  {entry['filepath']}: {entry['error']}")
        if len(corrupt_images) > 20:
            print(f"  ... and {len(corrupt_images) - 20} more.")

    if invalid_images:
        print(f"\nToo-small files ({len(invalid_images)}):")
        for entry in invalid_images[:10]:
            print(f"  {entry['filepath']}: {entry['error']}")
        if len(invalid_images) > 10:
            print(f"  ... and {len(invalid_images) - 10} more.")

    # Save valid image list
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    valid_list_path = MANIFEST_DIR / "valid_images.csv"
    with open(valid_list_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filepath", "dataset", "split", "class", "width", "height"])
        writer.writeheader()
        writer.writerows(valid_images)
    print(f"\nValid image list saved to: {valid_list_path}")

    # Save invalid/corrupt list
    if invalid_images or corrupt_images:
        invalid_path = MANIFEST_DIR / "invalid_images.csv"
        with open(invalid_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["filepath", "dataset", "split", "class", "error"])
            writer.writeheader()
            writer.writerows(invalid_images + corrupt_images)
        print(f"Invalid image list saved to: {invalid_path}")

    return len(valid_images), len(invalid_images), len(corrupt_images)


if __name__ == "__main__":
    main()
