"""Lexeme."""
from dataclasses import dataclass

from lexique.lexical_structures.LexemeEntry import LexemeEntry


@dataclass
class Lexeme:
    """Léxème à deux faces qui inclue la traduction.
    
    :param source: Léxème de langue source
    :param traduction: Léxème de la langue de destination
    """

    source: LexemeEntry
    destination: LexemeEntry
