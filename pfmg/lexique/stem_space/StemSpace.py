# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""StemSpace."""

from dataclasses import dataclass


@dataclass
class StemSpace:
    """StemSpace."""

    stems: tuple[str, ...]

    def __post_init__(self):
        """Vérifie que stems et lemma ne sont pas vides."""
        assert self.stems
        self.lemma = self.stems[0]
        assert self.lemma

    @classmethod
    def from_string(cls, key: str) -> "StemSpace":
        """Construit un StemSpace à partir d'une chaine de caractères."""
        assert key
        return cls(stems=tuple(key.split(",")))
