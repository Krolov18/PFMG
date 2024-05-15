# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

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
    """TODO : Write some doc."""

    paradigm: Paradigm
    lexemes: list[Lexeme]

    def __post_init__(self):
        """Some documentation."""
        self.lexicon = defaultdict(list)
        self.lexicon2: list[Forme] = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                self.lexicon[forme.to_string()].append(forme.source.index)
                self.lexicon2.append(forme)

    @classmethod
    def from_yaml(cls, path: str | Path) -> Self:
        """TODO : Write some doc."""
        path = Path(path)
        return cls(
            paradigm=Paradigm.from_yaml(path),
            lexemes=list(Stems.from_yaml(path / "Stems.yaml")),
        )

    def to_validation(self) -> str:
        """TODO : Write some doc."""
        result = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                result.append(forme.to_validation())
        return "\n".join(result)

    def to_translation(self) -> str:
        """TODO : Write some doc."""
        result = []
        for lexeme in self.lexemes:
            for forme in self.paradigm.realize(lexeme):
                result.append(forme.to_translation())
        return "\n".join(result)

    def __iter__(self):
        """TODO : Write some doc."""
        for lexeme in self.lexemes:
            yield from self.paradigm.realize(lexeme)

    def __getitem__(self, item: str) -> list[int]:
        """Récupère une entrée dans le lexique."""
        return self.lexicon[item]
