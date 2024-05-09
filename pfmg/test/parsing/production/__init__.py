# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from pfmg.parsing.features.Features import Features
from pfmg.parsing.features.Percolation import Percolation
from pfmg.parsing.production.Production import Production


@pytest.mark.parametrize(
    "data", [
        {
            "lhs":         "NP",
            "Syntagmes":   ["D", "A", "N"],
            "Accords":     "genre,nombre",
            "Percolation": "genre,nombre",
            "translations":  [2, 0, 1]
        }
    ]
)
def test_from_yaml(data) -> None:
    production = Production.from_yaml(data=data, target="S")
    assert production.lhs == data["lhs"]
    assert production.syntagmes == data["Syntagmes"]
    assert isinstance(production.accords, Features)
    assert isinstance(production.percolation, Percolation)


parametrize = pytest.mark.parametrize(
    "data_s, data_d, expected", [
        ({
             "lhs":         "NP",
             "Syntagmes":   ["D", "N"],
             "Accords":     "Genre",
             "Percolation": "Genre",
             "translations":  [1, 0]
         },
         {
             "lhs":         "NP",
             "Syntagmes":   ["N", "D"],
             "Accords":     "Genre",
             "Percolation": "Genre"
         },
         ("NP[SGenre=?SGenre,translation=(?N1,?D0)] -> "
          "D[SGenre=?SGenre,translation=?D0] N[SGenre=?SGenre,translation=?N1]")),

        ({
             "lhs":         "NP",
             "Syntagmes":   ["N"],
             "Accords":     "Genre",
             "Percolation": "Genre",
             "translations":  [0]
         },
         {
             "lhs":         "NP",
             "Syntagmes":   ["N"],
             "Accords":     "Genre",
             "Percolation": "Genre",
             "translations":  [0]
         },
         ("NP[SGenre=?SGenre,translation=(?N0)] -> "
          "N[SGenre=?SGenre,translation=?N0]")),

    ]
)


@parametrize
def test_production(data_s, data_d, expected) -> None:
    source = Production.from_yaml(data=data_s, target="S")
    destination = Production.from_yaml(data=data_d, target="S")
    source.update(production=destination, indices=data_s["translations"])
    actual = source.to_nltk()
    assert actual == expected


@pytest.mark.parametrize(
    "pos, realization, sigma, expected",
    [
        ("N",
         "'garçon'",
         {
             "Genre": "'m'"
         },
         "N[Genre='m'] -> 'garçon'"),

        ("N",
         "'garçon'",
         {
             "SGenre":     "'m'",
             "DGenre":     "'f'",
             "translation": "'hazif'"
         },
         "N[SGenre='m',DGenre='f',translation='hazif'] -> 'garçon'"),
    ]
)
def test_production_lexical(pos, realization, sigma, expected) -> None:
    actual = Production(
        lhs=pos,
        syntagmes=[realization],
        accords=Features([{}]),
        percolation=Percolation(sigma)
    ).to_nltk()
    assert actual == expected
