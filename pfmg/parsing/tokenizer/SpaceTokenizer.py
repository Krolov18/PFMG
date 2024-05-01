"""Tokenizer sur les espaces."""

from pfmg.parsing.tokenizer.TokenizerReMixin import TokenizerReMixin


class SpaceTokenizer(TokenizerReMixin):
    """Le plus basique des Tokenizers.

    Découpe sur les espaces uniquement.
    """

    separator = " "
