# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Prefix."""

import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict

from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.lexique.equality.MixinEquality import MixinEquality
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Prefix(MixinDisplay, MixinEquality, MixinRepresentor):
    """Un préfixe encode une règle affixale ajoutant un élément à la gauche du Radical."""

    __PATTERN: Callable[[str], Match | None] = re.compile(
        r"^(.*)\+X$",
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
        """Initialise rule, sigma et phonology.

        :param rule:
        :param sigma:
        :param phonology:
        """
        _rule = Prefix.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        assert sigma
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Représente un Préfix sur un StemSpace.

        :param term: un espace thématique
        :return: la réalisation d'un Prefix
        """
        return f"{self.__rule.group(1)}{term.stems[0]}"

    def _to_string__str(self, term: str) -> str:
        return f"{self.__rule.group(1)}{term}"

    def _to_decoupe__stemspace(
        self, term: StemSpace | str | None = None
    ) -> str:
        assert isinstance(term, StemSpace)
        return f"{self.__rule.group(1)}-{term.stems[0]}"

    def _to_decoupe__str(self, term: StemSpace | str | None = None) -> str:
        assert isinstance(term, str)
        return f"{self.__rule.group(1)}-{term}"

    def get_sigma(self) -> frozendict:
        """Récupère le sigma d'un préfixe.

        :return: le sigma d'un préfixe
        """
        return self.__sigma

    def _repr_params(self) -> str:
        """Write some doc."""
        return self.__rule.string

    def get_rule(self) -> Match:
        """Récupère la règle.

        :return: le Match de la rule
        """
        return self.__rule
