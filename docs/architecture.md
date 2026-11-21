# WasteWise — System Architecture

## Overview

WasteWise follows a layered architecture with clear separation between the frontend presentation layer, the backend API layer, the machine learning inference engine, and the data persistence layer. The system is designed for local deployment during development and academic evaluation, with a clear path to cloud deployment for production use.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌────────────┐ │
│  │  Upload   │  │  Prediction  │  │  History  │  │   Model    │ │
│  │  Component│  │  Results     │  │  Dashboard│  │   Status   │ │
│  └──────────┘  └──────────────┘  └──────────┘  └────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/REST (JSON)
┌──────────────────────────▼──────────────────────────────────────┐
│                     Backend (Flask API)                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   API Routes Layer                         │ │
│  │  /api/v1/health  /api/v1/predict  /api/v1/history  /model │ │
│  └───────────────────────┬────────────────────────────────────┘ │
│  ┌───────────────────────▼────────────────────────────────────┐ │
│  │                   Service Layer                            │ │
│  │  ImageService  PredictionService  HistoryService           │ │
│  └───────────┬───────────┬────────────────────┬───────────────┘ │
│              │           │                    │                  │
│  ┌───────────▼──┐  ┌─────▼──────────┐  ┌─────▼──────────────┐ │
│  │   ML Engine  │  │   Database     │  │   File Storage     │ │
│  │  ModelLoader  │  │   SQLAlchemy   │  │   uploads/         │ │
│  │  Preprocessor │  │   SQLite       │  │                    │ │
│  │  Inference    │  │   Repository   │  │                    │ │
│  │  LabelMapping │  │                │  │                    │ │
│  └──────────────┘  └────────────────┘  └────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend — React Application

The frontend is a single-page application built with React and Vite. It communicates with the backend exclusively through the REST API. Key components include:

- **ImageUpload**: Drag-and-drop or file picker for uploading waste images. Validates file type (JPEG, PNG, WebP) and size before upload.
- **PredictionResult**: Displays the classification result (Wet/Dry) with a confidence score visualized as a progress bar or gauge.
- **HistoryDashboard**: Tabular view of past predictions with filtering and sorting. Each row shows the uploaded image thumbnail, prediction, confidence, and timestamp.
- **ModelStatus**: Shows the currently loaded model's accuracy metrics, training date, and dataset summary.

### Backend — Flask REST API

The backend is structured as a Flask application using the application factory pattern. It is organized into several sub-packages:

- **`app/api/routes/`**: Blueprint-based route definitions. Each resource (health, prediction, history, model_status) has its own module.
- **`app/services/`**: Business logic layer. The `PredictionService` orchestrates image validation, preprocessing, model inference, and result persistence.
- **`app/ml/`**: Machine learning module encapsulating model loading, image preprocessing, inference, label mapping, and confidence calibration.
- **`app/database/`**: SQLAlchemy models and repository pattern for data access.
- **`app/utils/`**: Shared utilities for input validation, file handling, and standardized API response formatting.

### ML Engine

The ML engine loads trained Keras models at application startup and holds them in memory for fast inference. It consists of:

- **ModelLoader**: Loads `.keras` model files, caches them, and provides health-check capabilities.
- **Preprocessing**: Resizes input images to 224×224, normalizes pixel values, and applies any required format transformations.
- **Inference**: Runs the preprocessed image tensor through the model and returns raw prediction probabilities.
- **LabelMapping**: Maps model output indices to human-readable labels (e.g., index 0 → "wet", index 1 → "dry").
- **Confidence**: Applies softmax calibration and formats confidence scores for API response.

### Database — SQLite via SQLAlchemy

The database stores prediction history records. The primary table is `predictions` with columns for the image filename, predicted class, confidence score, model used, and timestamp. SQLAlchemy's ORM provides a clean abstraction, and the repository pattern keeps database queries isolated from business logic.

### File Storage

Uploaded images are saved to the `backend/uploads/` directory. Each file is renamed with a UUID to prevent collisions. The database stores the filename reference, allowing the history endpoint to serve image thumbnails if needed.

## Data Flow — Prediction Request

1. User uploads an image via the React frontend.
2. Frontend sends a `POST /api/v1/predict` request with the image as `multipart/form-data`.
3. The `prediction` route handler receives the request and passes it to `PredictionService`.
4. `ImageService` validates the file type and size, saves it to `uploads/`, and returns the file path.
5. `Preprocessing` loads and transforms the image into a model-ready tensor.
6. `Inference` runs the tensor through the loaded model.
7. `LabelMapping` and `Confidence` transform the raw output into a labeled, calibrated result.
8. `HistoryService` persists the prediction record to the database.
9. The API returns a JSON response with the prediction, confidence, and metadata.

## Deployment Considerations

For local development, the Flask development server is sufficient. For production:
- Use Gunicorn (Linux) or Waitress (Windows) as the WSGI server.
- Serve the React build through Nginx or as Flask static files.
- Consider PostgreSQL for the database in production.
- Model files should be versioned and stored in a model registry or cloud storage.
