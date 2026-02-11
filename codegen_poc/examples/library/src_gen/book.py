# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Book(object):
    writtenby_author: List["Author"] = field(default_factory=list)
    publishedby_publisher: Optional["Publisher"] = None

    def add_writtenby_author(self, item: "Author") -> None:
        self.writtenby_author.append(item)

    def remove_writtenby_author(self, item: "Author") -> None:
        self.writtenby_author.remove(item)
