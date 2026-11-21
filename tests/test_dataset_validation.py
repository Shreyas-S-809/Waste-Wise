"""
Unit tests for image validation and corrupt file filtering logic.
"""

import io
from PIL import Image
import pytest


def validate_test_image(img_bytes, min_size=(32, 32)):
    """Validation helper replicating script validation."""
    try:
        with Image.open(io.BytesIO(img_bytes)) as img:
            img.verify()
        with Image.open(io.BytesIO(img_bytes)) as img:
            w, h = img.size
            if w < min_size[0] or h < min_size[1]:
                return False, f"Image dimensions too small: ({w}, {h})"
        return True, "Valid"
    except Exception as e:
        return False, f"Corrupt image: {e}"


def test_valid_image_passes_validation():
    # Create a synthetic 100x100 RGB image
    buf = io.BytesIO()
    img = Image.new("RGB", (100, 100), color="green")
    img.save(buf, format="JPEG")
    valid, msg = validate_test_image(buf.getvalue())
    assert valid is True
    assert msg == "Valid"


def test_too_small_image_rejected():
    buf = io.BytesIO()
    img = Image.new("RGB", (16, 16), color="red")
    img.save(buf, format="JPEG")
    valid, msg = validate_test_image(buf.getvalue(), min_size=(32, 32))
    assert valid is False
    assert "too small" in msg


def test_corrupt_bytes_rejected():
    corrupt_bytes = b"This is not a real JPEG file content!"
    valid, msg = validate_test_image(corrupt_bytes)
    assert valid is False
    assert "Corrupt image" in msg

