# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Ensemble de Sigma."""

import itertools as it
from collections.abc import Iterator
from dataclasses import dataclass

from pfmg.lexique.sigma.Sigma import Sigma
from pfmg.lexique.utils import gridify


@dataclass
class Sigmas:
    """Ensemble de Sigma."""

    data: list[Sigma]

    def __contains__(self, item: Sigma) -> bool:
        """TODO Doc à écrire.

        :param item:
        :return:
        """
        for x in self.data:
            if x <= item:
                return True
        return False

    def __iter__(self) -> Iterator[Sigma]:
        """Itérateur de Sigma.

        :return: un itérateur de Sigma
        """
        return iter(self.data)

    @classmethod
    def from_dict(cls, source: dict, destination: dict) -> "Sigmas":
        """Construit un Sigmas à partir de deux dictionnaires.

        :param source: la config de la langue source
        :param destination: la config de la langue de destination
        :return: Une instance de Sigmas
        """
        return cls(
            [Sigma(*x) for x in it.product(*gridify([source, destination]))]
        )
