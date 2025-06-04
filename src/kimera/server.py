from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .ecoform import EcoFormStore, GrammarNode, OrthographyVector

app = FastAPI(title="Kimera EcoForm API")
store = EcoFormStore()


class GrammarNodeModel(BaseModel):
    node_id: str
    label: str
    children: List['GrammarNodeModel'] = []
    features: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True


class OrthographyVectorModel(BaseModel):
    script_code: str
    unicode_normal_form: str
    diacritic_profile: List[float]
    ligature_profile: List[float]
    variant_flags: Dict[str, bool] = {}


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

