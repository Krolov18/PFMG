"""Indexer that disambiguates token sequences using a lexicon."""

from dataclasses import dataclass

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.indexer import ABCindexer


@dataclass
class DesambIndexer(ABCindexer):
    """Resolves each token to a list of possible indices via the lexicon."""

    lexicon: Lexicon

    def __call__(self, tokens: list[str]) -> list[list[str]]:
        """Return disambiguated sequences: for each token, list of lexicon indices."""
        assert tokens

        output = [list(map(str, self.lexicon[token])) for token in tokens]

        assert output
        return output
