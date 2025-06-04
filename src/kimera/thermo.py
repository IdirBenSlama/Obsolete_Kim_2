from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from math import exp
from typing import Dict


@dataclass
class EnergyUnit:
    unit_id: str
    unit_type: str
    SE_current: float
    decay_rate: float
    C_max: float
    last_update_time: datetime
    metadata: Dict[str, float] = field(default_factory=dict)
    entropy_accumulated: float = 0.0
    status: str = "Active"


class ThermoRegistry:
    def __init__(self) -> None:
        self.registry: Dict[str, EnergyUnit] = {}

    def register(self, unit: EnergyUnit) -> None:
        self.registry[unit.unit_id] = unit

    def lookup(self, unit_id: str) -> EnergyUnit | None:
        return self.registry.get(unit_id)


T_MIN = 0.1
ALPHA_ENTROPY = 0.01
KAPPA = 0.5
RHO_RES = 0.75


def update_energy(registry: ThermoRegistry, unit_id: str, new_se: float, now: datetime) -> None:
    unit = registry.lookup(unit_id)
    if not unit:
        raise KeyError("UNIT_NOT_FOUND")
    unit.SE_current = min(new_se, unit.C_max)
    unit.last_update_time = now
    local_density = unit.metadata.get("local_density", 0)
    t_sem = unit.SE_current / (1 + local_density)
    unit.status = "ThermallyInactive" if t_sem < T_MIN else "Active"


def decay_all(registry: ThermoRegistry, now: datetime) -> None:
    for unit in registry.registry.values():
        if unit.status == "Active":
            dt = (now - unit.last_update_time).total_seconds()
            unit.SE_current *= exp(-unit.decay_rate * dt)
            unit.last_update_time = now
            local_density = unit.metadata.get("local_density", 0)
            t_sem = unit.SE_current / (1 + local_density)
            unit.status = "ThermallyInactive" if t_sem < T_MIN else "Active"


def resonate(registry: ThermoRegistry, id_a: str, id_b: str, now: datetime) -> None:
    unit_a = registry.lookup(id_a)
    unit_b = registry.lookup(id_b)
    if not unit_a or not unit_b:
        raise KeyError("UNIT_NOT_FOUND")
    # simple similarity placeholder
    sim = 1.0
    if sim < RHO_RES:
        raise ValueError("LOW_SIMILARITY")
    min_se = min(unit_a.SE_current, unit_b.SE_current)
    delta_se = KAPPA * min_se
    if unit_a.SE_current >= unit_b.SE_current:
        unit_a.SE_current -= delta_se
        unit_b.SE_current += delta_se
    else:
        unit_b.SE_current -= delta_se
        unit_a.SE_current += delta_se
    unit_a.SE_current = min(unit_a.SE_current, unit_a.C_max)
    unit_b.SE_current = min(unit_b.SE_current, unit_b.C_max)
    unit_a.last_update_time = now
    unit_b.last_update_time = now
    delta_s = ALPHA_ENTROPY * delta_se
    unit_a.entropy_accumulated += delta_s
    unit_b.entropy_accumulated += delta_s

