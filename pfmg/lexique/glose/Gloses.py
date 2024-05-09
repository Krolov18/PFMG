# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Implémente les cases des paradigmes par POS."""

from dataclasses import dataclass
from itertools import product
from pathlib import Path

import yaml

from pfmg.lexique.glose.Sigma import Sigma
from pfmg.lexique.glose.Sigmas import Sigmas
from pfmg.lexique.utils import gridify


@dataclass
class Gloses:
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
    def from_yaml(cls, path: Path | str) -> "Gloses":
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
    def from_dict(cls, data: dict) -> "Gloses":
        """Construit un Gloses à partir d'un dictionnaire.

        :param data: les données pour construire Gloses
        :return: Un Gloses valide et prêt à l'emploi
        """
        output = {}
        source = data["source"]
        dest = data["destination"]
        pos_sd = zip(source.keys(), source.values(), dest.values(), strict=True)
        for pos, *sd in pos_sd:
            output[pos] = Sigmas(
                [Sigma(x, y) for x, y in product(*gridify(list(sd)))]
            )
        return cls(data=output)
