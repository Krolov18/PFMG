"""Radical."""
from dataclasses import dataclass

from pfmg.lexique.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass(repr=False)
class Radical(MixinRepresentor):
    """Represente le radical d'une Forme."""

    stems: StemSpace

    def _repr_params(self) -> str:
        """Représente les params d'un radical.

        :return: les params d'un radical
        """
        return "::".join(self.stems.stems)
