# generated file - PoC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from .book import Book

@dataclass
class Copy(object):
    iscopyof__book: Optional[Book] = None
