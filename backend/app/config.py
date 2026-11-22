"""Application configuration."""

import os
import tempfile

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
IS_VERCEL = bool(os.environ.get('VERCEL'))
TEMP_DIR = tempfile.gettempdir()


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    UPLOAD_FOLDER = os.environ.get(
        'UPLOAD_FOLDER',
        os.path.join(TEMP_DIR, 'uploads') if IS_VERCEL else os.path.join(BASE_DIR, 'uploads')
    )
    MODEL_DIR = os.environ.get(
        'MODEL_DIR',
        os.path.join(BASE_DIR, 'models') if os.path.isdir(os.path.join(BASE_DIR, 'models')) else os.path.join(PROJECT_ROOT, 'models')
    )
    CONFIDENCE_THRESHOLD = 0.6


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'wastewise.db'),
    )


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'tests', 'uploads')


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(TEMP_DIR, 'wastewise.db').replace('\\', '/') if IS_VERCEL else 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'wastewise.db'),
    )


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
