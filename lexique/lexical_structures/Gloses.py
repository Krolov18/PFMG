from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Iterator, Literal, overload

import yaml
from frozendict import frozendict

from lexique.lexical_structures.interfaces.Reader import Reader

d_grid = dict[str, list[str]]
l_grid = list[dict[str, list[str]]]
d_or_l_grid = d_grid | l_grid

SubGlose = dict[str, list[frozendict]]


@dataclass
class Gloses(Reader):
    source: SubGlose
    destination: SubGlose

    def __post_init__(self):
        self.struct = {k: [dict(zip(vars(self).keys(), sigma))
                           for sigma in
                           product(self.source[k], self.destination[k])]
                       for k in self.source.keys()
                       if k in self.source and k in self.destination}

    def __call__(
        self,
        pos: str
    ) -> list[dict[Literal["source", "destination"], str]]:
        return self.struct[pos]

    @classmethod
    def from_disk(cls, path: Path) -> 'Gloses':
        assert path.name.endswith("Gloses.yaml")
        with open(path, mode="r", encoding="utf8") as file_handler:
            data: dict[str, dict[str, list[str]]] = yaml.load(
                file_handler,
                Loader=yaml.Loader
            )
        source = {category: list(cls.__gridify(att_vals))
                  for category, att_vals in data["source"].items()}
        destination = {category: list(cls.__gridify(att_vals))
                       for category, att_vals in data["destination"].items()}

        return cls(
            source=source,
            destination=destination
        )

    @staticmethod
    @overload
    def __gridify(grid: dict[str, list[str]]) -> Iterator[frozendict]:
        ...

    @staticmethod
    @overload
    def __gridify(grid: list[dict[str, list[str]]]) -> Iterator[frozendict]:
        ...

    @staticmethod
    def __gridify(grid) -> Iterator[frozendict]:
        """
        :param grid: dictionnaire Attribut -> [Valeurs]
                     ou liste de dictionnaires Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        method_name: str = (f"_{Gloses.__name__}__gridify_"
                            f"{grid.__class__.__name__.lower()}")
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
        for value in product(*values):
            yield frozendict(
                [*zip(keys, value),
                 *zip(value, keys)]
            )

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
