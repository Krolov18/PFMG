# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Structure de données pour représenter la réalisation d'un Léxème."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class Forme(MixinDisplay, ABCGloser):
    """Réalsation d'un Léxème."""

    source: FormeEntry
    destination: FormeEntry

    def __post_init__(self):
        """Vérifications post initialisation."""
        assert self.source.pos == self.destination.pos

    def to_translation(self) -> str:
        """Transforme une Forme en règle syntaxique lexicale.

        N[SGenre='m',DGenre='f',translation='hazif'] -> 'garçon'
        N[Genre='f'] -> 'hazif'

        :return: une production lexicale.
        """
        infos = {f"D{k}": v for k, v in self.destination.get_sigma().items()}
        infos["translation"] = self.destination.to_string()
        return self.source.to_nltk(infos)

    def to_validation(self):
        """TODO : Write some doc.

        :return:
        """
        return self.destination.to_nltk()

    def _to_string__nonetype(self, term: None = None) -> str:
        """Inner function pour représenter une forme.

        :param term:
        :return:
        """
        return self.source.to_string()

    def get_sigma(self) -> frozendict:
        """Récupère les propriétés d'une forme."""
        raise NotImplementedError

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return self.source.to_glose()

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        return self.source.to_decoupe()
