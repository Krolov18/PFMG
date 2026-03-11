"""Circumfix: affixal rule that adds both a prefix and a suffix to the Radical."""

import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict

from pfmg.external.decoupeur.MixinDecoupeur import MixinDecoupeur
from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.equality.MixinEquality import MixinEquality
from pfmg.external.gloser.MixinGloser import MixinGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Circumfix(
    MixinDisplay, MixinEquality, MixinRepresentor, MixinDecoupeur, MixinGloser
):
    """Affixal rule that prefixes and suffixes the Radical at the same time."""

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
        """Initialize circumfix rule (prefix+X+suffix), sigma, and phonology."""
        _rule = Circumfix.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Apply circumfix to a StemSpace radical (prefix + first stem + suffix)."""
        assert isinstance(term, StemSpace)
        return f"{self.__rule.group(1)}{term.stems[0]}{self.__rule.group(2)}"

    def _to_string__str(self, term: str) -> str:
        """Apply circumfix to a string radical."""
        assert isinstance(term, str)
        return f"{self.__rule.group(1)}{term}{self.__rule.group(2)}"

    def _to_decoupe__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return f"{self.__rule.group(1)}+{term.stems[0]}+{self.__rule.group(2)}"

    def _to_decoupe__str(self, term: str) -> str:
        assert isinstance(term, str)
        return f"{self.__rule.group(1)}+{term}+{self.__rule.group(2)}"

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return (
            f"{'.'.join(self.__sigma.values())}"
            f"+{term.lemma}"
            f"+{'.'.join(self.__sigma.values())}"
        )

    def _to_glose__str(self, term: str) -> str:
        assert isinstance(term, str)
        return (
            f"{'.'.join(self.__sigma.values())}"
            f"+{term}"
            f"+{'.'.join(self.__sigma.values())}"
        )

    def get_sigma(self) -> frozendict:
        """Return this circumfix's sigma (feature dict)."""
        return self.__sigma

    def get_rule(self) -> Match[str]:
        """Return the compiled rule match object."""
        return self.__rule

    def _repr_params(self) -> str:
        """Return rule and sigma for repr."""
        sigma = f"sigma=frozendict({dict(self.__sigma)})"
        rule = f"rule={self.__rule.string}"  # type: ignore[attr-defined]
        return f"{rule}, {sigma}"
