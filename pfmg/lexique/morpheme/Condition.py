"""Conditional morpheme rule: cond ? true : false."""

import re
from collections.abc import Callable
from re import Match
from typing import ClassVar

from frozendict import frozendict

from pfmg.external.decoupeur.MixinDecoupeur import MixinDecoupeur
from pfmg.external.display import ABCDisplay
from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.equality.MixinEquality import MixinEquality
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Condition(
    MixinDisplay, MixinEquality, MixinRepresentor, MixinDecoupeur, ABCGloser
):
    """Ternary rule in morphological rules: if cond then true else false."""

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
        """Initialize condition rule (cond?true:false), sigma, and phonology."""
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
        """Return segmentation from cond branch; on IndexError use false branch."""
        try:
            self.__cond.to_string(term)
        except IndexError:
            return self.__false.to_decoupe(term)  # type: ignore
        return self.__true.to_decoupe(term)  # type: ignore

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """Return glose from cond branch; on IndexError use false branch."""
        try:
            self.__cond.to_string(term)
        except IndexError:
            return self.__false.to_glose(term)  # type: ignore
        return self.__true.to_glose(term)  # type: ignore

    def get_sigma(self) -> frozendict:
        """Return this condition's sigma (feature dict)."""
        return self.sigma

    def _repr_params(self) -> str:
        """Return the original rule string for representation."""
        return self.rule.string  # type: ignore[attr-defined]

    def get_rule(self) -> Match:
        """Return the compiled rule match object."""
        return self.rule
