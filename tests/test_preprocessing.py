"""
Unit tests for image preprocessing pipeline (MobileNetV2 scale [-1, 1] & 224x224).
"""

import io
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import pytest

# Ensure backend directory is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.ml.preprocessing import preprocess_image


def test_preprocess_image_from_bytes():
    buf = io.BytesIO()
    img = Image.new("RGB", (300, 400), color=(128, 64, 32))
    img.save(buf, format="JPEG")
    buf.seek(0)

    result = preprocess_image(buf, target_size=(224, 224))

    # Expected shape: (1, 224, 224, 3)
    assert result.shape == (1, 224, 224, 3)
    assert result.dtype == np.float32

    # MobileNetV2 scaling check: range should be within [-1.0, 1.0]
    assert np.all(result >= -1.0)
    assert np.all(result <= 1.0)


def test_preprocess_image_grayscale_converts_to_rgb():
    buf = io.BytesIO()
    img = Image.new("L", (100, 100), color=200)
    img.save(buf, format="PNG")
    buf.seek(0)

    result = preprocess_image(buf, target_size=(224, 224))
    assert result.shape == (1, 224, 224, 3)
