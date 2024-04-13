"""Selection."""
import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict
from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique.lexical_structures.mixins.MixinRepresentor import MixinRepresentor
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.StemSpace import StemSpace


class Selection(MixinDisplay, MixinEquality, MixinRepresentor):
    """Pseudo-Morpheme qui permet de construire une règle de sélection de radical."""

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
        """Initialise rule, sigma et phonology.

        :param rule:
        :param sigma:
        :param phonology:
        """
        _rule = Selection.__PATTERN(rule)

        if _rule is None:
            raise TypeError

        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Sélectionne le bon thème dans l'espace thématique.

        :return: un des thèmes de l'espace thématique
        """
        return term.stems[int(self.__rule.group(1)) - 1]

    def get_sigma(self) -> frozendict:
        """Récupère le sigma d'un Selection.

        :return: le sigma d'un Selection
        """
        return self.__sigma

    def _repr_params(self) -> str:
        """Récupère la string du matche de la règle.

        :return:
        """
        return self.__rule.string

    def get_rule(self) -> Match:
        """Récupère la règle d'un Selection.

        :return: l'objet Match qui correspond à la règle de sélection
        """
        return self.__rule
