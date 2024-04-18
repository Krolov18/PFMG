# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
from frozendict import frozendict
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.stem_space.StemSpace import StemSpace


def test_lexeme() -> None:
    source = LexemeEntry(
        stems=StemSpace(("gitun",)),
        pos="N",
        sigma=frozendict(genre="f"),
    )
    destination = LexemeEntry(
        stems=StemSpace(("banane",)),
        pos="N",
        sigma=frozendict(cf=1),
    )
    lexeme = Lexeme(
        source=source,
        destination=destination,
    )
    assert lexeme.source == source
    assert lexeme.destination == destination
