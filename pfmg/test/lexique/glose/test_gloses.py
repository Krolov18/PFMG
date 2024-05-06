# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
import yaml
from frozendict import frozendict
from pfmg.lexique.glose.Gloses import Gloses

parametrize = pytest.mark.parametrize("gloses, expected", [

    ({"source": {"N": {"Genre": ["m"]}},
      "destination": {"N": {"Genre": ["m"]}}},
     {"source": {"N": [frozendict({"Genre": "m"})]},
      "destination": {"N": [frozendict({"Genre": "m"})]}}),

    ({"source": {"N": {"Genre": ["m", "f"]}},
      "destination": {"N": {"Genre": ["m", "f"]}}},
     {"source": {"N": [frozendict({"Genre": "m"}),
                       frozendict({"Genre": "f"})]},
      "destination": {"N": [frozendict({"Genre": "m"}),
                            frozendict({"Genre": "f"})]}}),

    ({"source": {"N": {"Genre": ["m", "f"], "Nombre": ["sg", "pl"]}},
      "destination": {"N": {"Cas": ["nom", "acc", "dat"]}}},
     {"source": {"N": [frozendict({"Genre": "m",
                                   "Nombre": "sg"}),
                       frozendict({"Genre": "m",
                                   "Nombre": "pl"}),
                       frozendict({"Genre": "f",
                                   "Nombre": "sg"}),
                       frozendict({"Genre": "f",
                                   "Nombre": "pl"})]},
      "destination": {"N": [frozendict({"Cas": "nom"}),
                            frozendict({"Cas": "acc"}),
                            frozendict({"Cas": "dat"})]}}),
])


@parametrize
def test_gloses_from_disk(tmp_path, gloses, expected) -> None:
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)
    actual = Gloses.from_yaml(gloses_path)
    expected = Gloses(**expected)

    assert actual == expected


parametrize = pytest.mark.parametrize("params, expected", [

    ({"source": {"N": [frozendict({"Genre": "m"})]},
      "destination": {"N": [frozendict({"Genre": "m"})]}},
     [{"source": frozendict({"Genre": "m"}),
       "destination": frozendict({"Genre": "m"})}]),

    ({"source": {"N": [frozendict({"Genre": "m"}),
                       frozendict({"Genre": "f"})]},
      "destination": {"N": [frozendict({"Genre": "m"}),
                            frozendict({"Genre": "f"})]}},
     [{"destination": frozendict({"Genre": "m"}),
       "source": frozendict({"Genre": "m"})},
      {"destination": frozendict({"Genre": "f"}),
       "source": frozendict({"Genre": "m"})},
      {"destination": frozendict({"Genre": "m"}),
       "source": frozendict({"Genre": "f"})},
      {"destination": frozendict({"Genre": "f"}),
       "source": frozendict({"Genre": "f"})}]),

    ({"source": {"N": [frozendict({"Genre": "m",
                                   "Nombre": "sg"}),
                       frozendict({"Genre": "m",
                                   "Nombre": "pl"}),
                       frozendict({"Genre": "f",
                                   "Nombre": "sg"}),
                       frozendict({"Genre": "f",
                                   "Nombre": "pl"})]},
      "destination": {"N": [frozendict({"Cas": "m"})]}},
     [{"destination": frozendict({"Cas": "m"}),
       "source": frozendict({"Genre": "m",
                             "Nombre": "sg"})},
      {"destination": frozendict({"Cas": "m"}),
       "source": frozendict({"Genre": "m",
                             "Nombre": "pl"})},
      {"destination": frozendict({"Cas": "m"}),
       "source": frozendict({"Genre": "f",
                             "Nombre": "sg"})},
      {"destination": frozendict({"Cas": "m"}),
       "source": frozendict({"Genre": "f", "Nombre": "pl"})}]),
])


@parametrize
def test__call__(tmp_path, params, expected) -> None:
    gloses = Gloses(**params)
    actual = gloses(pos="N")
    assert actual == expected
