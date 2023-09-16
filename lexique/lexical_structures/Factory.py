from enum import Enum

from frozendict import frozendict

from lexique.lexical_structures.interfaces.Display import Display
from lexique.lexical_structures.Phonology import Phonology
from utils.abstract_factory import factory_method


class Ruler(Enum):
    """
    Attibutes :
    -----------
    :param PREFIX :
    :param SUFFIX :
    :param CIRCUMFIX :
    :param GABARIT :
    :param SELECTION :
    :param CONDITION :
    """
    PREFIX = "Prefix"
    SUFFIX = "Suffix"
    CIRCUMFIX = "Circumfix"
    GABARIT = "Gabarit"
    SELECTION = "Selection"
    CONDITION = "Condition"


def create_morpheme(rule: str, sigma: frozendict, phonology: Phonology) -> Display:
    for id_ruler in Ruler:
        try:
            return factory_method(concrete_product=id_ruler.value,
                                  package=__package__,
                                  rule=rule,
                                  sigma=sigma,
                                  phonology=phonology)
        except TypeError:
            continue
    raise TypeError()
