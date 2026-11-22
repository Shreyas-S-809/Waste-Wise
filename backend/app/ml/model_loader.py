"""ModelManager — singleton that lazy‑loads and caches LiteRT/TFLite and Keras models."""

import os
import json
import logging
import threading
import numpy as np
from PIL import Image
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

_MODEL_CANDIDATE_FILES = {
    'wet_dry': ['wet_dry_mobilenetv2.tflite', 'wet_dry_mobilenetv2.keras'],
    'segregation_status': ['segregation_status_mobilenetv2.tflite', 'segregation_status_mobilenetv2.keras'],
}


def _load_tflite_interpreter(path):
    """Load TFLite interpreter using ai-edge-litert, tflite-runtime, or tf.lite."""
    try:
        from ai_edge_litert.interpreter import Interpreter
        logger.info('Using ai_edge_litert Interpreter')
        return Interpreter(model_path=path)
    except ImportError:
        pass

    try:
        from tflite_runtime.interpreter import Interpreter
        logger.info('Using tflite_runtime Interpreter')
        return Interpreter(model_path=path)
    except ImportError:
        pass

    try:
        import tensorflow as tf
        logger.info('Using tf.lite.Interpreter')
        return tf.lite.Interpreter(model_path=path)
    except ImportError as exc:
        raise ImportError(
            "No LiteRT or TFLite interpreter found. Please install 'ai-edge-litert'."
        ) from exc


class TFLiteModelWrapper:
    """Wraps LiteRT / TFLite Interpreter to provide a Keras-like .predict() API."""

    def __init__(self, interpreter, model_path):
        self.interpreter = interpreter
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.model_path = model_path

    def predict(self, input_data, verbose=0):
        """Run inference on preprocessed numpy input (1, 224, 224, 3)."""
        input_data = input_data.astype(np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        return output

    def predict_waste(self, pil_image):
        """Direct helper to predict from a PIL Image object."""
        img = pil_image.convert('RGB').resize((224, 224), Image.LANCZOS)
        input_data = np.expand_dims(np.array(img, dtype=np.float32), axis=0)
        # MobileNetV2 preprocessing: (input_data / 127.5) - 1.0
        input_data = (input_data / 127.5) - 1.0
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        return prediction


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
        if not sub:
            return None
        candidates = _MODEL_CANDIDATE_FILES.get(model_type, [])
        for fname in candidates:
            p = os.path.join(self._model_dir, sub, fname)
            if os.path.isfile(p):
                return p
        return None

    def get_model(self, model_type):
        """Return a loaded LiteRT / Keras model or None if unavailable."""
        if model_type in self._models:
            return self._models[model_type]

        path = self._model_path(model_type)
        if path is None or not os.path.isfile(path):
            logger.info('Model file not found for %s (searched %s)', model_type, self._model_dir)
            return None

        try:
            if path.endswith('.tflite'):
                interpreter = _load_tflite_interpreter(path)
                model = TFLiteModelWrapper(interpreter, path)
                self._models[model_type] = model
                logger.info('Loaded TFLite/LiteRT model %s from %s', model_type, path)
                return model
            else:
                import tensorflow as tf
                model = tf.keras.models.load_model(path)
                self._models[model_type] = model
                logger.info('Loaded Keras model %s from %s', model_type, path)
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

        path = self._model_path(model_type)
        available = path is not None and os.path.isfile(path)
        active_file = os.path.basename(path) if path else 'unknown'

        info = {
            'model_type': model_type,
            'available': available,
            'model_file': active_file,
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
