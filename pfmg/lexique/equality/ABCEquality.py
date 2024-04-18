# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Interface définissant l'égalité."""

from abc import ABC, abstractmethod
from re import Match

from frozendict import frozendict


class ABCEquality(ABC):
    """Interface définissant l'égalité."""

    @abstractmethod
    def __eq__(self, other: "ABCEquality") -> bool:  # type: ignore reportIncompatibleMethodOverride
        """Calcule l'égalité entre deux objets.

        :param other: un autre objet pouvant être comparé
        :return: True si deux objets sont égaux
        """

    @abstractmethod
    def get_rule(self) -> Match:
        """Récupère le match de la régex.

        :return:
        """

    @abstractmethod
    def get_sigma(self) -> frozendict:
        """Récupère les propriétés d'un élément.

        :return:
        """
