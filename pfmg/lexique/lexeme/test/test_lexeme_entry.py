# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from frozendict import frozendict
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


@pytest.mark.parametrize("stems, pos, sigma", [
    (("stem",), "pos", {"sigma": "sigma"}),
])
def test_lexeme(stems, pos, sigma) -> None:
    lexeme = LexemeEntry(stems=StemSpace(stems), pos=pos, sigma=frozendict(sigma))

    assert isinstance(lexeme.stems, StemSpace)
    assert isinstance(lexeme.pos, str)
    assert isinstance(lexeme.sigma, frozendict)

    actual = lexeme.to_radical()
    expected = Radical(stems=StemSpace(stems), sigma=frozendict(sigma))
    assert actual == expected


@pytest.mark.parametrize("stems, pos, sigma", [
    ("", "N", {"Genre": "m"}),
    (",rad2,rad3", "N", {"Genre": "m"}),
    ("rad1,rad2,rad3", "", {"Genre": "m"}),
])
def test_assertions(stems, pos, sigma) -> None:
    with pytest.raises(AssertionError):
        _ = LexemeEntry(
            stems=StemSpace.from_string(stems),
            pos=pos,
            sigma=frozendict(sigma)
        )
