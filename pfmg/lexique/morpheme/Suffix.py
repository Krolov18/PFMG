# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Suffix."""

import re
from collections.abc import Callable
from re import Match
from typing import NoReturn

from frozendict import frozendict

from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.equality.MixinEquality import MixinEquality
from pfmg.external.gloser.MixinGloser import MixinGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Suffix(MixinDisplay, MixinEquality, MixinRepresentor, MixinGloser):
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

    def _to_decoupe__stemspace(
        self, term: StemSpace | str | None = None
    ) -> str:
        assert isinstance(term, StemSpace)
        return f"{term.stems[0]}-{self.__rule.group(1)}"

    def _to_decoupe__str(self, term: StemSpace | str | None = None) -> str:
        assert isinstance(term, str)
        return f"{term}-{self.__rule.group(1)}"

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return f"{term.lemma}-{".".join(self.__sigma.values())}"

    def _to_glose__str(self, term: str) -> str:
        assert isinstance(term, str)
        return f"{term}-{".".join(self.__sigma.values())}"

    def _to_glose__nonetype(self, term: None) -> NoReturn:
        assert term is None
        raise NotImplementedError

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
