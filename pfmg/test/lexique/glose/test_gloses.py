# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from pathlib import Path
import pytest
import yaml
from frozendict import frozendict

from pfmg.lexique.glose import new_gloses
from pfmg.lexique.glose.Gloses import Gloses
from pfmg.lexique.glose.Sigma import Sigma
from pfmg.lexique.glose.Sigmas import Sigmas

parametrize = pytest.mark.parametrize(
    "gloses, expected_data", [
        ({"N": {"source": {"Genre": ["m"]},
                "destination": {"Genre": ["m"]}}},
         {"N": Sigmas([Sigma(**{"source":      frozendict({"Genre": "m"}),
                                "destination": frozendict({"Genre": "m"})})])}),

        ({"N": {"source": {"Genre": ["m", "f"]},
                "destination": {"Genre": ["m", "f"]}}},
         {'N': Sigmas(data=[Sigma(source=frozendict({'Genre': 'm'}),
                                  destination=frozendict({'Genre': 'm'})),
                            Sigma(source=frozendict({'Genre': 'm'}),
                                  destination=frozendict({'Genre': 'f'})),
                            Sigma(source=frozendict({'Genre': 'f'}),
                                  destination=frozendict({'Genre': 'm'})),
                            Sigma(source=frozendict({'Genre': 'f'}),
                                  destination=frozendict({'Genre': 'f'}))])}),

        ({"N": {"source": {"Genre":  ["m", "f"], "Nombre": ["sg", "pl"]},
                "destination": {"Cas": ["nom", "acc", "dat"]}}},
         {'N': Sigmas(data=[
             Sigma(source=frozendict({'Genre':  'm', 'Nombre': 'sg'}),
                   destination=frozendict({'Cas': 'nom'})),
             Sigma(source=frozendict({'Genre':  'm', 'Nombre': 'sg'}),
                   destination=frozendict({'Cas': 'acc'})),
             Sigma(source=frozendict({'Genre':  'm', 'Nombre': 'sg'}),
                   destination=frozendict({'Cas': 'dat'})),
             Sigma(source=frozendict({'Genre':  'm', 'Nombre': 'pl'}),
                   destination=frozendict({'Cas': 'nom'})),
             Sigma(source=frozendict({'Genre':  'm', 'Nombre': 'pl'}),
                   destination=frozendict({'Cas': 'acc'})),
             Sigma(source=frozendict({'Genre':  'm', 'Nombre': 'pl'}),
                   destination=frozendict({'Cas': 'dat'})),
             Sigma(source=frozendict({'Genre':  'f', 'Nombre': 'sg'}),
                   destination=frozendict({'Cas': 'nom'})),
             Sigma(source=frozendict({'Genre':  'f', 'Nombre': 'sg'}),
                   destination=frozendict({'Cas': 'acc'})),
             Sigma(source=frozendict({'Genre':  'f', 'Nombre': 'sg'}),
                   destination=frozendict({'Cas': 'dat'})),
             Sigma(source=frozendict({'Genre':  'f', 'Nombre': 'pl'}),
                   destination=frozendict({'Cas': 'nom'})),
             Sigma(source=frozendict({'Genre':  'f', 'Nombre': 'pl'}),
                   destination=frozendict({'Cas': 'acc'})),
             Sigma(source=frozendict({'Genre':  'f', 'Nombre': 'pl'}),
                   destination=frozendict({'Cas': 'dat'}))])}),
    ]
)


@parametrize
def test_gloses_from_disk(tmp_path, gloses, expected_data) -> None:
    gloses_path = tmp_path / "Gloses.yaml"
    with open(gloses_path, mode="w", encoding="utf8") as file_handler:
        yaml.safe_dump(gloses, file_handler)
    actual = Gloses.from_yaml(gloses_path)
    expected = Gloses(expected_data)

    assert actual == expected


parametrize = pytest.mark.parametrize(
    "params, expected", [

        ({"N": {"source":      {"Genre": ["m"]},
                "destination": {"Genre": ["m"]}}},
         Sigmas([Sigma(**{"source":      frozendict({"Genre": "m"}),
                          "destination": frozendict({"Genre": "m"})})])),

        ({"N": {"source":      {"Genre": ["m", "f"]},
                "destination": {"Genre": ["m", "f"]}}},
         Sigmas([Sigma(**{"destination": frozendict({"Genre": "m"}),
                          "source":      frozendict({"Genre": "m"})}),
                 Sigma(**{"destination": frozendict({"Genre": "f"}),
                          "source":      frozendict({"Genre": "m"})}),
                 Sigma(**{"destination": frozendict({"Genre": "m"}),
                          "source":      frozendict({"Genre": "f"})}),
                 Sigma(**{"destination": frozendict({"Genre": "f"}),
                          "source":      frozendict({"Genre": "f"})})])),

        ({"N": {"source": {"Genre":  ["m", "f"],
                           "Nombre": ["sg", "pl"]},
                "destination": {"Cas": ["m"]}}},
         Sigmas([Sigma(**{"destination": frozendict({"Cas": "m"}),
                          "source":      frozendict({"Genre":  "m",
                                                     "Nombre": "sg"})}),
                 Sigma(**{"destination": frozendict({"Cas": "m"}),
                          "source":      frozendict({"Genre":  "m",
                                                     "Nombre": "pl"})}),
                 Sigma(**{"destination": frozendict({"Cas": "m"}),
                          "source":      frozendict({"Genre":  "f",
                                                     "Nombre": "sg"})}),
                 Sigma(**{"destination": frozendict({"Cas": "m"}),
                          "source":      frozendict({"Genre":  "f",
                                                     "Nombre": "pl"})})])),
    ]
)


@parametrize
def test__call__(params, expected) -> None:
    gloses = Gloses.from_dict(params)
    actual = gloses(pos="N")
    assert actual == expected


parametrize = pytest.mark.parametrize(
    "params, expected_type, expected_type_2", [
        ({"N": {"source":      {"Genre": ["m"]},
                "destination": {"Genre": ["m"]}}},
         "Gloses",
         "Sigmas"),
    ])


@parametrize
def test_alignments_constraints(
    tmp_path,
    params,
    expected_type,
    expected_type_2
) -> None:
    filename = tmp_path / "Gloses.yaml"
    with filename.open(mode="w") as fh:
        yaml.safe_dump(params, fh)
    gloses = new_gloses(Path(filename))
    assert gloses.__class__.__name__ == expected_type
    assert gloses("N").__class__.__name__ == expected_type_2
