"""Realizer."""
from abc import abstractmethod


class Realizer[T, E]:
    """Réalise n'importe quel T en liste de E."""

    @abstractmethod
    def realize(self, lexeme: T) -> list[E]:
        """Réalise T en liste de E.

        :param lexeme:
        :return:
        """
