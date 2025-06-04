from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class Scar:
    scar_id: str
    contradiction: str
    entropy: float
    cls_angle: float
    semantic_polarity: float
    mutation_frequency: float
    origin_time: datetime
    metadata: Dict[str, float] = field(default_factory=dict)


class Vault:
    def __init__(self, name: str) -> None:
        self.name = name
        self.scars: Dict[str, Scar] = {}

    def store(self, scar: Scar) -> None:
        self.scars[scar.scar_id] = scar


class DualVault:
    def __init__(self) -> None:
        self.vault_a = Vault("Vault-A")
        self.vault_b = Vault("Vault-B")

    def route(self, scar: Scar) -> Vault:
        if scar.mutation_frequency > 0.75:
            return self.vault_a
        if abs(scar.semantic_polarity) > 0.5:
            return self.vault_a if scar.semantic_polarity > 0 else self.vault_b
        diff_a = abs(scar.cls_angle - self.vault_a.scars.get(scar.scar_id, Scar(
            scar_id="", contradiction="", entropy=0.0, cls_angle=0.0, semantic_polarity=0.0,
            mutation_frequency=0.0, origin_time=scar.origin_time)).cls_angle)
        diff_b = abs(scar.cls_angle - self.vault_b.scars.get(scar.scar_id, Scar(
            scar_id="", contradiction="", entropy=0.0, cls_angle=0.0, semantic_polarity=0.0,
            mutation_frequency=0.0, origin_time=scar.origin_time)).cls_angle)
        return self.vault_a if diff_a <= diff_b else self.vault_b

    def add_scar(self, scar: Scar) -> None:
        vault = self.route(scar)
        vault.store(scar)

