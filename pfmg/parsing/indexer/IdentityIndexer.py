"""Indexer that leaves tokens untouched."""

from dataclasses import dataclass

from pfmg.parsing.indexer import ABCindexer


@dataclass
class IdentityIndexer(ABCindexer):
    """Maps every token to itself: for grammars whose terminals are words."""

    def __call__(self, tokens: list[str]) -> list[list[str]]:
        """Return one single-element candidate list per token."""
        assert tokens

        return [[token] for token in tokens]
