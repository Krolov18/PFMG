"""Lexeme: source and destination entries (bilingual lexical unit)."""

from dataclasses import dataclass

from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry


@dataclass
class Lexeme:
    """Two-sided lexeme: source and destination LexemeEntry (includes translation)."""

    source: LexemeEntry
    destination: LexemeEntry
