from dataclasses import dataclass

from lexique.lexical_structures.LexemeEntry import LexemeEntry


@dataclass
class Lexeme:
    source: LexemeEntry
    destination: LexemeEntry
