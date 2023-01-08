"""
    Fonctions permettant de réaliser les différentes structures définies dans structures.py
"""

from frozendict import frozendict  # type: ignore

from lexique.applier import format_stem, apply
from lexique.readers import select_morphemes
from lexique.ruler import ruler_radical
from lexique.structures import (Circumfix, Forme, Gabarit, Lexeme, Prefix, Suffix,
                                Radical, Condition, Selection, Phonology, type_Morpheme, Paradigm)
from utils.abstract_factory import factory_function


def realize(term, **kwargs):
    """
    :param term:
    :param kwargs:
    :return:
    """
    return factory_function(concrete_product=f"realize_{term.__class__.__name__.lower()}",
                            package=__name__,
                            **kwargs)


def realize_lexeme(term: Lexeme, paradigm: Paradigm) -> list[Forme]:
    """
    :param term: Lexeme
    :param paradigm: Structure encodant les gloses et les blocs d'un langage
    :return: les formes réalisables d'un lexème à partir d'un paradigme
    """
    sigmas: list[frozendict] = paradigm.gloses[term.pos]
    blocks: list[list[type_Morpheme]] = paradigm.blocks[term.pos]

    formes: list[Forme] = []

    for i_sigma in sigmas:
        if term.sigma.items() <= i_sigma.items():
            formes.append(Forme(pos=term.pos,
                                morphemes=[ruler_radical(rule="", sigma=i_sigma, stems=term.stem),
                                           *select_morphemes(i_sigma, blocks)],
                                sigma=i_sigma,
                                traduction=None))
    return formes



def realize_forme(term: Forme, phonology: Phonology) -> str:
    """
    Réalisation de la Forme par concaténation de la réalisation de tous ses morphèmes.
    :param term: Une Forme
    :param phonology: le DataClass encodant la phonologie
    :return: une forme réalisée sous forme de chaîne de caractères.
    """
    result = ""
    for morpheme in term.morphemes:
        assert morpheme.sigma is not None, morpheme
        m_sigma = dict(term.sigma)
        m_sigma.update(dict(morpheme.sigma))
        term.sigma = frozendict(m_sigma)
        result = realize(term=morpheme,
                         accumulator=result,
                         phonology=phonology)
    return result


def realize_suffix(term: Suffix, accumulator: str) -> str:
    """
    :param term:
    :param accumulator:
    :return: Réalisation d'un suffixe
    """
    assert term.rule is not None
    return f"{accumulator}{term.rule.group(1)}"


def realize_prefix(term: Prefix, accumulator: str) -> str:
    """
    :param term:
    :param accumulator:
    :return: Réalisation d'un préfixe
    """
    assert term.rule is not None
    return f"{term.rule.group(1)}{accumulator}"


def realize_circumfix(term: Circumfix, accumulator: str) -> str:
    """

    :param term:
    :param accumulator:
    :return: Réalisation d'un circonfixe
    """
    assert term.rule is not None
    return f"{term.rule.group(1)}{accumulator}{term.rule.group(2)}"


def realize_gabarit(term: Gabarit, accumulator: str, phonology: Phonology) -> str:
    """

    :param term:
    :param accumulator:
    :param phonology:
    :return: Réalisation d'un gabarit
    """
    assert term.rule is not None
    return apply(rule=term.rule.string,
                 stem=format_stem(accumulator, phonology),
                 phonology=phonology)


def realize_radical(term: Radical, **kwargs) -> str | tuple[str, ...]:
    """
    :param term:
    :param kwargs:
    :return: Réalisation d'un radical
    """
    match term.stem:
        case str():
            return term.stem
        case [first]:
            return first
        case tuple():
            return term.stem
        case _:
            raise TypeError()


def realize_selection(term: Selection, accumulator: str) -> str:
    """
    :param term:
    :param accumulator:
    :return: Choix du stem dans l'espace thématique
    """
    assert term.rule is not None
    return accumulator[int(term.rule.group(1)) - 1]


def realize_condition(term: Condition, accumulator: str) -> str:
    """
    :param term:
    :param accumulator:
    :return: Si cond alors la réalisation de true else la réalisation de false
    """
    try:
        _ = realize(term=term.cond, accumulator=accumulator)
    except IndexError:
        return realize(term=term.false, accumulator=accumulator)
    return realize(term=term.true, accumulator=accumulator)
