"""Structure de données pour représenter la réalisation d'un Léxème."""
from dataclasses import dataclass

from frozendict import frozendict
from nltk.grammar import FeatStructNonterminal, Production

from pfmg.lexique.display.MixinDisplay import MixinDisplay
from pfmg.lexique.forme.FormeEntry import FormeEntry


@dataclass
class KalabaProduction:
    """Production de Kalaba.

    source: Production pour la traduction
    destination: productionpour la validation
    """
    
    source: Production
    destination: Production


@dataclass
class Forme(MixinDisplay):
    """Réalsation d'un Léxème."""

    source: FormeEntry
    destination: FormeEntry

    def __post_init__(self):
        """Vérifications post initialisation."""
        assert self.source.pos == self.destination.pos

    def to_lexical(self) -> Production:
        """Transforme une Forme en règle syntaxique lexicale.

        :return: une production lexicale.
        """
        features = {
            "Source":      {
                "Traduction": self.destination.to_string(),
                **self.source.get_sigma(),
            },
            "Destination": {
                **self.destination.get_sigma(),
            },
        }
        source_lhs = FeatStructNonterminal(self.source.pos, **features)
        destination_lhs = FeatStructNonterminal(
            self.destination.pos,
            **features["Destination"],
        )
        rhs = self.source.to_string()
        source_prod = Production(lhs=source_lhs, rhs=[rhs])
        destination_prod = Production(
            lhs=destination_lhs,
            rhs=[features["Source"]["Traduction"]],
        )
        return KalabaProduction(
            source=source_prod,
            destination=destination_prod,
        )

    def _to_string__nonetype(self, term: None = None) -> str:
        """Inner function pour représenter une forme.

        :param term:
        :return:
        """
        return f"{self.source.to_string()}, {self.destination.to_string()}"

    def get_sigma(self) -> frozendict:
        """Récupère les propriétés d'une forme."""
        raise NotImplementedError
