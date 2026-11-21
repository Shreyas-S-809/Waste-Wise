"""History service — save and retrieve classification records."""

from app.database.repository import (
    create_record,
    get_record_by_id,
    get_all_records,
    delete_record,
    get_records_paginated,
)


class HistoryService:
    """Facade over the database repository for classification history."""

    @staticmethod
    def save_prediction(result_dict, image_filename, image_path):
        """Persist a prediction result to the database.

        Args:
            result_dict: dict returned by PredictionService.classify_*.
            image_filename: the saved file name on disk.
            image_path: full path to the saved image.

        Returns:
            ClassificationRecord instance.
        """
        record = create_record(
            image_filename=image_filename,
            image_path=image_path,
            classification_mode=result_dict['classification_mode'],
            predicted_category=result_dict['predicted_category'],
            confidence_score=result_dict['confidence_score'],
            model_name=result_dict['model_name'],
            model_version=result_dict.get('model_version'),
            area_name=result_dict.get('area_name'),
            ward_number=result_dict.get('ward_number'),
            district_name=result_dict.get('district_name'),
            location_source=result_dict.get('location_source'),
        )
        return record

    @staticmethod
    def get_history(page=1, per_page=20):
        """Return paginated history records."""
        pagination = get_records_paginated(page=page, per_page=per_page)
        records_list = [r.to_dict() for r in pagination.items]
        return {
            'records': records_list,
            'items': records_list,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
        }

    @staticmethod
    def get_prediction(record_id):
        """Return a single record dict or None."""
        record = get_record_by_id(record_id)
        return record.to_dict() if record else None

    @staticmethod
    def delete_prediction(record_id):
        """Delete a record. Returns True if deleted, False if not found."""
        return delete_record(record_id)
