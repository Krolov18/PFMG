import re
from typing import Match, Callable

from frozendict import frozendict

from lexique_2.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique_2.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique_2.lexical_structures.mixins.MixinRepresentor import MixinRepresentor
from lexique_2.lexical_structures.Phonology import Phonology
from lexique_2.lexical_structures.StemSpace import StemSpace


class Gabarit(MixinDisplay, MixinEquality, MixinRepresentor):
    """
    Le gabarit encode une règle affixale qui touche la structure du Radical.
    Dans la règle gabaritique, les consonnes comme les voyelles peuvent subir des modifications phonologiques.
    """
    __PATTERN: Callable[[str], Match[str] | None]
    rule: Match[str]
    sigma: frozendict
    phonology: Phonology

    def __init__(self, rule: str, sigma: frozendict, phonology: Phonology) -> None:
        if not hasattr(Gabarit, "_Gabarit__PATTERN"):
            setattr(Gabarit, "_Gabarit__PATTERN",
                    re.compile(fr"^([{''.join(phonology.voyelles)}AUV1-9]{{4,9}})$").fullmatch)

        _rule = Gabarit.__PATTERN(rule)
        if _rule is None:
            raise TypeError()

        self.rule = _rule
        self.sigma = sigma
        self.phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        result = ""
        for char in self.rule.string:
            result += self.__verify(char, Gabarit.__format_default_stem(term.stems[0]))
        return result

    def __verify(self, char: str, stem: frozendict) -> str:
        """
        TODO: Pourquoi pas considérer cette fonction comme méthode à Phonology ?
        :param char: Un caractère compris dans l'union [consonnes|voyelles|UAV1-9]
        :param stem: une racine au format d'un dictionnaire unique et figé
        :return: la réalisation du caractère d'une règle gabaritique appliqué à un stem (racine)
        """
        assert char
        match char:
            case "U":
                return self.phonology.apophonies[self.phonology.apophonies[stem['V']]]
            case "A":
                return self.phonology.apophonies[stem[self.phonology.derives[char]]]
            case "1" | "2" | "3" | "V":
                return stem[char]
            case "4" | "5" | "6":
                return self.phonology.mutations[stem[str(int(char) - 3)]]
            case "7" | "8" | "9":
                return self.phonology.mutations[self.phonology.mutations[stem[str(int(char) - 6)]]]
            case _:
                return char

    @staticmethod
    def __format_default_stem(stem: str) -> frozendict:
        """
        'default' signifie qu'on attend le schéma CCVC
        :param stem: CCVC
        :return: frozendict indiquant la voyelle thématique et les consonnes
        """
        return frozendict(zip("12V3", stem))

    def get_sigma(self) -> frozendict:
        return self.sigma

    def _repr_params(self) -> str:
        return self.rule.string

    def get_rule(self) -> str:
        return self.rule
