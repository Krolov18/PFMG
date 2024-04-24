# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""ABCSelector."""

from abc import ABC, abstractmethod

from frozendict import frozendict

from pfmg.external.display import ABCDisplay


class ABCSelector(ABC):
    """ABCSelector."""

    @abstractmethod
    def __call__(self, pos: str, sigma: frozendict) -> list[ABCDisplay]:
        """Sélectionne une liste d'objets satisfaisant pos et sigma.

        :param pos: un POS
        :param sigma: un sigma
        :return: une liste d'objet pouvant être affichés
        """
