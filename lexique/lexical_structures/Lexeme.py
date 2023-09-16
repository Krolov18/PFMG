from dataclasses import dataclass

from frozendict import frozendict

from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace


@dataclass
class LexemeEntry:
    """
    Class representing a Lexeme.

    Attributes:

    - :class:`StemSpace` stem --> Espace thématique d'un lexème
    - :class:`str` pos --> Catégorie morpho-syntaxique d'un léxème
    - :class:`frozendict` sigma --> Dictionnaire figé représentation les informations inhérentes d'un léxème
    - :class:`Lexeme` traduction --> Traduction de ce léxème qui est un léxème lui-même.
    """
    stem: StemSpace
    pos: str
    sigma: frozendict
    traduction: 'Lexeme'

    def to_radical(self) -> Radical:
        return Radical(stems=self.stem)


@dataclass
class Lexeme:
    source: LexemeEntry
    destination: LexemeEntry
