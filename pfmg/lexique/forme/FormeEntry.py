# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Entry d'une Forme."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.rulable.Rulable import Rulable


@dataclass
class FormeEntry(MixinDisplay, Rulable):
    """La forme est la réalisation d'un lexème.

    :param traduction : Réalisation du lexème de la traduction
    """

    pos: str
    morphemes: Morphemes
    sigma: frozendict[str, str]

    def _to_string__nonetype(self, term: None = None) -> str:
        result: str = ""
        for morpheme in self.morphemes.others:
            m_sigma = dict(self.sigma)
            m_sigma.update(morpheme.get_sigma())
            self.sigma = frozendict(m_sigma)
            result = morpheme.to_string(
                result or self.morphemes.radical.stems,
            )
        return result or self.morphemes.radical.stems.stems[0]

    def get_sigma(self) -> frozendict:
        """Récupère le sigma d'une Forme.

        :return: le sigma d'une Forme
        """
        return self.sigma

    def to_lexical(self) -> str:
        """Transforme la Forme en une production lexicale.

        :return: une production lexicale
        """
        sigma = {
            key: value
            for key, value in self.get_sigma().items()
            if key.istitle()
        }
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{self.pos}[{features}] -> '{self.to_string()}'"

    def to_partial_lexical(self) -> tuple[str, str]:
        """Transforme une Forme en une version partielle de production lexicale.

        :return: les features et la forme réalisée
        """
        sigma = {
            key: value
            for key, value in self.get_sigma().items()
            if key.istitle()
        }
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return features, self.to_string()
