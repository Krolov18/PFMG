"""Single side of a Lexeme: stems, POS, and sigma (inherent features)."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class LexemeEntry:
    """One side of a lexeme: stem space, part-of-speech, and inherent sigma."""

    stems: StemSpace
    pos: str
    sigma: frozendict  # inherent features

    def __post_init__(self) -> None:
        """Ensure pos is non-empty."""
        assert self.pos

    def to_radical(self) -> Radical:
        """Return a Radical built from this entry's stems and sigma."""
        return Radical(stems=self.stems, sigma=self.sigma)
