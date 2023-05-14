from dataclasses import dataclass
from pathlib import Path

import yaml

from lexique.types_for_kalaba import type_apophonies, type_derives, type_mutations, type_consonnes, type_voyelles
from lexique_2.lexical_structures.interfaces.Reader import Reader


@dataclass
class Phonology(Reader):
    """
    DataClass encodant les informations phonologiques.
    :param apophonies : Modifications phonétiques des voyelles.
    :param derives : ...
    :param mutations : Modifications phonétiques des consonnes.
    :param consonnes : Ensemble des consonnes.
    :param voyelles : Ensemble des voyelles.
    """
    apophonies: type_apophonies
    derives: type_derives
    mutations: type_mutations
    consonnes: type_consonnes
    voyelles: type_voyelles

    @classmethod
    def from_disk(cls, path: Path) -> 'Phonology':
        assert path.name.endswith("Phonology.yaml")

        with open(path, mode="r", encoding="utf8") as file_handler:
            data = yaml.load(file_handler, Loader=yaml.Loader)

        return cls(apophonies=data["apophonies"],
                   derives=data["derives"],
                   mutations=data["mutations"],
                   consonnes=data["consonnes"],
                   voyelles=data["voyelles"])
