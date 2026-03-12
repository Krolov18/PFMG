"""Factory to build morpheme instances from rule string, sigma, and phonology."""

from enum import Enum

from frozendict import frozendict

from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.utils.abstract_factory import factory_method


class Ruler(Enum):
    """Morpheme rule type names (Prefix, Suffix, Circumfix, Gabarit, Selection, Condition)."""

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
) -> "Morpheme":  # noqa # type: ignore
    """Build a morpheme (Prefix, Suffix, Gabarit, etc.) from rule, sigma, and phonology."""
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
