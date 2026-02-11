# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Car(object):
    has_wheel: List["Wheel"] = field(default_factory=list)
    has_licenceplate: Optional["LicencePlate"] = None

    def add_has_wheel(self, item: "Wheel") -> None:
        self.has_wheel.append(item)

    def remove_has_wheel(self, item: "Wheel") -> None:
        self.has_wheel.remove(item)
