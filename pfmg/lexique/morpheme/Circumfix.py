# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Circonfixe."""

import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict

from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.equality.MixinEquality import MixinEquality
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


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
        assert isinstance(term, StemSpace)
        return f"{self.__rule.group(1)}{term.stems[0]}{self.__rule.group(2)}"

    def _to_string__str(self, term: str) -> str:
        """Version avec un radical string.

        :param term: radical
        :return: application de la règle sur un radical string
        """
        assert isinstance(term, str)
        return f"{self.__rule.group(1)}{term}{self.__rule.group(2)}"

    def _to_decoupe__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return f"{self.__rule.group(1)}+{term.stems[0]}+{self.__rule.group(2)}"

    def _to_decoupe__str(self, term: str) -> str:
        assert isinstance(term, str)
        return f"{self.__rule.group(1)}+{term}+{self.__rule.group(2)}"

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
