import pytest
import yaml
from frozendict import frozendict

from lexique.lexical_structures.Blocks import Blocks
from lexique.lexical_structures.Forme import Forme
from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.Paradigm import Paradigm
from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace
from lexique.lexical_structures.Suffix import Suffix


def fx_phonology():
    return dict(apophonies=dict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
                     mutations=dict(p="p", t="p", k="t", b="p", d="b",
                                          g="d", m="m", n="m", N="n", f="f",
                                          s="f", S="s", v="f", z="v", Z="z",
                                          r="w", l="r", j="w", w="w"),
                     derives=dict(A="V", D="C"),
                     consonnes=set("ptkbdgmnNfsSvzZrljw"),
                     voyelles=set("iueoa"))


def fx_gloses():
    return {"N": {"Genre": ["m", "f"],
                  "Nombre": ["sg", "pl"]}}


def fx_blocks() -> Blocks:
    return {"N": [{"Nombre=pl": "X+s"}]}


@pytest.mark.parametrize("lexeme, formes", [
    (Lexeme(stem=StemSpace(stems=("manie",)), pos="N", sigma=frozendict(Genre="f")),
     [Forme(pos="N", morphemes=Morphemes(radical=Radical(stems=StemSpace(stems=("manie",))), others=[]),
            sigma=frozendict(Genre="f", f="Genre", Nombre="sg", sg="Nombre")),
      Forme(pos="N", morphemes=Morphemes(radical=Radical(stems=StemSpace(stems=("manie",))),
                                         others=[Suffix(rule="X+s", sigma=frozendict(Nombre="pl"),
                                                        phonology=fx_phonology())]),
            sigma=frozendict(Genre="f", f="Genre", Nombre="pl", pl="Nombre"))])
])
def test_paradigm(tmp_path, lexeme, formes) -> None:
    _path = tmp_path / "Blocks.yaml"
    with open(_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(fx_blocks(), file_handler)

    _path = tmp_path / "Gloses.yaml"
    with open(_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(fx_gloses(), file_handler)

    _path = tmp_path / "Phonology.yaml"
    with open(_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(fx_phonology(), file_handler)

    actual = Paradigm.from_disk(path=tmp_path)
    actual_formes = actual.realize(lexeme=lexeme)
    assert actual_formes == formes
