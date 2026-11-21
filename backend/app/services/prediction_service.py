"""Prediction service — orchestrates preprocessing, inference, and confidence analysis."""

import logging
from pathlib import Path
from PIL import Image
import numpy as np
from flask import current_app

from app.ml.preprocessing import preprocess_image
from app.ml.inference import predict
from app.ml.confidence import analyze_confidence, DISPOSAL_ADVICE
from app.ml.label_mapping import LABEL_MAP
from app.ml.model_loader import model_manager

logger = logging.getLogger(__name__)


def check_image_quality(image_path):
    """Check whether an image is suitable for classification or out-of-distribution.

    Returns:
        (is_valid: bool, reason: str or None)
    """
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            if w < 32 or h < 32:
                return False, f"Image resolution ({w}x{h}) is too low for reliable waste classification."

            img_rgb = img.convert('RGB')
            arr = np.array(img_rgb, dtype=np.float32)

            # Check standard deviation across pixels
            # A completely blank / solid color / uniform image has near zero std
            std = float(np.std(arr))
            if std < 12.0:
                return False, "Image lacks sufficient visual texture or details (nearly solid color or blank canvas)."

            return True, None
    except Exception as exc:
        return False, f"Failed to inspect image: {str(exc)}"


class PredictionService:
    """High‑level classification interface."""

    # -----------------------------------------------------------------
    # Item‑level classification (wet / dry)
    # -----------------------------------------------------------------

    @staticmethod
    def classify_item(image_path):
        """Classify a single waste image as Wet or Dry.

        Returns:
            dict with prediction, confidence, probabilities, model_info.

        Raises:
            RuntimeError if the model is not available.
        """
        model_type = 'wet_dry'
        labels = LABEL_MAP[model_type]
        threshold = current_app.config.get('CONFIDENCE_THRESHOLD', 0.60)
        model_info = model_manager.get_model_info(model_type)

        # Check image quality / out-of-distribution
        is_valid, reason = check_image_quality(image_path)
        if not is_valid:
            logger.warning('Image quality check failed for %s: %s', image_path, reason)
            return {
                'classification_mode': 'item',
                'model_type': model_type,
                'predicted_category': 'Uncertain',
                'suggested_class': 'Uncertain',
                'confidence_score': 0.0,
                'is_confident': False,
                'status': 'OUT_OF_DISTRIBUTION',
                'warning': reason,
                'disposal_advice': DISPOSAL_ADVICE['Uncertain'],
                'probabilities': {lbl: 0.0 for lbl in labels},
                'model_name': model_info.get('model_file', 'wet_dry_mobilenetv2.keras'),
                'model_version': model_info.get('version', '1.0.0'),
            }

        image_data = preprocess_image(image_path)
        predictions = predict(image_data, model_type)
        analysis = analyze_confidence(predictions, labels, threshold)

        return {
            'classification_mode': 'item',
            'model_type': model_type,
            'predicted_category': analysis['predicted_class'],
            'suggested_class': analysis.get('suggested_class', analysis['predicted_class']),
            'confidence_score': analysis['confidence'],
            'is_confident': analysis['is_confident'],
            'status': analysis['status'],
            'warning': analysis['warning'],
            'disposal_advice': analysis['disposal_advice'],
            'probabilities': analysis['probabilities'],
            'model_name': model_info.get('model_file', 'wet_dry_mobilenetv2.keras'),
            'model_version': model_info.get('version', '1.0.0'),
        }

    # -----------------------------------------------------------------
    # Segregation status classification
    # -----------------------------------------------------------------

    @staticmethod
    def classify_segregation(image_path):
        """Classify a scene image as Mixed Waste or Properly Segregated.

        Returns:
            dict with prediction, confidence, probabilities, model_info.

        Raises:
            RuntimeError if the model is not available.
        """
        model_type = 'segregation_status'
        labels = LABEL_MAP[model_type]
        threshold = current_app.config.get('CONFIDENCE_THRESHOLD', 0.60)
        model_info = model_manager.get_model_info(model_type)

        if not model_manager.is_model_available(model_type):
            raise RuntimeError(
                f"Model '{model_type}' is pending annotated multi-bin scenes. "
                "Phase 1 focused on Individual Waste Item Classification."
            )

        # Check image quality / out-of-distribution
        is_valid, reason = check_image_quality(image_path)
        if not is_valid:
            return {
                'classification_mode': 'segregation',
                'model_type': model_type,
                'predicted_category': 'Uncertain',
                'suggested_class': 'Uncertain',
                'confidence_score': 0.0,
                'is_confident': False,
                'status': 'OUT_OF_DISTRIBUTION',
                'warning': reason,
                'disposal_advice': DISPOSAL_ADVICE['Uncertain'],
                'probabilities': {lbl: 0.0 for lbl in labels},
                'model_name': model_info.get('model_file', 'segregation_status_mobilenetv2.keras'),
                'model_version': model_info.get('version', '0.1.0-alpha'),
            }

        image_data = preprocess_image(image_path)
        predictions = predict(image_data, model_type)
        analysis = analyze_confidence(predictions, labels, threshold)

        return {
            'classification_mode': 'segregation',
            'model_type': model_type,
            'predicted_category': analysis['predicted_class'],
            'suggested_class': analysis.get('suggested_class', analysis['predicted_class']),
            'confidence_score': analysis['confidence'],
            'is_confident': analysis['is_confident'],
            'status': analysis['status'],
            'warning': analysis['warning'],
            'disposal_advice': analysis['disposal_advice'],
            'probabilities': analysis['probabilities'],
            'model_name': model_info.get('model_file', 'segregation_status_mobilenetv2.keras'),
            'model_version': model_info.get('version', '0.1.0-alpha'),
        }
