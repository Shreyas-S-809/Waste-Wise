#!/usr/bin/env python3
"""
WasteWise — Dataset Inspection Script
Scans both TechSash and RealWaste datasets, counts images per class,
reports file formats and sizes, checks for corrupt images, and saves a report.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

# Add project root to path
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

REPORT_DIR = PROJECT_ROOT / "datasets" / "manifests"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}


def scan_directory(base_path, dataset_name):
    """Scan a dataset directory tree and collect image statistics."""
    stats = {}  # split/class -> {count, formats, sizes, corrupt, paths}

    if not base_path.exists():
        print(f"  WARNING: {base_path} does not exist — skipping.")
        return stats

    if dataset_name == "TechSash":
        # Structure: DATASET / {TRAIN, TEST} / {O, R}
        for split in ["TRAIN", "TEST"]:
            split_dir = base_path / split
            if not split_dir.exists():
                continue
            for class_dir in sorted(split_dir.iterdir()):
                if not class_dir.is_dir():
                    continue
                key = f"{split}/{class_dir.name}"
                stats[key] = _scan_class_dir(class_dir)
    elif dataset_name == "RealWaste":
        # Structure: RealWaste / {Cardboard, Food Organics, ...}
        for class_dir in sorted(base_path.iterdir()):
            if not class_dir.is_dir():
                continue
            stats[class_dir.name] = _scan_class_dir(class_dir)
    return stats


def _scan_class_dir(class_dir):
    """Scan a single class directory and return stats dict."""
    info = {
        "count": 0,
        "formats": defaultdict(int),
        "total_size_bytes": 0,
        "min_size": float("inf"),
        "max_size": 0,
        "corrupt": [],
        "widths": [],
        "heights": [],
    }
    for fpath in class_dir.rglob("*"):
        if not fpath.is_file():
            continue
        ext = fpath.suffix.lower()
        if ext not in IMAGE_EXTENSIONS:
            continue
        info["count"] += 1
        info["formats"][ext] += 1
        fsize = fpath.stat().st_size
        info["total_size_bytes"] += fsize
        info["min_size"] = min(info["min_size"], fsize)
        info["max_size"] = max(info["max_size"], fsize)

        # Check for corruption
        try:
            with Image.open(fpath) as img:
                img.verify()
            # Re-open to get size (verify() can invalidate the object)
            with Image.open(fpath) as img:
                w, h = img.size
                info["widths"].append(w)
                info["heights"].append(h)
        except Exception as e:
            info["corrupt"].append((str(fpath), str(e)))

    if info["min_size"] == float("inf"):
        info["min_size"] = 0
    return info


def format_bytes(nbytes):
    """Human-readable byte size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def build_report(techsash_stats, realwaste_stats):
    """Build a text report from the collected statistics."""
    lines = []
    lines.append("=" * 80)
    lines.append("  WasteWise — Dataset Inspection Report")
    lines.append("=" * 80)

    total_images = 0
    total_corrupt = 0

    for dataset_name, stats in [("TechSash (Organic/Recyclable)", techsash_stats),
                                 ("RealWaste", realwaste_stats)]:
        lines.append(f"\n{'─' * 80}")
        lines.append(f"  Dataset: {dataset_name}")
        lines.append(f"{'─' * 80}")
        lines.append(f"  {'Class':<30s} {'Count':>8s} {'Formats':<20s} {'Size Range':<25s} {'Corrupt':>8s}")
        lines.append(f"  {'-'*30} {'-'*8} {'-'*20} {'-'*25} {'-'*8}")

        ds_total = 0
        ds_corrupt = 0
        for key in sorted(stats.keys()):
            info = stats[key]
            count = info["count"]
            ds_total += count
            corrupt_count = len(info["corrupt"])
            ds_corrupt += corrupt_count
            formats_str = ", ".join(f"{ext}:{cnt}" for ext, cnt in sorted(info["formats"].items()))
            if count > 0:
                size_range = f"{format_bytes(info['min_size'])} – {format_bytes(info['max_size'])}"
            else:
                size_range = "N/A"
            lines.append(f"  {key:<30s} {count:>8d} {formats_str:<20s} {size_range:<25s} {corrupt_count:>8d}")

        lines.append(f"  {'SUBTOTAL':<30s} {ds_total:>8d} {'':<20s} {'':<25s} {ds_corrupt:>8d}")
        total_images += ds_total
        total_corrupt += ds_corrupt

        # Image dimension summary
        all_widths = []
        all_heights = []
        for info in stats.values():
            all_widths.extend(info["widths"])
            all_heights.extend(info["heights"])
        if all_widths:
            lines.append(f"\n  Image dimensions:")
            lines.append(f"    Width  — min: {min(all_widths)}, max: {max(all_widths)}, "
                         f"mean: {sum(all_widths)/len(all_widths):.0f}")
            lines.append(f"    Height — min: {min(all_heights)}, max: {max(all_heights)}, "
                         f"mean: {sum(all_heights)/len(all_heights):.0f}")

        # List corrupt files
        for key, info in sorted(stats.items()):
            for fpath, err in info["corrupt"]:
                lines.append(f"  [CORRUPT] {fpath}: {err}")

    lines.append(f"\n{'=' * 80}")
    lines.append(f"  GRAND TOTAL: {total_images} images, {total_corrupt} corrupt")
    lines.append(f"{'=' * 80}")

    return "\n".join(lines)


def main():
    print("WasteWise — Inspecting Datasets...\n")

    print("Scanning TechSash dataset...")
    techsash_stats = scan_directory(TECHSASH_BASE, "TechSash")

    print("Scanning RealWaste dataset...")
    realwaste_stats = scan_directory(REALWASTE_BASE, "RealWaste")

    report = build_report(techsash_stats, realwaste_stats)
    print(report)

    # Save report
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "dataset_inspection_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
