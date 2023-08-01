from dataclasses import dataclass

from frozendict import frozendict

from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace


@dataclass
class Lexeme:
    """
    Représentation abstraite d'une Forme.
    :param traduction : Lexeme
    """
    stem: StemSpace
    pos: str
    sigma: frozendict

    def to_radical(self) -> Radical:
        return Radical(stems=self.stem)
