# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Implémente les cases des paradigmes par POS."""

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.external.reader.ABCReader import ABCReader
from pfmg.lexique.glose import GlosesStruct, SubGlose, d_grid, l_grid


@dataclass
class Gloses(ABCReader):
    """Représente les cases des paradigmes.

    Quand cet objet est callé on récupère les cases
    du paradigme pour un POS donné.
    """

    source: SubGlose
    destination: SubGlose

    def __post_init__(self):
        """TODO : Doc to write."""
        self.struct = {
            k: [
                dict(zip(vars(self).keys(), sigma, strict=True))
                for sigma in product(self.source[k], self.destination[k])
            ]
            for k in self.source.keys()
            if k in self.source and k in self.destination
        }

    def __call__(
        self,
        pos: str,
    ) -> list[GlosesStruct]:
        """Rècupère un ensemble de sigma, soit un sigma par case.

        :param item: un POS valide
        :return: Les cases du paradigmes de 'item'
        """
        return self.struct[pos]  # type: ignore

    @classmethod
    def from_yaml(cls, path: Path) -> "Gloses":
        """Construit Gloses à partir d'un fichier YAML.

        :param path: Chemin vers le YAML des gloses de la grammaire.
        :return: Instance de Gloses
        """
        assert path.name.endswith("Gloses.yaml")
        with open(path, encoding="utf8") as file_handler:
            data: dict[str, dict[str, list[str]]] = yaml.load(
                file_handler, Loader=yaml.Loader
            )
        source = {
            category: list(cls.__gridify(att_vals))
            for category, att_vals in data["source"].items()
        }
        destination = {
            category: list(cls.__gridify(att_vals))
            for category, att_vals in data["destination"].items()
        }

        return cls(
            source=source,
            destination=destination,
        )

    @staticmethod
    def __gridify(grid: list | dict) -> Iterator[frozendict]:
        """Gridify a list or a dict.

        :param grid: dictionnaire Attribut -> [Valeurs]
                     ou liste de dictionnaires Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        method_name: str = (
            f"_{Gloses.__name__}__gridify_" f"{grid.__class__.__name__.lower()}"
        )
        return getattr(Gloses, method_name)(grid=grid)

    @staticmethod
    def __gridify_dict(grid: d_grid) -> Iterator[frozendict]:
        """Transform un dictionnaire Attribut -> [Valeurs] en un générateur.

        :param grid: dictionnaire Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        items: list[tuple[str, list[str]]] = sorted(grid.items())

        if not grid:
            # cas où grid est un dictionnaire vide
            return frozendict()

        keys, values = zip(*items, strict=True)
        for value in product(*values):
            yield frozendict(
                [
                    *zip(keys, value, strict=True),
                    *zip(value, keys, strict=True),
                ],
            )

    @staticmethod
    def __gridify_list(grid: l_grid) -> Iterator[frozendict]:
        """Gridify a list.

        :param grid: liste de dictionnaires Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        for i_grid in grid:
            yield from Gloses.__gridify_dict(i_grid)

    def __eq__(self, other: "Gloses") -> bool:  # type: ignore reportIncompatibleMethodOverride
        """Renvoie l'égalité entre self et other.

        :param other: Une autre Glose
        :return: bool
        """
        return (self.source == other.source) and (
            self.destination == other.destination
        )
