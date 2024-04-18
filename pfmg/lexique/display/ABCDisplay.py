# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Interface pour la représentation des objets."""

from abc import ABC, abstractmethod

from frozendict import frozendict

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCDisplay(ABC):
    """Interface pour la représentation des objets."""

    @abstractmethod
    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Convertit un objet en string.

        :param term:
        :return:
        """

    @abstractmethod
    def get_sigma(self) -> frozendict:
        """Renvoie les propriété d'un objet.

        :return:
        """

    @abstractmethod
    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Inner function quand term est un stem_space.

        :param term:
        :return:
        """

    @abstractmethod
    def _to_string__str(self, term: str) -> str:
        """Inner function quand term est un string.

        :param term:
        :return:
        """

    @abstractmethod
    def _to_string__nonetype(self, term: None = None) -> str:
        """Inner function quand term est None.

        :param term:
        :return:
        """
