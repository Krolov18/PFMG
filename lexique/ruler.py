import re
from typing import Match

from frozendict import frozendict  # type: ignore

from lexique.errors import Errors
from lexique.structures import Prefix, Suffix, Circumfix, Gabarit, Condition, Selection
from lexique.structures import Morpheme
from utils.abstract_factory import factory_function
from utils.functions import static_vars


def ruler(id_ruler: str, rule: str, sigma: frozendict, voyelles: frozenset) -> Morpheme:
    return factory_function(
        concrete_product=f"ruler_{id_ruler}",
        package=__name__,
        rule=rule,
        sigma=sigma,
        voyelles=voyelles
    )


@static_vars(REG=re.compile(r"^(.*)\+X$"))
def ruler_prefix(rule: str, sigma: frozendict, voyelles: frozenset) -> Prefix:
    reg_match = ruler_prefix.REG.fullmatch(rule)
    assert reg_match
    return Prefix(
        rule=reg_match,
        sigma=sigma
    )


@static_vars(REG=re.compile(r"^X\+(.*)$"))
def ruler_suffix(rule: str, sigma: frozendict, voyelles: frozenset) -> Suffix:
    reg_match = ruler_suffix.REG.fullmatch(rule)
    assert reg_match
    return Suffix(
        rule=reg_match,
        sigma=sigma
    )


@static_vars(REG=re.compile(r"^([^+]*)\+X\+([^+]*)$"))
def ruler_circumfix(rule: str, sigma: frozendict, voyelles: frozenset) -> Circumfix:
    reg_match = ruler_circumfix.REG.fullmatch(rule)

    assert reg_match

    return Circumfix(
        rule=reg_match,
        sigma=sigma
    )


def ruler_gabarit(rule: str, sigma: frozendict, voyelles: frozenset) -> Gabarit:
    _voyelles = "".join(voyelles)
    assert voyelles

    if not hasattr(ruler_gabarit, "REG"):
        setattr(ruler_gabarit, "REG", re.compile(fr"^([{_voyelles}AUV1-9]){{4,9}}$"))

    reg_match = ruler_gabarit.REG.fullmatch(rule)  # type: ignore

    assert reg_match

    return Gabarit(
        rule=reg_match,
        sigma=sigma
    )


@static_vars(REG=re.compile(r"^X(\d+)$"))
def ruler_selection(rule: str, sigma: frozendict, voyelles: frozenset) -> Selection:
    reg_match = ruler_selection.REG.fullmatch(rule)

    assert reg_match

    return Selection(
        rule=reg_match,
        sigma=sigma
    )


@static_vars(REG=re.compile(r"^(.*)\?(.*):(.*)$"))
def ruler_ternary(rule: str, sigma: frozendict, voyelles: frozenset) -> Morpheme:
    cond_true_false: Match = ruler_ternary.REG.fullmatch(rule)

    assert cond_true_false

    _condition: str
    _true: str
    _false: str
    _condition, _true, _false = cond_true_false.groups()

    return Condition(rule=None,
                     sigma=sigma,
                     cond=ruler(id_ruler="selection", rule=_condition, sigma=sigma, voyelles=voyelles),
                     true=ruler(id_ruler="selection", rule=_true, sigma=sigma, voyelles=voyelles),
                     false=ruler(id_ruler="selection", rule=_false, sigma=sigma, voyelles=voyelles))


def ruler_all(rule: str, sigma: frozendict, voyelles: frozenset) -> Morpheme:
    for id_ruler in ("prefix", "suffix", "circumfix", "gabarit", "selection", "ternary"):
        try:
            return ruler(id_ruler=id_ruler, rule=rule, sigma=sigma, voyelles=voyelles)
        except AssertionError:
            continue
    raise ValueError(Errors.E008.format(rule=rule))
