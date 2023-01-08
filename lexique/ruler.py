import re
from enum import Enum

from frozendict import frozendict  # type: ignore

from lexique.structures import Prefix, Suffix, Circumfix, Gabarit, Condition, Selection
from lexique.types_for_kalaba import type_Sigma
from utils.abstract_factory import factory_function
from utils.functions import static_vars

type_Morpheme = Prefix | Suffix | Circumfix | Gabarit | Condition | Selection


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
    PREFIX = "prefix"
    SUFFIX = "suffix"
    CIRCUMFIX = "circumfix"
    GABARIT = "gabarit"
    SELECTION = "selection"
    CONDITION = "condition"


def ruler(id_ruler: Ruler, rule: str, sigma: type_Sigma) -> type_Morpheme:
    """
    :param id_ruler: Identifiant possible pour une règle d'affixation
    :param rule: La règle en question
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: Le morphème prêt à être utilisé
    """
    return factory_function(concrete_product=f"ruler_{id_ruler.value}",
                            package=__name__,
                            rule=rule,
                            sigma=sigma)


@static_vars(REG=re.compile(r"^(.*)\+X$"))
def ruler_prefix(rule: str, sigma: type_Sigma) -> Prefix:
    """
    :param rule: Règle préfixale
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: un Préfix
    """
    assert (i_rule := getattr(ruler_prefix, "REG").fullmatch(rule)) is not None
    return Prefix(rule=i_rule, sigma=sigma)


@static_vars(REG=re.compile(r"^X\+(.*)$"))
def ruler_suffix(rule: str, sigma: type_Sigma) -> Suffix:
    """
    :param rule: Règle suffixale
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: un Suffix
    """
    assert (i_rule := getattr(ruler_suffix, "REG").fullmatch(rule)) is not None
    return Suffix(rule=i_rule, sigma=sigma)


@static_vars(REG=re.compile(r"^([^+]*)\+X\+([^+]*)$"))
def ruler_circumfix(rule: str, sigma: type_Sigma) -> Circumfix:
    """
    :param rule: Règle circonffixale
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: un Circumfix
    """
    assert (i_rule := getattr(ruler_circumfix, "REG").fullmatch(rule)) is not None
    return Circumfix(rule=i_rule, sigma=sigma)


@static_vars(REG=re.compile(r"^X(\d+)$"))
def ruler_selection(rule: str, sigma: type_Sigma) -> Selection:
    """
    :param rule: Règle sélectionnale
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: un Selection
    """
    assert (i_rule := getattr(ruler_selection, "REG").fullmatch(rule)) is not None
    return Selection(rule=i_rule, sigma=sigma)


@static_vars(REG=re.compile(r"^(.*)\?(.*):(.*)$"))
def ruler_condition(rule: str, sigma: type_Sigma) -> Condition:
    """
    :param rule: Règle conditionnale
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: une Condition
    """
    assert (i_rule := getattr(ruler_condition, "REG").fullmatch(rule)) is not None
    return Condition(rule=i_rule,
                     cond=ruler_selection(rule=i_rule.group(1), sigma=sigma),
                     true=ruler_selection(rule=i_rule.group(2), sigma=sigma),
                     false=ruler_selection(rule=i_rule.group(3), sigma=sigma),
                     sigma=sigma)


@static_vars(REG=re.compile(r"^[iueoaAUV1-9]{4,9}$"))
def ruler_gabarit(rule: str, sigma: type_Sigma) -> Gabarit:
    """
    :param rule: Règle gabaritique
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: un Gabarit
    """
    assert (i_rule := getattr(ruler_gabarit, "REG").fullmatch(rule)) is not None
    return Gabarit(rule=i_rule, sigma=sigma)


def any_ruler(rule: str, sigma: type_Sigma) -> type_Morpheme:
    """
    Parcourt chaucune des règles disponibles puis renvoie la première qui matche.
    :param rule: Une règle parmi toutes celles possibles
    :param sigma: Un ensemble de traits/valeurs pour cette règle
    :return: une Selection
    """
    for id_ruler in Ruler:
        try:
            return ruler(id_ruler=id_ruler,
                         rule=rule,
                         sigma=sigma)
        except AssertionError:
            continue
    raise ValueError()
