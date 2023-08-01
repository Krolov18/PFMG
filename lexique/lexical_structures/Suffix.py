import re
from typing import Match, Callable

from frozendict import frozendict

from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique.lexical_structures.mixins.MixinRepresentor import MixinRepresentor
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.StemSpace import StemSpace


class Suffix(MixinDisplay, MixinEquality, MixinRepresentor):
    """
    Un suffixe encode une règle affixale succédant le Radical.
    """
    __PATTERN: Callable[[str], Match[str] | None] = re.compile(r"^X\+(.*)$").fullmatch

    __rule: Match[str]
    __sigma: frozendict
    __phonology: Phonology

    def __init__(self, rule: str, sigma: frozendict, phonology: Phonology) -> None:
        _rule = Suffix.__PATTERN(rule)
        if _rule is None:
            raise TypeError()
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        return f"{term.stems[0]}{self.__rule.group(1)}"

    def _to_string__str(self, term: str) -> str:
        return f"{term}{self.__rule.group(1)}"

    def _repr_params(self) -> str:
        return self.__rule.string

    def get_sigma(self) -> frozendict:
        return self.__sigma

    def get_rule(self) -> Match[str]:
        return self.__rule
