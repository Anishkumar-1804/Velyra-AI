import sys
import os
from pathlib import Path

# Add project root directory to Python path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Ensure data directories exist in serverless environment
tmp_data = Path("/tmp/data")
try:
    tmp_data.mkdir(parents=True, exist_ok=True)
    (tmp_data / "audio").mkdir(parents=True, exist_ok=True)
    (tmp_data / "audio" / "tts_cache").mkdir(parents=True, exist_ok=True)
except Exception:
    pass

from backend.app.main import app
