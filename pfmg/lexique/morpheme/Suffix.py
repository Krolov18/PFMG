"""Suffix: affixal rule that adds a segment after the Radical."""

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


class Suffix(
    MixinDisplay, MixinEquality, MixinRepresentor, MixinDecoupeur, MixinGloser
):
    """Affixal rule that adds a suffix after the Radical (X+suffix)."""

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
        """Initialize suffix rule (X+suffix), sigma, and phonology."""
        _rule = Suffix.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Return stem + suffix (first stem from StemSpace)."""
        return f"{term.stems[0]}{self.__rule.group(1)}"

    def _to_string__str(self, term: str) -> str:
        """Return radical string + suffix."""
        return f"{term}{self.__rule.group(1)}"

    def _to_decoupe__stemspace(self, term: StemSpace | str | None = None) -> str:
        assert isinstance(term, StemSpace)
        return f"{term.stems[0]}-{self.__rule.group(1)}"

    def _to_decoupe__str(self, term: StemSpace | str | None = None) -> str:
        assert isinstance(term, str)
        return f"{term}-{self.__rule.group(1)}"

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return f"{term.lemma}-{'.'.join(self.__sigma.values())}"

    def _to_glose__str(self, term: str) -> str:
        assert isinstance(term, str)
        return f"{term}-{'.'.join(self.__sigma.values())}"

    def _to_glose__nonetype(self, term: None = None) -> NoReturn:
        assert term is None
        raise NotImplementedError

    def _repr_params(self) -> str:
        """Return rule and sigma for repr."""
        sigma = f"sigma=frozendict({dict(self.__sigma)})"
        rule = f"rule={self.__rule.string}"  # type: ignore[attr-defined]
        return f"{rule}, {sigma}"

    def get_sigma(self) -> frozendict:
        """Return this suffix's sigma (feature dict)."""
        return self.__sigma

    def get_rule(self) -> Match:
        """Return the compiled rule match object."""
        return self.__rule
