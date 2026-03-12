"""Lexicon utilities: dictify, gridify (cartesian product of traits)."""

from ast import literal_eval
from itertools import product
from typing import overload

from frozendict import frozendict

from pfmg.utils.abstract_factory import factory_function


def dictify(chars: str) -> frozendict:
    """Parse a key=value,key=value string into a frozendict."""
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
    """Cartesian product of trait values; returns a list of frozendict (sigmas)."""
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
    """Cartesian product per grid element; returns nested list of sigmas."""
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
    """Build sigmas from a parameter grid (dict or list); dispatches to gridify_dict or gridify_list."""
    name = f"gridify_{type(grid).__name__}"
    return factory_function(concrete_product=name, package=__name__, grid=grid)
