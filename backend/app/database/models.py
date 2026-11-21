"""Database models."""

from datetime import datetime, timezone

from app.extensions import db


class ClassificationRecord(db.Model):
    """Stores a single waste‑classification prediction."""

    __tablename__ = 'classification_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_filename = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(512), nullable=False)
    classification_mode = db.Column(db.String(50), nullable=False)  # 'item' or 'segregation'
    predicted_category = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    model_version = db.Column(db.String(50), nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Optional location fields
    area_name = db.Column(db.String(200), nullable=True)
    ward_number = db.Column(db.String(50), nullable=True)
    district_name = db.Column(db.String(200), nullable=True)
    location_source = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        """Serialise the record to a JSON‑friendly dict."""
        return {
            'id': self.id,
            'image_filename': self.image_filename,
            'image_path': self.image_path,
            'classification_mode': self.classification_mode,
            'predicted_category': self.predicted_category,
            'confidence_score': self.confidence_score,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'area_name': self.area_name,
            'ward_number': self.ward_number,
            'district_name': self.district_name,
            'location_source': self.location_source,
        }

    def __repr__(self):
        return f'<ClassificationRecord {self.id}: {self.predicted_category} ({self.confidence_score:.2f})>'
