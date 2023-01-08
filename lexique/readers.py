"""
queqerulquehiuve
"""

import itertools as it
from ast import literal_eval
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, TypedDict

import yaml
from frozendict import frozendict

from lexique.ruler import any_ruler
from lexique.structures import Phonology, Lexeme, Forme, type_Morpheme, Paradigm
from utils.abstract_factory import factory_function


class type_Phonology(TypedDict):
    consonnes: frozenset[str]
    voyelles: frozenset[str]
    mutations: frozendict
    derives: frozendict
    apophonies: frozendict


def gridify(grid: dict[str, list[str]] | list[dict[str, list[str]]]) -> Iterator[frozendict]:
    """
    :param grid:
    :return:
    """
    return factory_function(concrete_product=f"gridify_{grid.__class__.__name__.lower()}",
                            package=__name__,
                            grid=grid)


def gridify_dict(grid: dict[str, list[str]]) -> Iterator[frozendict]:
    """
    :param grid:
    :return:
    """
    items: list[tuple[str, list[str]]] = sorted(grid.items())

    if not items:
        raise ValueError()

    keys, values = zip(*items)
    if not all(keys) or not all(values):
        raise ValueError()
    for value in it.product(*values):
        yield frozendict(zip(keys, value))


def gridify_list(grid: list[dict[str, list[str]]]) -> Iterator[frozendict]:
    """
    :param grid:
    :return:
    """
    if not grid:
        raise ValueError()
    for i_grid in grid:
        yield from gridify_dict(i_grid)


def read_gloses(gloses_path: Path) -> dict[str, list[frozendict]]:
    """
    :param gloses_path: Chemin du fichier yaml
    :return: Lecteur/convertisseur des gloses en une table d'association catégorie / liste de sigmas
    """
    assert gloses_path.name.endswith("Gloses.yaml")
    with open(gloses_path, mode="r", encoding="utf8") as file_handler:
        data: dict[str, dict[str, list[str]]] = yaml.load(file_handler, Loader=yaml.Loader)
    return {category: list(gridify(att_vals)) for category, att_vals in data.items()}


def dictify_str(chars: str) -> frozendict:
    """
    :param chars: Une chaine de caractère prête à être parsée et convertie en frozendict.
    :return: Transforme une chaine de caractère en un frozendict python.
    """
    match chars:
        case "":
            return frozendict()
        case _:
            return frozendict(literal_eval("{\"" + chars.replace("=", "\":\"").replace(",", "\",\"") + "\"}"))


def rulify(block: dict[str, str] | list[dict[str, str]]
           ) -> Iterator[list[type_Morpheme]]:
    """
    :param block: Bloc ou liste de blocs de règles
    :return: liste de blocs au format frozendict/Morpheme
    """
    return factory_function(concrete_product=f"rulify_{block.__class__.__name__.lower()}",
                            package=__name__,
                            block=block)


def rulify_dict(block: dict[str, str]) -> Iterator[list[type_Morpheme]]:
    """
    :param block: Bloc de règles
    :return: liste de blocs au format frozendict/Morpheme
    """
    output: list[type_Morpheme] = []

    for key, value in block.items():
        _sigma = dictify_str(key)
        output.append(any_ruler(rule=value, sigma=_sigma))

    yield output


def rulify_list(block: list[dict[str, str]]) -> Iterator[list[type_Morpheme]]:
    """
    :param block: Liste de blocs de règles
    :return: liste de blocs au format frozendict/Morpheme
    """
    for i_block in block:
        yield from rulify_dict(i_block)


def read_blocks(blocks_path: Path) -> dict[str, list[list[type_Morpheme]]]:
    """
    :param blocks_path: Chemin vers le fichier contenant les blocs du langage
    :return: Table d'association entre un POS-Tag et une liste de règles (bloc)
    """
    assert blocks_path.name.endswith("Blocks.yaml")

    with open(blocks_path, mode="r", encoding="utf8") as file_handler:
        data: dict[str, list[dict[str, str]]] = yaml.load(file_handler, Loader=yaml.Loader)

    return {category: list(rulify(rules))
            for category, rules in data.items()}


def read_phonology(phonology_path: Path) -> Phonology:
    """
    :param phonology_path: Chemin vers le fichier contenant les informations phonologiques du langage
    :return: un Struct contenant les infos phonologiques
    """
    assert phonology_path.name.endswith("Phonology.yaml")

    with open(phonology_path, mode="r", encoding="utf8") as file_handler:
        data: type_Phonology = yaml.load(file_handler, Loader=yaml.Loader)

    return Phonology(apophonies=data["apophonies"],
                     derives=data["derives"],
                     mutations=data["mutations"],
                     consonnes=data["consonnes"],
                     voyelles=data["voyelles"])


def select_morpheme(sigma: frozendict, morphemes: list[type_Morpheme]) -> type_Morpheme:
    """
    :param sigma:
    :param morphemes:
    :return:
    """
    winner: type_Morpheme | None = None
    for morpheme in morphemes:
        assert morpheme.sigma is not None
        if morpheme.sigma.items() <= sigma.items():
            winner = morpheme
    assert winner
    return winner


def select_morphemes(sigma: frozendict, blocs: list[list[type_Morpheme]]) -> list[type_Morpheme]:
    """
    :param sigma:
    :param blocs:
    :return:
    """
    output: list[type_Morpheme] = []

    for bloc in blocs:
        try:
            output.append(select_morpheme(sigma, bloc))
        except AssertionError:
            continue

    return output
