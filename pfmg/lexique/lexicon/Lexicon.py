"""TODO : Write some doc."""
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from pfmg.external.reader import ABCReader
from pfmg.lexique.lexeme import Lexeme
from pfmg.lexique.paradigm import Paradigm
from pfmg.lexique.stems import Stems
from pfmg.parsing.validation.ABCToValidation import ABCToValidation


@dataclass
class Lexicon(ABCReader, ABCToValidation):
    """TODO : Write some doc."""

    paradigm: Paradigm
    lexemes: list[Lexeme]

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """TODO : Write some doc."""
        path = Path(path)
        return cls(
            paradigm=Paradigm.from_yaml(path),
            lexemes=list(Stems.from_yaml(path / "Stems.yaml"))
        )

    def to_validation(self) -> Self:
        """TODO : Write some doc."""
        raise NotImplementedError

    def __iter__(self):
        """TODO : Write some doc."""
        for lexeme in self.lexemes:
            yield from self.paradigm.realize(lexeme)
