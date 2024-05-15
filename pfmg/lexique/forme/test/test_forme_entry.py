# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict

from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_to_string() -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa"))

    forme = FormeEntry(index=2,
                       pos="N",
                       morphemes=Morphemes(radical=Radical(
                           stems=StemSpace(stems=("a", "b", "c"))),
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
                stems=StemSpace(stems=("a", "b", "c"))),
            others=[
                create_morpheme(
                    rule="a+X",
                    sigma=frozendict({"Genre": "m", "Nombre": "s"}),
                    phonology=phonology
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
                           stems=StemSpace(stems=("a", "b", "c"))),
                           others=[]),
                       sigma=frozendict({"Genre": "m", "Nombre": "s"}))
    actual = forme.get_sigma()
    expected = frozendict({"Genre": "m", "Nombre": "s"})
    assert actual == expected


def test_to_nltk() -> None:
    phonology = Phonology(
        apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
        mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                             g="d", m="m", n="m", N="n", f="f",
                             s="f", S="s", v="f", z="v", Z="z",
                             r="w", l="r", j="w", w="w"),
        derives=frozendict(A="V", D="C"),
        consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
        voyelles=frozenset("iueoa")
    )

    forme = FormeEntry(index=3,
                       pos="N",
                       morphemes=Morphemes(radical=Radical(
                           stems=StemSpace(stems=("a", "b", "c"))),
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
                    stems=("a", "b", "c"))),
            others=[
                create_morpheme(
                    rule="a+X",
                    sigma=frozendict({"Genre": "m", "Nombre": "s"}),
                    phonology=phonology)
            ]
        ),
        sigma=frozendict({"Genre": "m", "Nombre": "s"})
    )

    actual = forme.to_nltk()
    expected = "N[Genre='m',Nombre='s'] -> '4'"
    assert actual == expected
