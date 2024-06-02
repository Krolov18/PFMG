# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Interface pour les objets qui doivent renvoyer une glose formatée."""

from abc import ABC, abstractmethod

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCGloser(ABC):
    """Contient les méthodes pour construire des gloses formatées."""

    @abstractmethod
    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
