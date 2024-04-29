# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from pfmg.parsing.features.Features import Features
from pfmg.parsing.percolation.Percolation import Percolation
from pfmg.parsing.production.Production import Production


@pytest.mark.parametrize(
    "data", [
        {
            "Source": {
                "lhs":          "NP",
                "Syntagmes":    ["D", "A", "N"],
                "Accords":      "genre,nombre",
                "Percolation":  "genre,nombre",
                "Traduction": [2, 0, 1]
            }
        }
    ]
)
def test_from_yaml(data) -> None:
    production = Production.from_yaml(data=data)
    assert production.lhs == data["Source"]["lhs"]
    assert production.syntagmes == data["Source"]["Syntagmes"]
    assert isinstance(production.accords, Features)
    assert isinstance(production.percolation, Percolation)


parametrize = pytest.mark.parametrize(
    "data, expected", [
        ({
             "Source": {
                 "lhs":         "NP",
                 "Syntagmes":   ["D", "N"],
                 "Accords":     "Genre",
                 "Percolation": "Genre",
                 "Traduction": [1, 0]
             }
         },
         "NP[SGenre=?SGenre,Traduction=(?N1,?D0)] -> D[SGenre=?SGenre,Traduction=?D0] N[SGenre=?SGenre,Traduction=?N1]"),

        ({
             "Source": {
                 "lhs":         "NP",
                 "Syntagmes":   ["N"],
                 "Accords":     "Genre",
                 "Percolation": "Genre",
                 "Traduction": [0]
             }
         },
         "NP[SGenre=?SGenre,Traduction=(?N0)] -> N[SGenre=?SGenre,Traduction=?N0]"),

    ]
)


@parametrize
def test_production(data, expected) -> None:
    production = Production.from_yaml(data=data)
    actual = production.to_nltk()
    assert actual == expected
