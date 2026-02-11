# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from .car import Car
from .person import Person

@dataclass
class Driver(Person):
    drives: Optional[Car] = None
