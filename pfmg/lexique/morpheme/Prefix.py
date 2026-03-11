"""Prefix: affixal rule that adds an element before the Radical."""

import re
from collections.abc import Callable
from re import Match
from typing import NoReturn

from frozendict import frozendict

from pfmg.external.decoupeur.MixinDecoupeur import MixinDecoupeur
from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.equality.MixinEquality import MixinEquality
from pfmg.external.gloser.MixinGloser import MixinGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Prefix(
    MixinDisplay, MixinEquality, MixinRepresentor, MixinDecoupeur, MixinGloser
):
    """Encodes an affixal rule that adds an element before the Radical."""

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
        """Initialize prefix rule, sigma, and phonology."""
        _rule = Prefix.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        assert sigma
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Return the prefix realization for a StemSpace (prefix + first stem)."""
        return f"{self.__rule.group(1)}{term.stems[0]}"

    def _to_string__str(self, term: str) -> str:
        return f"{self.__rule.group(1)}{term}"

    def _to_decoupe__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return f"{self.__rule.group(1)}-{term.stems[0]}"

    def _to_decoupe__str(self, term: str) -> str:
        assert isinstance(term, str)
        return f"{self.__rule.group(1)}-{term}"

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return f"{'.'.join(self.__sigma.values())}-{term.lemma}"

    def _to_glose__str(self, term: str) -> str:
        assert isinstance(term, str)
        return f"{'.'.join(self.__sigma.values())}-{term}"

    def _to_glose__nonetype(self, term: None = None) -> NoReturn:
        raise NotImplementedError

    def get_sigma(self) -> frozendict:
        """Return this prefix's sigma (feature dict)."""
        return self.__sigma

    def _repr_params(self) -> str:
        """Return the original rule string for representation."""
        return self.__rule.string

    def get_rule(self) -> Match:
        """Return the compiled rule match object."""
        return self.__rule
