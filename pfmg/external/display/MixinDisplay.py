# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Mixin pour la représentation des objects."""

from pfmg.external.display.ABCDisplay import ABCDisplay
from pfmg.lexique.stem_space.StemSpace import StemSpace


class MixinDisplay(ABCDisplay):
    """Mixin qui implémente la factory to_string."""

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Transforme un objet en un string le décrivant.

        :param term: radical utiliser pour représenter un objet
            StemSpace: objet avec plusieurs radicaux
            str: objet avec un seul radical
            None: objet sans radical
        :return: une string décrivant l'objet
        """
        return getattr(self, f"_to_string__{term.__class__.__name__.lower()}")(
            term=term,
        )

    def _to_string__str(self, term: str) -> str:
        """TODO : Doc à écrire."""
        raise NotImplementedError

    def _to_string__nonetype(self, term: None = None) -> str:
        """TODO : Doc à écrire."""
        raise NotImplementedError

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """TODO : Doc à écrire."""
        raise NotImplementedError
