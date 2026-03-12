"""Mixin that tokenizes strings using a regex separator."""

import re

from pfmg.parsing.tokenizer.ABCTokenizer import ABCTokenizer


class TokenizerReMixin(ABCTokenizer):
    """Mixin that splits strings into tokens using re and a separator pattern."""

    separator: str

    def __call__(self, sentence: str) -> list[str]:
        """Split sentence into tokens using the separator regex pattern."""
        assert isinstance(sentence, str)
        assert sentence

        output = re.split(self.separator, sentence)

        assert output
        assert isinstance(output, list)

        return output
