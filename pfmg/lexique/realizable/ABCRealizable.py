"""ABCRealizer."""

from abc import abstractmethod
from collections.abc import Iterator


class ABCRealizable[T, E]:
    """Réalise n'importe quel T en liste de E."""

    @abstractmethod
    def realize(self, lexeme: T) -> Iterator[E]:
        """Réalise T en liste de E.

        :param lexeme:
        :return:
        """
