# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace

parametrize = pytest.mark.parametrize(
    "radical, morphemes, expected", [
        (
            (
                "jardin,jardins",
                {
                    "Genre": "m"
                }
            ),
            [],
            "jardin"
        ),

        (
            (
                "jardin,jardins",
                {
                    "Genre": "m"
                }
            ),
            [
                (
                    "X2?X2:X1",
                    {
                        "Nombre": "pl"
                    }
                )
            ],
            "jardins"
        ),

        (
            (
                "jardin",
                {
                    "Genre": "m"
                }
            ),
            [
                (
                    "X+s",
                    {
                        "Nombre": "pl"
                    }
                )
            ],
            "jardins"
        ),

        (
            (
                "jardin",
                {
                    "Genre": "m"
                }
            ),
            [
                (
                    "s+X+k",
                    {
                        "Nombre": "pl"
                    }
                )
            ],
            "sjardink"
        ),
    ]
)


@parametrize
def test_to_string(fx_df_phonology, radical, morphemes, expected):
    morphemes = Morphemes(
        radical=Radical(
            stems=StemSpace.from_string(radical[0]),
            sigma=frozendict(radical[1])
        ),
        others=[create_morpheme(
            rule=rule, sigma=frozendict(sigma),
            phonology=fx_df_phonology
        )
            for rule, sigma in morphemes]

    )
    actual = morphemes.to_string()
    assert actual == expected


parametrize = pytest.mark.parametrize(
    "radical, morphemes, expected", [
        (
            (
                "jardin,jardins",
                {
                    "Genre": "m"
                }
            ),
            [],
            "jardin"
        ),

        (
            (
                "jardin,jardins",
                {
                    "Genre": "m"
                }
            ),
            [
                (
                    "X2?X2:X1",
                    {
                        "Nombre": "pl"
                    }
                )
            ],
            "jardins"
        ),

        (
            (
                "jardin",
                {
                    "Genre": "m"
                }
            ),
            [
                (
                    "X+s",
                    {
                        "Nombre": "pl"
                    }
                )
            ],
            "jardin-s"
        ),

        (
            (
                "jardin",
                {
                    "Genre": "m"
                }
            ),
            [
                (
                    "s+X+k",
                    {
                        "Nombre": "pl"
                    }
                )
            ],
            "s+jardin+k"
        ),
    ]
)


@parametrize
def test_to_decoupe(fx_df_phonology, radical, morphemes, expected):
    morphemes = Morphemes(
        radical=Radical(
            stems=StemSpace.from_string(radical[0]),
            sigma=frozendict(radical[1])
        ),
        others=[create_morpheme(
            rule=rule, sigma=frozendict(sigma),
            phonology=fx_df_phonology
        )
            for rule, sigma in morphemes]

    )
    actual = morphemes.to_decoupe()
    assert actual == expected


parametrize = pytest.mark.parametrize(
    "radical, morphemes, expected", [
        (("jardin,jardins", {"Genre": "m"}), [], "jardin.m"),

        (("jardin,jardins", {"Genre": "m"}), [("X2?X2:X1", {"Nombre": "pl"})], "jardin.m.pl"),

        (("jardin,jardins", {"Genre": "m"}), [("X2", {"Nombre": "pl"})], "jardin.m.pl"),

        (("jardin", {"Genre": "m"}), [("X+s", {"Nombre": "pl"})], "jardin.m-pl"),

        (("jardin", {"Genre": "m"}), [("s+X", {"Nombre": "pl"})], "pl-jardin.m"),

        (("jardin", {"Genre": "m"}), [("s+X+k", {"Nombre": "pl"})], "pl+jardin.m+pl"),
    ])


@parametrize
def test_to_glose(fx_df_phonology, radical, morphemes, expected):
    morphemes = Morphemes(
        radical=Radical(
            stems=StemSpace.from_string(radical[0]),
            sigma=frozendict(radical[1])
        ),
        others=[create_morpheme(
            rule=rule, sigma=frozendict(sigma),
            phonology=fx_df_phonology
        )
            for rule, sigma in morphemes]

    )
    actual = morphemes.to_glose()
    assert actual == expected


def test_get_sigma():
    morphemes = Morphemes(
        radical=Radical(
            stems=StemSpace.from_string("toto,tutu"),
            sigma=frozendict(Genre="m")
        ),
        others=[]
    )
    with pytest.raises(NotImplementedError):
        morphemes.get_sigma()
