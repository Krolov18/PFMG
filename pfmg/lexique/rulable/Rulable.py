"""Rulable."""
from abc import ABC, abstractmethod


class Rulable(ABC):
    """Rulable."""

    @abstractmethod
    def to_lexical(self) -> str:
        """Transforme un objet en une production lexicale.

        :return: Une représentation de l'objet sous forme
                 de règle de production au format NLTK.
        """
