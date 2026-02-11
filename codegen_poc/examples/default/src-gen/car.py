# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from .wheel import Wheel
from .licenceplate import LicencePlate

@dataclass
class Car(object):
    has__wheel: List[Wheel] = field(default_factory=list)
    has__licenceplate: Optional[LicencePlate] = None

    def add_has__wheel(self, item: Wheel) -> None:
        self.has__wheel.append(item)

    def remove_has__wheel(self, item: Wheel) -> None:
        self.has__wheel.remove(item)
