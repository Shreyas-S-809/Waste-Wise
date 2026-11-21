"""Prediction endpoints."""

import logging
from flask import Blueprint, request

from app.utils.responses import success_response, error_response
from app.utils.validators import validate_image_file
from app.services.image_service import validate_and_save_image
from app.services.prediction_service import PredictionService
from app.services.history_service import HistoryService

logger = logging.getLogger(__name__)

prediction_bp = Blueprint('prediction', __name__)


def _handle_prediction(classification_fn, model_label):
    """Shared logic for both prediction endpoints."""
    # Check for file in request
    if 'image' not in request.files:
        return error_response('No image file provided. Send a file with key "image".', 400)

    file = request.files['image']

    # Validate the image
    valid, msg = validate_image_file(file)
    if not valid:
        return error_response(msg, 400)

    # Save image
    try:
        saved_path, filename = validate_and_save_image(file)
    except ValueError as exc:
        return error_response(str(exc), 400)

    # Run prediction
    try:
        result = classification_fn(saved_path)
    except RuntimeError:
        return error_response(
            f'Model not trained yet. Please train the {model_label} classifier first.',
            503,
        )
    except Exception as exc:
        logger.exception('Prediction failed')
        return error_response(f'Prediction failed: {str(exc)}', 500)

    # Save to history
    try:
        record = HistoryService.save_prediction(result, filename, saved_path)
        result['id'] = record.id
    except Exception as exc:
        logger.warning('Failed to save prediction to history: %s', exc)

    return success_response(result, 200)


@prediction_bp.route('/api/v1/predict/item', methods=['POST'])
def predict_item():
    """Classify a waste item image as Wet or Dry."""
    return _handle_prediction(PredictionService.classify_item, 'wet/dry')


@prediction_bp.route('/api/v1/predict/segregation', methods=['POST'])
def predict_segregation():
    """Classify a scene image as Mixed Waste or Properly Segregated."""
    return _handle_prediction(PredictionService.classify_segregation, 'segregation status')
