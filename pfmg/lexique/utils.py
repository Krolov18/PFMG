# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Différents utilitaires."""

from ast import literal_eval
from itertools import product
from typing import overload

from frozendict import frozendict

from pfmg.utils.abstract_factory import factory_function


def dictify(chars: str) -> frozendict:
    """Transforme une chaine de caractères en un frozendict.

    :param chars: Une chaine de caractère prête
                  à être parsée et convertie en frozendict.
    :return: un frozendict
    """
    return frozendict(
        (
            {}
            if chars == ""
            else literal_eval(
                ('{"' + chars.replace("=", '":"').replace(",", '","') + '"}'),
            )
        ),
    )


def gridify_dict(grid: dict[str, list[str]]) -> list[frozendict]:
    """Produit cartésien sur les Traits d'une langue.

    :param grid: Grille de paramètres
    :return: liste de sigmas
    """
    assert isinstance(grid, dict)
    assert grid

    result = []

    keys, values = zip(*sorted(grid.items()), strict=True)
    for value in product(*values):
        assert value
        result.append(frozendict([*zip(keys, value, strict=True)]))

    assert result
    return result


def gridify_list(grid: list) -> list[list[frozendict]]:
    """Produit cartésien sur les Traits d'une langue.

    :param grid: Grille de paramètres
    :return: liste imbriquée de sigmas
    """
    assert isinstance(grid, list)
    assert grid

    result = []
    for i_grid in grid:
        result.append(gridify_dict(i_grid))

    assert result
    return result


@overload
def gridify(grid: dict) -> list[frozendict]: ...


@overload
def gridify(grid: list) -> list[list[frozendict]]: ...


def gridify(grid):
    """Factory qui construit les Sigmas.

    :param grid: une grilles de paramètres
    :return: Une liste de sigmas
    """
    name = f"gridify_{type(grid).__name__}"
    return factory_function(concrete_product=name, package=__name__, grid=grid)
