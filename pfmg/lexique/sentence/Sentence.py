# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Sentence."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.display import ABCDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class Sentence(ABCDisplay, ABCGloser):
    """Représente une phrase dans notre système.

    :param words: une liste de formes
    """

    words: list[Forme]

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return " ".join(x.to_string() for x in self.words)

    def get_sigma(self) -> frozendict:
        """TODO : Doc à écrire."""
        sigma = {}
        for w in self.words:
            sigma.update(w.get_sigma())
        return frozendict(sigma)

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return " ".join(x.to_decoupe() for x in self.words)

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return " ".join(x.to_glose() for x in self.words)
