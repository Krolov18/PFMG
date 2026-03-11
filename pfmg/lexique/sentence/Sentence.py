"""Sentence: sequence of Forme (word forms) with display and glose."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.display import ABCDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class Sentence(ABCDisplay, ABCGloser):
    """A sentence in the system: a list of word forms (Forme).

    Attributes:
        words: List of Forme (word forms).

    """

    words: list[Forme]

    def to_string(self, term: StemSpace | str | None = None) -> str:
        """Return space-joined string representation of all words.

        Args:
            term: Optional stem (unused for Sentence; delegates to words).

        Returns:
            str: Space-joined string of all word forms.

        """
        return " ".join(x.to_string() for x in self.words)

    def get_sigma(self) -> frozendict:
        """Return merged sigma (feature dict) from all words.

        Returns:
            frozendict: Merged feature dict from all words.

        """
        sigma = {}
        for w in self.words:
            sigma.update(w.get_sigma())
        return frozendict(sigma)

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """Return space-joined segmentation (decoupe) of all words.

        Args:
            term: Optional stem (delegates to words).

        Returns:
            str: Space-joined segmentation string.

        """
        return " ".join(x.to_decoupe() for x in self.words)

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """Return space-joined glose of all words.

        Args:
            term: Optional stem (delegates to words).

        Returns:
            str: Space-joined glose string.

        """
        return " ".join(x.to_glose() for x in self.words)
