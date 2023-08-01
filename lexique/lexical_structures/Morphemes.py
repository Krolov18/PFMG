from dataclasses import dataclass

from lexique.lexical_structures.interfaces.Display import Display
from lexique.lexical_structures.Radical import Radical


@dataclass
class Morphemes:
    """
    Attributes:
        radical: contenant du stemspace d'un lexeme
        others: liste de morphèmes d'une forme
    """
    radical: Radical
    others: list[Display]
