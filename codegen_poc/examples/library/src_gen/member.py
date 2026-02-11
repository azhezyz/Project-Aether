# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

@dataclass
class Member(object):
    hasloan__loan: List["Loan"] = field(default_factory=list)

    def add_hasloan__loan(self, item: "Loan") -> None:
        self.hasloan__loan.append(item)

    def remove_hasloan__loan(self, item: "Loan") -> None:
        self.hasloan__loan.remove(item)
