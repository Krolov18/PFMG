# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Mixin utilisant re découper en tokens."""

import re

from pfmg.parsing.tokenizer.ABCTokenizer import ABCTokenizer


class TokenizerReMixin(ABCTokenizer):
    """Mixin pour découper des chaines de caractères avec le module re."""

    separator: str

    def tokenize(self, sentence: str) -> list[str]:
        """Découpe sentences en tokens.

        Le module re est utiliser ici pour découper.
        `separator` est donc un pattern indiquant le séparateur entre les
        tokens.

        :param sentence: Une chaine de caractères quelconque.
        :return: une liste de tokens
        """
        assert isinstance(sentence, str)
        assert sentence

        output = re.split(self.separator, sentence)

        assert output
        assert isinstance(output, list)

        return output
