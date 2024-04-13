"""Structure qui rassemble un radical et ses morphèmes."""
from dataclasses import dataclass

from lexique.lexical_structures.interfaces.Display import Display
from lexique.lexical_structures.Radical import Radical


@dataclass
class Morphemes:
    """Structure qui rassemble un radical et ses morphèmes.

    radical: StemSpace d'un léxème
    others: liste des morphèmes d'une forme
    """

    radical: Radical
    others: list[Display]
