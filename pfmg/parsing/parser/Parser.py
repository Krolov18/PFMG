# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""
from collections.abc import Iterator
from dataclasses import dataclass

import nltk.grammar
from nltk import EarleyChartParser

from pfmg.lexique.lexicon import Lexicon
from pfmg.lexique.sentence.Sentence import Sentence
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.parsable.MixinParseParsable import MixinParseParsable


@dataclass
class Parser(MixinParseParsable):
    """TODO : Write some doc."""

    lexique: Lexicon
    grammar: Grammar
    how: str

    def __post_init__(self):
        """TODO : Write some doc."""
        grammar = nltk.grammar.FeatureGrammar.fromstring(
            "\n\n".join(
                (self.grammar.to_nltk(),
                 getattr(self.lexique, f"to_{self.how}")())
            )
        )
        self.parser = EarleyChartParser(grammar)

    def _parse_first_str(self, data: str) -> Sentence:
        raise NotImplementedError

    def _parse_first_list(self, data: list[str]) -> Iterator[Sentence]:
        raise NotImplementedError

    def _parse_all_str(self, data: str) -> Iterator[Sentence]:
        raise NotImplementedError

    def _parse_all_list(self, data: list[str]) -> Iterator[Sentence]:
        raise NotImplementedError
