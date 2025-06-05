import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from kimera.server import app


def test_symbolic_insert_and_vault_listing():
    client = TestClient(app)
    payload = {
        "triples": [
            {"subject": "Fire", "predicate": "HAS_PROPERTY", "obj": "Hot"},
            {"subject": "Fire", "predicate": "HAS_PROPERTY", "obj": "Cold"},
        ]
    }
    resp = client.post("/symbolic/insert", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["contradictions"]
    scars = client.get("/vault/scars").json()["scars"]
    assert any(s["scar_id"] in data["scar_ids"] for s in scars)
