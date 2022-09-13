"""
    Fonctions permettant de valider les productions d'une grammaire.
    Fonctions permettant de séparer les contractions.
    Fonctions permettant de générer les productions non lexicales fournies dans Rules.yaml
"""
import itertools as it
import re
from functools import reduce
from operator import add
from typing import Iterator


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


@static_vars(  # type: ignore
    REG=re.compile(r"{(?: (\d+),(\d+) }|,(?: (\d+)}|(\d+)})|(\d+)(?: ,(?: (\d+)}|(\d+)})|,(?: (\d+)}|(\d+)})))")
)
def repeat(term: str) -> list[list[str]]:
    match term:
        case c if _is_q_mark(c):
            assert len(term.split("/")[1]) == 1
            return [[""], [term.split("/")[0]]]
        case c if _is_accolade(c):
            reg = getattr(repeat, "REG").search(term)
            deb: str
            fin: str
            assert reg
            deb, *fin = filter(None, reg.groups())
            term = term.rsplit("/", 1)[0]
            if not fin:
                return [([term] * i or [""]) for i in range(int(deb) + 1)]
            return [([term] * i or [""]) for i in range(int(deb), int(fin[0]) + 1)]
        case c if _is_star(c):
            raise NotImplementedError("Fonctionnalité non développée pour éviter l'infini")
        case c if _is_plus(c):
            raise NotImplementedError("Fonctionnalité non développée pour éviter l'infini")
        case _:
            assert term
            return [[term]]


def develop(rhs: list[str] | list[list[str]]) -> Iterator[list[str]]:
    match rhs:
        case [str(), *_]:
            for i_x in it.product(*(repeat(t) for t in rhs)):
                yield [f"'{i_y}'" if (i_y and i_y.islower()) else i_y for i_y in reduce(add, i_x)]
        case [list(), *_]:
            for i_x in rhs:
                yield from develop(i_x)


def cleave(word: str | list[str] | list[list[str]], morpho) -> list[str] | list[list[str]]:
    match word:
        case str() as c if c in morpho.contractions:
            return morpho.contractions[word]
        case str():
            return [word]
        case [str(), *_]:
            res: list[str] = []
            for i_w in word:
                res += cleave(i_w, morpho)
            return res
        case [list(), *_]:
            result: list[list[str]] = []
            for i_sent in word:
                result.append(cleave(i_sent, morpho))
            return result
