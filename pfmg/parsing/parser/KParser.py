# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

from pfmg.external.reader import ABCReader
from pfmg.parsing.parser import Parser


@dataclass
class KParser(ABCReader):
    """Parser bipartite.

    Le KParser va parser une première pour traduire
    puis une seconde fois pour valider la traduction.
    """

    translator: Parser
    validator: Parser

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """TODO : Write some doc."""
        from pfmg.lexique.lexicon import Lexicon
        from pfmg.parsing.grammar import KGrammar

        lexicon = Lexicon.from_yaml(path)
        grammar = KGrammar.from_yaml(path)
        return cls(
            translator=Parser(lexique=lexicon, grammar=grammar.translator),
            validator=Parser(
                lexique=lexicon.to_validation(), grammar=grammar.validator
            ),
        )
