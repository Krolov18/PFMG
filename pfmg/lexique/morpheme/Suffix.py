"""Suffix."""

import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict

from pfmg.lexique.display.MixinDisplay import MixinDisplay
from pfmg.lexique.equality.MixinEquality import MixinEquality
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Suffix(MixinDisplay, MixinEquality, MixinRepresentor):
    """Un suffixe encode une règle affixale succédant le Radical."""

    __PATTERN: Callable[[str], Match[str] | None] = re.compile(
        r"^X\+(.*)$",
    ).fullmatch

    __rule: Match
    __sigma: frozendict
    __phonology: Phonology

    def __init__(
        self,
        rule: str,
        sigma: frozendict,
        phonology: Phonology,
    ) -> None:
        """Initialialise rule, sigma et phonology.

        :param rule: une règle suffixale valide.
        :param sigma: un sigma pour cette règle
        :param phonology: instance de Phonology
        """
        _rule = Suffix.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Applique la concaténation du radical et du suffixe.

        :param term: Un espace thématique
        :return: la forme réalisée en string
        """
        return f"{term.stems[0]}{self.__rule.group(1)}"

    def _to_string__str(self, term: str) -> str:
        """Applique la concaténation du radical et du suffixe.

        :param term: Le radical est une simple chaine de caractères
        :return: La forme réalisée en string
        """
        return f"{term}{self.__rule.group(1)}"

    def _repr_params(self) -> str:
        """Pré-forme les attribut du suffixe.

        :return: représentation de la rule et du sigma ensemble
        """
        sigma = f"sigma=frozendict({dict(self.__sigma)})"
        rule = f"rule={self.__rule.string}"
        return f"{rule}, {sigma}"

    def get_sigma(self) -> frozendict:
        """Récupère le sigma.

        :return: le sigma
        """
        return self.__sigma

    def get_rule(self) -> Match:
        """Récupère la règle.

        :return: la rule
        """
        return self.__rule
