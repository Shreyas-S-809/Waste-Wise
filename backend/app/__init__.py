"""Flask application factory."""

import os
import logging

from flask import Flask
from flask_cors import CORS

from app.config import config_by_name
from app.extensions import db


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    import tempfile
    is_vercel = bool(os.environ.get('VERCEL'))
    instance_path = os.path.join(tempfile.gettempdir(), 'instance') if is_vercel else None

    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )

    # CORS — allow all origins for API in production and local dev
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    # Extensions
    db.init_app(app)

    # Ensure upload directory exists (handle read-only serverless filesystems)
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError as exc:
        logging.warning("Could not create upload directory %s: %s", app.config.get('UPLOAD_FOLDER'), exc)

    # Ensure instance directory exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as exc:
        logging.warning("Could not create instance directory %s: %s", app.instance_path, exc)

    # Initialise model manager with the configured model directory
    from app.ml.model_loader import model_manager
    model_manager.set_model_dir(app.config['MODEL_DIR'])

    # Register blueprints
    from app.api.routes.health import health_bp
    from app.api.routes.prediction import prediction_bp
    from app.api.routes.history import history_bp
    from app.api.routes.model_status import model_status_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(model_status_bp)

    # Create database tables on first request
    with app.app_context():
        try:
            db.create_all()
        except Exception as exc:
            logging.warning("db.create_all() failed: %s", exc)

    return app
