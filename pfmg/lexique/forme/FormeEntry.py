# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Entry d'une Forme."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class FormeEntry(MixinDisplay, ABCGloser):
    """La forme est la réalisation d'un lexème."""

    pos: str
    morphemes: Morphemes
    sigma: frozendict[str, str]
    index: int

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return self.morphemes.to_string(term)

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return self.morphemes.to_decoupe(term)

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return self.morphemes.to_glose(term)

    def get_sigma(self) -> frozendict:
        """Récupère le sigma d'une Forme.

        :return: le sigma d'une Forme
        """
        return self.sigma

    def to_nltk(self, infos: dict | None = None) -> str:
        """Transforme la Forme en une production lexicale.

        :return: une production lexicale
        """
        name = (
            f"_{self.__class__.__name__}__to_nltk_"
            f"{type(infos).__name__.lower()}"
        )
        return getattr(self, name)(infos)

    def __to_nltk_nonetype(self, infos: None = None) -> str:
        assert infos is None

        sigma = {
            key: value
            for key, value in self.get_sigma().items()
            if key.istitle()
        }
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{self.pos}[{features}] -> '{self.index}'"

    def __to_nltk_dict(self, infos: dict) -> str:
        assert isinstance(infos, dict)
        sigma = {
            f"S{key}": value
            for key, value in self.get_sigma().items()
            if key.istitle()
        }
        sigma.update(infos)
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{self.pos}[{features}] -> '{self.index}'"
