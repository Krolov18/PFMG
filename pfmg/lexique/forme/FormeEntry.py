"""Single entry of a Forme: POS, morphemes, sigma, and index."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.decoupeur.ABCDecoupeur import ABCDecoupeur
from pfmg.external.display.MixinDisplay import MixinDisplay
from pfmg.external.gloser.ABCGloser import ABCGloser
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.stem_space.StemSpace import StemSpace


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

    def to_nltk(self, infos: dict | None = None) -> str:
        """Return this FormeEntry as an NLTK lexical production string."""
        name = f"_{self.__class__.__name__}__to_nltk_{type(infos).__name__.lower()}"
        return getattr(self, name)(infos)

    def __to_nltk_nonetype(self, infos: None = None) -> str:
        assert infos is None

        sigma = {key: value for key, value in self.get_sigma().items() if key.istitle()}
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{self.pos}[{features}] -> '{self.index}'"

    def __to_nltk_dict(self, infos: dict) -> str:
        assert isinstance(infos, dict)
        sigma = {
            f"S{key}": value for key, value in self.get_sigma().items() if key.istitle()
        }
        sigma.update(infos)
        features = ",".join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{self.pos}[{features}] -> '{self.index}'"
