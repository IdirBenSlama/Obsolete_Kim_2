import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from kimera.server import app, vault


def test_ecoform_endpoints():
    client = TestClient(app)
    create_payload = {
        "origin_context": {"module": "test", "cycle_number": 1},
        "grammar_payload": {"node_id": "n1", "label": "S", "children": [], "features": {}},
        "grammar_vector": [0.1, 0.1, 0.1],
        "orthography_vector": {
            "script_code": "Latn",
            "unicode_normal_form": "NFC",
            "diacritic_profile": [0.0],
            "ligature_profile": [0.0],
            "variant_flags": {},
        },
        "initial_AS": 0.9,
        "decay_rate": 0.003,
    }
    resp = client.post("/ecoform/create", json=create_payload)
    assert resp.status_code == 200
    data = resp.json()
    ecoform_id = data["ecoform_id"]
    assert data["status"] == "Active"
    assert data["initial_AS"] == create_payload["initial_AS"]

    resp_status = client.get(f"/ecoform/{ecoform_id}/status")
    assert resp_status.status_code == 200
    status_data = resp_status.json()
    assert status_data["ecoform_id"] == ecoform_id
    assert status_data["status"] == "Active"

    resp_query = client.post("/ecoform/query", json={"max_age_seconds": 60, "min_NSS": 0.5})
    assert resp_query.status_code == 200
    query_data = resp_query.json()
    assert any(m["ecoform_id"] == ecoform_id for m in query_data["matches"])


def test_symbolic_insert_and_vault_routing():
    client = TestClient(app)
    vault.vault_a.scars.clear()
    vault.vault_b.scars.clear()

    payload = {
        "triples": [
            {"subject": "Fire", "predicate": "HAS_PROPERTY", "obj": "Hot"},
            {"subject": "Fire", "predicate": "HAS_PROPERTY", "obj": "Cold"},
        ]
    }
    resp = client.post("/symbolic/insert", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    scar_ids = data["scar_ids"]
    assert data["contradictions"]

    for sid in scar_ids:
        assert sid in vault.vault_a.scars
        assert sid not in vault.vault_b.scars

    resp_list = client.get("/vault/scars")
    assert resp_list.status_code == 200
    scars = [s["scar_id"] for s in resp_list.json()["scars"]]
    assert all(sid in scars for sid in scar_ids)
