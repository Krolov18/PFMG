# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Rulable."""

from abc import ABC, abstractmethod


class Rulable(ABC):
    """Rulable."""

    @abstractmethod
    def to_lexical(self) -> str:
        """Transforme un objet en une production lexicale.

        :return: Une représentation de l'objet sous forme
                 de règle de production au format NLTK.
        """
