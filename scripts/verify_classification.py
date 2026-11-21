#!/usr/bin/env python3
"""
WasteWise — Classification Verification Script
Tests the trained MobileNetV2 model against independently labeled test images,
verifying predictions against ground truth and generating the verification report:
models/evaluation/prediction_verification_report.csv
"""

import os
import sys
import csv
import argparse
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))
os.environ.setdefault("KERAS_HOME", str(PROJECT_ROOT / ".keras"))

from app.ml.preprocessing import preprocess_image
from app.ml.confidence import analyze_confidence


def parse_args():
    parser = argparse.ArgumentParser(description="Verify WasteWise classifier on independent test images")
    parser.add_argument("--test-manifest", type=str, default=str(PROJECT_ROOT / "datasets" / "manifests" / "test.csv"), help="Path to test.csv manifest")
    parser.add_argument("--sample-per-class", type=int, default=100, help="Number of samples to evaluate per class")
    parser.add_argument("--output-csv", type=str, default=str(PROJECT_ROOT / "models" / "evaluation" / "prediction_verification_report.csv"), help="Output CSV path")
    return parser.parse_args()


def main():
    args = parse_args()
    print("=" * 70)
    print("WasteWise — Running Classification Verification on Independent Test Data")
    print("=" * 70)

    import numpy as np
    import pandas as pd
    import tensorflow as tf

    model_path = PROJECT_ROOT / "models" / "wet_dry" / "wet_dry_mobilenetv2.keras"
    if not model_path.is_file():
        print(f"ERROR: Model file not found at {model_path}")
        sys.exit(1)

    print(f"Loading MobileNetV2 model: {model_path.name}")
    model = tf.keras.models.load_model(str(model_path))

    test_manifest = Path(args.test_manifest)
    if not test_manifest.is_file():
        print(f"ERROR: Test manifest not found at {test_manifest}")
        sys.exit(1)

    df = pd.read_csv(test_manifest)
    # Filter to existing files
    df = df[df["filepath"].apply(os.path.exists)]
    print(f"Total available test records in manifest: {len(df)}")

    # Sample balanced set per class and across sources if possible
    sampled_df = df.groupby("mapped_class", group_keys=False).apply(
        lambda x: x.sample(min(len(x), args.sample_per_class), random_state=42)
    ).reset_index(drop=True)

    print(f"Selected {len(sampled_df)} test images for verification ({Counter(sampled_df['mapped_class'])})")

    labels = ["Dry", "Wet"]
    results = []
    correct_count = 0
    incorrect_count = 0
    uncertain_count = 0

    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    print("\nRunning verification inference...")
    for idx, row in sampled_df.iterrows():
        fpath = row["filepath"]
        gt = row["mapped_class"]
        orig_class = row.get("original_class", "unknown")
        fname = Path(fpath).name

        try:
            arr = preprocess_image(fpath)
            probs = model.predict(arr, verbose=0)
            analysis = analyze_confidence(probs, labels, threshold=0.60)

            predicted = analysis["predicted_class"]
            conf = analysis["confidence"]

            if predicted == "Uncertain":
                status = "UNCERTAIN"
                uncertain_count += 1
            elif predicted == gt:
                status = "CORRECT"
                correct_count += 1
            else:
                status = "INCORRECT"
                incorrect_count += 1

            results.append({
                "filename": fname,
                "ground_truth": gt,
                "original_category": orig_class,
                "predicted": predicted,
                "probability": f"{conf:.4f}",
                "status": status,
                "dry_probability": f"{analysis['probabilities'].get('Dry', 0.0):.4f}",
                "wet_probability": f"{analysis['probabilities'].get('Wet', 0.0):.4f}"
            })
        except Exception as exc:
            print(f"Error evaluating {fname}: {exc}")

    # Write CSV report
    fieldnames = ["filename", "ground_truth", "original_category", "predicted", "probability", "status", "dry_probability", "wet_probability"]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    total_evaluated = len(results)
    decisive_total = correct_count + incorrect_count
    accuracy = (correct_count / decisive_total * 100) if decisive_total > 0 else 0

    print("\n" + "=" * 70)
    print("VERIFICATION RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total Test Images Evaluated: {total_evaluated}")
    print(f"Correct Predictions:        {correct_count} ({correct_count/total_evaluated*100:.1f}%)")
    print(f"Incorrect Predictions:      {incorrect_count} ({incorrect_count/total_evaluated*100:.1f}%)")
    print(f"Uncertain / Low Confidence: {uncertain_count} ({uncertain_count/total_evaluated*100:.1f}%)")
    print(f"Accuracy on Decisive Calls: {accuracy:.2f}%")
    print(f"\nVerification report successfully written to:")
    print(f"  {output_csv}")
    print("=" * 70)


if __name__ == "__main__":
    main()

