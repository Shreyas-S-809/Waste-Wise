# Wet/Dry Classification Model

This directory stores trained model files for the **Wet/Dry waste classifier**.

## Model Architecture

- **Base**: MobileNetV2 (pre-trained on ImageNet)
- **Input**: 224×224×3 RGB images
- **Output**: 2 classes — Wet (Organic), Dry (Recyclable)
- **Transfer Learning**: Frozen base layers with custom classification head

## Files

After training, this directory will contain:
- `wet_dry_mobilenetv2.keras` — Full trained Keras model
- `training_history.json` — Training metrics per epoch

## Training

```powershell
python scripts/train_wet_dry.py --epochs 20 --batch-size 32
```
