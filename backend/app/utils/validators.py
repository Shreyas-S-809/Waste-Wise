"""Request validation helpers."""

ALLOWED_MIME_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
}

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

VALID_CLASSIFICATION_MODES = {'item', 'segregation'}


def validate_image_file(file):
    """Validate an uploaded image file.

    Returns:
        (True, None) if valid, (False, error_message) otherwise.
    """
    if file is None or file.filename == '':
        return False, 'No image file provided.'

    if file.content_type not in ALLOWED_MIME_TYPES:
        return False, (
            f'Invalid file type "{file.content_type}". '
            f'Allowed: {", ".join(sorted(ALLOWED_MIME_TYPES))}.'
        )

    ext = ''
    if '.' in file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return False, (
            f'Invalid file extension ".{ext}". '
            f'Allowed: {", ".join(sorted(ALLOWED_EXTENSIONS))}.'
        )

    return True, None


def validate_classification_mode(mode):
    """Validate a classification mode string.

    Returns:
        (True, None) if valid, (False, error_message) otherwise.
    """
    if mode not in VALID_CLASSIFICATION_MODES:
        return False, (
            f'Invalid classification mode "{mode}". '
            f'Allowed: {", ".join(sorted(VALID_CLASSIFICATION_MODES))}.'
        )
    return True, None
