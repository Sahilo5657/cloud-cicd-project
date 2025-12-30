import sys
from pathlib import Path

# Ensure repo root is on Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app  # noqa: E402

def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
