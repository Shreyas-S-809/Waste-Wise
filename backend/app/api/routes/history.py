"""History endpoints — list, retrieve, delete classification records."""

from flask import Blueprint, request

from app.utils.responses import success_response, error_response
from app.services.history_service import HistoryService

history_bp = Blueprint('history', __name__)


@history_bp.route('/api/v1/history', methods=['GET'])
def list_history():
    """Return paginated classification history."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    except (ValueError, TypeError):
        return error_response('page and per_page must be integers.', 400)

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20

    data = HistoryService.get_history(page=page, per_page=per_page)
    return success_response(data)


@history_bp.route('/api/v1/history/<int:record_id>', methods=['GET'])
def get_history_record(record_id):
    """Return a single classification record."""
    record = HistoryService.get_prediction(record_id)
    if record is None:
        return error_response('Record not found.', 404)
    return success_response(record)


@history_bp.route('/api/v1/history/<int:record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    """Delete a classification record."""
    deleted = HistoryService.delete_prediction(record_id)
    if not deleted:
        return error_response('Record not found.', 404)
    return success_response({'message': 'Record deleted successfully.'})
