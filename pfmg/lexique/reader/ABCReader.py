"""Reader."""

from abc import ABC, abstractmethod
from pathlib import Path


class ABCReader[T](ABC):
    """Construit un type depuis des infos sur le disque."""

    @classmethod
    @abstractmethod
    def from_disk(cls, path: Path) -> T:
        """Construit un type depuis un fichier sur le disque.

        :param path: Chemin du fichier
        :return: une instance T
        """
