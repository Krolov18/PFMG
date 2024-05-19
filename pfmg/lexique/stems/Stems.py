# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Itérateur de Lexèmes."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.external.reader.ABCReader import ABCReader
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.lexeme.LexemeEntry import LexemeEntry
from pfmg.lexique.stem_space.StemSpace import StemSpace
from pfmg.lexique.utils import dictify
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Stems(ABCReader, Iterable):
    """Itérateur de Lexèmes."""

    data: Iterator[Lexeme]

    @classmethod
    def from_yaml(cls, path: Path) -> "Stems":
        """Construit l'Itérateur à partir d'un fichier YAML.

        :param path: Chemin vers le fichier YAML.
        :return: Objet Stems
        """
        assert path.name.endswith("Stems.yaml")
        with open(path, encoding="utf8") as file_handler:
            data = yaml.safe_load(file_handler)
            return cls(data=iter(Stems.__read_stems(data)))

    @staticmethod
    def __read_stems(data: dict[str, str | dict], accumulator: str = ""):
        for key, value in data.items():
            match value:
                case str():
                    pos_inherence = accumulator.split(";", maxsplit=1)
                    pos, inherence = pos_inherence[0], ""
                    d_sigma = [{}]

                    if len(pos_inherence) == 2:
                        pos, inherence = pos_inherence
                        d_sigma = FeatureReader().parse(
                            inherence.replace(";", ",")
                        )

                    stems, s_sigma = Stems.__parse_translation(value)
                    yield Lexeme(
                        source=LexemeEntry(
                            stems=stems,
                            pos=pos,
                            sigma=s_sigma,
                        ),
                        destination=LexemeEntry(
                            stems=StemSpace.from_string(key),
                            pos=pos,
                            sigma=frozendict(d_sigma[0]),
                        ),
                    )
                case dict():
                    yield from Stems.__read_stems(
                        value, f"{accumulator};{key}" if accumulator else key
                    )

    @staticmethod
    def __parse_translation(token: str) -> tuple[StemSpace, frozendict]:
        """Méthode privée qui parse la traduction.

        :param token: string + POS + inhérence
        :return: un StemSpace et ses traits inhérents (sigma)
        """
        str_stems, str_sigma = token.split(".") if "." in token else (token, "")
        return StemSpace(stems=tuple(str_stems.split(","))), dictify(str_sigma)

    def __iter__(self):
        """Récupère l'itérateur de Lexèmes."""
        return self.data
