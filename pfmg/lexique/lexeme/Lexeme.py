# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Lexeme."""

from dataclasses import dataclass

from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry


@dataclass
class Lexeme:
    """Léxème à deux faces qui inclue la traduction.

    :param source: Léxème de langue source
    :param destination: Léxème de la langue de destination
    """

    source: LexemeEntry
    destination: LexemeEntry
