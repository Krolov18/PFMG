"""TODO : Write some doc."""
from dataclasses import dataclass

from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.grammar import Grammar
from pfmg.parsing.parsable import ABCParsable


@dataclass
class Parser(ABCParsable):
    """TODO : Write some doc."""

    lexique: Lexicon
    grammar: Grammar
