# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Member(object):
    hasloan_loan: List["Loan"] = field(default_factory=list)

    def add_hasloan_loan(self, item: "Loan") -> None:
        self.hasloan_loan.append(item)

    def remove_hasloan_loan(self, item: "Loan") -> None:
        self.hasloan_loan.remove(item)
