from __future__ import annotations

from datetime import datetime
from uuid import uuid4
from typing import Any, Dict, List
from copy import deepcopy

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
 cjwkpv-codex/update-model-fields-with-default_factory

 67qxt6-codex/update-model-fields-with-default_factory
 main

try:  # support both Pydantic v1 and v2
    from pydantic import ConfigDict, field_validator
    _PYDANTIC_V2 = True
except ImportError:  # pragma: no cover - running on Pydantic v1
    from pydantic import validator as field_validator  # type: ignore
    ConfigDict = None  # type: ignore
    _PYDANTIC_V2 = False
 cjwkpv-codex/update-model-fields-with-default_factory


 main
 main

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
 cjwkpv-codex/update-model-fields-with-default_factory

 67qxt6-codex/update-model-fields-with-default_factory
 main

    if _PYDANTIC_V2:
        model_config = ConfigDict(arbitrary_types_allowed=True)
    else:  # pragma: no cover - Pydantic v1
        class Config:
            arbitrary_types_allowed = True

 cjwkpv-codex/update-model-fields-with-default_factory
    @field_validator('features', **({'mode': 'after'} if _PYDANTIC_V2 else {'always': True}))
    @classmethod
    def copy_features(cls, v: Dict[str, Any] | None) -> Dict[str, Any]:
        return deepcopy(v or {})

 main

    @field_validator('features', **({'mode': 'before'} if _PYDANTIC_V2 else {'pre': True}))
    @classmethod
    def copy_features(cls, v: Dict[str, Any] | None) -> Dict[str, Any]:
        return deepcopy(v) if v is not None else {}
 main


class OrthographyVectorModel(BaseModel):
    script_code: str
    unicode_normal_form: str
    diacritic_profile: List[float]
    ligature_profile: List[float]
    variant_flags: Dict[str, bool] = Field(default_factory=dict)
 cjwkpv-codex/update-model-fields-with-default_factory

    @field_validator('variant_flags', **({'mode': 'after'} if _PYDANTIC_V2 else {'always': True}))
    @classmethod
    def copy_variant_flags(cls, v: Dict[str, bool] | None) -> Dict[str, bool]:
        return deepcopy(v or {})


# ensure forward refs resolve for self-referential children
if _PYDANTIC_V2:
    GrammarNodeModel.model_rebuild()
else:  # pragma: no cover - Pydantic v1
    GrammarNodeModel.update_forward_refs()

 67qxt6-codex/update-model-fields-with-default_factory

    @field_validator('variant_flags', **({'mode': 'before'} if _PYDANTIC_V2 else {'pre': True}))
    @classmethod
    def copy_variant_flags(cls, v: Dict[str, bool] | None) -> Dict[str, bool]:
        return deepcopy(v) if v is not None else {}

 main
 main


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

