# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Morpheme quiu permet de faire une règle conditionnelle."""

import re
from collections.abc import Callable
from re import Match
from typing import ClassVar

from frozendict import frozendict

from pfmg.external.display import ABCDisplay
from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.equality.MixinEquality import MixinEquality
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Condition(MixinDisplay, MixinEquality, MixinRepresentor, ABCGloser):
    """Règle ternaire au sein des règles morphologiques.

    :param cond : Construction du morphème
    :param true : Si la construction de la condition réussie, on récupère true.
    :param false : Si la construction de la condition échoue, on récupère false.
    """

    __PATTERN: ClassVar[Callable[[str], Match | None]] = re.compile(
        r"^(.*)\?(.*):(.*)$",
    ).fullmatch

    rule: Match
    sigma: frozendict

    __cond: ABCDisplay
    __true: ABCDisplay
    __false: ABCDisplay
    phonology: Phonology

    def __init__(
        self,
        rule: str,
        sigma: frozendict,
        phonology: Phonology,
    ) -> None:
        """Initialise la règle, le sigma et la phonologie.

        :param rule:
        :param sigma:
        :param phonology:
        """
        _rule = Condition.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        self.rule = _rule
        self.sigma = sigma
        self.__cond = create_morpheme(
            rule=_rule.group(1), sigma=sigma, phonology=phonology
        )
        self.__true = create_morpheme(
            rule=_rule.group(2), sigma=sigma, phonology=phonology
        )
        self.__false = create_morpheme(
            rule=_rule.group(3), sigma=sigma, phonology=phonology
        )
        self.phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        try:
            self.__cond.to_string(term)
        except IndexError:
            return self.__false.to_string(term)
        return self.__true.to_string(term)

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        try:
            self.__cond.to_string(term)
        except IndexError:
            return self.__false.to_decoupe(term)
        return self.__true.to_decoupe(term)

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """TODO : Doc à écrire."""
        try:
            self.__cond.to_string(term)
        except IndexError:
            return self.__false.to_glose(term)  # type: ignore
        return self.__true.to_glose(term)  # type: ignore

    def get_sigma(self) -> frozendict:
        """Récupère le sigma.

        :return: le sigma
        """
        return self.sigma

    def _repr_params(self) -> str:
        """TODO : Doc à écrire."""
        return self.rule.string

    def get_rule(self) -> Match:
        """Récupère la règle.

        :return: la règle
        """
        return self.rule
