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
        return re.split(self.separator, sentence)
