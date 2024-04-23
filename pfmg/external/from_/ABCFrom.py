from abc import ABC, abstractmethod

from pathlib import Path


class ABCFrom[T](ABC):
    """"""

    @classmethod
    @abstractmethod
    def from_yaml(cls, path: str | Path) -> T:
        """Construit un objet depuis un dossier contenant des YAML ou un fichier YAML.

        :param path: Chemin vers un dossier de YAML ou un fichier YAML
        :return: une instance de T
        """

