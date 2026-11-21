"""Tests for prediction endpoints."""

from io import BytesIO


def test_predict_item_no_file(client):
    """POST without an image should return 400."""
    resp = client.post('/api/v1/predict/item')
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['success'] is False
    assert 'No image file' in data['error']


def test_predict_item_invalid_mime(client, sample_image_bytes):
    """POST with a non‑image MIME type should be rejected."""
    resp = client.post(
        '/api/v1/predict/item',
        data={'image': (BytesIO(sample_image_bytes), 'test.txt', 'text/plain')},
        content_type='multipart/form-data',
    )
    assert resp.status_code == 400


def test_predict_item_success(client, sample_image_file):
    """When model is trained, POSTing an image returns 200 with prediction."""
    buf, name, ctype = sample_image_file
    resp = client.post(
        '/api/v1/predict/item',
        data={'image': (BytesIO(buf.read() if hasattr(buf, 'read') else buf), name, ctype)},
        content_type='multipart/form-data',
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    res = data['data']
    assert res['predicted_category'] in ('Dry', 'Wet')
    assert 0.0 <= res['confidence_score'] <= 1.0
    assert 'probabilities' in res


def test_predict_segregation_model_not_trained(client, sample_image_file):
    """Segregation endpoint should also 503 when model is missing."""
    buf, name, ctype = sample_image_file
    resp = client.post(
        '/api/v1/predict/segregation',
        data={'image': (BytesIO(buf.read() if hasattr(buf, 'read') else buf), name, ctype)},
        content_type='multipart/form-data',
    )
    assert resp.status_code == 503
