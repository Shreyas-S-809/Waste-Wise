"""WSGI entry point for WasteWise backend service."""
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ['VERCEL'] = '1'
os.environ.setdefault('FLASK_ENV', 'production')

from app import create_app

app = create_app('production')
