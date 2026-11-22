"""Health check endpoint."""

from datetime import datetime, timezone
from flask import Blueprint

from app.utils.responses import success_response

health_bp = Blueprint('health', __name__)


@health_bp.route('/api/health', methods=['GET'])
@health_bp.route('/api/v1/health', methods=['GET'])
def health_check():
    """Return basic health status."""
    return success_response({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'service': 'WasteWise API',
    })
