"""TODO : Write some doc."""
from dataclasses import (
    dataclass
)

from pathlib import Path

from pfmg.external.reader import ABCReader
from pfmg.parsing.parser import Parser


@dataclass
class KParser[T](ABCReader[T]):
    """Parser bipartite.

    Le KParser va parser une première pour traduire
    puis une seconde fois pour valider la traduction.
    """
    translator: Parser
    validator: Parser

    @classmethod
    def from_yaml(cls, path: str | Path) -> T:
        """TODO : Write some doc."""
        from pfmg.lexique.lexicon import Lexicon
        from pfmg.parsing.grammar import KGrammar

        lexicon = Lexicon.from_yaml(path)
        grammar = KGrammar.from_yaml(path)
        return cls(
            translator=Parser(
                lexique=lexicon,
                grammar=grammar.translator
            ),
            validator=Parser(
                lexique=lexicon.to_translation(),
                grammar=grammar.validator
            )
        )
