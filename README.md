# STARFORGE PROTOCOL: draw.io -> Python Codegen

> Vessel ID: `codegen_poc`
> 
> Mission: transform simplified draw.io UML signals into executable Python class stubs.

## What This Is

`drawio_codegen.py` parses a simplified draw.io (mxGraph XML) model and emits Python dataclasses.

Generated output includes:
- one file per class
- typed attributes for associations
- helper methods for `N`-cardinality links (`add_*`, `remove_*`)
- inheritance wiring

## Launch Sequence

Run from `codegen_poc/`:

```bash
python drawio_codegen.py examples/default/model/model.drawio examples/default/src_gen
python examples/default/client.py

python drawio_codegen.py examples/library/model/library.drawio.xml examples/library/src_gen
python examples/library/client.py
```

## Signal Format (Model Rules)

Association edge labels must follow:
- `name (1)`
- `name (N)`

Examples:
- `drives (1)`
- `hasWheel (N)`

Inheritance is detected when edge style contains:
- `endArrow=block`
- `endFill=0`

## Naming + Import Safety

The generator now enforces stable field names and import-safe typing:
- normalizes role names to avoid accidental double underscores
- uses forward references for association types to avoid circular import crashes in bidirectional links

## Output Topology

Typical generated package:

```text
src_gen/
  __init__.py
  person.py
  car.py
  wheel.py
  ...
```

## Known Scope (PoC)

This is intentionally limited:
- assumes a simplified draw.io structure
- ignores edges with unparseable labels
- does not generate persistence, validation, or runtime graph constraints

## If The Reactor Fails

Quick checks:
1. confirm edge labels exactly match `name (1|N)`
2. confirm class nodes are `mxCell` with `vertex="1"`
3. regenerate into a clean output folder
4. run client with the same Python interpreter used for generation
