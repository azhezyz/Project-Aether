from pathlib import Path

from codegen_poc.drawio_codegen import generate_python, parse_drawio


def test_parse_and_generate_smoke(tmp_path):
    model = Path("codegen_poc/examples/default/model/model.drawio")
    classes, assoc, inh = parse_drawio(str(model))

    assert classes
    assert assoc

    out_dir = tmp_path / "src_gen"
    generate_python(classes, assoc, inh, str(out_dir))

    assert (out_dir / "__init__.py").exists()
    assert any(p.name.endswith(".py") and p.name != "__init__.py" for p in out_dir.iterdir())
