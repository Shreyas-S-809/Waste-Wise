# WasteWise — REST API Documentation

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

No authentication is required for the current version (local development). Future versions may implement API key or JWT-based authentication.

## Common Headers

```
Content-Type: application/json        (for JSON requests)
Content-Type: multipart/form-data     (for file uploads)
Accept: application/json
```

## Standard Response Format

All API responses follow a consistent structure:

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "File type not supported. Allowed: jpg, jpeg, png, webp"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Endpoints

### 1. Health Check

**`GET /api/v1/health`**

Returns the health status of the API and its dependencies.

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "models": {
      "wet_dry": {
        "loaded": true,
        "accuracy": 0.92
      },
      "segregation_status": {
        "loaded": false,
        "accuracy": null
      }
    },
    "database": "connected",
    "uptime_seconds": 3600
  }
}
```

---

### 2. Predict Waste Type

**`POST /api/v1/predict`**

Upload a waste image and receive a wet/dry classification prediction.

#### Request

- **Content-Type**: `multipart/form-data`
- **Body**:
  | Field | Type | Required | Description |
  |-------|------|----------|-------------|
  | `image` | File | Yes | Image file (JPEG, PNG, or WebP) |
  | `model` | String | No | Model to use: `wet_dry` (default) or `segregation_status` |

#### Example (PowerShell)

```powershell
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/predict" `
    -Method Post `
    -Form @{ image = Get-Item ".\test_image.jpg" }
$response | ConvertTo-Json
```

#### Example (curl)

```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -F "image=@test_image.jpg" \
  -F "model=wet_dry"
```

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "prediction": {
      "class": "wet",
      "confidence": 0.934,
      "probabilities": {
        "wet": 0.934,
        "dry": 0.066
      }
    },
    "model_used": "wet_dry",
    "image_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "processing_time_ms": 45
  }
}
```

#### Error Responses

| Status | Code | Description |
|--------|------|-------------|
| 400 | `NO_IMAGE` | No image file provided |
| 400 | `INVALID_FILE_TYPE` | File is not a supported image format |
| 400 | `FILE_TOO_LARGE` | File exceeds maximum upload size |
| 400 | `INVALID_IMAGE` | File is corrupted or not a valid image |
| 503 | `MODEL_NOT_LOADED` | The requested model is not available |

---

### 3. Prediction History

**`GET /api/v1/history`**

Retrieve past prediction records.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | Integer | 1 | Page number for pagination |
| `per_page` | Integer | 20 | Number of records per page (max 100) |
| `model` | String | — | Filter by model name |
| `prediction` | String | — | Filter by predicted class |
| `sort` | String | `desc` | Sort order by timestamp: `asc` or `desc` |

#### Example

```
GET /api/v1/history?page=1&per_page=10&model=wet_dry&sort=desc
```

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "records": [
      {
        "id": 42,
        "image_filename": "a1b2c3d4.jpg",
        "prediction": "wet",
        "confidence": 0.934,
        "model_used": "wet_dry",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total_records": 156,
      "total_pages": 16
    }
  }
}
```

---

### 4. Model Status

**`GET /api/v1/model/status`**

Returns detailed status information about all available models.

#### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "models": [
      {
        "name": "wet_dry_classifier",
        "architecture": "MobileNetV2",
        "status": "loaded",
        "num_classes": 2,
        "class_labels": ["wet", "dry"],
        "training_accuracy": 0.95,
        "test_accuracy": 0.92,
        "last_trained": "2024-01-10T08:00:00Z",
        "total_predictions": 1234
      },
      {
        "name": "segregation_status_classifier",
        "architecture": "MobileNetV2",
        "status": "not_trained",
        "num_classes": 2,
        "class_labels": ["mixed_waste", "properly_segregated"],
        "training_accuracy": null,
        "test_accuracy": null,
        "last_trained": null,
        "total_predictions": 0
      }
    ]
  }
}
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `NO_IMAGE` | 400 | No image file in request |
| `INVALID_FILE_TYPE` | 400 | Unsupported file format |
| `FILE_TOO_LARGE` | 400 | File exceeds size limit |
| `INVALID_IMAGE` | 400 | Corrupted or invalid image data |
| `MODEL_NOT_LOADED` | 503 | Requested model not available |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `NOT_FOUND` | 404 | Requested resource not found |

## Rate Limits

No rate limits are enforced in the development version. Production deployments should implement rate limiting (recommended: 60 requests/minute per client).
