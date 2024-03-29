import re
from typing import Match, Callable

from frozendict import frozendict

from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique.lexical_structures.mixins.MixinRepresentor import MixinRepresentor
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.Selection import Selection
from lexique.lexical_structures.StemSpace import StemSpace


class Condition(MixinDisplay, MixinEquality, MixinRepresentor):
    """
    Pseudo-morpheme permettant d'encoder la règle ternaire au sein des règles morphologiques.

    :param cond : Construction du morphème
    :param true : Si la construction de la condition réussie, on récupère true.
    :param false : Si la construction de la condition échoue, on récupère false.
    """
    __PATTERN: Callable[[str], Match[str] | None] = re.compile(r"^(.*)\?(.*):(.*)$").fullmatch

    rule: Match[str]
    sigma: frozendict

    __cond: Selection
    __true: Selection
    __false: Selection
    phonology: Phonology

    def __init__(self,
                 rule: str,
                 sigma: frozendict,
                 phonology: Phonology) -> None:
        _rule = Condition.__PATTERN(rule)
        if _rule is None:
            raise TypeError()
        self.rule = _rule
        self.sigma = sigma
        self.__cond = Selection(rule=_rule.group(1), sigma=sigma, phonology=phonology)
        self.__true = Selection(rule=_rule.group(2), sigma=sigma, phonology=phonology)
        self.__false = Selection(rule=_rule.group(3), sigma=sigma, phonology=phonology)
        self.phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        try:
            self.__cond.to_string(term)
        except IndexError:
            return self.__false.to_string(term)
        return self.__true.to_string(term)

    def get_sigma(self) -> frozendict:
        return self.sigma

    def _repr_params(self) -> str:
        return self.rule.string

    def get_rule(self) -> str:
        return self.rule
