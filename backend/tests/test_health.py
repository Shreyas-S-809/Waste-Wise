"""Tests for the /api/health endpoint."""


def test_health_returns_200(client):
    """Health check should return 200 with healthy status."""
    resp = client.get('/api/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert data['data']['status'] == 'healthy'
    assert 'timestamp' in data['data']


def test_health_returns_service_name(client):
    resp = client.get('/api/health')
    data = resp.get_json()
    assert data['data']['service'] == 'WasteWise API'
