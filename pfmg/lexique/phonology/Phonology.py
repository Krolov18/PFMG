"""Phonology."""
from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.lexique.reader.ABCReader import ABCReader


@dataclass
class Phonology(ABCReader):
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

    apophonies: frozendict
    derives: frozendict
    mutations: frozendict
    consonnes: frozenset
    voyelles: frozenset

    @classmethod
    def from_disk(cls, path: Path) -> "Phonology":
        """Construit un Phonology à partir d'un Fichier YAML.

        :param path: Chemin vers le fichier YAML
        :return: une instance de Phonology
        """
        assert path.name.endswith("Phonology.yaml")

        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)

        return cls(**Phonology.from_json(data))

    def to_json(self) -> dict:
        """Convertit les membres en un dictionnaire sérialisable par JSON/YAML
        :return: un dico des memebres de Phonology
        """
        return {
            "apophonies": dict(self.apophonies),
            "derives": dict(self.derives),
            "mutations": dict(self.mutations),
            "consonnes": list(self.consonnes),
            "voyelles": list(self.voyelles),
        }

    @staticmethod
    def from_json(data: dict) -> dict:
        """Met data au bon format.
        :reurn: les membres de phonologie au bon format
        """
        return {
            "apophonies": frozendict(data["apophonies"]),
            "derives": frozendict(data["derives"]),
            "mutations": frozendict(data["mutations"]),
            "consonnes": frozenset(data["consonnes"]),
            "voyelles": frozenset(data["voyelles"]),
        }

