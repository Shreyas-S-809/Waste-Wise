#!/usr/bin/env python3
"""
WasteWise — CLI Image Prediction Utility
Runs inference on a single image file from the command line.
"""

import os
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("KERAS_HOME", str(PROJECT_ROOT / ".keras"))


def parse_args():
    parser = argparse.ArgumentParser(description="Predict waste category for a given image")
    parser.add_argument("--image", type=str, required=True, help="Path to input waste image")
    parser.add_argument("--mode", type=str, default="item", choices=["item", "segregation"], help="Classification mode")
    parser.add_argument("--threshold", type=float, default=0.60, help="Confidence threshold for certainty")
    return parser.parse_args()


def main():
    args = parse_args()
    image_path = Path(args.image)
    if not image_path.is_file():
        print(f"ERROR: Image file not found: {image_path}")
        sys.exit(1)

    model_type = "wet_dry" if args.mode == "item" else "segregation_status"
    model_file = PROJECT_ROOT / "models" / model_type / f"{model_type}_mobilenetv2.keras"

    if not model_file.is_file():
        print(f"ERROR: Model '{model_type}' is not trained yet (expected at {model_file}).")
        sys.exit(1)

    try:
        import numpy as np
        from PIL import Image
        import tensorflow as tf
    except ImportError as e:
        print(f"Missing required ML libraries: {e}")
        sys.exit(1)

    print(f"Loading {model_type} model...")
    model = tf.keras.models.load_model(str(model_file))

    # Preprocess
    with Image.open(image_path) as img:
        img = img.convert("RGB").resize((224, 224), Image.LANCZOS)
        arr = np.array(img, dtype=np.float32)
        arr = (arr / 127.5) - 1.0
        arr = np.expand_dims(arr, axis=0)

    classes = ["Dry", "Wet"] if args.mode == "item" else ["Mixed Waste", "Properly Segregated"]
    probs = model.predict(arr, verbose=0)[0]

    pred_idx = int(np.argmax(probs))
    pred_class = classes[pred_idx]
    confidence = float(probs[pred_idx])

    print("\n" + "=" * 50)
    print("  WasteWise Classification Result")
    print("=" * 50)
    print(f"  Input Image : {image_path.name}")
    print(f"  Mode        : {'Individual Item' if args.mode == 'item' else 'Segregation Scene'}")
    print(f"  Prediction  : {pred_class}")
    print(f"  Confidence  : {confidence * 100:.2f}%")
    print(f"  Certainty   : {'High Confidence' if confidence >= args.threshold else 'Low Confidence / Uncertain'}")
    print("  Class Probabilities:")
    for cls_name, p in zip(classes, probs):
        print(f"    - {cls_name:20s}: {p * 100:.2f}%")
    print("=" * 50)


if __name__ == "__main__":
    main()
