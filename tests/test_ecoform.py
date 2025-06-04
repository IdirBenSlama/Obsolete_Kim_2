import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kimera.ecoform import EcoFormStore, GrammarNode, OrthographyVector


def test_create_and_query():
    store = EcoFormStore()
    grammar = GrammarNode(node_id="n1", label="S")
    ortho = OrthographyVector(
        script_code="Latn",
        unicode_normal_form="NFC",
        diacritic_profile=[0.0]*32,
        ligature_profile=[0.0]*32,
    )
    eco = store.create(
        origin_context={"module": "test", "cycle_number": 1, "source_language": "en"},
        grammar_payload=grammar,
        grammar_vector=[0.1]*128,
        orthography_vector=ortho,
        initial_as=0.9,
        decay_rate=0.003,
    )
    matches = store.query(max_age_seconds=60, min_nss=0.5)
    assert matches and matches[0].ecoform_id == eco.ecoform_id
