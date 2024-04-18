# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Sentence."""

from dataclasses import dataclass

from pfmg.lexique.forme.Forme import Forme


@dataclass
class Sentence:
    """Représente une phrase dans notre système.

    :param words: une liste de formes
    """

    words: list[Forme]
