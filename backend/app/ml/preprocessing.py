"""Image preprocessing utilities for MobileNetV2 models."""

import io
import numpy as np
from PIL import Image


def preprocess_image(image_path_or_bytes, target_size=(224, 224)):
    """Load an image, resize, convert to RGB, and apply MobileNetV2 preprocessing.

    Args:
        image_path_or_bytes: A filesystem path (str) or raw bytes / BytesIO.
        target_size: Tuple (height, width) expected by the model.

    Returns:
        numpy array of shape (1, H, W, 3) ready for model.predict().
    """
    if isinstance(image_path_or_bytes, (bytes, bytearray)):
        img = Image.open(io.BytesIO(image_path_or_bytes))
    elif hasattr(image_path_or_bytes, 'read'):
        img = Image.open(image_path_or_bytes)
    else:
        img = Image.open(image_path_or_bytes)

    img = img.convert('RGB')
    img = img.resize(target_size, Image.LANCZOS)

    img_array = np.array(img, dtype=np.float32)

    # MobileNetV2 preprocessing: scale pixels from [0, 255] to [-1, 1]
    img_array = (img_array / 127.5) - 1.0

    # Add batch dimension
    return np.expand_dims(img_array, axis=0)
