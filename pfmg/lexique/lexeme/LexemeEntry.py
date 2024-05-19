# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""LexemeEntry."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class LexemeEntry:
    """Léxème d'une source ou d'une destination.

    :param stems: Espace thématique d'un lexème
    :param pos: Catégorie morpho-syntaxique d'un léxème
    :param sigma: Dictionnaire figé représentation
                  les informations inhérentes d'un léxème
    """

    stems: StemSpace
    pos: str
    sigma: frozendict  # inhérence

    def __post_init__(self):
        """Vérifie que pos n'est pas vide."""
        assert self.pos

    def to_radical(self) -> Radical:
        """Convertir un Lexeme en un Radical.

        :return: un radical
        """
        return Radical(stems=self.stems, sigma=self.sigma)
