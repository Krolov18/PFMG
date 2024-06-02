# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Doc à écrire."""

from abc import ABC, abstractmethod

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCDecoupeur(ABC):
    """TODO : Doc à écrire."""

    @abstractmethod
    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
