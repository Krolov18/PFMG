"""Radical: stem space and sigma for the root of a form."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.gloser.MixinGloser import MixinGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass(repr=False)
class Radical(MixinRepresentor, MixinGloser):
    """The radical (root) of a Forme: StemSpace and sigma."""

    stems: StemSpace
    sigma: frozendict

    def __post_init__(self) -> None:
        """Set lemma from the first stem in the stem space."""
        self.lemma = self.stems.lemma

    def _repr_params(self) -> str:
        """Return stems and sigma string for repr."""
        stems = "::".join(self.stems.stems)
        sigma = ",".join([f"{k}={v}" for k, v in self.sigma.items()])
        return f"{stems},{sigma}"

    def _to_glose__nonetype(self, term: None = None) -> str:
        assert term is None
        return f"{self.lemma}.{'.'.join(self.sigma.values())}".rstrip(".")
