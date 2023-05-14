from dataclasses import dataclass

from lexique_2.lexical_structures.StemSpace import StemSpace
from lexique_2.lexical_structures.mixins.MixinRepresentor import MixinRepresentor


@dataclass(repr=False)
class Radical(MixinRepresentor):
    """
    """
    stems: StemSpace

    def _repr_params(self) -> str:
        return "::".join(self.stems.stems)
