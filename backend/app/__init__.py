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

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )

    # CORS — allow the Vite dev server
    CORS(app, resources={r'/api/*': {'origins': ['http://localhost:5173']}})

    # Extensions
    db.init_app(app)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Ensure instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)

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
        db.create_all()

    return app
