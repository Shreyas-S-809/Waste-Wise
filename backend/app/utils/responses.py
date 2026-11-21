"""Standardised JSON response helpers."""

from flask import jsonify


def success_response(data, status=200):
    """Return a consistent success envelope."""
    return jsonify({'success': True, 'data': data}), status


def error_response(message, status=400):
    """Return a consistent error envelope."""
    return jsonify({'success': False, 'error': message}), status
