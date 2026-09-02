"""Protocols for lexicon lookup at the parsing boundary."""

from collections.abc import Iterator
from typing import Protocol, runtime_checkable

from pfmg.lexique.forme.Forme import Forme


@runtime_checkable
class LexiconIndex(Protocol):
    """Lookup realized forms by surface string and grammar side."""

    def get_indexes(self, item: str, how: str = "translation") -> list[int]:
        """Return form indexes for *item* on the side used by *how*."""


@runtime_checkable
class RealizedLexicon(LexiconIndex, Protocol):
    """A lexicon that has been realized into :class:`Forme` instances."""

    def __iter__(self) -> Iterator[Forme]:
        """Yield every realized form."""
