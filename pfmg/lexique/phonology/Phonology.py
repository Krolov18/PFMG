# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Phonology."""

from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.external.reader.ABCReader import ABCReader


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
    def from_yaml(cls, path: Path) -> "Phonology":
        """Construit un Phonology à partir d'un Fichier YAML.

        :param path: Chemin vers le fichier YAML
        :return: une instance de Phonology
        """
        assert path.name.endswith("Phonology.yaml")

        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)

        return cls(**Phonology.from_dict(data))

    def to_dict(self) -> dict:
        """Convertit la structure interne en JSON-compatible.

        :return: un dictionnaire sérialisable par JSON
        """
        return {
            "apophonies": dict(self.apophonies),
            "derives": dict(self.derives),
            "mutations": dict(self.mutations),
            "consonnes": list(self.consonnes),
            "voyelles": list(self.voyelles),
        }

    @staticmethod
    def from_dict(data: dict) -> dict:
        """Construit la strcture interne depuis un dict JSON.

        :param data: un dict provenant d'un fichier JSON
        :return: un dictionnaire formatté pour la structure interne à Phonology
        """
        return {
            "apophonies": frozendict(data["apophonies"]),
            "derives": frozendict(data["derives"]),
            "mutations": frozendict(data["mutations"]),
            "consonnes": frozenset(data["consonnes"]),
            "voyelles": frozenset(data["voyelles"]),
        }
