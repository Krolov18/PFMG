from dataclasses import dataclass

from frozendict import frozendict

from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.interfaces.Rulable import Rulable
from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay


@dataclass
class FormeEntry(MixinDisplay, Rulable):
    """
    La forme est la réalisation d'un lexème.
    :param traduction : Réalisation du lexème de la traduction
    """
    pos: str
    morphemes: Morphemes
    sigma: frozendict[str, str]

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
        sigma = {key: value
                 for key, value in self.get_sigma().items()
                 if key.istitle()}
        features = ','.join(f"{key}='{value}'"
                            for key, value in sigma.items())
        return f"{self.pos}[{features}] -> '{self.to_string()}'"
