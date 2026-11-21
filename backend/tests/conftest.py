"""Shared test fixtures."""

import os
import sys
import pytest
import tempfile
from io import BytesIO
from PIL import Image

# Ensure the backend package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    """Create a test Flask application."""
    app = create_app('testing')
    yield app


@pytest.fixture(scope='function')
def client(app):
    """Provide a Flask test client with a fresh database per test."""
    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def db(app):
    """Provide the SQLAlchemy db instance."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def sample_image_bytes():
    """Return raw JPEG bytes of a tiny test image."""
    img = Image.new('RGB', (224, 224), color=(128, 64, 32))
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    return buf.read()


@pytest.fixture()
def sample_image_file(sample_image_bytes):
    """Return a tuple (BytesIO, filename, content_type) for use with test client."""
    return (BytesIO(sample_image_bytes), 'test.jpg', 'image/jpeg')
