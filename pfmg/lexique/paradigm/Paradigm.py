# Copyright (c) <year>, <copyright holder>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Réalise les léxèmes."""

from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

from pfmg.lexique.block.Blocks import Blocks
from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.glose.Gloses import Gloses
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.reader.ABCReader import ABCReader
from pfmg.lexique.realizable.ABCRealizable import ABCRealizable


@dataclass
class Paradigm(ABCRealizable, ABCReader):
    """Réalise les Lexeme en Forme."""

    gloses: Gloses
    blocks: Blocks

    def realize(self, lexeme: Lexeme) -> Generator[Forme, None, None]:
        """Méthode qui permet de réaliser un lexème donné.

        :param lexeme: Lexème à réaliser.
        :return: Liste des réalisations du lexème.
        """
        gloses = self.gloses(lexeme.source.pos)
        source_sigma_items = lexeme.source.sigma.items()
        destination_sigma_items = lexeme.destination.sigma.items()
        lexeme_pos = lexeme.source.pos
        for i_sigma in gloses:
            i_sigma_source = i_sigma["source"]
            i_sigma_destination = i_sigma["destination"]
            source_validation = source_sigma_items <= i_sigma_source.items()
            destination_validation = (
                destination_sigma_items <= i_sigma_destination.items()
            )
            if source_validation and destination_validation:
                yield Forme(
                    source=FormeEntry(
                        pos=lexeme_pos,
                        sigma=i_sigma_source,
                        morphemes=Morphemes(
                            radical=lexeme.source.to_radical(),
                            others=self.blocks.source(
                                pos=lexeme_pos,
                                sigma=i_sigma_source,
                            ),
                        ),
                    ),
                    destination=FormeEntry(
                        pos=lexeme_pos,
                        sigma=i_sigma_destination,
                        morphemes=Morphemes(
                            radical=lexeme.destination.to_radical(),
                            others=self.blocks.destination(
                                pos=lexeme_pos,
                                sigma=i_sigma_destination,
                            ),
                        ),
                    ),
                )

    @classmethod
    def from_disk(cls, path: Path) -> "Paradigm":
        """Méthode permettant de charger un paradigme à partir d'un chemin donné.

        :param path: Chemin à partir duquel charger le paradigme.
        :return: Instance de Paradigm.
        """
        assert (path / "Gloses.yaml").exists()
        return cls(
            gloses=Gloses.from_disk(
                path=path / "Gloses.yaml",
            ),
            blocks=Blocks.from_disk(
                path=path / "Blocks.yaml",
            ),
        )
