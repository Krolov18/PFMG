"""ABCSelector."""
from abc import ABC, abstractmethod

from frozendict import frozendict

from pfmg.lexique.display.ABCDisplay import ABCDisplay


class ABCSelector(ABC):
    """ABCSelector."""

    @abstractmethod
    def __call__(self, pos: str, sigma: frozendict) -> list[ABCDisplay]:
        """Sélectionne une liste d'objets satisfaisant pos et sigma.

        :param pos: un POS
        :param sigma: un sigma
        :return: une liste d'objet pouvant être affichés
        """
