"""Single entry of a Forme: POS, morphemes, sigma, and index."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.decoupeur.ABCDecoupeur import ABCDecoupeur
from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.utils.stem_space import StemSpace


@dataclass
class FormeEntry(MixinDisplay, ABCGloser, ABCDecoupeur):
    """One side of a Forme: POS, morphemes, sigma (features), and lexical index."""

    pos: str
    morphemes: Morphemes
    sigma: frozendict[str, str]
    index: int

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Return string representation via morphemes."""
        return self.morphemes.to_string(term)

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """Return segmentation via morphemes."""
        return self.morphemes.to_decoupe(term)

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """Return glose via morphemes."""
        return self.morphemes.to_glose(term)

    def get_sigma(self) -> frozendict:
        """Return this entry's sigma (feature mapping)."""
        return self.sigma
