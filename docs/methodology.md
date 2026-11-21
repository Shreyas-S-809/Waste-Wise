# WasteWise — ML Methodology

## Overview

WasteWise employs **transfer learning** with the **MobileNetV2** architecture pre-trained on ImageNet to build two binary classifiers:

1. **Wet/Dry Classifier**: Classifies individual waste item images as Wet (organic/biodegradable) or Dry (recyclable/inorganic).
2. **Segregation Status Classifier** (Phase 2): Classifies waste scene images as Properly Segregated or Mixed Waste.

Both models share the same base architecture and training methodology, differing only in their training datasets and output semantics.

## Why MobileNetV2?

MobileNetV2 was selected for several reasons:

- **Efficiency**: MobileNetV2 uses depthwise separable convolutions and inverted residual blocks, making it lightweight enough for inference on commodity hardware and even mobile devices. The model has approximately 3.4 million parameters, compared to 25.6 million for ResNet50 or 143 million for VGG16.
- **Strong transfer learning performance**: Despite its compact size, MobileNetV2 achieves 71.8% top-1 accuracy on ImageNet, and the learned features transfer well to domain-specific tasks like waste classification.
- **Fast inference**: Average inference time is under 50ms on a modern CPU, enabling real-time predictions in the web application without requiring GPU acceleration.
- **Keras integration**: MobileNetV2 is available directly through `tf.keras.applications.MobileNetV2`, simplifying model construction and weight loading.

## Transfer Learning Procedure

### Step 1: Base Model Preparation

```python
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
base_model.trainable = False  # Freeze all base layers
```

The pre-trained MobileNetV2 is loaded without the ImageNet classification head (`include_top=False`). Global average pooling reduces the final feature map to a 1280-dimensional vector. All base model layers are frozen to preserve the learned feature representations.

### Step 2: Custom Classification Head

```python
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2, activation='softmax')
])
```

A custom head is added with:
- **Dropout (0.3)**: Regularization to prevent overfitting on the training set.
- **Dense (128, ReLU)**: A hidden layer to learn task-specific feature combinations.
- **Dropout (0.2)**: Additional regularization before the final layer.
- **Dense (2, Softmax)**: Output layer producing probabilities for each class.

### Step 3: Compilation

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

- **Adam optimizer** with a low learning rate (1e-4) to make gentle updates to the classification head.
- **Categorical cross-entropy** as the loss function for multi-class (here, binary via softmax) classification.

### Step 4: Data Augmentation

Training images are augmented in real-time using `tf.keras.preprocessing.image.ImageDataGenerator`:

- Horizontal flip
- Random rotation (±15°)
- Width and height shift (±10%)
- Zoom range (±10%)
- Brightness adjustment (±20%)
- Rescaling (1/255 normalization)

Augmentation increases the effective training set size and improves generalization by exposing the model to varied presentations of the same waste items.

### Step 5: Training

Training is performed for 20 epochs with a batch size of 32. The following callbacks are used:

- **EarlyStopping**: Monitors validation loss with patience of 5 epochs to prevent overfitting.
- **ModelCheckpoint**: Saves the best model (by validation accuracy) to `models/wet_dry/wet_dry_mobilenetv2.keras`.
- **ReduceLROnPlateau**: Reduces the learning rate by a factor of 0.5 if validation loss plateaus for 3 epochs.

### Step 6: Fine-Tuning (Optional)

After initial training, the top layers of MobileNetV2 can be unfrozen for fine-tuning:

```python
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False
```

Fine-tuning uses a very low learning rate (1e-5) to adjust the pre-trained features slightly to the waste classification domain. This step typically improves accuracy by 1–3%.

## Evaluation Metrics

Models are evaluated using:

- **Accuracy**: Overall percentage of correct predictions on the test set.
- **Precision**: For each class, the fraction of predicted positives that are truly positive.
- **Recall**: For each class, the fraction of actual positives correctly identified.
- **F1-Score**: Harmonic mean of precision and recall.
- **Confusion Matrix**: Visual breakdown of true positives, false positives, true negatives, and false negatives.
- **ROC-AUC**: Area under the receiver operating characteristic curve, measuring discrimination ability.

## Dataset Preparation

### Wet/Dry Classifier

The primary training data comes from the TechSash dataset, with Organic mapped to Wet and Recyclable mapped to Dry. This is supplemented with RealWaste images where Food Organics and Vegetation map to Wet, and Cardboard, Glass, Metal, Paper, and Plastic map to Dry. Textile Trash and Miscellaneous Trash are excluded due to ambiguity.

### Segregation Status Classifier

This model requires scene-level images annotated as either "properly segregated" (separate wet and dry bins, correctly filled) or "mixed waste" (single bin with both wet and dry items). These images are collected and annotated following the guidelines in `docs/annotation_guidelines.md`.

## Reproducibility

All training scripts accept command-line arguments for hyperparameters and use fixed random seeds for reproducibility. Training history (loss, accuracy per epoch) is saved as JSON alongside the model file. The `models/metadata/model_metadata.json` file records the configuration used for each trained model.
