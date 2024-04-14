"""Méthode de construction d'un morphème."""
from enum import Enum

from frozendict import frozendict

from pfmg.lexique.display.ABCDisplay import ABCDisplay
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.utils.abstract_factory import factory_method


class Ruler(Enum):
    """Structure pour les noms d'une règle."""

    PREFIX = "Prefix"
    SUFFIX = "Suffix"
    CIRCUMFIX = "Circumfix"
    GABARIT = "Gabarit"
    SELECTION = "Selection"
    CONDITION = "Condition"


def create_morpheme(
        rule: str,
        sigma: frozendict,
        phonology: Phonology,
) -> ABCDisplay:
    """Factory pour construire n'importe quel morphème.

    :param rule: une règle valide
    :param sigma: un ensemble de traits
    :param phonology: une instance de Phonology
    :return: quelque chose qui peut s'afficher
    """
    assert __package__ is not None

    for id_ruler in Ruler:
        try:
            result = factory_method(
                concrete_product=id_ruler.value,
                package=__package__,
                rule=rule,
                sigma=sigma,
                phonology=phonology,
            )
        except TypeError:
            continue
        else:
            return result
    else:
        message = f"{rule} n'est pas une règle valide"
        raise TypeError(message)
