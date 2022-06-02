from typing import List, Dict

from multimethod import multimethod

from lexique.structures import Forme, Phonology
from lexique.unary import unary
from utils.abstract_factory import factory_function


@multimethod
def translate(term: List[str], lexicon: Dict[str, List[Forme]], phonology: Phonology) -> List[str]:
    """
    Donne moi des tokens, je te donnerais des règles lexicales
    :param term: une séquences de tokens en français
    :param lexicon:
    :param phonology:
    :return:
    """
    output: List[str] = []

    for token in term:
        for forme in lexicon[token]:
            output.append(unary("fcfg", forme, phonology))
    return output


@multimethod
def translate(term: List[List[str]], lexicon: Dict[str, List[Forme]]) -> List[str]:
    """
    Donne moi une phrase, je te donnerais des règles lexicales
    :param lexicon:
    :param term: une séquences de tokens en français
    :return:
    """
    pass


@multimethod
def translate(id_translation: str, term: str, lexicon: Dict[str, List[Forme]]) -> Forme:
    assert term
    return factory_function(
        concrete_product=f"translate_{id_translation}",
        package=__name__,
        term=term,
        lexicon=lexicon
    )


# def translate_deux
