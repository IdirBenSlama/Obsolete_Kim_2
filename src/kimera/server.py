from __future__ import annotations

from datetime import datetime
from uuid import uuid4
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .ecoform import EcoFormStore, GrammarNode, OrthographyVector
from .symbolic import Triple, detect_contradictions
from .vault import DualVault, Scar

app = FastAPI(title="Kimera EcoForm API")
store = EcoFormStore()
vault = DualVault()


class GrammarNodeModel(BaseModel):
    node_id: str
    label: str
    children: List['GrammarNodeModel'] = Field(default_factory=list)
    features: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class OrthographyVectorModel(BaseModel):
    script_code: str
    unicode_normal_form: str
    diacritic_profile: List[float]
    ligature_profile: List[float]
    variant_flags: Dict[str, bool] = Field(default_factory=dict)


class CreateEcoFormRequest(BaseModel):
    origin_context: Dict[str, Any]
    grammar_payload: GrammarNodeModel
    grammar_vector: List[float]
    orthography_vector: OrthographyVectorModel
    initial_AS: float
    decay_rate: float = 0.003


class QueryRequest(BaseModel):
    max_age_seconds: int
    min_NSS: float = 0.7


class TripleModel(BaseModel):
    subject: str
    predicate: str
    obj: str


class InsertTriplesRequest(BaseModel):
    triples: List[TripleModel]


@app.post("/ecoform/create")
def create_ecoform(req: CreateEcoFormRequest):
    grammar_node = GrammarNode(
        node_id=req.grammar_payload.node_id,
        label=req.grammar_payload.label,
        children=[GrammarNode(**child.dict()) for child in req.grammar_payload.children],
        features=req.grammar_payload.features,
    )
    orth_vec = OrthographyVector(**req.orthography_vector.dict())
    eco = store.create(
        origin_context=req.origin_context,
        grammar_payload=grammar_node,
        grammar_vector=req.grammar_vector,
        orthography_vector=orth_vec,
        initial_as=req.initial_AS,
        decay_rate=req.decay_rate,
    )
    return {
        "ecoform_id": eco.ecoform_id,
        "status": eco.status,
        "initial_AS": eco.activation_strength,
    }


@app.get("/ecoform/{ecoform_id}/status")
def get_status(ecoform_id: str):
    eco = store.get_status(ecoform_id)
    if not eco:
        raise HTTPException(status_code=404, detail="Not Found")
    return {
        "ecoform_id": eco.ecoform_id,
        "status": eco.status,
        "AS_current": eco.activation_strength,
        "age_seconds": eco.age_seconds(),
        "creation_time": eco.creation_time.isoformat(),
    }


@app.post("/ecoform/query")
def query(req: QueryRequest):
    matches = store.query(req.max_age_seconds, req.min_NSS)
    return {
        "matches": [
            {"ecoform_id": m.ecoform_id, "AS_current": m.activation_strength, "NSS": m.activation_strength}
            for m in matches
        ]
    }


@app.post("/symbolic/insert")
def symbolic_insert(req: InsertTriplesRequest):
    triples = [Triple(**t.dict()) for t in req.triples]
    contradictions = detect_contradictions(triples)
    scar_ids: List[str] = []
    for c in contradictions:
        scar = Scar(
            scar_id=str(uuid4()),
            contradiction=c,
            entropy=0.0,
            cls_angle=0.0,
            semantic_polarity=0.0,
            mutation_frequency=0.0,
            origin_time=datetime.utcnow(),
        )
        vault.add_scar(scar)
        scar_ids.append(scar.scar_id)
    return {"inserted": len(triples), "contradictions": contradictions, "scar_ids": scar_ids}


@app.get("/vault/scars")
def list_scars():
    scars = vault.list_scars()
    return {
        "scars": [
            {
                "scar_id": s.scar_id,
                "contradiction": s.contradiction,
                "origin_time": s.origin_time.isoformat(),
            }
            for s in scars.values()
        ]
    }

