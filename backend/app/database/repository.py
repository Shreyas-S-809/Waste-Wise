"""CRUD operations for ClassificationRecord."""

from app.extensions import db
from app.database.models import ClassificationRecord


def create_record(**kwargs):
    """Create and persist a new ClassificationRecord."""
    record = ClassificationRecord(**kwargs)
    db.session.add(record)
    db.session.commit()
    return record


def get_record_by_id(record_id):
    """Return a single record by primary key, or None."""
    return db.session.get(ClassificationRecord, record_id)


def get_all_records():
    """Return every record ordered by most recent first."""
    return (
        ClassificationRecord.query
        .order_by(ClassificationRecord.created_at.desc())
        .all()
    )


def delete_record(record_id):
    """Delete a record by id. Returns True if deleted, False if not found."""
    record = db.session.get(ClassificationRecord, record_id)
    if record is None:
        return False
    db.session.delete(record)
    db.session.commit()
    return True


def get_records_paginated(page=1, per_page=20):
    """Return a paginated query result (Flask‑SQLAlchemy pagination object)."""
    return (
        ClassificationRecord.query
        .order_by(ClassificationRecord.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
