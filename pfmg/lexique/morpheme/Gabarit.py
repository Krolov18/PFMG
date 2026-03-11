"""Template (gabarit) for affixal rules that apply to the Radical structure."""

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


class Gabarit(
    MixinDisplay, MixinEquality, MixinRepresentor, MixinDecoupeur, MixinGloser
):
    """Template encoding an affixal rule that applies to the Radical; consonants and vowels may undergo phonological changes."""

    __PATTERN: Callable[[str], Match | None]
    rule: Match
    sigma: frozendict
    phonology: Phonology

    def __init__(
        self,
        rule: str,
        sigma: frozendict,
        phonology: Phonology,
    ) -> None:
        """Initialize template rule, sigma, and phonology."""
        if not hasattr(Gabarit, "_Gabarit__PATTERN"):
            Gabarit.__PATTERN = re.compile(
                rf"^([{''.join(phonology.voyelles)}AUV1-9]{{4,9}})$",
            ).fullmatch

        _rule = Gabarit.__PATTERN(rule)
        if _rule is None:
            raise TypeError

        self.rule = _rule
        self.sigma = sigma
        self.phonology = phonology

    def __verify(self, char: str, stem: frozendict) -> str:
        """Apply the phonological rule for the given character (consonant, vowel, or U/A/V/1-9).

        Args:
            char: A character from the template (consonants, vowels, or U/A/V/1-9).
            stem: Root as a single frozen dict.

        Returns:
            str: Surface realization of that character for the template applied to the stem.

        """
        assert char
        match char:
            case "U":
                return self.phonology.apophonies[self.phonology.apophonies[stem["V"]]]
            case "A":
                return self.phonology.apophonies[stem[self.phonology.derives[char]]]
            case "1" | "2" | "3" | "V":
                return stem[char]
            case "4" | "5" | "6":
                return self.phonology.mutations[stem[str(int(char) - 3)]]
            case "7" | "8" | "9":
                return self.phonology.mutations[
                    self.phonology.mutations[stem[str(int(char) - 6)]]
                ]
            case _:
                return char

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Return surface string for this template applied to a StemSpace (first stem).

        Args:
            term: StemSpace whose first stem is used.

        Returns:
            str: Result of applying the template to the stem.

        """
        result = ""
        for char in self.rule.string:
            result += self.__verify(char, Gabarit.__format_default_stem(term.stems[0]))
        return result

    def _to_decoupe__stemspace(self, term: StemSpace) -> str:
        return self._to_string__stemspace(term)

    def _to_glose__stemspace(self, term: StemSpace) -> str:
        assert isinstance(term, StemSpace)
        return f"X({term.lemma}).{''.join(self.sigma.values())}"

    def _to_glose__nonetype(self, term: None = None) -> str:
        raise NotImplementedError

    @staticmethod
    def __format_default_stem(stem: str) -> frozendict:
        """Force a stem to have structure 12V3 (consonant-vowel-consonant slots).

        Args:
            stem: e.g. CCVC string.

        Returns:
            frozendict: Mapping of "1", "2", "V", "3" to stem characters.

        """
        return frozendict(zip("12V3", stem, strict=True))

    def get_sigma(self) -> frozendict:
        """Return this template's sigma (feature dict)."""
        return self.sigma

    def _repr_params(self) -> str:
        """Return the rule string for representation."""
        return self.rule.string  # type: ignore[attr-defined]

    def get_rule(self) -> Match:
        """Return the compiled rule match object."""
        return self.rule
