"""
    Fonctions permettant de réaliser les différentes structures définies dans structures.py
"""
from typing import Callable, Dict, List, Tuple, TypeVar, Union

from frozendict import frozendict  # type: ignore

from lexique.applier import format_stem, apply
from lexique.structures import (Circumfix, Forme, Gabarit,
                                Lexeme, Prefix, Suffix,
                                Radical, Phonology,
                                Condition, Selection, Morpheme, Realisation)
from utils.abstract_factory import factory_function

Formes = List[Forme]
TypeRealisation = TypeVar("TypeRealisation", str, Formes)
Term = TypeVar("Term", Lexeme, Forme, Morpheme, Realisation)


def realize(term: Term, **kwargs) -> TypeRealisation:
    concrete_product = f"realize_{type(term).__name__.lower()}"
    concrete_product += "" if kwargs.get(
        "accumulator") is None else f"_{type(kwargs.get('accumulator')).__name__.lower()}"
    return factory_function(
        concrete_product=concrete_product,
        package=__name__,
        term=term,
        **kwargs
    )


def realize_lexeme(term: Lexeme, paradigm: Dict[str, Dict[frozendict, Callable]], **kwargs) -> List[Forme]:
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


def realize_forme(term: Forme, phonology: Phonology, **kwargs) -> str:
    """
    Concatène la réalisation de chaque morphème
    :param term:
    :param phonology:
    :return:
    """
    result: str = ""
    for morpheme in term.morphemes:
        result = realize(term=morpheme, accumulator=result, phonology=phonology)
    return result


def realize_suffix_str(term: Suffix, accumulator: str, **kwargs) -> str:
    assert term is not None
    return f"{accumulator}{term.rule.group(1)}"


def realize_suffix_tuple(term: Suffix, accumulator: Tuple[str, ...], **kwargs) -> str:
    return realize_suffix_str(term=term, accumulator=accumulator[0])


def realize_prefix_str(term: Prefix, accumulator: str, **kwargs) -> str:
    assert term is not None
    return f"{term.rule.group(1)}{accumulator}"


def realize_prefix_tuple(term: Prefix, accumulator: Tuple[str, ...], **kwargs) -> str:
    return realize_prefix_str(term=term, accumulator=accumulator[0])


def realize_circumfix_str(term: Circumfix, accumulator: str, **kwargs) -> str:
    assert term is not None
    return f"{term.rule.group(1)}{accumulator}{term.rule.group(2)}"


def realize_circumfix_str_tuple(term: Circumfix, accumulator: Tuple[str, ...], **kwargs) -> str:
    return realize_circumfix_str(term=term, accumulator=accumulator[0])


def realize_radical_str(term: Radical, accumulator: str, **kwargs) -> str:
    assert term is not None
    if term.rule:
        return accumulator
    return term.stem


def realize_radical_tuple(term: Radical, accumulator: Tuple[str, ...], **kwargs) -> Tuple[str, ...]:

    if term.rule:
        return accumulator[int(term.rule.group(1)) - 1]
    return term.stem


def realize_gabarit_str(term: Gabarit, accumulator: str, phonology: Phonology, **kwargs) -> str:
    stem_ = format_stem(accumulator, phonology)
    return apply(term.rule.string, stem_, phonology)


def realize_gabarit_tuple(term: Gabarit, accumulator: Tuple[str, ...], phonology: Phonology, **kwargs) -> str:
    return realize_gabarit_str(term=term, accumulator=accumulator[0], phonology=phonology)


def realize_selection_tuple(term: Selection, accumulator: Tuple[str, ...], **kwargs) -> str:
    assert term is not None
    return accumulator[int(term.rule.group(1)) - 1]


def realize_selection_str(term: Selection, accumulator: str, **kwargs) -> str:
    return accumulator


def realize_condition(term: Condition, accumulator: Tuple[str, ...], **kwargs) -> str:
    try:
        _ = realize(term=term.cond, accumulator=accumulator)
    except IndexError:
        return realize(term=term.false, accumulator=accumulator)
    return realize(term=term.true, accumulator=accumulator)

# def realize_condition(term: Condition, accumulator: Tuple[str, ...]) -> str:
#     """
#     :param term:
#     :param accumulator:
#     :return:
#     """
#     try:
#         _ = realize(term.cond, accumulator)
#     except IndexError:
#         return realize(term.false, accumulator)
#     return realize(term.true, accumulator)
