"""Selection: morpheme that selects one stem from a StemSpace by index (e.g. X1, X2)."""

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


class Selection(
    MixinDisplay, MixinEquality, MixinRepresentor, MixinDecoupeur, MixinGloser
):
    """Rule that selects one stem from a StemSpace by index (e.g. X1, X2)."""

    __PATTERN: Callable[[str], Match | None] = re.compile(
        r"^X(\d+)$",
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
        """Initialize selection rule (X<n>), sigma, and phonology."""
        _rule = Selection.__PATTERN(rule)

        if _rule is None:
            raise TypeError

        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Return the selected stem from the StemSpace (by rule index)."""
        return term.stems[int(self.__rule.group(1)) - 1]

    def _to_string__str(self, term: str) -> str:
        assert isinstance(term, str)
        return term

    def _to_decoupe__stemspace(self, term: StemSpace | str | None = None) -> str:
        assert isinstance(term, StemSpace)
        return term.stems[int(self.__rule.group(1)) - 1]

    def _to_decoupe__str(self, term: StemSpace | str | None = None) -> str:
        assert isinstance(term, str)
        return term

    def _to_glose__nonetype(self, term: None = None) -> NoReturn:
        raise NotImplementedError

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        return f"{term.lemma}.{'.'.join(self.__sigma.values())}"

    def _to_glose__str(self, term: str) -> str:
        return f"{term}.{'.'.join(self.__sigma.values())}"

    def get_sigma(self) -> frozendict:
        """Return this Selection's sigma (feature dict)."""
        return self.__sigma

    def _repr_params(self) -> str:
        """Return the rule match string for representation."""
        return self.__rule.string  # type: ignore[attr-defined]

    def get_rule(self) -> Match:
        """Return the compiled rule match object."""
        return self.__rule
