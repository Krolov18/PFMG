# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Mixin implémentant le comportement par défaut de __str__ et __repr__."""

from pfmg.lexique.representor.ABCRepresentor import ABCRepresentor


class MixinRepresentor(ABCRepresentor):
    """Mixin."""

    def __repr__(self) -> str:
        """Représente n'importe quel objet de la librairie."""
        return f"{self.__class__.__name__}({self._repr_params()})"

    def __str__(self) -> str:
        """Fonctionnement par défaut de __str__."""
        return repr(self)

    def _repr_params(self) -> str:
        raise NotImplementedError
