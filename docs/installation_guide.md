# WasteWise — Installation Guide (Windows)

## Prerequisites

Before installing WasteWise, ensure you have the following software installed on your Windows system:

| Software | Version | Download |
|----------|---------|----------|
| Python | 3.10 or 3.11 | https://www.python.org/downloads/ |
| Node.js | 18 LTS or newer | https://nodejs.org/ |
| Git | Latest | https://git-scm.com/download/win |
| Visual Studio Build Tools | 2019+ (optional) | For native Python packages |

### GPU Support (Optional)

For faster model training, install NVIDIA GPU drivers and CUDA:

1. Install the latest NVIDIA GPU driver from https://www.nvidia.com/drivers
2. Install CUDA Toolkit 11.8 from https://developer.nvidia.com/cuda-toolkit
3. Install cuDNN 8.6+ from https://developer.nvidia.com/cudnn
4. Verify GPU detection:
   ```powershell
   python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
   ```

## Step-by-Step Installation

### Step 1: Clone the Repository

Open PowerShell and navigate to your desired installation directory:

```powershell
cd D:\
git clone https://github.com/your-org/waste-wise.git "Waste Wise"
cd "Waste Wise"
```

### Step 2: Create a Python Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### Step 3: Install Python Dependencies

```powershell
# Install all project-level dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install backend-specific dependencies
pip install -r backend\requirements.txt
```

### Step 4: Configure Environment Variables

```powershell
# Copy the example environment file
Copy-Item .env.example .env

# Open in your preferred editor and update values
notepad .env
```

**Important settings to configure:**
- `SECRET_KEY`: Change this to a random string (e.g., generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URI`: Default SQLite is fine for development
- `MODEL_DIR`: Path to the models directory (default: `../models`)

### Step 5: Verify Your Environment

```powershell
python scripts\check_environment.py
```

This script checks:
- Python version compatibility
- All required packages are installed
- Dataset directories exist and contain images
- Environment variables are configured
- GPU availability (optional)

### Step 6: Inspect and Validate Datasets

```powershell
# View dataset statistics
python scripts\inspect_datasets.py

# Validate dataset integrity
python scripts\validate_dataset.py
```

### Step 7: Build Dataset Manifests

```powershell
python scripts\build_manifest.py
```

This creates CSV manifest files in `datasets/manifests/` mapping image paths to labels.

### Step 8: Train the Wet/Dry Model

```powershell
# Train with default settings
python scripts\train_wet_dry.py --epochs 20 --batch-size 32

# Monitor training progress — metrics are printed per epoch
# Best model is saved automatically to models/wet_dry/
```

Training time estimates:
- **GPU (NVIDIA RTX 3060+)**: ~15–30 minutes for 20 epochs
- **CPU only**: ~2–4 hours for 20 epochs

### Step 9: Evaluate the Model

```powershell
python scripts\evaluate_model.py --model wet_dry
python scripts\generate_confusion_matrix.py --model wet_dry
```

### Step 10: Start the Backend Server

```powershell
cd backend
python run.py
```

The Flask development server starts at `http://localhost:5000`. Test it:

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/health"
```

### Step 11: Start the Frontend (New Terminal)

```powershell
cd "D:\Waste Wise\frontend"
npm install
npm run dev
```

The React development server starts at `http://localhost:5173`.

## Troubleshooting

### Common Issues

**`pip install tensorflow` fails with compilation errors:**
- Ensure you're using Python 3.10 or 3.11 (TensorFlow may not support 3.12+ yet)
- Try: `pip install tensorflow-cpu` if you don't need GPU support

**`ModuleNotFoundError` when running scripts:**
- Ensure the virtual environment is activated: `.\venv\Scripts\Activate.ps1`
- Ensure you installed dependencies: `pip install -r requirements.txt`

**PowerShell execution policy prevents activation:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Port 5000 already in use:**
- Kill the process: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess`
- Or use a different port: `$env:FLASK_RUN_PORT=5001; python run.py`

**Images not found by training script:**
- Verify the dataset paths in `scripts/inspect_datasets.py` output
- Ensure the `Datasets` folder is in `D:\Waste Wise\Datasets\`

## Uninstallation

To remove WasteWise:

```powershell
# Deactivate virtual environment
deactivate

# Remove the project directory
Remove-Item -Recurse -Force "D:\Waste Wise"
```
