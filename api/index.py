"""Vercel serverless entry point for WasteWise."""
import os
import sys
import tempfile
from pathlib import Path

# Paths
API_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = API_DIR.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'

# Add backend directory to sys.path
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Set Vercel & serverless runtime environment
os.environ['VERCEL'] = '1'
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('KERAS_HOME', os.path.join(tempfile.gettempdir(), '.keras'))

from app import create_app

app = create_app('production')
