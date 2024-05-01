# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass

from pfmg.lexique.stem_space.StemSpace import StemSpace
from pfmg.parsing.production import Production


@dataclass
class Grammar:
    """TODO : Write some doc."""

    start: str
    productions: list[Production]

    def to_nltk(self, term: StemSpace | str | None = None) -> str:
        """Convertit la Grammar en une chaîne de caractère pour NLTK.

        :param term: inutile pour cette implémentation
        :return: Une grammaire parsable par FeatureGrammar.fromstring
        """
        return "\n\n".join(
            (
                f"% start {self.start}",
                "\n".join(x.to_nltk() for x in self.productions),
            )
        )
