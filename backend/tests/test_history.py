"""Tests for history endpoints."""

from app.database.models import ClassificationRecord
from app.extensions import db as _db
from datetime import datetime, timezone


def _seed_record(app):
    """Insert a sample record and return its id."""
    with app.app_context():
        rec = ClassificationRecord(
            image_filename='test.jpg',
            image_path='/tmp/test.jpg',
            classification_mode='item',
            predicted_category='Dry',
            confidence_score=0.92,
            model_name='wet_dry_mobilenetv2.keras',
            model_version='1.0.0',
            created_at=datetime.now(timezone.utc),
        )
        _db.session.add(rec)
        _db.session.commit()
        return rec.id


def test_list_history_empty(client):
    """GET /api/v1/history with no records."""
    resp = client.get('/api/v1/history')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert data['data']['records'] == []
    assert data['data']['total'] == 0


def test_list_history_with_record(client, app):
    """GET /api/v1/history with one record."""
    _seed_record(app)
    resp = client.get('/api/v1/history')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['data']['records']) == 1
    assert data['data']['records'][0]['predicted_category'] == 'Dry'


def test_get_history_record(client, app):
    """GET single record by id."""
    rid = _seed_record(app)
    resp = client.get(f'/api/v1/history/{rid}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['data']['id'] == rid


def test_get_history_record_not_found(client):
    resp = client.get('/api/v1/history/9999')
    assert resp.status_code == 404


def test_delete_history_record(client, app):
    """DELETE a record and confirm it's gone."""
    rid = _seed_record(app)
    resp = client.delete(f'/api/v1/history/{rid}')
    assert resp.status_code == 200
    # Verify deleted
    resp2 = client.get(f'/api/v1/history/{rid}')
    assert resp2.status_code == 404


def test_delete_nonexistent_record(client):
    resp = client.delete('/api/v1/history/9999')
    assert resp.status_code == 404
