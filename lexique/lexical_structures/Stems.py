from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Iterable

import yaml
from frozendict import frozendict

from lexique.lexical_structures.interfaces.Reader import Reader
from lexique.lexical_structures.Lexeme import Lexeme
from lexique.lexical_structures.LexemeEntry import LexemeEntry
from lexique.lexical_structures.StemSpace import StemSpace
from lexique.lexical_structures.utils import dictify


@dataclass
class Stems(Reader, Iterable):
    data: Iterator[Lexeme]

    @classmethod
    def from_disk(cls, path: Path) -> 'Stems':
        assert path.name.endswith("Stems.yaml")
        with open(path, mode="r", encoding="utf8") as file_handler:
            data = yaml.load(file_handler, Loader=yaml.Loader)
            return cls(data=iter(Stems.__read_stems(data, data.keys())))

    @staticmethod
    def __read_stems(
        data: dict[str, dict[str, list[str]] | dict[str, dict]],
        posses: set,
        accumulator: dict | None = None
    ) -> Iterator[Lexeme]:
        for key, value in data.items():
            match value:
                case str():
                    _acc = accumulator.copy()
                    accumulator = {"pos": _acc.pop("pos")}
                    pos = (key
                           if accumulator is None
                           else accumulator["pos"])
                    t_stems, t_sigma = Stems.__parse_traduction(value)
                    yield Lexeme(
                        source=LexemeEntry(
                            stems=StemSpace(stems=tuple(key.split(","))),
                            pos=pos,
                            sigma=frozendict(_acc)
                        ),
                        destination=LexemeEntry(
                            stems=t_stems,
                            pos=pos,
                            sigma=t_sigma
                        )
                    )
                case dict():
                    if key in posses:
                        accumulator = {"pos": key}
                    else:
                        accumulator.__setitem__(*key.split("="))
                    yield from Stems.__read_stems(value, posses, accumulator)

    @staticmethod
    def __parse_traduction(token: str) -> tuple[StemSpace, frozendict]:
        str_stems, str_sigma = token.split(".") if "." in token else (token, "")
        return StemSpace(stems=tuple(str_stems.split(","))), dictify(str_sigma)

    def __iter__(self):
        return self.data
