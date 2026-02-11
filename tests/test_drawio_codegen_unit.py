from pathlib import Path

from codegen_poc.drawio_codegen import (
    ASSOC_RE,
    AssocDef,
    ClassDef,
    InheritanceDef,
    _assoc_base_name,
    _sanitize_identifier,
    generate_python,
    main,
    parse_drawio,
)


def test_sanitize_and_assoc_helpers_cover_edge_cases():
    assert _sanitize_identifier(" 123-abc ") == "x_123_abc"
    assert _sanitize_identifier("A  B") == "A_B"
    assert _assoc_base_name("___") == "x"
    assert ASSOC_RE.match("role_name (N)")


def test_parse_drawio_handles_invalid_edges_and_inheritance(tmp_path):
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile>
  <diagram>
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" />
        <mxCell id="A" vertex="1" value="Parent" />
        <mxCell id="B" vertex="1" value="Child" />
        <mxCell id="C" vertex="1" value="" />
        <mxCell id="E1" edge="1" source="B" target="A" style="endArrow=block;endFill=0;" />
        <mxCell id="E2" edge="1" source="A" target="B" value="friends (N)" />
        <mxCell id="E3" edge="1" source="A" target="missing" value="ghost (1)" />
        <mxCell id="E4" edge="1" source="A" target="B" value="not-parseable" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    model = tmp_path / "model.drawio"
    model.write_text(xml, encoding="utf-8")

    classes, assoc, inh = parse_drawio(str(model))

    assert set(classes.keys()) == {"A", "B"}
    assert len(assoc) == 1
    assert assoc[0].source == "A"
    assert assoc[0].target == "B"
    assert assoc[0].raw_name.strip() == "friends"
    assert assoc[0].card == "N"
    assert inh == [InheritanceDef(sub="B", sup="A")]


def test_generate_python_covers_duplicate_names_inheritance_and_pass(tmp_path):
    classes = {
        "A": ClassDef(id="A", name="Base"),
        "B": ClassDef(id="B", name="Child"),
        "C": ClassDef(id="C", name="Library-User"),
        "D": ClassDef(id="D", name="Lonely"),
    }
    assoc = [
        AssocDef(source="B", target="A", raw_name="links", card="N"),
        AssocDef(source="B", target="C", raw_name="links", card="N"),
        AssocDef(source="B", target="D", raw_name="singleRef", card="1"),
    ]
    inh = [InheritanceDef(sub="B", sup="A")]

    out_dir = tmp_path / "src_gen"
    generate_python(classes, assoc, inh, str(out_dir))

    child_py = (out_dir / "child.py").read_text(encoding="utf-8")
    lonely_py = (out_dir / "lonely.py").read_text(encoding="utf-8")
    init_py = (out_dir / "__init__.py").read_text(encoding="utf-8")

    assert "from .base import Base" in child_py
    assert 'links_base: List["Base"]' in child_py
    assert 'links_library_user: List["Library-User"]' in child_py
    assert "def add_links_base" in child_py
    assert "def remove_links_library_user" in child_py
    assert 'singleref: Optional["Lonely"] = None' in child_py
    assert "class Lonely(object):" in lonely_py
    assert "pass" in lonely_py
    assert "from .base import Base" in init_py


def test_main_usage_and_success(tmp_path, capsys):
    assert main(["drawio_codegen.py"]) == 2
    assert "Usage: python drawio_codegen.py <model.drawio> <out_dir>" in capsys.readouterr().out

    model = Path("codegen_poc/examples/default/model/model.drawio")
    out_dir = tmp_path / "generated"
    rc = main(["drawio_codegen.py", str(model), str(out_dir)])

    assert rc == 0
    assert out_dir.exists()
    assert "Generated" in capsys.readouterr().out
