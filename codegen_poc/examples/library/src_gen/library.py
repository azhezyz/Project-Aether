# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from .copy import Copy
from .librarian import Librarian

@dataclass
class Library(object):
    stores__copy: List[Copy] = field(default_factory=list)
    employs__librarian: List[Librarian] = field(default_factory=list)

    def add_stores__copy(self, item: Copy) -> None:
        self.stores__copy.append(item)

    def remove_stores__copy(self, item: Copy) -> None:
        self.stores__copy.remove(item)

    def add_employs__librarian(self, item: Librarian) -> None:
        self.employs__librarian.append(item)

    def remove_employs__librarian(self, item: Librarian) -> None:
        self.employs__librarian.remove(item)
