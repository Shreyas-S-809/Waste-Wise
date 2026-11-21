#!/usr/bin/env python3
"""
WasteWise — Dataset Split Script
Reads all_images.csv and creates stratified train/validation/test splits.
Uses TechSash TEST subset preferentially for the test set to reduce leakage.
70% train / 15% validation / 15% test.
"""

import os
import sys
import csv
import random
from pathlib import Path
from collections import Counter, defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

MANIFEST_DIR = PROJECT_ROOT / "datasets" / "manifests"
SEED = 42


def read_manifest(path):
    """Read CSV manifest and return list of dicts."""
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_split(records, path):
    """Write a list of dicts to a CSV file."""
    if not records:
        return
    fieldnames = list(records[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def stratified_split(records, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, seed=42):
    """
    Stratified split that respects TechSash original splits to reduce leakage.
    
    Strategy:
    1. TechSash TEST images → preferentially go to test set
    2. Remaining images are stratified-split by mapped_class
    """
    random.seed(seed)

    # Separate TechSash TEST images from everything else
    techsash_test = [r for r in records
                     if r["source_dataset"] == "TechSash" and r["original_split"] == "TEST"]
    other_images = [r for r in records
                    if not (r["source_dataset"] == "TechSash" and r["original_split"] == "TEST")]

    # Group 'other' by mapped_class for stratified splitting
    by_class = defaultdict(list)
    for r in other_images:
        by_class[r["mapped_class"]].append(r)

    train_set = []
    val_set = []
    test_set = []

    # TechSash TEST → test set (all of it)
    test_set.extend(techsash_test)

    # For remaining images, do stratified split
    # We already have some test images from TechSash TEST,
    # so adjust how many more test images we need
    total = len(records)
    target_test = int(total * test_ratio)
    target_val = int(total * val_ratio)

    remaining_test_needed = max(0, target_test - len(techsash_test))

    for cls, cls_records in by_class.items():
        random.shuffle(cls_records)
        n = len(cls_records)

        # Proportional allocation for this class from 'other' pool
        cls_fraction = n / len(other_images) if other_images else 0

        n_test = int(remaining_test_needed * cls_fraction)
        n_val = int(target_val * (n / (len(other_images) if other_images else 1)))
        # Rest to train
        n_train = n - n_test - n_val

        # Clamp
        n_test = max(0, min(n_test, n))
        n_val = max(0, min(n_val, n - n_test))
        n_train = n - n_test - n_val

        test_set.extend(cls_records[:n_test])
        val_set.extend(cls_records[n_test:n_test + n_val])
        train_set.extend(cls_records[n_test + n_val:])

    return train_set, val_set, test_set


def report_distribution(name, records):
    """Print class distribution for a split."""
    class_counts = Counter(r["mapped_class"] for r in records)
    source_counts = Counter(r["source_dataset"] for r in records)
    total = len(records)
    print(f"\n  {name}: {total} images")
    print(f"    By class:")
    for cls, cnt in sorted(class_counts.items()):
        pct = 100.0 * cnt / total if total else 0
        print(f"      {cls:<10s}: {cnt:>6d} ({pct:5.1f}%)")
    print(f"    By source:")
    for src, cnt in sorted(source_counts.items()):
        pct = 100.0 * cnt / total if total else 0
        print(f"      {src:<15s}: {cnt:>6d} ({pct:5.1f}%)")


def main():
    print("WasteWise — Dataset Splitting\n")

    manifest_path = MANIFEST_DIR / "all_images.csv"
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found at {manifest_path}")
        print("Run build_manifest.py first.")
        sys.exit(1)

    records = read_manifest(manifest_path)
    print(f"Loaded {len(records)} records from manifest.\n")

    train_set, val_set, test_set = stratified_split(records, seed=SEED)

    total = len(records)
    print(f"{'=' * 60}")
    print(f"  Split Summary (seed={SEED})")
    print(f"{'=' * 60}")
    print(f"  Total images: {total}")
    print(f"  Train: {len(train_set)} ({100.0 * len(train_set) / total:.1f}%)")
    print(f"  Val:   {len(val_set)} ({100.0 * len(val_set) / total:.1f}%)")
    print(f"  Test:  {len(test_set)} ({100.0 * len(test_set) / total:.1f}%)")

    report_distribution("Train", train_set)
    report_distribution("Validation", val_set)
    report_distribution("Test", test_set)
    print(f"{'=' * 60}")

    # Save splits
    write_split(train_set, MANIFEST_DIR / "train.csv")
    write_split(val_set, MANIFEST_DIR / "validation.csv")
    write_split(test_set, MANIFEST_DIR / "test.csv")

    print(f"\nSplit files saved to: {MANIFEST_DIR}")
    print(f"  - train.csv      ({len(train_set)} records)")
    print(f"  - validation.csv ({len(val_set)} records)")
    print(f"  - test.csv       ({len(test_set)} records)")


if __name__ == "__main__":
    main()
