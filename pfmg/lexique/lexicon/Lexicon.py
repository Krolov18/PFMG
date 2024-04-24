"""TODO : Write some doc."""
from dataclasses import dataclass

from pathlib import Path

from pfmg.lexique.lexeme import Lexeme
from pfmg.lexique.paradigm import Paradigm
from pfmg.external.reader import ABCReader
from pfmg.lexique.stems import Stems
from pfmg.parsing.validation.ABCToValidation import ABCToValidation


@dataclass
class Lexicon[T](ABCReader[T], ABCToValidation[T]):
    """TODO : Write some doc."""
    paradigm: Paradigm
    lexemes: list[Lexeme]

    @classmethod
    def from_yaml(cls, path: str | Path) -> T:
        """TODO : Write some doc."""
        return cls(
            paradigm=Paradigm.from_yaml(path),
            lexemes=list(Stems.from_yaml(path / "Stems.yaml"))
        )

    def to_validation(self) -> T:
        """TODO : Write some doc."""
