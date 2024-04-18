# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
from frozendict import frozendict

from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_morpheme() -> None:
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
    morpheme = Morphemes(
        radical=Radical(stems=StemSpace(("radical",))),
        others=[
            create_morpheme(
                rule="a+X",
                sigma=frozendict({"Genre": "m"}),
                phonology=phonology
            ),
            create_morpheme(
                rule="b+X",
                sigma=frozendict({"Nombre": "s"}),
                phonology=phonology)]
    )
    assert morpheme.radical == Radical(stems=StemSpace(("radical",)))
    expected_morphemes = [
        create_morpheme(
            rule="a+X",
            sigma=frozendict({"Genre": "m"}),
            phonology=phonology
        ),
        create_morpheme(
            rule="b+X",
            sigma=frozendict(
                {"Nombre": "s"}),
            phonology=phonology
        )
    ]
    assert morpheme.others == expected_morphemes
