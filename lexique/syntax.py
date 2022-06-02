"""
    Fonctions permettant de valider les productions d'une grammaire.
    Fonctions permettant de séparer les contractions.
    Fonctions permettant de générer les productions non lexicales fournies dans Rules.yaml
"""
import itertools as it
import re
from functools import reduce
from operator import add
from typing import Dict, Iterator, List, NoReturn

from frozendict import frozendict  # type: ignore
from multimethod import overload, multimethod
from nltk import ParserI, Production, Feature, Variable  # type: ignore

from lexique.structures import MorphoSyntax
from utils.functions import static_vars


def _is_q_mark(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return term.endswith("?")


def _is_star(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return term.endswith("*")


def _is_plus(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return term.endswith("+")


def _is_accolade(term: str) -> bool:
    """
    :param term:
    :return:
    """
    return ("{" in term) or ("}" in term)


@overload
def repeat(term: str) -> List[List[str]]:
    """
    :param term:
    :return:
    """
    assert term
    return [[term]]


@overload  # type: ignore
def repeat(term: _is_q_mark) -> List[List[str]]:  # type: ignore
    """
    :param term:
    :return:
    """
    assert len(term.split("/")[1]) == 1
    return [[""], [term.split("/")[0]]]


@static_vars(  # type: ignore
    REG=re.compile(r"{(?: (\d+),(\d+) }|,(?: (\d+)}|(\d+)})|(\d+)(?: ,(?: (\d+)}|(\d+)})|,(?: (\d+)}|(\d+)})))")
)
@overload
def repeat(term: _is_accolade) -> List[List[str]]:  # type: ignore
    """
    :param term:
    :return:
    """
    reg = getattr(repeat, "REG").search(term)
    assert reg

    deb, *fin = list(filter(None, reg.groups()))

    term = term.rsplit("/", 1)[0]
    if not fin:
        return [([term] * i or [""]) for i in range(int(deb) + 1)]
    return [([term] * i or [""]) for i in range(int(deb), int(fin[0]) + 1)]


@overload  # type: ignore
def repeat(term: _is_star) -> NoReturn:  # type: ignore
    """
    :param term:
    :return:
    """
    raise NotImplementedError("Fonctionnalité non développée pour éviter l'infini")


@overload  # type: ignore
def repeat(term: _is_plus) -> NoReturn:  # type: ignore
    """
    :param term:
    :return:
    """
    raise NotImplementedError("Fonctionnalité non développée pour éviter l'infini")


# @multimethod
# def develop(rhs: Dict[str, List[List[str]]]) -> Iterator[str]:
#     """
#     :param rhs:
#     :return:
#     """
#     assert rhs
#
#     for lhs, rhss in rhs.items():
#         yield from (f"{lhs} -> {y}" for y in develop(rhss))


# # pylint: disable=function-redefined
# @multimethod  # type: ignore
# def develop(rhs: Dict[str, Dict[str, List[List[str]]]]) -> Iterator[str]:
#     """
#     :param rhs:
#     :return:
#     """
#     assert rhs
#
#     for lhs, perco_rhss in rhs.items():
#         for perco, rhss in perco_rhss.items():
#             for rule in develop(rhss):
#                 yield f"{lhs}[{perco}] -> {rule}"


# pylint: disable=function-redefined
@multimethod  # type: ignore
def develop(rhs: List[str]) -> Iterator[List[str]]:
    """
    :param rhs:
    :return:
    """
    assert rhs

    for i_x in it.product(*(repeat(t) for t in rhs)):
        yield [f"'{i_y}'" if (i_y and i_y.islower()) else i_y for i_y in reduce(add, i_x)]


# pylint: disable=function-redefined
@multimethod  # type: ignore
def develop(rhs: List[List[str]]) -> Iterator[List[str]]:
    """
    :param rhs:
    :return:
    """
    assert rhs

    for i_x in rhs:
        yield from develop(i_x)


@multimethod
def cleave(word: str, morpho: MorphoSyntax) -> List[str]:
    """
    En prétraitement d'un prasing, on choisit de remplacer certaines chaines comme au > [à, les]
    :param word : mot à tester s'il existe dans contractions
    :param morpho : Structure encodant les données morphosyntaxiques
    :return : une liste de tokens
    """
    return [word] if word not in morpho.contractions else morpho.contractions[word]


# pylint: disable=function-redefined
@multimethod  # type: ignore
def cleave(word: List[str], morpho: MorphoSyntax) -> List[str]:
    """
    :param word:
    :param morpho:
    :return:
    """
    words: List[str] = []
    for i_w in word:
        words += cleave(i_w, morpho)
    return words


@multimethod  # type: ignore
def cleave(word: List[List[str]], morpho: MorphoSyntax) -> List[List[str]]:
    """
    :param word:
    :param morpho:
    :return:
    """
    wordss: List[List[str]] = []

    for i_sent in word:
        wordss.append(cleave(i_sent, morpho))
    return wordss


__all__ = ["repeat",
           "develop",
           "cleave"]
