from abc import ABC, abstractmethod


class Rulable(ABC):
    @abstractmethod
    def to_unary(self) -> str:
        """
        :return: Une représentation de l'objet sous forme
                 de règle de production au format NLTK.
        """
