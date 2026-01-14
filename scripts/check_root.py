import sys
import traceback
from pathlib import Path

from fastapi.testclient import TestClient

# Ensure repo root is on sys.path so `src` imports work
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

try:
    from src import create_app

    app = create_app()
    client = TestClient(app)
    resp = client.get("/")
    print("STATUS:", resp.status_code)
    print(resp.text)
except Exception:
    print("EXCEPTION TRACEBACK:")
    traceback.print_exc()
