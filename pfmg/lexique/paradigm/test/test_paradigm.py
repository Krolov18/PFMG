import yaml
from frozendict import frozendict

from lexique.lexical_structures.Forme import Forme
from lexique.lexical_structures.FormeEntry import FormeEntry
from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.LexemeEntry import LexemeEntry
from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.Paradigm import Paradigm
from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace
from lexique.lexical_structures.Suffix import Suffix


def phonology():
    return dict(
        apophonies=dict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=dict(
            p="p", t="p", k="t", b="p", d="b",
            g="d", m="m", n="m", N="n", f="f",
            s="f", S="s", v="f", z="v", Z="z",
            r="w", l="r", j="w", w="w"
        ),
        derives=dict(A="V", D="C"),
        consonnes=set("ptkbdgmnNfsSvzZrljw"),
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
                            phonology=phonology()
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
