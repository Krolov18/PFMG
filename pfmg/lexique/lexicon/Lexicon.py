"""Lexicon: paradigm plus lexemes with realized-form index maps."""

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
        """Realize every lexeme once and index the resulting Forme by string.

        Realization happens exactly once: ``Paradigm.realize`` draws a fresh
        index for each Forme it yields, so realizing twice would produce two
        incompatible index spaces — one for the string -> index maps, another
        for the grammars exported by the parsing layer.
        """
        self.lexicon: defaultdict[str, list[int]] = defaultdict(list)
        self.lexicon_destination: defaultdict[str, list[int]] = defaultdict(list)
        self.lexicon2: list[Forme] = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                self.lexicon[forme.source.to_string()].append(forme.source.index)
                self.lexicon_destination[forme.destination.to_string()].append(
                    forme.destination.index
                )
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

    def __iter__(self):
        """Iterate over all realized Forme (one per lexeme per paradigm slot).

        Yields:
            Forme: Each realized form.

        """
        yield from self.lexicon2

    def __getitem__(self, item: str) -> list[int]:
        """Return the list of source form indices for the given string key.

        Args:
            item: String key (e.g. word form string).

        Returns:
            list[int]: List of form indices for that key.

        """
        return self.get_indexes(item)

    def get_indexes(self, item: str, how: str = "translation") -> list[int]:
        """Return the form indexes of *item* on the side used by *how*.

        The translation grammar has source indexes as terminals while the
        validation grammar has destination ones, so a token must be looked up
        on the matching side.

        Args:
            item: Word form to look up.
            how: "translation" (source side) or "validation" (destination side).

        Returns:
            list[int]: Indexes of that form, empty when unknown.

        """
        match how:
            case "translation":
                return self.lexicon[item]
            case "validation":
                return self.lexicon_destination[item]
            case _:
                message = f"'{how}' n'est ni 'translation' ni 'validation'."
                raise ValueError(message)
