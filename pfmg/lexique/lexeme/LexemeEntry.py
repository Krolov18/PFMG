"""LexemeEntry."""
from dataclasses import dataclass

from frozendict import frozendict

from pfmg.lexique.morpheme.Radical import Radical
from pfmg.lexique.stem_space.StemSpace import StemSpace


@dataclass
class LexemeEntry:
    """Léxème d'une source ou d'une destination.

    :param stems: Espace thématique d'un lexème
    :param pos: Catégorie morpho-syntaxique d'un léxème
    :param sigma: Dictionnaire figé représentation 
                  les informations inhérentes d'un léxème
    """

    stems: StemSpace
    pos: str
    sigma: frozendict

    def to_radical(self) -> Radical:
        """Convertir un Lexeme en un Radical.
        
        :return: un radical
        """
        return Radical(stems=self.stems)
