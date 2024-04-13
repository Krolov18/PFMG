"""ABCRepresentor."""
from abc import ABC, abstractmethod


class ABCRepresentor(ABC):
    """ABCRepresentor."""

    @abstractmethod
    def __repr__(self) -> str:
        """Représente un object en string.
        
        :return: la représentation d'un objet
        """

    @abstractmethod
    def __str__(self) -> str:
        """Convertit un objet en string.
        
        :return: le string d'un objet
        """

    @abstractmethod
    def _repr_params(self) -> str:
        """Représente les params d'un objet.

        :return: la string des params d'un objet
        """
