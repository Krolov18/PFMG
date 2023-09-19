import re
from typing import Match, Callable

from frozendict import frozendict

from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.StemSpace import StemSpace
from lexique.lexical_structures.mixins.MixinRepresentor import MixinRepresentor


class Selection(MixinDisplay, MixinEquality, MixinRepresentor):
    """
    Pseudo-Morpheme qui permet de construire une règle de sélection de radical.
    """
    __PATTERN: Callable[[str], Match[str] | None] = re.compile(
        r"^X(\d+)$"
    ).fullmatch

    __rule: Match[str]
    __sigma: frozendict
    __phonology: Phonology

    def __init__(self, rule: str, sigma: frozendict,
                 phonology: Phonology) -> None:
        _rule = Selection.__PATTERN(rule)
        if _rule is None:
            raise TypeError()
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        return term.stems[int(self.__rule.group(1)) - 1]

    def get_sigma(self) -> frozendict:
        return self.__sigma

    def _repr_params(self) -> str:
        return self.__rule.string

    def get_rule(self) -> Match[str]:
        """
        :return: l'objet Match[str] qui correspond à la règle de sélection.
        """
        return self.__rule
