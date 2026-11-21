#!/usr/bin/env python3
"""
WasteWise — Model Evaluation Script
Evaluates trained models on unseen test sets and computes Accuracy, Precision,
Recall, F1-Score, Balanced Accuracy, and Per-Class Metrics.
"""

import os
import sys
import json
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("KERAS_HOME", str(PROJECT_ROOT / ".keras"))


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate WasteWise Classification Model on Test Set")
    parser.add_argument("--model-type", type=str, default="wet_dry", choices=["wet_dry", "segregation_status"], help="Model to evaluate")
    parser.add_argument("--test-manifest", type=str, default=str(PROJECT_ROOT / "datasets" / "manifests" / "test.csv"), help="Test manifest CSV")
    parser.add_argument("--sample-limit", type=int, default=None, help="Optional test sample limit for fast evaluation")
    parser.add_argument("--model-file", type=str, default=None, help="Custom path to .keras model file")
    parser.add_argument("--output-report", type=str, default=None, help="Output JSON/text report path")
    return parser.parse_args()


def main():
    args = parse_args()
    print("=" * 70)
    print(f"WasteWise — Evaluating Model: {args.model_type}")
    print("=" * 70)

    try:
        import numpy as np
        import pandas as pd
        from PIL import Image
        from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score, accuracy_score
    except ImportError as e:
        print(f"Missing required evaluation libraries: {e}")
        sys.exit(1)

    model_path = args.model_file
    if model_path is None:
        if args.model_type == "wet_dry":
            model_path = str(PROJECT_ROOT / "models" / "wet_dry" / "wet_dry_mobilenetv2.keras")
        else:
            model_path = str(PROJECT_ROOT / "models" / "segregation_status" / "segregation_status_mobilenetv2.keras")

    if not os.path.isfile(model_path):
        print(f"ERROR: Model file not found at: {model_path}")
        print("Please train the model first before running evaluation.")
        sys.exit(1)

    try:
        import tensorflow as tf
        print(f"Loading trained model from: {model_path}")
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        print(f"Failed to load Keras model: {e}")
        sys.exit(1)

    if not os.path.isfile(args.test_manifest):
        print(f"ERROR: Test manifest not found at: {args.test_manifest}")
        sys.exit(1)

    df = pd.read_csv(args.test_manifest)
    if args.sample_limit:
        df = df.groupby("mapped_class", group_keys=False).apply(lambda x: x.sample(min(len(x), args.sample_limit // 2), random_state=42)).reset_index(drop=True)
        print(f"Sample limit applied: {len(df)} test samples.")
    else:
        print(f"Loaded {len(df)} test records from manifest.")

    classes = ["Dry", "Wet"] if args.model_type == "wet_dry" else ["Mixed Waste", "Properly Segregated"]
    class_to_idx = {c: i for i, c in enumerate(classes)}

    y_true = []
    y_pred = []
    y_scores = []

    print("Running inference over test set...")
    for idx, row in df.iterrows():
        fpath = row["filepath"]
        mapped = row["mapped_class"]
        if not os.path.isfile(fpath) or mapped not in class_to_idx:
            continue

        try:
            with Image.open(fpath) as img:
                img = img.convert("RGB").resize((224, 224), Image.LANCZOS)
                arr = np.array(img, dtype=np.float32)
                arr = (arr / 127.5) - 1.0
                arr = np.expand_dims(arr, axis=0)

            preds = model.predict(arr, verbose=0)[0]
            pred_idx = int(np.argmax(preds))

            y_true.append(class_to_idx[mapped])
            y_pred.append(pred_idx)
            y_scores.append(float(preds[pred_idx]))
        except Exception as e:
            continue

    if not y_true:
        print("ERROR: No valid test images could be evaluated.")
        sys.exit(1)

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    acc = accuracy_score(y_true, y_pred)
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    report_dict = classification_report(y_true, y_pred, target_names=classes, output_dict=True)
    report_text = classification_report(y_true, y_pred, target_names=classes)

    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)
    print(f"Overall Accuracy:          {acc * 100:.2f}%")
    print(f"Balanced Accuracy:         {bal_acc * 100:.2f}%")
    print("\nClassification Report:")
    print(report_text)

    # Save evaluation report
    eval_dir = PROJECT_ROOT / "models" / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    out_file = args.output_report or str(eval_dir / f"evaluation_report_{args.model_type}.json")

    results_payload = {
        "model_type": args.model_type,
        "model_file": Path(model_path).name,
        "num_test_samples": len(y_true),
        "overall_accuracy": round(float(acc), 4),
        "balanced_accuracy": round(float(bal_acc), 4),
        "metrics_by_class": report_dict
    }

    with open(out_file, "w") as f:
        json.dump(results_payload, f, indent=2)
    print(f"Evaluation report saved to: {out_file}")


if __name__ == "__main__":
    main()
