# WasteWise — Model Cards

This document provides model cards for both WasteWise classifiers, following the format proposed by Mitchell et al. (2019).

---

## Model Card: Wet/Dry Waste Classifier

### Model Details

- **Model Name**: WasteWise Wet/Dry Classifier v1.0
- **Architecture**: MobileNetV2 + Custom Classification Head
- **Framework**: TensorFlow / Keras
- **Model File**: `models/wet_dry/wet_dry_mobilenetv2.keras`
- **Input**: 224×224×3 RGB image
- **Output**: 2-class probability distribution [Wet, Dry]
- **Parameters**: ~3.5M (3.4M frozen MobileNetV2 base + ~100K trainable head)
- **Status**: Not yet trained

### Intended Use

- **Primary use**: Classifying photographs of individual waste items as Wet (organic/biodegradable) or Dry (recyclable/inorganic) through the WasteWise web application.
- **Primary users**: Households, sanitation workers, municipal waste management operators, and educators demonstrating AI-assisted waste sorting.
- **Out-of-scope uses**: This model is not designed for industrial-scale sorting on conveyor belts in real-time, medical waste classification, hazardous waste identification, or any safety-critical application where misclassification could cause harm.

### Training Data

- **TechSash Dataset**: 22,564 training images (12,565 Organic → Wet, 9,999 Recyclable → Dry)
- **RealWaste Supplement**: ~3,939 images mapped to Wet/Dry (847 Wet, 3,092 Dry)
- **Augmentation**: Horizontal flip, rotation (±15°), shift (±10%), zoom (±10%), brightness (±20%)
- **Validation Split**: 20% of training data held out for validation

### Evaluation Data

- **TechSash Test Set**: 2,513 images (1,401 Organic, 1,112 Recyclable)
- **Evaluation is performed on the unaugmented test set**

### Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Test Accuracy | ≥90% | *Pending training* |
| Precision (Wet) | ≥88% | *Pending* |
| Recall (Wet) | ≥88% | *Pending* |
| Precision (Dry) | ≥88% | *Pending* |
| Recall (Dry) | ≥88% | *Pending* |
| F1-Score (macro) | ≥88% | *Pending* |

### Limitations

- **Domain shift**: The model is trained on images from specific datasets. Performance may degrade on images captured in very different conditions (e.g., extreme lighting, unusual waste items, non-standard backgrounds).
- **Cultural bias**: Waste composition varies by region. The training data primarily represents waste types common in certain geographies and may not generalize globally.
- **Single-item assumption**: The model expects images of individual waste items. Images containing multiple items or cluttered scenes may produce unreliable predictions.
- **Image quality**: Very low-resolution, blurry, or heavily occluded images may result in incorrect classifications.

### Ethical Considerations

- The model should not be used as the sole decision-maker in any regulatory or punitive waste management enforcement.
- Misclassifications should not result in penalties for individuals or communities.
- The model's predictions should be treated as suggestions to assist human decision-making, not as authoritative determinations.

---

## Model Card: Segregation Status Classifier

### Model Details

- **Model Name**: WasteWise Segregation Status Classifier v1.0
- **Architecture**: MobileNetV2 + Custom Classification Head
- **Framework**: TensorFlow / Keras
- **Model File**: `models/segregation_status/segregation_mobilenetv2.keras`
- **Input**: 224×224×3 RGB image
- **Output**: 2-class probability distribution [Mixed Waste, Properly Segregated]
- **Parameters**: ~3.5M
- **Status**: Not yet trained — awaiting annotated scene images

### Intended Use

- **Primary use**: Assessing whether a photograph of a waste collection point or bin shows properly segregated waste or mixed waste.
- **Primary users**: Municipal waste management inspectors, sanitation supervisors, and ward-level monitoring dashboards (Phase 2).
- **Out-of-scope uses**: Not suitable for real-time video surveillance of waste bins, automated enforcement actions, or use in contexts where the model's accuracy has not been validated against local waste management standards.

### Training Data

- **Source**: Custom-collected and annotated scene images
- **Classes**: `properly_segregated`, `mixed_waste`
- **Target Size**: 1,000+ images per class
- **Status**: Data collection not yet started — see `docs/annotation_guidelines.md`

### Limitations

- This model has not yet been trained and performance characteristics are unknown.
- Scene-level classification is inherently more challenging than single-item classification due to visual complexity.
- The definition of "properly segregated" may vary by local municipal guidelines.

### Ethical Considerations

- Same as the Wet/Dry classifier — predictions should support human decision-making, not replace it.
- Special care should be taken when deploying this model in ward-level monitoring systems to ensure equitable assessment across different socioeconomic areas.
