import re
from typing import Match, Callable

from frozendict import frozendict

from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.StemSpace import StemSpace
from lexique.lexical_structures.mixins.MixinRepresentor import MixinRepresentor


class Prefix(MixinDisplay, MixinEquality, MixinRepresentor):
    """
    Un préfixe encode une règle affixale 
    ajoutant un élément à la gauche du Radical.
    """
    __PATTERN: Callable[[str], Match[str] | None] = re.compile(
        r"^(.*)\+X$"
    ).fullmatch

    __rule: Match[str]
    __sigma: frozendict
    __phonology: Phonology

    def __init__(
            self,
            rule: str,
            sigma: frozendict,
            phonology: Phonology
    ) -> None:
        _rule = Prefix.__PATTERN(rule)
        if _rule is None:
            raise TypeError()
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        return f"{self.__rule.group(1)}{term.stems[0]}"

    def _to_string__str(self, term: str) -> str:
        return f"{self.__rule.group(1)}{term}"

    def get_sigma(self) -> frozendict:
        return self.__sigma

    def _repr_params(self) -> str:
        return self.__rule.string

    def get_rule(self) -> Match[str]:
        return self.__rule
