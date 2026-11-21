"""ModelManager — singleton that lazy‑loads and caches Keras models."""

import os
import json
import logging
import threading
from pathlib import Path

# Ensure KERAS_HOME points to project .keras cache
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
os.environ.setdefault('KERAS_HOME', str(PROJECT_ROOT / '.keras'))

logger = logging.getLogger(__name__)

# Mapping from logical model type to sub‑directory under MODEL_DIR
_MODEL_DIRS = {
    'wet_dry': 'wet_dry',
    'segregation_status': 'segregation_status',
}

_MODEL_FILES = {
    'wet_dry': 'wet_dry_mobilenetv2.keras',
    'segregation_status': 'segregation_status_mobilenetv2.keras',
}


class ModelManager:
    """Thread‑safe singleton that manages ML model loading and caching."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialised = False
        return cls._instance

    def __init__(self, model_dir=None):
        if self._initialised:
            return
        self._model_dir = model_dir or ''
        self._models = {}
        self._metadata = {}
        self._initialised = True

    def set_model_dir(self, model_dir):
        """Set / update the base model directory (called from app factory)."""
        self._model_dir = model_dir

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def _load_metadata(self):
        """Read models/metadata/model_metadata.json if available."""
        if self._metadata:
            return
        meta_path = os.path.join(self._model_dir, 'metadata', 'model_metadata.json')
        if os.path.isfile(meta_path):
            try:
                with open(meta_path, 'r') as fh:
                    self._metadata = json.load(fh)
                logger.info('Loaded model metadata from %s', meta_path)
            except Exception as exc:
                logger.warning('Failed to read model metadata: %s', exc)

    # ------------------------------------------------------------------
    # Model loading
    # ------------------------------------------------------------------

    def _model_path(self, model_type):
        sub = _MODEL_DIRS.get(model_type)
        fname = _MODEL_FILES.get(model_type)
        if not sub or not fname:
            return None
        return os.path.join(self._model_dir, sub, fname)

    def get_model(self, model_type):
        """Return a loaded Keras model or None if unavailable."""
        if model_type in self._models:
            return self._models[model_type]

        path = self._model_path(model_type)
        if path is None or not os.path.isfile(path):
            logger.info('Model file not found for %s (expected %s)', model_type, path)
            return None

        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(path)
            self._models[model_type] = model
            logger.info('Loaded model %s from %s', model_type, path)
            return model
        except Exception as exc:
            logger.error('Failed to load model %s: %s', model_type, exc)
            return None

    def is_model_available(self, model_type):
        """Check whether a model file exists on disk (without loading it)."""
        path = self._model_path(model_type)
        return path is not None and os.path.isfile(path)

    def get_model_info(self, model_type):
        """Return metadata dict for a model type."""
        self._load_metadata()

        available = self.is_model_available(model_type)
        info = {
            'model_type': model_type,
            'available': available,
            'model_file': _MODEL_FILES.get(model_type, 'unknown'),
        }

        # Merge metadata from JSON if present
        models_meta = self._metadata.get('models', {})
        if model_type in models_meta:
            meta = models_meta[model_type]
            info.update({
                'version': meta.get('version', '0.0.0'),
                'status': meta.get('status', 'not_trained'),
                'classes': meta.get('classes', []),
                'training_date': meta.get('training_date'),
                'metrics': meta.get('metrics', {}),
            })
        else:
            info.update({
                'version': '0.0.0',
                'status': 'not_trained' if not available else 'trained',
                'classes': [],
                'training_date': None,
                'metrics': {},
            })

        return info


# Module‑level convenience instance
model_manager = ModelManager()
