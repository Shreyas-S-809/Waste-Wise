"""Tests for database model and basic queries."""

from datetime import datetime, timezone

from app.database.models import ClassificationRecord
from app.extensions import db as _db


def test_create_classification_record(db, app):
    """Create a record and verify it persists."""
    with app.app_context():
        rec = ClassificationRecord(
            image_filename='sample.jpg',
            image_path='/uploads/sample.jpg',
            classification_mode='item',
            predicted_category='Wet',
            confidence_score=0.87,
            model_name='wet_dry_mobilenetv2.keras',
            model_version='1.0.0',
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(rec)
        db.session.commit()

        fetched = db.session.get(ClassificationRecord, rec.id)
        assert fetched is not None
        assert fetched.predicted_category == 'Wet'
        assert fetched.confidence_score == 0.87


def test_record_to_dict(db, app):
    """to_dict() should include all expected keys."""
    with app.app_context():
        rec = ClassificationRecord(
            image_filename='a.png',
            image_path='/uploads/a.png',
            classification_mode='segregation',
            predicted_category='Mixed Waste',
            confidence_score=0.65,
            model_name='segregation_status_mobilenetv2.keras',
        )
        db.session.add(rec)
        db.session.commit()

        d = rec.to_dict()
        for key in (
            'id', 'image_filename', 'image_path', 'classification_mode',
            'predicted_category', 'confidence_score', 'model_name',
            'model_version', 'created_at',
        ):
            assert key in d


def test_query_by_mode(db, app):
    """Filter records by classification_mode."""
    with app.app_context():
        for mode in ('item', 'segregation', 'item'):
            db.session.add(ClassificationRecord(
                image_filename='x.jpg',
                image_path='/uploads/x.jpg',
                classification_mode=mode,
                predicted_category='Dry',
                confidence_score=0.9,
                model_name='test',
            ))
        db.session.commit()

        items = ClassificationRecord.query.filter_by(classification_mode='item').all()
        assert len(items) == 2

        segs = ClassificationRecord.query.filter_by(classification_mode='segregation').all()
        assert len(segs) == 1
