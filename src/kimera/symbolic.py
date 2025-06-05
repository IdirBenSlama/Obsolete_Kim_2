from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


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
                contradictions.append(f"{t.subject} conflicting property {t.obj}")
            props[t.subject].add(t.obj)
        elif t.predicate == "CONTRADICTS":
            contradictions.append(f"{t.subject} contradicts {t.obj}")
    return contradictions

