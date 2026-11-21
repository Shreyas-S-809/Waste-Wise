"""Label mappings for classification models.

The order matches the alphabetical class‑directory order that
tf.keras.utils.image_dataset_from_directory uses by default.
"""

# Model A — Wet / Dry (item‑level) classifier
WET_DRY_LABELS = ['Dry', 'Wet']

# Model B — Segregation Status classifier
SEGREGATION_LABELS = ['Mixed Waste', 'Properly Segregated']

# Convenience lookup by model type key
LABEL_MAP = {
    'wet_dry': WET_DRY_LABELS,
    'segregation_status': SEGREGATION_LABELS,
}
