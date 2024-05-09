# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Informations morphosyntaxiques d'une Forme."""

from dataclasses import dataclass

from frozendict import frozendict


@dataclass
class Sigma:
    """Informations morphosyntaxiques d'une Forme.

    Args:
    ----
        source: Dictionnaire non éditable
        destination: Dictionnaire non éditable

    """

    source: frozendict[str, str]
    destination: frozendict[str, str]

    def __le__(self, other: "Sigma") -> bool:
        """Vérifie si les clés/valeurs de other.source sont dans self.source.

        :param other: un autre Sigma
        :return: True si les clés/valeurs de other.source sont dans self.source
        """
        return (self.source.items() <= other.source.items()) and (
            self.destination.items() <= other.destination.items()
        )
