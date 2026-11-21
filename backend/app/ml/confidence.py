"""Confidence analysis and uncertainty assessment for model predictions."""

import numpy as np


DISPOSAL_ADVICE = {
    'Dry': 'Place in the Dry / Recyclable waste bin (Paper, Cardboard, Clean Plastics, Metal, Glass). Ensure items are clean and free of organic residues.',
    'Wet': 'Place in the Wet / Compostable organic waste bin (Food Scraps, Peels, Biodegradable Kitchen Waste). Suitable for composting or biomethanation.',
    'Mixed Waste': 'Wet and dry waste are mixed in the same receptacle. Segregate into separate wet (organic) and dry (recyclable) streams before disposal.',
    'Properly Segregated': 'Waste streams are properly segregated into their respective receptacles. Ready for municipal collection or recycling processing.',
    'Uncertain': 'Insufficient visual evidence to reliably determine waste type. Please inspect the item manually or provide a clearer photo under proper lighting.',
}


def analyze_confidence(predictions, labels, threshold=0.60):
    """Analyse a prediction vector and return structured, calibrated results.

    Args:
        predictions: numpy array of shape (1, num_classes) or (num_classes,)
                     containing raw model output probabilities.
        labels: list of class label strings matching output indices.
        threshold: minimum confidence score to flag the prediction as confident.

    Returns:
        dict with keys:
            predicted_class  — str, winning label or 'Uncertain'
            suggested_class  — str, argmax class for transparency
            confidence       — float, highest probability
            is_confident     — bool, confidence >= threshold and probability margin sufficient
            status           — 'CONFIDENT' or 'UNCERTAIN'
            warning          — str or None
            disposal_advice  — str
            probabilities    — dict mapping each label to its probability
    """
    probs = np.array(predictions).flatten()

    # For binary sigmoid output (single neuron) expand to 2-class
    if probs.shape[0] == 1 and len(labels) == 2:
        p = float(probs[0])
        probs = np.array([1.0 - p, p])

    predicted_idx = int(np.argmax(probs))
    confidence = float(probs[predicted_idx])
    suggested = labels[predicted_idx]

    probabilities = {
        label: round(float(probs[i]), 4)
        for i, label in enumerate(labels)
    }

    # Margin check between top 2 classes
    sorted_probs = np.sort(probs)[::-1]
    margin = float(sorted_probs[0] - sorted_probs[1]) if len(sorted_probs) > 1 else sorted_probs[0]

    # Evaluate certainty criteria:
    # 1. Top probability must meet threshold (default 0.60)
    # 2. Probability margin between classes must be >= 0.15 (prevents ambiguous ~52-54% calls)
    is_confident = (confidence >= threshold) and (margin >= 0.15)

    if is_confident:
        predicted_class = suggested
        status = 'CONFIDENT'
        warning = None
    else:
        predicted_class = 'Uncertain'
        status = 'UNCERTAIN'
        warning = (
            f"Low confidence ({confidence * 100:.1f}%) or insufficient visual evidence. "
            f"The image does not provide definitive features to distinguish between categories."
        )

    return {
        'predicted_class': predicted_class,
        'suggested_class': suggested,
        'confidence': round(confidence, 4),
        'is_confident': is_confident,
        'status': status,
        'warning': warning,
        'disposal_advice': DISPOSAL_ADVICE.get(predicted_class, DISPOSAL_ADVICE['Uncertain']),
        'probabilities': probabilities,
    }
