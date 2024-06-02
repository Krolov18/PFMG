# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Mixin définissant l'égalité par défaut."""

from pfmg.external.equality.ABCEquality import ABCEquality


class MixinEquality(ABCEquality):
    """Mixin définissant l'égalité par défaut."""

    def __eq__(self, other: ABCEquality):
        """Vérifie l'égalité entre deux objets.

        :param other: un autre object
        :return: bool
        """
        eq_rules = self.get_rule().string == other.get_rule().string
        return eq_rules and (
            (self.get_sigma().items() <= other.get_sigma().items())
            or (other.get_sigma().items() <= self.get_sigma().items())
        )
