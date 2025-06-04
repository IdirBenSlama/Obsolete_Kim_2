import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kimera.symbolic import KnowledgeBase, Triple
from kimera.vault import DualVault


def test_contradiction_creates_scar():
    kb = KnowledgeBase()
    vault = DualVault()
    triples = [
        Triple(subject="Fire", predicate="HAS_PROPERTY", obj="Hot"),
        Triple(subject="Fire", predicate="HAS_PROPERTY", obj="Cold"),
    ]
    contradictions = kb.add_triples(triples, vault)
    assert contradictions
    assert vault.vault_a.scars or vault.vault_b.scars
