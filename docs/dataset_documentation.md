# WasteWise — Dataset Documentation

## Overview

WasteWise uses two publicly available waste image datasets for training and evaluation. This document describes each dataset, its structure, licensing, and how the labels are mapped to the WasteWise classification scheme.

---

## Dataset 1: TechSash Organic/Recyclable Dataset

### Source

- **Name**: Waste Classification data (Organic vs Recyclable)
- **Platform**: Kaggle
- **Original Authors**: TechSash
- **URL**: https://www.kaggle.com/datasets/techsash/waste-classification-data

### Description

This dataset contains images of waste items classified into two categories: **Organic** (O) and **Recyclable** (R). The images were collected from various online sources and manually labelled. The dataset is pre-split into training and testing sets.

### Structure

```
Datasets/Additional WetDry images/DATASET/
├── TRAIN/
│   ├── O/     # Organic waste — 12,565 images
│   └── R/     # Recyclable waste — 9,999 images
└── TEST/
    ├── O/     # Organic waste — 1,401 images
    └── R/     # Recyclable waste — 1,112 images
```

### Statistics

| Split | Organic (O) | Recyclable (R) | Total |
|-------|-------------|-----------------|-------|
| Train | 12,565 | 9,999 | 22,564 |
| Test | 1,401 | 1,112 | 2,513 |
| **Total** | **13,966** | **11,111** | **25,077** |

### Class Imbalance

The training set has a 56:44 ratio (Organic:Recyclable). This mild imbalance is managed through data augmentation and class weight adjustment during training rather than under/oversampling, as the skew is not severe enough to warrant resampling.

### Image Properties

- **Format**: JPEG
- **Resolution**: Variable (typically 200×200 to 600×400)
- **Color**: RGB
- **Content**: Single waste items on various backgrounds

### WasteWise Label Mapping

| Original Label | WasteWise Label | Rationale |
|---------------|-----------------|-----------|
| O (Organic) | **Wet** | Organic waste is biodegradable/compostable → wet waste |
| R (Recyclable) | **Dry** | Recyclable materials are inorganic → dry waste |

---

## Dataset 2: RealWaste Dataset

### Source

- **Name**: RealWaste: A Novel Real-Life Data Set for Landfill Waste Classification Using Deep Learning
- **Institution**: University
- **Format**: Directory per category

### Description

The RealWaste dataset contains images of real waste items captured on a conveyor belt at a materials recovery facility. Unlike many waste datasets that use stock photos, these are authentic real-world images with realistic lighting, angles, and backgrounds. The dataset has nine categories representing common waste types.

### Structure

```
Datasets/realwaste-main/RealWaste/
├── Cardboard/           # 461 images
├── Food Organics/       # 411 images
├── Glass/               # 420 images
├── Metal/               # 790 images
├── Miscellaneous Trash/ # 495 images
├── Paper/               # 500 images
├── Plastic/             # 921 images
├── Textile Trash/       # 318 images
└── Vegetation/          # 436 images
```

### Statistics

| Category | Count | WasteWise Mapping |
|----------|-------|-------------------|
| Cardboard | 461 | Dry |
| Food Organics | 411 | Wet |
| Glass | 420 | Dry |
| Metal | 790 | Dry |
| Miscellaneous Trash | 495 | Excluded |
| Paper | 500 | Dry |
| Plastic | 921 | Dry |
| Textile Trash | 318 | Excluded |
| Vegetation | 436 | Wet |
| **Total** | **4,752** | — |

### WasteWise Label Mapping

| Original Label | WasteWise Label | Rationale |
|---------------|-----------------|-----------|
| Food Organics | **Wet** | Biodegradable food waste → wet waste |
| Vegetation | **Wet** | Biodegradable plant material → wet waste |
| Cardboard | **Dry** | Recyclable material → dry waste |
| Glass | **Dry** | Recyclable material → dry waste |
| Metal | **Dry** | Recyclable material → dry waste |
| Paper | **Dry** | Recyclable material → dry waste |
| Plastic | **Dry** | Recyclable material → dry waste |
| Textile Trash | **Excluded** | Ambiguous — can be recyclable or non-recyclable depending on condition |
| Miscellaneous Trash | **Excluded** | Catch-all category with no clear wet/dry distinction |

### Image Properties

- **Format**: JPEG
- **Resolution**: Variable (conveyor belt captures)
- **Color**: RGB
- **Content**: Single waste items on a conveyor belt under controlled lighting

---

## Combined Dataset Statistics

After label mapping and exclusion:

| Source | Wet | Dry | Excluded | Total |
|--------|-----|-----|----------|-------|
| TechSash Train | 12,565 | 9,999 | 0 | 22,564 |
| TechSash Test | 1,401 | 1,112 | 0 | 2,513 |
| RealWaste | 847 | 3,092 | 813 | 4,752 |
| **Combined** | **14,813** | **14,203** | **813** | **29,829** |

After exclusion, the combined dataset has approximately 28,016 usable images with a nearly balanced 52:48 Wet:Dry ratio.

---

## Preprocessing Pipeline

1. **Load** images from source directories
2. **Filter** excluded categories (Textile Trash, Miscellaneous Trash from RealWaste)
3. **Map** labels to binary Wet/Dry
4. **Resize** to 224×224 pixels
5. **Normalize** pixel values to [0, 1] range
6. **Split** (if needed) into train/validation/test sets
7. **Augment** training images with random transformations
8. **Generate** manifest CSV files documenting each image's path, label, source, and split
