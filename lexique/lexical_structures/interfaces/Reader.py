from abc import ABC, abstractmethod
from pathlib import Path


class Reader(ABC):
    """
    Base class qui liste les méthodes 
    pour les lire des fichiers depuis le disque.
    """

    @classmethod
    @abstractmethod
    def from_disk(cls, path: Path):
        """
        :param path:
        :return:
        """
