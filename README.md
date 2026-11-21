# WasteWise — AI-Powered Waste Classification System

WasteWise is an intelligent municipal solid waste classification platform designed to automate waste segregation monitoring using Convolutional Neural Networks and Transfer Learning (MobileNetV2).

The system disentangles waste categorization across two separate visual dimensions:
1. **Model A — Individual Waste Item Classifier**: Identifies whether a single object is **Wet** (organic, compostable) or **Dry** (recyclable).
2. **Model B — Segregation Status Auditor**: Evaluates collection scenes and dual-bin receptacles for compliance (**Mixed Waste** vs. **Properly Segregated**).

---

## Key Features

- **Single-Command Startup**: Launch both backend (Flask) and frontend (Vite) concurrently with `python app.py`.
- **Strict Dark Theme Workspace**: Vercel & ChatGPT Desktop inspired minimal UI (`100vw × 100vh` non-scrollable viewport).
- **Calibrated Confidence Scoring**: Margin checks and visual entropy filters detect low-confidence or ambiguous images and return an honest `Uncertain` status instead of arbitrary guesses.
- **Out-of-Distribution Protection**: Rejects blank canvases or featureless images before inference.
- **Actionable Disposal Guidance**: Context-specific municipal bin instructions for Wet, Dry, and Mixed streams.
- **Audit History**: SQLite-backed persistent audit trail with real-time logging and deletion capabilities.
- **Model Diagnostics**: Interactive performance metrics, confusion matrix heatmap, and dataset breakdown.

---

## Verified Model Performance

Evaluated against an independent, unseen test split from **TechSash** and **RealWaste** datasets (29,016 verified images):

| Metric | Result |
|--------|--------|
| **Accuracy on Decisive Calls** | **90.22%** |
| **Overall Test Accuracy** | **88.00%** |
| **Dry Waste Precision** | **92.00%** |
| **Dry Waste Recall** | **83.00%** (F1: 0.87) |
| **Wet Waste Precision** | **85.00%** |
| **Wet Waste Recall** | **93.00%** (F1: 0.89) |
| **Macro F1-Score** | **0.88** |

*Verification report: `models/evaluation/prediction_verification_report.csv`*

---

## Quick Start

### 1. Prerequisites
- **Python 3.10+ / 3.11**
- **Node.js 18+** and **npm**

### 2. Single-Command Launch (Recommended)

From the project root directory, run:

```bash
python app.py
```

This single command:
1. Validates environment and port availability.
2. Starts the Flask backend on `http://127.0.0.1:5000`.
3. Starts the Vite frontend on `http://localhost:5173`.
4. Automatically opens the application in your default web browser.
5. Manages graceful shutdown on `Ctrl+C` without orphan background processes.

---

## Manual Service Execution

If you prefer running services independently in separate terminal windows:

### Backend API (Terminal 1)
```powershell
python backend/run.py
# API starts at http://127.0.0.1:5000
```

### Frontend UI (Terminal 2)
```powershell
cd frontend
npm run dev
# Frontend starts at http://localhost:5173
```

---

## Dataset Ingestion & Category Mapping

WasteWise uses only verified samples from two core datasets:
- **TechSash Waste Classification**:
  - `Organic` (`O`) &rarr; **Wet Waste**
  - `Recyclable` (`R`) &rarr; **Dry Waste**
- **RealWaste**:
  - `Cardboard`, `Glass`, `Metal`, `Paper`, `Plastic` &rarr; **Dry Waste**
  - `Food Organics`, `Vegetation` &rarr; **Wet Waste**
  - *Ambiguous categories (`Textile Trash`, `Miscellaneous Trash`) are strictly excluded to avoid synthetic label bias.*

---

## REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Service health status and timestamp |
| `GET` | `/api/v1/models/status` | Loaded model details and training status |
| `POST` | `/api/v1/predict/item` | Classify individual waste item (`Wet` / `Dry` / `Uncertain`) |
| `POST` | `/api/v1/predict/segregation` | Classify bin scene (`Mixed` / `Properly Segregated`) |
| `GET` | `/api/v1/history` | Paginated classification audit history |
| `DELETE` | `/api/v1/history/<id>` | Delete an individual audit record |

---

## Test Suite Execution

Run the complete test suite (26 passing tests):

```powershell
python -m pytest backend/tests/ tests/ -v
```

---

## Project Structure

```
Waste Wise/
├── app.py                # Unified launcher for Flask and Vite
├── backend/              # Flask REST API
│   ├── app/
│   │   ├── api/routes/   # REST routes (predict, history, health, models)
│   │   ├── ml/           # Model loading, inference, preprocessing, confidence
│   │   ├── database/     # SQLite database and repository models
│   │   └── services/     # Prediction and history services
│   └── run.py            # Backend entry-point
├── frontend/             # React 18 + Vite Web Application
│   ├── src/
│   │   ├── components/   # Workspace panels, layout, sidebar, header
│   │   ├── pages/        # Classifier, History, ModelInfo, About, Home
│   │   └── styles/       # Strict dark theme CSS design system
│   └── vite.config.js    # Vite configuration & API proxy
├── models/
│   ├── wet_dry/          # Trained MobileNetV2 model (.keras)
│   ├── evaluation/       # Verification report, confusion matrix, JSON reports
│   └── metadata/         # Model metadata specifications
├── datasets/             # Data manifests (train, validation, test CSVs)
├── scripts/              # Training, evaluation, and verification CLI utilities
└── tests/                # Automated integration & validation tests
```
