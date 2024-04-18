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
    (("stem",), "pos", frozendict({"sigma": "sigma"})),
])
def test_lexeme(stems, pos, sigma) -> None:
    lexeme = LexemeEntry(stems=StemSpace(stems),
                         pos=pos,
                         sigma=sigma)
    assert lexeme.stems == StemSpace(stems)
    assert lexeme.pos == pos
    assert lexeme.sigma == sigma
    assert lexeme.to_radical() == Radical(stems=StemSpace(stems))
