"""Indexer that disambiguates token sequences using a lexicon."""

from dataclasses import dataclass

from pfmg.parsing.indexer import ABCindexer
from pfmg.parsing.lexicon_index import LexiconIndex


@dataclass
class DesambIndexer(ABCindexer):
    """Resolves each token to a list of possible indices via the lexicon.

    Attributes:
        lexicon: Lexicon holding the form -> indexes maps.
        how: Side of the lexicon to look tokens up in ("translation" for the
            source forms, "validation" for the destination ones).

    """

    lexicon: LexiconIndex
    how: str = "translation"

    def __call__(self, tokens: list[str]) -> list[list[str]]:
        """Return disambiguated sequences: for each token, list of lexicon indices."""
        assert tokens

        output = [
            list(map(str, self.lexicon.get_indexes(token, self.how)))
            for token in tokens
        ]

        unknown = [
            token for token, indexes in zip(tokens, output, strict=True) if not indexes
        ]
        assert not unknown, f"Ces mots sont inconnus du lexique : {unknown}"
        return output
