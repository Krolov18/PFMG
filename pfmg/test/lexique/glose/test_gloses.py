# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
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
     {"source": {"N": [frozendict({"Genre": "m", "m": "Genre"})]},
      "destination": {"N": [frozendict({"Genre": "m", "m": "Genre"})]}}),

    ({"source": {"N": {"Genre": ["m", "f"]}},
      "destination": {"N": {"Genre": ["m", "f"]}}},
     {"source": {"N": [frozendict({"Genre": "m", "m": "Genre"}),
                       frozendict({"Genre": "f", "f": "Genre"})]},
      "destination": {"N": [frozendict({"Genre": "m", "m": "Genre"}),
                            frozendict({"Genre": "f", "f": "Genre"})]}}),

    ({"source": {"N": {"Genre": ["m", "f"], "Nombre": ["sg", "pl"]}},
      "destination": {"N": {"Cas": ["nom", "acc", "dat"]}}},
     {"source": {"N": [frozendict({"Genre": "m", "m": "Genre",
                                   "Nombre": "sg", "sg": "Nombre"}),
                       frozendict({"Genre": "m", "m": "Genre",
                                   "Nombre": "pl", "pl": "Nombre"}),
                       frozendict({"Genre": "f", "f": "Genre",
                                   "Nombre": "sg", "sg": "Nombre"}),
                       frozendict({"Genre": "f", "f": "Genre",
                                   "Nombre": "pl", "pl": "Nombre"})]},
      "destination": {"N": [frozendict({"Cas": "nom", "nom": "Cas"}),
                            frozendict({"Cas": "acc", "acc": "Cas"}),
                            frozendict({"Cas": "dat", "dat": "Cas"})]}}),
])


@parametrize
def test_gloses_from_disk(tmp_path, gloses, expected) -> None:
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.dump(gloses, file_handler)
    actual = Gloses.from_yaml(gloses_path)

    assert actual == Gloses(**expected)


parametrize = pytest.mark.parametrize("params, expected", [

    ({"source": {"N": [frozendict({"Genre": "m", "m": "Genre"})]},
      "destination": {"N": [frozendict({"Genre": "m", "m": "Genre"})]}},
     [{"source": frozendict({"Genre": "m", "m": "Genre"}),
       "destination": frozendict({"Genre": "m", "m": "Genre"})}]),

    ({"source": {"N": [frozendict({"Genre": "m", "m": "Genre"}),
                       frozendict({"Genre": "f", "f": "Genre"})]},
      "destination": {"N": [frozendict({"Genre": "m", "m": "Genre"}),
                            frozendict({"Genre": "f", "f": "Genre"})]}},
     [{"destination": frozendict({"Genre": "m", "m": "Genre"}),
       "source": frozendict({"Genre": "m", "m": "Genre"})},
      {"destination": frozendict({"Genre": "f", "f": "Genre"}),
       "source": frozendict({"Genre": "m", "m": "Genre"})},
      {"destination": frozendict({"Genre": "m", "m": "Genre"}),
       "source": frozendict({"Genre": "f", "f": "Genre"})},
      {"destination": frozendict({"Genre": "f", "f": "Genre"}),
       "source": frozendict({"Genre": "f", "f": "Genre"})}]),

    ({"source": {"N": [frozendict({"Genre": "m", "m": "Genre",
                                   "Nombre": "sg", "sg": "Nombre"}),
                       frozendict({"Genre": "m", "m": "Genre",
                                   "Nombre": "pl", "pl": "Nombre"}),
                       frozendict({"Genre": "f", "f": "Genre",
                                   "Nombre": "sg", "sg": "Nombre"}),
                       frozendict({"Genre": "f", "f": "Genre",
                                   "Nombre": "pl", "pl": "Nombre"})]},
      "destination": {"N": [frozendict({"Cas": "m", "m": "Cas"})]}},
     [{"destination": frozendict({"Cas": "m", "m": "Cas"}),
       "source": frozendict({"Genre": "m", "m": "Genre",
                             "Nombre": "sg", "sg": "Nombre"})},
      {"destination": frozendict({"Cas": "m", "m": "Cas"}),
       "source": frozendict({"Genre": "m", "m": "Genre",
                             "Nombre": "pl", "pl": "Nombre"})},
      {"destination": frozendict({"Cas": "m", "m": "Cas"}),
       "source": frozendict({"Genre": "f", "f": "Genre",
                             "Nombre": "sg", "sg": "Nombre"})},
      {"destination": frozendict({"Cas": "m", "m": "Cas"}),
       "source": frozendict({"Genre": "f", "f": "Genre",
                             "Nombre": "pl", "pl": "Nombre"})}]),
])


@parametrize
def test__call__(tmp_path, params, expected) -> None:
    actual = Gloses(**params)
    assert actual(pos="N") == expected
