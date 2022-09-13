import re
from typing import Literal, Pattern

from frozendict import frozendict  # type: ignore

# from lexique.errors import Errors
from lexique.structures import Prefix, Suffix, Circumfix, Gabarit, Condition, Selection
from lexique.structures import Morpheme
from utils.functions import static_vars


# from utils.abstract_factory import factory_function
# from utils.functions import static_vars


@static_vars(rules={"prefix": re.compile(r"^(.*)\+X$"),
                    "suffix": re.compile(r"^X\+(.*)$"),
                    "circumfix": re.compile(r"^([^+]*)\+X\+([^+]*)$"),
                    "selection": re.compile(r"^X(\d+)$"),
                    "condition": re.compile(r"^(.*)\?(.*):(.*)$")})
def ruler(rule: str, sigma: frozendict, voyelles: frozenset) -> Morpheme:
    attr = getattr(ruler, "rules")
    if voyelles and ("gabarit" not in attr):
        attr["gabarit"] = re.compile(fr"^([{''.join(voyelles)}AUV1-9]){{4,9}}$")

    match rule:
        case r if i_rule := attr["prefix"].fullmatch(r):
            return Prefix(rule=i_rule, sigma=sigma)
        case r if i_rule := attr["suffix"].fullmatch(r):
            return Suffix(rule=i_rule, sigma=sigma)
        case r if i_rule := attr["circumfix"].fullmatch(r):
            return Circumfix(rule=i_rule, sigma=sigma)
        case r if i_rule := attr["selection"].fullmatch(r):
            return Selection(rule=i_rule, sigma=sigma)
        case r if i_rule := attr["gabarit"].fullmatch(r):
            return Gabarit(rule=i_rule, sigma=sigma)
        case r if i_rule := attr["condition"].fullmatch(r):
            return Condition(rule=i_rule,
                             sigma=sigma,
                             cond=ruler(rule=i_rule.group(1), sigma=sigma, voyelles=voyelles),
                             true=ruler(rule=i_rule.group(2), sigma=sigma, voyelles=voyelles),
                             false=ruler(rule=i_rule.group(3), sigma=sigma, voyelles=voyelles))
        case _:
            raise ValueError()
