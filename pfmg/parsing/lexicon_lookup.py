"""Protocols for lexicon lookup at the parsing boundary."""

from collections.abc import Iterator
from typing import Protocol, runtime_checkable

from pfmg.lexique.forme.Forme import Forme


@runtime_checkable
class LexiconLookup(Protocol):
    """Tell whether a surface form belongs to one side of the lexicon."""

    def knows(self, item: str, how: str = "translation") -> bool:
        """Return True when *item* is a realized form on the side used by *how*."""


@runtime_checkable
class RealizedLexicon(LexiconLookup, Protocol):
    """A lexicon that has been realized into :class:`Forme` instances."""

    def __iter__(self) -> Iterator[Forme]:
        """Yield every realized form."""
