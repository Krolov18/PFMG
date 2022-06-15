from typing import List, Dict, Callable

from frozendict import frozendict
from multimethod import multimethod

from lexique.realizer import realize
from lexique.structures import Forme, Phonology, Lexeme
from utils.abstract_factory import factory_function


@multimethod
def unary(id_unary: str,
          term: Forme,
          phonology: Phonology) -> str:
    return factory_function(concrete_product=f"{id_unary}_unary",
                            package=__name__,
                            term=term,
                            phonology=phonology)


@multimethod
def unary(id_unary: str,
          term: List[Lexeme],
          paradigm: Dict[str, Dict[frozendict, Callable]],
          phonology: Phonology) -> List[str]:
    output: List[str] = list()
    for lexeme in term:
        for form in realize(lexeme, paradigm):
            output.append(unary(id_unary, form, phonology))
    return output


def fcfg_unary(term: Forme, phonology: Phonology) -> str:
    features = ",".join(f"{feat}='{val}'" for feat, val in term.sigma.items())
    return f"{term.pos}[{features},Traduction='{realize(term.traduction, phonology)}'] -> '{realize(term, phonology)}'"


def tcfg_unary(term: Forme, phonology: Phonology) -> str:
    features = ",".join(f"{feat}='{val}'" for feat, val in term.sigma.items())
    return f"{term.pos}[{features},Traduction='{realize(term, phonology)}'] -> '{realize(term.traduction, phonology)}'"


def cfg_unary(term: Forme, phonology: Phonology) -> str:
    return f"{term.pos} -> '{realize(term, phonology)}'"