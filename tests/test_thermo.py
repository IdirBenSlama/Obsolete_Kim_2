from datetime import datetime, timedelta

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kimera.thermo import EnergyUnit, ThermoRegistry, decay_all


def test_decay_all():
    registry = ThermoRegistry()
    unit = EnergyUnit(
        unit_id="u1",
        unit_type="EcoForm",
        SE_current=1.0,
        decay_rate=0.1,
        C_max=1.0,
        last_update_time=datetime.utcnow() - timedelta(seconds=10),
    )
    registry.register(unit)
    now = datetime.utcnow()
    decay_all(registry, now)
    assert unit.SE_current < 1.0
