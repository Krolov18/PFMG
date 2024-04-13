"""Phonology."""
from dataclasses import dataclass
from pathlib import Path

import yaml

from pfmg.lexique.reader.Reader import Reader


@dataclass
class Phonology(Reader):
    """DataClass encodant les informations phonologiques.

    TODO : transformer cette classe en Singleton.
    Ce changement demandera de retirer tous les endroits
    où il existe des paramètres phonology.
    Il suffira de faire Phonology() partout où c'est utile.

    :param apophonies : Modifications phonétiques des voyelles.
    :param derives : ...
    :param mutations : Modifications phonétiques des consonnes.
    :param consonnes : Ensemble des consonnes.
    :param voyelles : Ensemble des voyelles.
    """

    apophonies: dict[str, str]
    derives: dict[str, str]
    mutations: dict[str, str]
    consonnes: set[str]
    voyelles: set[str]

    @classmethod
    def from_disk(cls, path: Path) -> "Phonology":
        """Construit un Phonology à partir d'un Fichier YAML.

        :param path: Chemin vers le fichier YAML
        :return: une instance de Phonology
        """
        assert path.name.endswith("Phonology.yaml")

        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)

        return cls(
            apophonies=data["apophonies"],
            derives=data["derives"],
            mutations=data["mutations"],
            consonnes=data["consonnes"],
            voyelles=data["voyelles"],
        )
