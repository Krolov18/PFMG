"""Data structure for the realization of a lexeme (source + destination form)."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.utils.stem_space import StemSpace


@dataclass
class Forme(MixinDisplay, ABCGloser):
    """Realization of a lexeme: source and destination FormeEntry with same POS."""

    source: FormeEntry
    destination: FormeEntry

    def __post_init__(self) -> None:
        """Ensure source and destination share the same part-of-speech."""
        assert self.source.pos == self.destination.pos

    def _to_string__nonetype(self, term: None = None) -> str:
        """Return string representation of the form (source) when term is None."""
        return self.source.to_string()

    def get_sigma(self) -> frozendict:
        """Return the form's sigma (feature dict). To be implemented by subclasses."""
        raise NotImplementedError

    def to_glose(self, term: StemSpace | str | None = None) -> str:
        """Return the glose of the source form."""
        return self.source.to_glose()

    def to_decoupe(self, term: StemSpace | str | None = None) -> str:
        """Return the segmentation (decoupe) of the source form."""
        return self.source.to_decoupe()
