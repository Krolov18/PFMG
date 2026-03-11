"""Structure holding a radical (stem) and its morphemes."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.decoupeur.ABCDecoupeur import ABCDecoupeur
from pfmg.external.display import ABCDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class Morphemes(ABCDisplay, ABCGloser, ABCDecoupeur):
    """A radical plus a list of morphemes for one word form."""

    radical: Radical
    others: list[ABCDisplay]

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Build surface string by applying each morpheme to the radical (or previous result)."""
        assert term is None
        result: str = ""
        for morpheme in self.others:
            result = morpheme.to_string(
                result or self.radical.stems,
            )
        return result or self.radical.lemma

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """Build segmentation string by chaining each morpheme's decoupe."""
        assert term is None
        result: str = ""

        for morpheme in self.others:
            result += morpheme.to_decoupe(  # type: ignore
                result or self.radical.stems,
            )

        return result or self.radical.lemma

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """Build glose string from radical then each morpheme."""
        result = self.radical.to_glose()
        for morpheme in self.others:
            result = morpheme.to_glose(result)  # type: ignore

        return result or self.radical.lemma

    def get_sigma(self) -> frozendict:
        """Return merged sigma from radical and morphemes. To be implemented by subclasses."""
        raise NotImplementedError
