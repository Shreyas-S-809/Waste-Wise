"""Inference — run a prediction through a loaded LiteRT / Keras model."""

import logging
import numpy as np
from PIL import Image

from app.ml.model_loader import model_manager

logger = logging.getLogger(__name__)


def predict(image_data, model_type):
    """Run model.predict() on preprocessed image data.

    Args:
        image_data: numpy array of shape (1, 224, 224, 3).
        model_type: 'wet_dry' or 'segregation_status'.

    Returns:
        numpy predictions array, or None if the model is unavailable.

    Raises:
        RuntimeError: if the model is not available.
    """
    model = model_manager.get_model(model_type)
    if model is None:
        raise RuntimeError(
            f"Model '{model_type}' is not available. "
            "Please train or provide the model first."
        )

    predictions = model.predict(image_data, verbose=0)
    logger.info(
        'Prediction for %s: %s',
        model_type,
        predictions.tolist(),
    )
    return predictions


def predict_waste(pil_image, model_type='wet_dry'):
    """Helper to predict from a PIL Image object using LiteRT / TFLite.

    Args:
        pil_image: PIL Image instance.
        model_type: 'wet_dry' or 'segregation_status'.

    Returns:
        1D numpy array of class probabilities (e.g., [p_dry, p_wet]).
    """
    model = model_manager.get_model(model_type)
    if model is None:
        raise RuntimeError(f"Model '{model_type}' is not available.")

    if hasattr(model, 'predict_waste'):
        return model.predict_waste(pil_image)

    from app.ml.preprocessing import preprocess_image
    arr = preprocess_image(pil_image)
    return model.predict(arr)[0]
