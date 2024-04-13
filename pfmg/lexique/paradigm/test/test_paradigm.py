import yaml
from frozendict import frozendict

from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.paradigm.Paradigm import Paradigm
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace
from pfmg.lexique.morpheme.Suffix import Suffix


def phonology() -> dict:
    return dict(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(
            p="p", t="p", k="t", b="p", d="b",
            g="d", m="m", n="m", N="n", f="f",
            s="f", S="s", v="f", z="v", Z="z",
            r="w", l="r", j="w", w="w"
        ),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=set("iueoa")
    )


# @pytest.mark.parametrize("lexeme, formes", [
#     (Lexeme(stem=StemSpace(stems=("manie",)),
#             pos="N",
#             sigma=frozendict(Genre="f")),
#      [Forme(pos="N",
#             morphemes=Morphemes(radical=Radical(
#                 stems=StemSpace(stems=("manie",))),
#                                 others=[]),
#             sigma=frozendict(Genre="f", f="Genre",
#                              Nombre="sg", sg="Nombre")),
#       Forme(pos="N",
#             morphemes=Morphemes(radical=Radical(
#                 stems=StemSpace(stems=("manie",))),
#                                 others=[
#                                     Suffix(rule="X+s",
#                                            sigma=frozendict(Nombre="pl"),
#                                            phonology=fx_phonology())]),
#             sigma=frozendict(Genre="f",
#                              f="Genre",
#                              Nombre="pl",
#                              pl="Nombre"))])
# ])
# def test_paradigm_from_disk(tmp_path, lexeme, formes) -> None:
#     blocks = {"N": [{"Nombre=pl": "X+s"}]}
#     gloses = {"N": {"Genre": ["m", "f"],
#                   "Nombre": ["sg", "pl"]}}
#
#     _path = tmp_path / "Blocks.yaml"
#     with open(_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(blocks, file_handler)
#
#     _path = tmp_path / "Gloses.yaml"
#     with open(_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(gloses, file_handler)
#
#     _path = tmp_path / "Phonology.yaml"
#     with open(_path, mode="w", encoding="utf8") as file_handler:
#         yaml.dump(fx_phonology(), file_handler)
#
#     actual = Paradigm.from_disk(path=tmp_path)
#     actual_formes = actual.realize(lexeme=lexeme)
#     assert actual_formes == formes


def test_from_disk(tmp_path):
    gloses = {"source": {"N": {"Genre": ["m", "f"],
                               "Nombre": ["sg", "pl"]}},
              "destination": {"N": {"Genre": ["m"],
                                    "Nombre": ["sg"]}}}

    blocks = {"source": {"N": [{"Nombre=pl": "X+s"}]},
              "destination": {"N": [{"Nombre=pl": "X+s"}]}}

    _path = tmp_path / "Blocks.yaml"
    with open(_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(blocks, file_handler)

    _path = tmp_path / "Gloses.yaml"
    with open(_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)

    _path = tmp_path / "Phonology.yaml"
    with open(_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(phonology(), file_handler)

    paradigm = Paradigm.from_disk(path=tmp_path)

    actual = list(
        paradigm.realize(
            Lexeme(
                source=LexemeEntry(
                    stems=StemSpace(("tortue",)),
                    pos="N",
                    sigma=frozendict(Genre="f")
                ),
                destination=LexemeEntry(
                    stems=StemSpace(("turtle",)),
                    pos="N",
                    sigma=frozendict()
                )
            )
        )
    )
    expected = [
        Forme(
            source=FormeEntry(
                pos="N",
                morphemes=Morphemes(
                    radical=Radical(StemSpace(("tortue",))),
                    others=[]
                    ),
                sigma=frozendict(Genre="f", Nombre="sg", f="Genre", sg="Nombre")
            ),
            destination=FormeEntry(
                pos="N",
                morphemes=Morphemes(
                    radical=Radical(StemSpace(("turtle",))),
                    others=[]
                    ),
                sigma=frozendict(Genre="m", Nombre="sg", m="Genre", sg="Nombre")
            )
        ),

        Forme(
            source=FormeEntry(
                pos="N",
                morphemes=Morphemes(
                    radical=Radical(StemSpace(("tortue",))),
                    others=[
                        Suffix(
                            rule="X+s",
                            sigma=frozendict({'Nombre': 'pl'}),
                            phonology=Phonology(**phonology())
                        )]
                    ),
                sigma=frozendict(Genre="f", Nombre="pl", f="Genre", pl="Nombre")
            ),
            destination=FormeEntry(
                pos="N",
                morphemes=Morphemes(
                    radical=Radical(StemSpace(("turtle",))),
                    others=[]
                    ),
                sigma=frozendict(Genre="m", Nombre="sg", m="Genre", sg="Nombre")
            )
        )
    ]
    assert actual == expected
