#!/usr/bin/env python3
"""
drawio_codegen.py
PoC code generator for a simplified draw.io (mxGraph) XML model.

Usage:
  python drawio_codegen.py path/to/model.drawio path/to/output_dir

Model assumptions (PoC):
- Classes are mxCell elements with vertex="1" and their name in @value.
- Relationships are mxCell elements with edge="1", and:
  - source, target are mxCell ids
  - @value contains "name (1)" or "name (N)" for associations
  - @style containing "endArrow=block" + "endFill=0" denotes inheritance (is-a)
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

ASSOC_RE = re.compile(r"^\s*(?P<name>[A-Za-z_][A-Za-z0-9_ ]*)\s*\(\s*(?P<card>1|N)\s*\)\s*$")

@dataclass(frozen=True)
class ClassDef:
    id: str
    name: str

@dataclass(frozen=True)
class AssocDef:
    source: str
    target: str
    raw_name: str
    card: str  # "1" or "N"

@dataclass(frozen=True)
class InheritanceDef:
    sub: str
    sup: str

def _sanitize_identifier(s: str) -> str:
    s = s.strip().replace(" ", "_")
    s = re.sub(r"[^A-Za-z0-9_]", "_", s)
    s = re.sub(r"_+", "_", s)
    if not s or not re.match(r"^[A-Za-z_]", s):
        s = "x_" + s
    return s

def _assoc_base_name(raw_name: str) -> str:
    """
    Normalize association role names into stable python identifiers.
    """
    name = _sanitize_identifier(raw_name.strip().lower())
    return name.rstrip("_") or "x"

def parse_drawio(path: str) -> Tuple[Dict[str, ClassDef], List[AssocDef], List[InheritanceDef]]:
    tree = ET.parse(path)
    root = tree.getroot()

    # draw.io exports often nest mxGraphModel/root multiple levels; find all mxCell nodes.
    cells = root.findall(".//mxCell")

    classes: Dict[str, ClassDef] = {}
    assoc: List[AssocDef] = []
    inh: List[InheritanceDef] = []

    for c in cells:
        if c.get("vertex") == "1":
            cid = c.get("id")
            name = (c.get("value") or "").strip()
            if cid and name:
                classes[cid] = ClassDef(id=cid, name=name)

    for c in cells:
        if c.get("edge") == "1":
            src = c.get("source")
            tgt = c.get("target")
            if not src or not tgt or src not in classes or tgt not in classes:
                continue

            style = c.get("style") or ""
            value = (c.get("value") or "").strip()

            is_inheritance = ("endArrow=block" in style and "endFill=0" in style)
            if is_inheritance:
                inh.append(InheritanceDef(sub=src, sup=tgt))
                continue

            m = ASSOC_RE.match(value)
            if not m:
                # ignore edges without a parsable label
                continue
            assoc.append(AssocDef(source=src, target=tgt, raw_name=m.group("name"), card=m.group("card")))

    return classes, assoc, inh

def _resolve_attribute_names(classes: Dict[str, ClassDef], assoc: List[AssocDef]) -> Dict[AssocDef, str]:
    """
    Make python-safe attribute names and disambiguate duplicates by appending target name.
    """
    by_src_name = {}
    for a in assoc:
        src_name = classes[a.source].name
        key = (src_name, a.raw_name.strip().lower())
        by_src_name.setdefault(key, []).append(a)

    mapping: Dict[AssocDef, str] = {}
    for (src_name, raw), items in by_src_name.items():
        if len(items) == 1:
            mapping[items[0]] = _assoc_base_name(items[0].raw_name)
        else:
            for it in items:
                base = _assoc_base_name(it.raw_name)
                tgt = _sanitize_identifier(classes[it.target].name.strip().lower()).strip("_") or "x"
                mapping[it] = f"{base}_{tgt}"
    return mapping

def _toposort_classes(classes: Dict[str, ClassDef], inh: List[InheritanceDef]) -> List[ClassDef]:
    # Simple ordering: supertypes first, then rest
    supers = {x.sup for x in inh}
    subs = {x.sub for x in inh}
    ordered = []
    # add pure supertypes
    for cid, c in classes.items():
        if cid in supers and cid not in subs:
            ordered.append(c)
    # add remaining
    for cid, c in classes.items():
        if c not in ordered:
            ordered.append(c)
    return ordered

def generate_python(classes: Dict[str, ClassDef], assoc: List[AssocDef], inh: List[InheritanceDef], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)

    sup_of: Dict[str, str] = {x.sub: x.sup for x in inh}
    assoc_attr = _resolve_attribute_names(classes, assoc)

    # Group associations by source
    assoc_by_src: Dict[str, List[AssocDef]] = {}
    for a in assoc:
        assoc_by_src.setdefault(a.source, []).append(a)

    # Write __init__.py (optional convenience)
    init_lines = ["# generated package\n"]
    for c in _toposort_classes(classes, inh):
        init_lines.append(f"from .{_sanitize_identifier(c.name.lower())} import {c.name}\n")
    with open(os.path.join(out_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.writelines(init_lines)

    # Generate per-class files
    for c in _toposort_classes(classes, inh):
        base = sup_of.get(c.id)
        base_name = classes[base].name if base else "object"
        file_name = _sanitize_identifier(c.name.lower()) + ".py"
        path = os.path.join(out_dir, file_name)

        lines: List[str] = []
        lines.append("# generated file - PoC\n")
        lines.append("from __future__ import annotations\n\n")
        lines.append("from dataclasses import dataclass, field\n")
        lines.append("from typing import Optional, List\n\n")

        # Import base type (needed at runtime for class definition).
        targets = assoc_by_src.get(c.id, [])
        if base and classes[base].name != c.name:
            base_cls = classes[base].name
            base_mod = _sanitize_identifier(base_cls.lower())
            lines.append(f"from .{base_mod} import {base_cls}\n")
        if base:
            lines.append("\n")

        lines.append(f"@dataclass\nclass {c.name}({base_name}):\n")

        # Attributes
        any_attr = False
        for a in targets:
            attr = assoc_attr[a]
            tgt_cls = classes[a.target].name
            if a.card == "1":
                lines.append(f"    {attr}: Optional[\"{tgt_cls}\"] = None\n")
            else:
                lines.append(f"    {attr}: List[\"{tgt_cls}\"] = field(default_factory=list)\n")
            any_attr = True

        if not any_attr:
            lines.append("    pass\n")

        # Convenience methods for N relationships
        for a in targets:
            if a.card == "N":
                attr = assoc_attr[a]
                tgt_cls = classes[a.target].name
                add_name = f"add_{attr}"
                rem_name = f"remove_{attr}"
                lines.append("\n")
                lines.append(f"    def {add_name}(self, item: \"{tgt_cls}\") -> None:\n")
                lines.append(f"        self.{attr}.append(item)\n")
                lines.append("\n")
                lines.append(f"    def {rem_name}(self, item: \"{tgt_cls}\") -> None:\n")
                lines.append(f"        self.{attr}.remove(item)\n")

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: python drawio_codegen.py <model.drawio> <out_dir>")
        return 2
    model, out_dir = argv[1], argv[2]
    classes, assoc, inh = parse_drawio(model)
    generate_python(classes, assoc, inh, out_dir)
    print(f"Generated {len(classes)} classes into {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
