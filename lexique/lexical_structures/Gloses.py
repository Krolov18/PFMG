from dataclasses import dataclass
import itertools as it
from functools import cache
from pathlib import Path
from typing import Iterator

import yaml
from frozendict import frozendict

from lexique.lexical_structures.interfaces.Reader import Reader
from lexique.lexical_structures.interfaces.Searchable import Searchable

d_grid = dict[str, list[str]]
l_grid = list[dict[str, list[str]]]
d_or_l_grid = d_grid | l_grid


@dataclass
class Gloses(Reader, Searchable):
    """
    Structure contenant les informations morphosyntaxiques
    par catégorie grammaticale.
    Attributes :
        data : membre contenant la structure
    """
    data: dict[str, list[frozendict]]

    @classmethod
    # @cache
    def from_disk(cls, path: Path) -> 'Gloses':
        """
        Cette méthode de classe est décorée de 'cache'
        afin de rendre cette méthode "comme" un singleton
        Si cette méthode est appelée plusieurs fois avec
        le même paramètre alors cette fonction sera exécutée
        la première fois, puis récupérée en cache les autres fois.
        :param path:
        :return:
        """
        assert path.name.endswith("Gloses.yaml")
        with open(path, mode="r", encoding="utf8") as file_handler:
            data: dict[str, dict[str, list[str]]] = yaml.load(
                file_handler,
                Loader=yaml.Loader
            )
        return cls(data={category: list(cls.__gridify(att_vals))
                         for category, att_vals in data.items()})

    @staticmethod
    def __gridify(grid: d_or_l_grid) -> Iterator[frozendict]:
        """
        :param grid: dictionnaire Attribut -> [Valeurs]
                     ou liste de dictionnaires Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        method_name: str = f"_{Gloses.__name__}__gridify_{grid.__class__.__name__.lower()}"
        return getattr(Gloses, method_name)(grid=grid)

    @staticmethod
    def __gridify_dict(grid: d_grid) -> Iterator[frozendict]:
        """
        Transforme un dictionnaire Attribut -> [Valeurs]
        en un générateur de Gloses.
        :param grid: dictionnaire Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        items: list[tuple[str, list[str]]] = sorted(grid.items())  # noqa

        if not grid:
            # cas où grid est un dictionnaire vide
            return frozendict()

        keys, values = zip(*items)
        for value in it.product(*values):
            yield frozendict([*zip(keys, value),
                              *zip(value, keys)])

    @staticmethod
    def __gridify_list(grid: l_grid) -> Iterator[frozendict]:
        """
        :param grid: liste de dictionnaires Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        if not grid:
            # cas où grid est une liste vide
            yield []
            return
        for i_grid in grid:
            yield from Gloses.__gridify_dict(i_grid)

    def search(self, pos: str, value: str) -> str | None:
        """
        Méthode qui permet de rechercher une glose
        à partir d'une catégorie grammaticale et d'une valeur.
        :param pos: Catégorie grammaticale.
        :param value: Valeur recherchée.
        :return: Glose correspondante.
        """
        if (result := next((sigma[value]
                            for sigma in self.data[pos]
                            if value in sigma), None)) is None:
            raise ValueError(pos, value)
        return result

    def is_pos(self, pos: str) -> bool:
        """
        Méthode qui permet de savoir si une catégorie grammaticale est présente dans la structure.
        :param pos: Catégorie grammaticale.
        :return: Présence de la catégorie grammaticale.
        """
        return pos in self.data
