"""Abstract base for realizers: T -> iterable of E."""

from abc import abstractmethod
from collections.abc import Iterator


class ABCRealizable[T, E]:
    """Abstract base for objects that realize a T (e.g. Lexeme) as a sequence of E (e.g. Forme)."""

    @abstractmethod
    def realize(self, lexeme: T) -> Iterator[E]:
        """Yield realized instances (e.g. Forme) for the given lexeme."""
