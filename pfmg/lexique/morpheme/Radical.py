"""Radical."""
from dataclasses import dataclass

from frozendict import frozendict

from pfmg.external.gloser.MixinGloser import MixinGloser
from pfmg.external.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass(repr=False)
class Radical(MixinRepresentor, MixinGloser):
    """Represente le radical d'une Forme."""

    stems: StemSpace
    sigma: frozendict

    def __post_init__(self):
        """Initialise lemma à partir du premier stem dans stems."""
        self.lemma = self.stems.lemma

    def _repr_params(self) -> str:
        """Représente les params d'un radical.

        :return: les params d'un radical
        """
        stems = "::".join(self.stems.stems)
        sigma = ",".join([f"{k}={v}" for k, v in self.sigma.items()])
        return f"{stems},{sigma}"

    def _to_glose__nonetype(self, term: None = None) -> str:
        assert term is None
        return f"{self.lemma}.{".".join(self.sigma.values())}".rstrip(".")
