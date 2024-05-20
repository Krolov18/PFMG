# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Doc."""

from dataclasses import dataclass

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.indexer import ABCindexer


@dataclass
class DesambIndexer(ABCindexer):
    """DesambIndexer."""

    lexicon: Lexicon

    def __call__(self, tokens: list[str]) -> list[list[str]]:
        """À l'aide d'un lexique indéxé, on checher tous les tokens.

        :param tokens: phrase utilisateur découpée en tokens
        :return: les séquences désambiguisées
        """
        assert tokens

        output = [list(map(str, self.lexicon[token])) for token in tokens]

        assert output
        return output
