"""Lexicon: paradigm plus lexemes, realized once into surface forms."""

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
    """Lexicon built from a paradigm and a list of lexemes.

    Attributes:
        paradigm: Paradigm used to realize lexemes into Forme.
        lexemes: List of Lexeme instances.

    """

    paradigm: Paradigm
    lexemes: list[Lexeme]

    def __post_init__(self) -> None:
        """Realize every lexeme once and collect the surface forms of both sides.

        The realized forms are kept, not recomputed on demand: they are the
        terminals of the grammars exported by the parsing layer, and the two
        string sets are what tells a known word from an unknown one.
        """
        self.source_forms: set[str] = set()
        self.destination_forms: set[str] = set()
        self.formes: list[Forme] = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                self.source_forms.add(forme.source.to_string())
                self.destination_forms.add(forme.destination.to_string())
                self.formes.append(forme)

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

    def __iter__(self):
        """Iterate over all realized Forme (one per lexeme per paradigm slot).

        Yields:
            Forme: Each realized form.

        """
        yield from self.formes

    def knows(self, item: str, how: str = "translation") -> bool:
        """Return True when *item* is a realized form on the side used by *how*.

        The translation grammar has source forms as terminals while the
        validation grammar has destination ones, so a token must be looked up
        on the matching side.

        Args:
            item: Word form to look up.
            how: "translation" (source side) or "validation" (destination side).

        Returns:
            bool: True when that side realizes *item*.

        """
        match how:
            case "translation":
                return item in self.source_forms
            case "validation":
                return item in self.destination_forms
            case _:
                message = f"'{how}' n'est ni 'translation' ni 'validation'."
                raise ValueError(message)
