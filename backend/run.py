"""WasteWise Flask backend entry‑point."""

import os
import sys
from pathlib import Path

# Ensure backend root is in sys.path and KERAS_HOME points to project .keras cache
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('KERAS_HOME', str(PROJECT_ROOT / '.keras'))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    print(f"Starting WasteWise Flask server on http://127.0.0.1:{port}...")
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
