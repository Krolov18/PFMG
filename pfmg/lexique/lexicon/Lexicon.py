from dataclasses import dataclass

from pathlib import Path

from pfmg.external import ABCFrom
from pfmg.lexique.lexeme import Lexeme
from pfmg.lexique.paradigm import Paradigm
from pfmg.lexique.stems import Stems


@dataclass
class Lexicon(ABCFrom):
    paradigm: Paradigm
    lexemes: list[Lexeme]

    @classmethod
    def from_yaml(cls, path: str | Path) -> 'Lexicon':
        return cls(
            paradigm=Paradigm.from_yaml(path),
            lexemes=list(Stems.from_yaml(path / "Stems.yaml"))
        )
