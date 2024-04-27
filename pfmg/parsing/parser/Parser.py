# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from collections.abc import Iterator
from dataclasses import dataclass

from pfmg.lexique.lexicon import Lexicon
from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.parsable import ABCParsable


@dataclass
class Parser(ABCParsable):
    """TODO : Write some doc."""

    lexique: Lexicon
    grammar: Grammar

    def parse_one(self, sent: str) -> Sentence | None:
        """TODO : Write some doc."""
        raise NotImplementedError

    def parse_all(self, sent: str) -> Iterator[Sentence]:
        """TODO : Write some doc."""
        raise NotImplementedError

    def parse_sents(self, sents: Iterator[str]) -> Iterator[Iterator[Sentence]]:
        """TODO : Write some doc."""
        raise NotImplementedError
