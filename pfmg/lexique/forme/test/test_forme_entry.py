# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_to_string(fx_df_phonology) -> None:

    forme = FormeEntry(index=2,
                       pos="N",
                       morphemes=Morphemes(radical=Radical(
                           stems=StemSpace(stems=("a", "b", "c")), sigma=frozendict({"Genre": "m", "Nombre": "s"})),
                           others=[]),
                       sigma=frozendict({"Genre": "m", "Nombre": "s"}))
    actual = forme.to_string(None)
    expected = "a"
    assert actual == expected

    forme = FormeEntry(
        index=2,
        pos="N",
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(stems=("a", "b", "c")),
                sigma=frozendict({"Genre": "m", "Nombre": "s"})
            ),
            others=[
                create_morpheme(
                    rule="a+X",
                    sigma=frozendict({"Genre": "m", "Nombre": "s"}),
                    phonology=fx_df_phonology
                )
            ]
        ),
        sigma=frozendict({"Genre": "m", "Nombre": "s"}))

    actual = forme.to_string(None)
    expected = "aa"
    assert actual == expected

    with pytest.raises(NotImplementedError):
        _ = forme.to_string("")

    with pytest.raises(NotImplementedError):
        _ = forme.to_string(StemSpace(stems=("a", "b", "c")))


def test_get_sigma() -> None:
    forme = FormeEntry(index=2,
                       pos="N",
                       morphemes=Morphemes(radical=Radical(
                           stems=StemSpace(stems=("a", "b", "c")),
                           sigma=frozendict({"Genre": "m", "Nombre": "s"})
                       ),
                           others=[]),
                       sigma=frozendict({"Genre": "m", "Nombre": "s"}))
    actual = forme.get_sigma()
    expected = frozendict({"Genre": "m", "Nombre": "s"})
    assert actual == expected


def test_to_nltk(fx_df_phonology) -> None:
    forme = FormeEntry(index=3,
                       pos="N",
                       morphemes=Morphemes(radical=Radical(
                           stems=StemSpace(stems=("a", "b", "c")),
                           sigma=frozendict({"Genre": "m", "Nombre": "s"})
                       ),
                           others=[]),
                       sigma=frozendict({"Genre": "m", "Nombre": "s"}))
    actual = forme.to_nltk()
    expected = "N[Genre='m',Nombre='s'] -> '3'"
    assert actual == expected

    forme = FormeEntry(
        index=4,
        pos="N",
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(
                    stems=("a", "b", "c")
                ),
                sigma=frozendict({"Genre": "m", "Nombre": "s"})
            ),
            others=[
                create_morpheme(
                    rule="a+X",
                    sigma=frozendict({"Genre": "m", "Nombre": "s"}),
                    phonology=fx_df_phonology)
            ]
        ),
        sigma=frozendict({"Genre": "m", "Nombre": "s"})
    )

    actual = forme.to_nltk()
    expected = "N[Genre='m',Nombre='s'] -> '4'"
    assert actual == expected
