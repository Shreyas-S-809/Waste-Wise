#!/usr/bin/env python3
"""
WasteWise — Model A (Wet / Dry) Training Pipeline
Uses MobileNetV2 with transfer learning and fine-tuning.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Ensure project root is in sys.path and KERAS_HOME points to project .keras cache
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("KERAS_HOME", str(PROJECT_ROOT / ".keras"))


def parse_args():
    parser = argparse.ArgumentParser(description="Train MobileNetV2 for Wet vs Dry Waste Classification")
    parser.add_argument("--epochs-phase1", type=int, default=15, help="Epochs for initial classification head training")
    parser.add_argument("--epochs-phase2", type=int, default=10, help="Epochs for fine-tuning top layers")
    parser.add_argument("--batch-size", type=int, default=32, help="Mini-batch size")
    parser.add_argument("--sample-limit", type=int, default=None, help="Optional max training samples (useful for fast CPU training/testing)")
    parser.add_argument("--lr-head", type=float, default=1e-3, help="Learning rate for Phase 1 head training")
    parser.add_argument("--lr-finetune", type=float, default=1e-5, help="Learning rate for Phase 2 fine-tuning")
    parser.add_argument("--image-size", type=int, default=224, help="Target image height/width (224 recommended)")
    parser.add_argument("--manifest-dir", type=str, default=str(PROJECT_ROOT / "datasets" / "manifests"), help="Path to manifest directory")
    parser.add_argument("--output-model", type=str, default=str(PROJECT_ROOT / "models" / "wet_dry" / "wet_dry_mobilenetv2.keras"), help="Target path for trained .keras file")
    parser.add_argument("--metadata-file", type=str, default=str(PROJECT_ROOT / "models" / "metadata" / "model_metadata.json"), help="Path to model metadata JSON")
    return parser.parse_args()


def build_model(input_shape=(224, 224, 3), num_classes=2):
    """Build MobileNetV2 transfer learning model with custom classification head."""
    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import MobileNetV2

    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet"
    )
    # Freeze the base feature extractor initially
    base_model.trainable = False

    inputs = layers.Input(shape=input_shape, name="image_input")
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs, name="wet_dry_mobilenetv2")
    return model, base_model


def load_dataframe(csv_path):
    import pandas as pd
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Manifest not found: {csv_path}. Please run split_dataset.py first.")
    df = pd.read_csv(csv_path)
    # Filter to existing files
    df = df[df["filepath"].apply(os.path.exists)]
    return df


def main():
    args = parse_args()
    print("=" * 70)
    print("WasteWise — Training Wet/Dry Waste Classifier (MobileNetV2)")
    print("=" * 70)

    try:
        import tensorflow as tf
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
        import pandas as pd
    except ImportError as e:
        print(f"Missing required ML libraries: {e}")
        print("Please install tensorflow, pandas, and scikit-learn.")
        sys.exit(1)

    manifest_dir = Path(args.manifest_dir)
    train_csv = manifest_dir / "train.csv"
    val_csv = manifest_dir / "validation.csv"

    print(f"Loading manifests from {manifest_dir}...")
    train_df = load_dataframe(str(train_csv))
    val_df = load_dataframe(str(val_csv))

    if args.sample_limit:
        half_train = args.sample_limit // 2
        half_val = max(10, args.sample_limit // 6)
        train_df = train_df.groupby("mapped_class", group_keys=False).apply(lambda x: x.sample(min(len(x), half_train), random_state=42)).reset_index(drop=True)
        val_df = val_df.groupby("mapped_class", group_keys=False).apply(lambda x: x.sample(min(len(x), half_val), random_state=42)).reset_index(drop=True)
        print(f"Sample limit applied: {len(train_df)} train samples, {len(val_df)} validation samples.")
    else:
        print(f"Train samples: {len(train_df)}, Validation samples: {len(val_df)}")

    classes = ["Dry", "Wet"]  # Target alphabetical classes

    # Image generators with augmentation for training and MobileNetV2 preprocessing
    train_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
        rotation_range=20,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.1,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    val_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
    )

    train_gen = train_datagen.flow_from_dataframe(
        dataframe=train_df,
        x_col="filepath",
        y_col="mapped_class",
        target_size=(args.image_size, args.image_size),
        batch_size=args.batch_size,
        classes=classes,
        class_mode="categorical",
        shuffle=True
    )

    val_gen = val_datagen.flow_from_dataframe(
        dataframe=val_df,
        x_col="filepath",
        y_col="mapped_class",
        target_size=(args.image_size, args.image_size),
        batch_size=args.batch_size,
        classes=classes,
        class_mode="categorical",
        shuffle=False
    )

    # Build model
    model, base_model = build_model(
        input_shape=(args.image_size, args.image_size, 3),
        num_classes=len(classes)
    )

    # Phase 1: Compile classification head
    print("\n--- Phase 1: Training Classification Head (Base Frozen) ---")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=args.lr_head),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
    )

    checkpoint_dir = PROJECT_ROOT / "models" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    best_weights_path = str(checkpoint_dir / "best_wet_dry_weights.weights.h5")

    callbacks_phase1 = [
        EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-6, verbose=1),
        ModelCheckpoint(filepath=best_weights_path, monitor="val_loss", save_best_only=True, save_weights_only=True, verbose=1)
    ]

    history1 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs_phase1,
        callbacks=callbacks_phase1
    )

    # Phase 2: Fine-tuning top layers of MobileNetV2
    print("\n--- Phase 2: Fine-Tuning Top Convolutional Layers ---")
    base_model.trainable = True
    # Freeze all layers before the last 30 layers
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=args.lr_finetune),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")]
    )

    callbacks_phase2 = [
        EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-7, verbose=1),
        ModelCheckpoint(filepath=best_weights_path, monitor="val_loss", save_best_only=True, save_weights_only=True, verbose=1)
    ]

    history2 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs_phase2,
        callbacks=callbacks_phase2
    )

    # Save final model
    output_path = Path(args.output_model)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(output_path))
    print(f"\nTrained model saved successfully to: {output_path}")

    # Update metadata
    meta_path = Path(args.metadata_file)
    meta_data = {}
    if meta_path.exists():
        with open(meta_path, "r") as f:
            meta_data = json.load(f)

    if "models" not in meta_data:
        meta_data["models"] = {}

    final_val_loss = float(history2.history["val_loss"][-1])
    final_val_acc = float(history2.history["val_accuracy"][-1])

    meta_data["models"]["wet_dry"] = {
        "version": "1.0.0",
        "architecture": "MobileNetV2",
        "input_dimensions": [args.image_size, args.image_size, 3],
        "classes": classes,
        "training_dataset_sources": ["TechSash Waste Classification", "RealWaste"],
        "training_date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "preprocessing_method": "MobileNetV2 scale [-1, 1]",
        "status": "trained",
        "model_file": output_path.name,
        "metrics": {
            "validation_loss": round(final_val_loss, 4),
            "validation_accuracy": round(final_val_acc, 4)
        }
    }

    with open(meta_path, "w") as f:
        json.dump(meta_data, f, indent=2)
    print(f"Updated metadata in: {meta_path}")


if __name__ == "__main__":
    main()
