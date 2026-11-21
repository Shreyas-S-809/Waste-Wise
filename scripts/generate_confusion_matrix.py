#!/usr/bin/env python3
"""
WasteWise — Confusion Matrix Generation Script
Generates and plots a normalized confusion matrix heatmap for test evaluation.
"""

import os
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("KERAS_HOME", str(PROJECT_ROOT / ".keras"))


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Confusion Matrix Plot for WasteWise Classifier")
    parser.add_argument("--model-type", type=str, default="wet_dry", choices=["wet_dry", "segregation_status"], help="Model type")
    parser.add_argument("--test-manifest", type=str, default=str(PROJECT_ROOT / "datasets" / "manifests" / "test.csv"), help="Test manifest")
    parser.add_argument("--sample-limit", type=int, default=None, help="Optional test sample limit")
    parser.add_argument("--output-plot", type=str, default=None, help="Output PNG path")
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Generating Confusion Matrix for: {args.model_type}")

    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from PIL import Image
        from sklearn.metrics import confusion_matrix
    except ImportError as e:
        print(f"Missing libraries for confusion matrix: {e}")
        sys.exit(1)

    model_path = str(PROJECT_ROOT / "models" / args.model_type / f"{args.model_type}_mobilenetv2.keras")
    if not os.path.isfile(model_path):
        print(f"Model not found at: {model_path}. Please train model first.")
        sys.exit(1)

    import tensorflow as tf
    model = tf.keras.models.load_model(model_path)
    df = pd.read_csv(args.test_manifest)
    if args.sample_limit:
        df = df.groupby("mapped_class", group_keys=False).apply(lambda x: x.sample(min(len(x), args.sample_limit // 2), random_state=42)).reset_index(drop=True)
        print(f"Sample limit applied: {len(df)} test samples.")

    classes = ["Dry", "Wet"] if args.model_type == "wet_dry" else ["Mixed Waste", "Properly Segregated"]
    class_to_idx = {c: i for i, c in enumerate(classes)}

    y_true = []
    y_pred = []

    for _, row in df.iterrows():
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
            y_true.append(class_to_idx[mapped])
            y_pred.append(int(np.argmax(preds)))
        except Exception:
            continue

    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    plt.figure(figsize=(7, 6))
    sns.heatmap(cm_norm, annot=True, fmt=".2%", cmap="Greens", xticklabels=classes, yticklabels=classes, cbar=True)
    plt.title(f"Confusion Matrix — {args.model_type.replace('_', ' ').title()} (Normalized)")
    plt.ylabel("True Class")
    plt.xlabel("Predicted Class")
    plt.tight_layout()

    out_plot = args.output_plot or str(PROJECT_ROOT / "models" / "evaluation" / f"confusion_matrix_{args.model_type}.png")
    Path(out_plot).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_plot, dpi=300)
    plt.close()
    print(f"Confusion matrix plot saved to: {out_plot}")


if __name__ == "__main__":
    main()
