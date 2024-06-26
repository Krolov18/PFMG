# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Implémente les cases des paradigmes par POS."""

from dataclasses import dataclass
from pathlib import Path

import yaml

from pfmg.external.reader import ABCReader
from pfmg.lexique.sigma.Sigmas import Sigmas


@dataclass
class StraightPos2Sigmas(ABCReader):
    """Structure simulant les cases des paradigmes d'une langue.

    Un ensemble de case représente un paradigme.
    Les Sigmas sont les étiquettes des cases.
    Les cases d'un paradigmes sont dirigés par le POS.

    Args:
    ----
        data: Structure interne contenant les différents paradigmes.

    """

    data: dict[str, Sigmas]

    def __call__(self, pos: str) -> Sigmas:
        """Récupère le paradigme d'un 'pos' donné.

        :param pos: un POS existant dans la structure interne
        :return: les Sigmas pour le 'pos' donné
        :raise KeyError: Si le 'pos' n'existe pas
        """
        return self.data[pos]

    @classmethod
    def from_yaml(cls, path: Path | str) -> "StraightPos2Sigmas":
        """Construit un Gloses à partir d'un fichier YAML.

        :param path: Chemin vers le fichier YAML.
        :return: Un Gloses valide et prêt à l'emploi
        """
        path = Path(path)
        assert path.name.endswith("Gloses.yaml")
        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "StraightPos2Sigmas":
        """Construit un Gloses à partir d'un dictionnaire.

        :param data: doit contenir au deuxième niveau 'source' et 'destination'
        :return: une instance de Gloses
        """
        return cls(
            data={
                pos: Sigmas.from_dict(sigmas["source"], sigmas["destination"])
                for pos, sigmas in data.items()
            }
        )
