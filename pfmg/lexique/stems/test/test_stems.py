import pytest
import yaml
from frozendict import frozendict
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.stems.Stems import Stems
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize(
    "stems, gloses, expected", [
        ({"N": {"pSit": "toto,tutu.Genre=m"},
          "A": {"Cas=erg": {"ksit": "kiki,koko"}},
          },
         {
             "source": {
                 "N": {"Genre": ["m", "f"],
                       "Nombre": ["sg", "pl"]},
                 "A": {"Cas": ["erg"]},
             },
             "destination": {
                 "N": {"Genre": ["m", "f"],
                       "Nombre": ["sg", "pl"]},
                 "A": {"Cas": ["erg"]},
             },
         },
         [
             Lexeme(
                 source=LexemeEntry(
                     stems=StemSpace(stems=("ksit",)),
                     pos="A",
                     sigma=frozendict(Cas="erg"),
                 ),
                 destination=LexemeEntry(
                     stems=StemSpace(stems=("kiki", "koko")),
                     pos="A",
                     sigma=frozendict(),
                 ),
             ),
             Lexeme(
                 source=LexemeEntry(
                     stems=StemSpace(stems=("pSit",)),
                     pos="N",
                     sigma=frozendict(),
                 ),
                 destination=LexemeEntry(
                     stems=StemSpace(stems=("toto", "tutu")),
                     pos="N",
                     sigma=frozendict(Genre="m"),
                 ),
             )]),

    ],
)
def test_from_disk(tmp_path, stems, gloses, expected):
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)

    stems_path = tmp_path / "Stems.yaml"
    with open(stems_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(stems, file_handler)

    actual = Stems.from_disk(stems_path)
    assert list(actual) == expected
