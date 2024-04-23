# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Structure qui rassemble un radical et ses morphèmes."""

from dataclasses import dataclass

from pfmg.external.display import ABCDisplay
from pfmg.lexique.morpheme.Radical import Radical


@dataclass
class Morphemes:
    """Structure qui rassemble un radical et ses morphèmes.

    radical: StemSpace d'un léxème
    others: liste des morphèmes d'une forme
    """

    radical: Radical
    others: list[ABCDisplay]
