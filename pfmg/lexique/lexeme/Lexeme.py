"""Lexeme."""

from dataclasses import dataclass

from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry


@dataclass
class Lexeme:
    """Léxème à deux faces qui inclue la traduction.

    :param source: Léxème de langue source
    :param destination: Léxème de la langue de destination
    """

    source: LexemeEntry
    destination: LexemeEntry
