"""Lexicon: paradigm plus lexemes, with translation/validation grammar strings."""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from pfmg.external.reader import ABCReader
from pfmg.lexique.forme import Forme
from pfmg.lexique.lexeme import Lexeme
from pfmg.lexique.paradigm import Paradigm
from pfmg.lexique.stems import Stems


@dataclass
class Lexicon(ABCReader):
    """Lexicon built from a paradigm and a list of lexemes; indexes forms by string.

    Attributes:
        paradigm: Paradigm used to realize lexemes into Forme.
        lexemes: List of Lexeme instances.

    """

    paradigm: Paradigm
    lexemes: list[Lexeme]

    def __post_init__(self) -> None:
        """Build lexicon index (string -> list of indices) and flat list of Forme."""
        self.lexicon = defaultdict(list)
        self.lexicon2: list[Forme] = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                self.lexicon[forme.to_string()].append(forme.source.index)
                self.lexicon2.append(forme)

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """Load Lexicon from a directory (Paradigm + Stems.yaml).

        Args:
            path: Path to the directory containing paradigm data and Stems.yaml.

        Returns:
            Lexicon: New Lexicon instance.

        """
        path = Path(path)
        return cls(
            paradigm=Paradigm.from_yaml(path),
            lexemes=list(Stems.from_yaml(path / "Stems.yaml")),
        )

    def to_validation(self) -> str:
        """Return all realized forms as NLTK lexical productions (validation grammar)."""
        result = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                result.append(forme.to_validation())
        return "\n".join(result)

    def to_translation(self) -> str:
        """Return all realized forms as NLTK lexical productions (translation grammar).

        Returns:
            str: Newline-joined NLTK lexical production strings.

        """
        result = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                result.append(forme.to_translation())
        return "\n".join(result)

    def __iter__(self):
        """Iterate over all realized Forme (one per lexeme per paradigm slot).

        Yields:
            Forme: Each realized form.

        """
        for lexeme in self.lexemes:
            yield from self.paradigm.realize(lexeme)

    def __getitem__(self, item: str) -> list[int]:
        """Return the list of form indices for the given string key.

        Args:
            item: String key (e.g. word form string).

        Returns:
            list[int]: List of form indices for that key.

        """
        return self.lexicon[item]
