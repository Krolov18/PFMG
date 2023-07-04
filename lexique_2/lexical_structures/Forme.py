from dataclasses import dataclass

from frozendict import frozendict

from lexique.types_for_kalaba import type_pos, type_sigma
from lexique_2.lexical_structures.interfaces.Rulable import Rulable
from lexique_2.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique_2.lexical_structures.Morphemes import Morphemes
from lexique_2.lexical_structures.StemSpace import StemSpace


@dataclass
class Forme(MixinDisplay, Rulable):
    """
    La forme est la réalisation d'un lexème.
    :param traduction : Réalisation du lexème de la traduction
    """
    pos: type_pos
    morphemes: Morphemes
    sigma: type_sigma

    def _to_string__nonetype(self, term: None = None) -> str:
        result: str = ""
        for morpheme in self.morphemes.others:
            m_sigma = dict(self.sigma)
            m_sigma.update(morpheme.get_sigma())
            self.sigma = frozendict(m_sigma)
            result = morpheme.to_string(result or self.morphemes.radical.stems)
        return result or self.morphemes.radical.stems.stems[0]

    def get_sigma(self) -> frozendict:
        return self.sigma

    def to_unary(self) -> str:
        sigma = {key: value for key, value in self.get_sigma().items() if key.istitle()}
        features = ','.join(f"{key}='{value}'" for key, value in sigma.items())
        return f"{self.pos}[{features}] -> '{self.to_string()}'"