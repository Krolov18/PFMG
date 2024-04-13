"""Searchable."""
from abc import ABC, abstractmethod


class Searchable(ABC):
    """Searchable."""

    @abstractmethod
    def search(self, pos: str, value: str) -> str:
        """TODO : documenter cette méthode.

        :param pos:
        :param value:
        :return:
        """

    @abstractmethod
    def is_pos(self, pos: str) -> bool:
        """Savoir si pos est un pos ou pas.

        :param pos: clé de premier niveau
        :return: si oui ou non cette clé dans la structure
        """
