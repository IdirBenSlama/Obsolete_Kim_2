from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from .vault import DualVault, Scar


@dataclass
class Triple:
    subject: str
    predicate: str
    obj: str


def detect_contradictions(triples: List[Triple]) -> List[str]:
    props: Dict[str, set[str]] = {}
    contradictions: List[str] = []
    for t in triples:
        if t.predicate == "HAS_PROPERTY":
            props.setdefault(t.subject, set())
            if t.obj not in props[t.subject] and props[t.subject]:
                msg = f"{t.subject} conflicting property {t.obj}"
                contradictions.append(msg)
            props[t.subject].add(t.obj)
        elif t.predicate == "CONTRADICTS":
            contradictions.append(f"{t.subject} contradicts {t.obj}")
    return contradictions


@dataclass
class KnowledgeBase:
    triples: List[Triple] = field(default_factory=list)

    def add_triples(
        self,
        new_triples: List[Triple],
        vault: Optional[DualVault] = None,
    ) -> List[str]:
        self.triples.extend(new_triples)
        contradictions = detect_contradictions(self.triples)
        if vault is not None:
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
        return contradictions
