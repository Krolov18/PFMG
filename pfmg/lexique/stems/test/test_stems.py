# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import pytest
import yaml
from frozendict import frozendict
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.stems.Stems import Stems
from pfmg.lexique.stem_space.StemSpace import StemSpace


parametrize = pytest.mark.parametrize(
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
                     stems=StemSpace(stems=("kiki", "koko")),
                     pos="A",
                     sigma=frozendict({}),
                 ),
                 destination=LexemeEntry(
                     stems=StemSpace(stems=("ksit",)),
                     pos="A",
                     sigma=frozendict({"Cas": "erg"}),
                 ),
             ),
             Lexeme(
                 source=LexemeEntry(
                     stems=StemSpace(stems=("toto", "tutu")),
                     pos="N",
                     sigma=frozendict(Genre="m"),
                 ),
                 destination=LexemeEntry(
                     stems=StemSpace(stems=("pSit",)),
                     pos="N",
                     sigma=frozendict(),
                 ),
             )]),

    ],
)

@parametrize
def test_from_disk(tmp_path, stems, gloses, expected):
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)

    stems_path = tmp_path / "Stems.yaml"
    with open(stems_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(stems, file_handler)

    actual = Stems.from_disk(stems_path)
    assert list(actual) == expected

