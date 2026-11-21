# WasteWise — Segregation Scene Annotation Guidelines

## Purpose

This document provides guidelines for annotating images of waste collection scenes for the **Segregation Status Classifier** (Phase 2). The model needs labelled scene images to learn the visual difference between properly segregated waste and improperly mixed waste.

## Scope

Annotators will label photographs of waste bins, waste collection points, or waste disposal scenes. Each image receives one label indicating whether the waste shown is **properly segregated** or **mixed (improperly segregated)**.

## Label Definitions

### 1. Properly Segregated (`properly_segregated`)

An image should be labelled as "properly segregated" if it meets **all** of the following criteria:

- **Separate containers**: There are at least two distinct containers or bins visible — one for wet waste and one for dry waste (or clearly separated piles).
- **Correct contents**: Each container predominantly contains the correct type of waste:
  - Wet bin: Food scraps, vegetable peels, fruit waste, garden trimmings, soiled paper/napkins.
  - Dry bin: Plastic bottles/packaging, glass, metal cans, clean paper, cardboard.
- **Minimal cross-contamination**: Less than approximately 10% of the contents in any bin appear to be the wrong waste type.
- **Clear visual evidence**: The image is clear enough to visually confirm that the segregation is appropriate.

### 2. Mixed Waste (`mixed_waste`)

An image should be labelled as "mixed waste" if **any** of the following apply:

- **Single container**: All waste is in a single bin or pile with both wet and dry items visibly mixed together.
- **Significant cross-contamination**: More than approximately 10% of a bin's contents are the wrong type.
- **No segregation attempt**: There is no visual indication that any sorting has taken place.
- **Empty or ambiguous bins**: If the bins are empty or the contents cannot be determined, label as mixed waste (conservative approach).

## Annotation Process

### Image Collection

1. Photograph waste bins at collection points, households, or municipal waste stations.
2. Capture the scene from a distance that shows the bin contents clearly.
3. Ensure adequate lighting — avoid very dark or heavily shadowed images.
4. Each image file should be named descriptively or with a sequential ID.

### Labelling

1. Examine each image carefully.
2. Assign exactly one label: `properly_segregated` or `mixed_waste`.
3. Record the annotation in a CSV file with the following format.

### CSV Template

```csv
filename,label,annotator,confidence,notes
scene_001.jpg,properly_segregated,annotator_name,high,"Two bins clearly separated"
scene_002.jpg,mixed_waste,annotator_name,medium,"Single bin with mixed items"
scene_003.jpg,mixed_waste,annotator_name,low,"Unclear contents, defaulting to mixed"
```

**Columns:**
- `filename`: The image file name
- `label`: One of `properly_segregated` or `mixed_waste`
- `annotator`: Name or ID of the person who annotated this image
- `confidence`: `high`, `medium`, or `low` — the annotator's confidence in the label
- `notes`: Any additional observations about the image

## Quality Guidelines

- **When in doubt, label as `mixed_waste`**: It is better to have false negatives (missing a properly segregated scene) than false positives (labelling mixed waste as segregated).
- **Minimum image quality**: Images should be at least 640×480 pixels. Blurry, overexposed, or underexposed images should be discarded.
- **Avoid biased angles**: Do not photograph bins at angles that obscure the contents. Top-down or slightly angled top-down views are preferred.
- **Inter-annotator review**: Aim for at least two annotators per image. Disagreements should be resolved by a third annotator or discussion.

## File Organization

Place annotated images in the following directories:

```
datasets/raw/segregation_scenes/
├── mixed_waste/              # Images labelled as mixed_waste
├── properly_segregated/      # Images labelled as properly_segregated
└── annotations.csv           # Combined CSV manifest
```

## Target Dataset Size

For initial model development, we recommend:
- **Minimum**: 500 images per class (1,000 total)
- **Recommended**: 1,000+ images per class (2,000+ total)
- **Balanced**: Aim for roughly equal numbers in each class

## Privacy Considerations

- Do not photograph individuals or identifiable personal information.
- Blur any visible names, addresses, or identifying marks on waste items.
- Ensure compliance with local data protection regulations.
