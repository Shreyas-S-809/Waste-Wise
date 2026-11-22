# Segregation Status Model

This directory stores trained model files for the **waste segregation status classifier**.

## Model Architecture

- **Base**: MobileNetV2 (pre-trained on ImageNet)
- **Input**: 224×224×3 RGB images
- **Output**: 2 classes — Properly Segregated, Mixed Waste
- **Transfer Learning**: Frozen base layers with custom classification head

## Files

After training, this directory will contain:
- `segregation_mobilenetv2.keras` — Full trained Keras model
- `training_history.json` — Training metrics per epoch

## Training

```powershell
python scripts/train_segregation.py --epochs 20 --batch-size 32
```

## Note

This model requires annotated segregation scene images placed in:
- `datasets/raw/segregation_scenes/mixed_waste/`
- `datasets/raw/segregation_scenes/properly_segregated/`

See `docs/annotation_guidelines.md` for annotation instructions.
