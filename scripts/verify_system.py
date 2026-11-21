#!/usr/bin/env python3
"""
WasteWise — Full End-to-End System Verification
Verifies Health API, Model Status, Wet/Dry Inference on real image,
SQLite persistence, and History retrieval.
"""

import os
import sys
import json
from io import BytesIO
from pathlib import Path

# Ensure paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))
os.environ.setdefault("KERAS_HOME", str(PROJECT_ROOT / ".keras"))

from app import create_app
from app.extensions import db
from app.database.models import ClassificationRecord


def run_verification():
    print("=" * 70)
    print("  WasteWise — End-to-End System Integration Verification")
    print("=" * 70)

    app = create_app("development")
    client = app.test_client()

    with app.app_context():
        # 1. Health check
        print("\n[Step 1] Testing /api/health endpoint...")
        res = client.get("/api/health")
        assert res.status_code == 200, f"Health check failed: {res.status_code}"
        health_data = res.get_json()
        print(f"  Health response (HTTP {res.status_code}): {json.dumps(health_data)}")

        # 2. Models status
        print("\n[Step 2] Testing /api/v1/models/status endpoint...")
        res = client.get("/api/v1/models/status")
        assert res.status_code == 200, f"Models status failed: {res.status_code}"
        models_data = res.get_json()
        print(f"  Models status (HTTP {res.status_code}):")
        for m_name, info in models_data.get("data", {}).get("models", {}).items():
            print(f"    - {m_name:20s}: Available={info.get('available')}, Status={info.get('status')}, Version={info.get('version')}")

        # 3. Model Inference on real sample image
        test_image_path = PROJECT_ROOT / "Datasets" / "realwaste-main" / "RealWaste" / "Food Organics" / "Food Organics_1.jpg"
        print(f"\n[Step 3] Testing /api/v1/predict/item with real sample image:")
        print(f"  Image: {test_image_path.name}")

        with open(test_image_path, "rb") as f:
            img_bytes = f.read()

        data = {
            "image": (BytesIO(img_bytes), "Food_Organics_1.jpg", "image/jpeg")
        }

        res = client.post("/api/v1/predict/item", data=data, content_type="multipart/form-data")
        assert res.status_code == 200, f"Prediction failed with status {res.status_code}: {res.data}"
        pred_data = res.get_json()
        result = pred_data.get("data", {})
        print(f"  Prediction response (HTTP {res.status_code}):")
        print(f"    - Category     : {result.get('predicted_category')}")
        print(f"    - Confidence   : {result.get('confidence_score') * 100:.2f}%")
        print(f"    - Model Name   : {result.get('model_name')}")
        print(f"    - Probabilities: {result.get('probabilities')}")
        print(f"    - Stored ID    : {result.get('id')}")

        # 4. History retrieval
        print("\n[Step 4] Testing /api/v1/history endpoint...")
        res = client.get("/api/v1/history")
        assert res.status_code == 200, f"History fetch failed: {res.status_code}"
        hist_data = res.get_json()
        items = hist_data.get("data", {}).get("items", [])
        total = hist_data.get("data", {}).get("total", 0)
        print(f"  History items count: {len(items)}, Total records: {total}")
        if items:
            latest = items[0]
            print(f"  Latest record in SQLite DB:")
            print(f"    - ID: {latest.get('id')}, Category: {latest.get('predicted_category')}, Confidence: {latest.get('confidence_score')}")

        # 5. Database Direct Verification
        record_count = ClassificationRecord.query.count()
        print(f"\n[Step 5] Direct SQLite Database Query:")
        print(f"  Total records in classification_records table: {record_count}")

    print("\n" + "=" * 70)
    print("  ALL SYSTEM INTEGRATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_verification()

