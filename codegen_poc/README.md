# PoC draw.io XML -> Python code generator (SFWRENG 2AA4 B2)

This is a proof-of-concept generator that reads a simplified draw.io (mxGraph) XML file and generates Python class skeletons.

## Quick start

```bash
python drawio_codegen.py examples/default/model/model.drawio examples/default/src-gen
python examples/default/client.py

python drawio_codegen.py examples/new/model/model.drawio examples/new/src-gen
python examples/new/client.py
```

Notes:
- Associations must be labeled as `name (1)` or `name (N)`.
- Inheritance edges are detected by the style containing `endArrow=block` and `endFill=0`.
