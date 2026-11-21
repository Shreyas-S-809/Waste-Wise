"""Image validation and storage service."""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_MIME_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
}

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}


def _allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_and_save_image(file):
    """Validate the uploaded file and save it to the uploads directory.

    Args:
        file: werkzeug FileStorage object.

    Returns:
        tuple (saved_path, filename) on success.

    Raises:
        ValueError with a human‑readable message on validation failure.
    """
    if file is None or file.filename == '':
        raise ValueError('No file provided.')

    # MIME type check
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(
            f'Invalid file type "{file.content_type}". '
            f'Allowed types: {", ".join(sorted(ALLOWED_MIME_TYPES))}.'
        )

    # Extension check
    if not _allowed_extension(file.filename):
        raise ValueError(
            f'Invalid file extension. '
            f'Allowed extensions: {", ".join(sorted(ALLOWED_EXTENSIONS))}.'
        )

    # Generate a unique secure filename
    original = secure_filename(file.filename)
    ext = original.rsplit('.', 1)[1].lower() if '.' in original else 'png'
    unique_name = f'{uuid.uuid4().hex}.{ext}'

    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)

    saved_path = os.path.join(upload_dir, unique_name)
    file.save(saved_path)

    return saved_path, unique_name
