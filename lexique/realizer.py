"""
    Fonctions permettant de réaliser les différentes structures définies dans structures.py
"""
from typing import Callable, Dict, List, Tuple, Union

from frozendict import frozendict
from multimethod import multimethod, DispatchError

from lexique.applier import format_stem, apply
from lexique.structures import (Circumfix, Forme, Gabarit,
                                Lexeme, Prefix, Suffix,
                                Radical, Phonology,
                                Condition, Selection)


@multimethod
def realize(term: Lexeme, paradigm: Dict[str, Dict[frozendict, Callable]]) -> List[Forme]:
    """
    Réalise ou construit toutes les formes d'un lexème
    :param term : un Lexeme
    :param paradigm :
    :return : Liste des Formes disponibles pour ce Lexeme
    """
    output = []

    for sigma, func in paradigm[term.pos].items():
        if (term.sigma.items() <= sigma.items()) and (term.traduction.sigma.items() <= sigma.items()):
            output.append(func(term))

    return output


@multimethod
def realize(term: Forme, phonology: Phonology) -> str:
    """
    Concatène la réalisation de chaque morphème
    :param term:
    :param phonology:
    :return:
    """
    result = ""
    for morpheme in term.morphemes:
        try:
            result = realize(morpheme, result)
        except DispatchError:
            result = realize(morpheme, result, phonology)
    return result


@multimethod
def realize(term: Suffix, accumulator: str) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return f"{accumulator}{term.rule.group(1)}"


@multimethod
def realize(term: Suffix, accumulator: Tuple[str, ...]) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return realize(term, accumulator[0])


@multimethod
def realize(term: Prefix, accumulator: str) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return f"{term.rule.group(1)}{accumulator}"


@multimethod
def realize(term: Prefix, accumulator: Tuple[str, ...]) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return realize(term, accumulator[0])


@multimethod
def realize(term: Circumfix, accumulator: str) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return f"{term.rule.group(1)}{accumulator}{term.rule.group(2)}"


@multimethod
def realize(term: Circumfix, accumulator: Tuple[str, ...]) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return realize(term, accumulator[0])


@multimethod
def realize(term: Radical, accumulator: Tuple[str, ...]) -> Tuple[str, ...]:
    """
    :param term:
    :param accumulator:
    :return:
    """
    if term.rule:
        return accumulator[int(term.rule.group(1)) - 1]
    return term.stem


@multimethod
def realize(term: Radical, accumulator: str) -> Union[str, Tuple[str, ...]]:
    """
    :param term:
    :param accumulator:
    :return:
    """
    if term.rule:
        return accumulator
    return term.stem


@multimethod
def realize(term: Gabarit, accumulator: str, phonology: Phonology) -> str:
    """
    :param term:
    :param accumulator:
    :param phonology:
    :return:
    """
    stem_ = format_stem(accumulator, phonology)
    return apply(term.rule.string, stem_, phonology)


@multimethod
def realize(term: Gabarit, accumulator: Tuple[str, ...], phonology: Phonology) -> str:
    """
    :param term:
    :param accumulator:
    :param phonology:
    :return:
    """
    return realize(term, accumulator[0], phonology)


@multimethod
def realize(term: Selection, accumulator: Tuple[str, ...]) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return accumulator[int(term.rule.group(1)) - 1]


@multimethod
def realize(term: Condition, accumulator: Tuple[str, ...]) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    try:
        _ = realize(term.cond, accumulator)
    except IndexError:
        return realize(term.false, accumulator)
    return realize(term.true, accumulator)


@multimethod
def realize(term: Selection, accumulator: Tuple[str, ...]) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    return accumulator[int(term.rule.group(1)) - 1]


@multimethod
def realize(term: Condition, accumulator: Tuple[str, ...]) -> str:
    """
    :param term:
    :param accumulator:
    :return:
    """
    try:
        _ = realize(term.cond, accumulator)
    except IndexError:
        return realize(term.false, accumulator)
    return realize(term.true, accumulator)
