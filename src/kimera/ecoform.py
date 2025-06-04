from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass
class GrammarNode:
    node_id: str
    label: str
    children: List['GrammarNode'] = field(default_factory=list)
    features: Dict[str, str] = field(default_factory=dict)


@dataclass
class OrthographyVector:
    script_code: str
    unicode_normal_form: str
    diacritic_profile: List[float]
    ligature_profile: List[float]
    variant_flags: Dict[str, bool] = field(default_factory=dict)


@dataclass
class EcoForm:
    ecoform_id: str
    origin_context: Dict[str, str]
    grammar_payload: GrammarNode
    grammar_vector: List[float]
    orthography_vector: OrthographyVector
    activation_strength: float
    decay_rate: float
    creation_time: datetime
    status: str = "Active"
    last_reactivation_time: Optional[datetime] = None
    evaporation_time: Optional[datetime] = None

    def age_seconds(self, now: Optional[datetime] = None) -> int:
        now = now or datetime.utcnow()
        return int((now - self.creation_time).total_seconds())


class EcoFormStore:
    def __init__(self) -> None:
        self.active: Dict[str, EcoForm] = {}
        self.archive: Dict[str, EcoForm] = {}

    def create(
        self,
        origin_context: Dict[str, str],
        grammar_payload: GrammarNode,
        grammar_vector: List[float],
        orthography_vector: OrthographyVector,
        initial_as: float,
        decay_rate: float,
    ) -> EcoForm:
        ecoform_id = str(uuid4())
        ecoform = EcoForm(
            ecoform_id=ecoform_id,
            origin_context=origin_context,
            grammar_payload=grammar_payload,
            grammar_vector=grammar_vector,
            orthography_vector=orthography_vector,
            activation_strength=initial_as,
            decay_rate=decay_rate,
            creation_time=datetime.utcnow(),
        )
        self.active[ecoform_id] = ecoform
        return ecoform

    def get_status(self, ecoform_id: str) -> Optional[EcoForm]:
        if ecoform_id in self.active:
            return self.active[ecoform_id]
        return self.archive.get(ecoform_id)

    def query(self, max_age_seconds: int, min_nss: float) -> List[EcoForm]:
        now = datetime.utcnow()
        results = []
        for ef in list(self.active.values()):
            if ef.age_seconds(now) <= max_age_seconds:
                # simplified similarity using activation strength
                nss = ef.activation_strength
                if nss >= min_nss:
                    results.append(ef)
        return results
