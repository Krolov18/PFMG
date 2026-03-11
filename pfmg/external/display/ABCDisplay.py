"""Interface pour la représentation des objets."""

from abc import ABC, abstractmethod

from frozendict import frozendict

from pfmg.lexique.stem_space.StemSpace import StemSpace


class ABCDisplay(ABC):
    """Interface pour la représentation des objets."""

    @abstractmethod
    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Convertit un objet en string.

        :param term:
        :return:
        """

    @abstractmethod
    def get_sigma(self) -> frozendict:
        """Renvoie les propriété d'un objet.

        :return:
        """
