from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Iterable

import yaml
from frozendict import frozendict

from lexique_2.lexical_structures.interfaces.Reader import Reader
from lexique_2.lexical_structures.Gloses import Gloses
from lexique_2.lexical_structures.Lexeme import Lexeme
from lexique_2.lexical_structures.StemSpace import StemSpace
from lexique_2.lexical_structures.interfaces.Searchable import Searchable


@dataclass
class Stems(Reader, Iterable):
    data: Iterator[Lexeme]
    searcher: Searchable

    @classmethod
    def from_disk(cls, path: Path) -> 'Stems':
        assert path.name.endswith("Stems.yaml")
        with open(path, mode="r", encoding="utf8") as file_handler:
            gloses_from_disk = Gloses.from_disk(path.parent / "Gloses.yaml")
            return cls(data=iter(Stems.__read_stems(yaml.load(file_handler, Loader=yaml.Loader),
                                                    gloses_from_disk)),
                       searcher=gloses_from_disk)

    @staticmethod
    def __read_stems(data: dict[str, dict[str, list[str]] | dict[str, dict]],
                     searcher: Searchable,
                     accumulator: dict | None = None) -> Iterator[Lexeme]:
        for key, value in data.items():
            match value:
                case str():
                    _acc = accumulator.copy()
                    accumulator = {"pos": _acc.pop("pos")}
                    yield Lexeme(stem=StemSpace(stems=tuple(key.split(","))),
                                 pos=key if accumulator is None else accumulator["pos"],
                                 sigma=frozendict(_acc))
                case dict():
                    if searcher.is_pos(key):
                        accumulator = {"pos": key}
                    else:
                        accumulator[searcher.search(accumulator["pos"], key)] = key
                    yield from Stems.__read_stems(value, searcher, accumulator)

    def __iter__(self):
        return self.data
