# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Library(object):
    stores_copy: List["Copy"] = field(default_factory=list)
    employs_librarian: List["Librarian"] = field(default_factory=list)

    def add_stores_copy(self, item: "Copy") -> None:
        self.stores_copy.append(item)

    def remove_stores_copy(self, item: "Copy") -> None:
        self.stores_copy.remove(item)

    def add_employs_librarian(self, item: "Librarian") -> None:
        self.employs_librarian.append(item)

    def remove_employs_librarian(self, item: "Librarian") -> None:
        self.employs_librarian.remove(item)
