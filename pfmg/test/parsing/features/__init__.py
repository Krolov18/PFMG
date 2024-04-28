# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
import pytest

from pfmg.parsing.features.utils import FeatureReader


parametrize = pytest.mark.parametrize(
    "data, target, expected",
    [
        # ("Genre",
        #  "s",
        #  [{"sGenre": "?sGenre"}]),
        #
        # ("Genre,Nombre",
        #  "s",
        #  [{"sGenre": "?sGenre", "sNombre": "?sNombre"}]),
        #
        # ("Genre;Nombre",
        #  "s",
        #  [{"sGenre": "?sGenre"}, {"sNombre": "?sNombre"}]),
        #
        # ("Genre=m",
        #  "s",
        #  [{"sGenre": "m"}]),
        #
        # ("Genre,Nombre;Genre,Nombre",
        #  "s",
        #  [{"sGenre":  "?sGenre", "sNombre": "?sNombre"},
        #   {"sGenre":  "?sGenre", "sNombre": "?sNombre"}]),
        #
        # ("Genre,Nombre;Genre,Nombre;Cas=erg",
        #  "s",
        #  [{"sGenre":  "?sGenre", "sNombre": "?sNombre"},
        #   {"sGenre":  "?sGenre", "sNombre": "?sNombre"},
        #   {"sCas":  "erg"}]),
        #
        # ("Genre;;", "s", [{"sGenre":  "?sGenre"}, {}, {}]),

        ("Genre;;Nombre", "s", [{"sGenre":  "?sGenre"}, {}, {"sNombre": "?sNombre"}]),
    ]
)


@parametrize
def test_features_parse(data, target, expected):
    features = FeatureReader().parse(data, target=target)
    assert features == expected


# parametrize = pytest.mark.parametrize()
#
#
# @parametrize
# def test_features_parse(data, target, expected):
#     features = Features()
#     assert features == expected
