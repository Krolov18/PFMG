"""Circonfixe."""
import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict
from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique.lexical_structures.mixins.MixinRepresentor import MixinRepresentor
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.StemSpace import StemSpace


class Circumfix(MixinDisplay, MixinEquality, MixinRepresentor):
    """Structurte représentant un Circonfixe.

    Un circonfixe encode une règle affixale 
    préfixant ET suffixant le Radical simultanément.
    """

    __PATTERN: Callable[[str], Match[str] | None] = re.compile(
        r"^([^+]*)\+X\+([^+]*)$",
    ).fullmatch

    __rule: Match[str]
    __sigma: frozendict
    __phonology: Phonology

    def __init__(
        self,
        rule: str,
        sigma: frozendict,
        phonology: Phonology,
    ) -> None:
        """Initialise rule/sigma/phonology.

        :param rule: Regex représentant un circonfixe
        :param sigma: traits liés à la règle
        :param phonology: instance de Phonology
        """
        _rule = Circumfix.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Version avec un radical StemSpace.

        :param term:
        :return: Application de larègle sur un radical StemSpace
        """
        return f"{self.__rule.group(1)}{term.stems[0]}{self.__rule.group(2)}"

    def _to_string__str(self, term: str) -> str:
        """Version avec un radical string.

        :param term: radical
        :return: application de la règle sur un radical string
        """
        return f"{self.__rule.group(1)}{term}{self.__rule.group(2)}"

    def get_sigma(self) -> frozendict:
        """Récupère les propriétés du circonfixe."""
        return self.__sigma

    def get_rule(self) -> Match[str]:
        """Récupère le match de la règle."""
        return self.__rule

    def _repr_params(self) -> str:
        """Construit le repr du rule/sigma."""
        sigma = f"sigma=frozendict({dict(self.__sigma)})"
        rule = f"rule={self.__rule.string}"
        return f"{rule}, {sigma}"

