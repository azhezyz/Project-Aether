# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from .author import Author
from .publisher import Publisher

@dataclass
class Book(object):
    writtenby__author: List[Author] = field(default_factory=list)
    publishedby__publisher: Optional[Publisher] = None

    def add_writtenby__author(self, item: Author) -> None:
        self.writtenby__author.append(item)

    def remove_writtenby__author(self, item: Author) -> None:
        self.writtenby__author.remove(item)
