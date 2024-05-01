# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Tokenizer sur les espaces."""

from pfmg.parsing.tokenizer.TokenizerReMixin import TokenizerReMixin


class SpaceTokenizer(TokenizerReMixin):
    """Le plus basique des Tokenizers.

    Découpe sur les espaces uniquement.
    """

    separator = " "
