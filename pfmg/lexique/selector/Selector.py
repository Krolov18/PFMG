"""Selector."""
from abc import ABC, abstractmethod

from frozendict import frozendict
from lexique.lexical_structures.interfaces.Display import Display


class Selector(ABC):
    """Selector."""

    @abstractmethod
    def __call__(self, pos: str, sigma: frozendict) -> list[Display]:
        """Sélectionne une liste d'objets satisfaisant pos et sigma.

        :param pos: un POS
        :param sigma: un sigma
        :return: une liste d'objet pouvant être affichés
        """
