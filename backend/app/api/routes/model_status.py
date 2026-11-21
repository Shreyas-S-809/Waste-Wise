"""Model status endpoint."""

from flask import Blueprint

from app.utils.responses import success_response
from app.ml.model_loader import model_manager
from app.ml.label_mapping import LABEL_MAP

model_status_bp = Blueprint('model_status', __name__)


@model_status_bp.route('/api/v1/models/status', methods=['GET'])
def models_status():
    """Return availability and metadata for every registered model."""
    statuses = {}
    for model_type in ('wet_dry', 'segregation_status'):
        info = model_manager.get_model_info(model_type)
        # Enrich with known class labels
        if not info.get('classes'):
            info['classes'] = LABEL_MAP.get(model_type, [])
        statuses[model_type] = info

    return success_response({'models': statuses})
