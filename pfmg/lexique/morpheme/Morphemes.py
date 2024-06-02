# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Structure qui rassemble un radical et ses morphèmes."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.decoupeur.ABCDecoupeur import ABCDecoupeur
from pfmg.external.display import ABCDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class Morphemes(ABCDisplay, ABCGloser, ABCDecoupeur):
    """Structure qui rassemble un radical et ses morphèmes.

    radical: StemSpace d'un léxème
    others: liste des morphèmes d'une forme
    """

    radical: Radical
    others: list[ABCDisplay]

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        assert term is None
        result: str = ""
        for morpheme in self.others:
            result = morpheme.to_string(
                result or self.radical.stems,
            )
        return result or self.radical.lemma

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        assert term is None
        result: str = ""

        for morpheme in self.others:
            result += morpheme.to_decoupe(  # type: ignore
                result or self.radical.stems,
            )

        return result or self.radical.lemma

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        result = self.radical.to_glose()
        for morpheme in self.others:
            result = morpheme.to_glose(result)  # type: ignore

        return result or self.radical.lemma

    def get_sigma(self) -> frozendict:
        """TODO : Doc à écrire."""
        raise NotImplementedError
