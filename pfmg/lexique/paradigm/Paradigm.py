# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Réalise les léxèmes."""

from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

from pfmg.external.reader.ABCReader import ABCReader
from pfmg.lexique.block.BlockEntry import BlockEntry
from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.glose import new_gloses
from pfmg.lexique.glose.Gloses import Gloses
from pfmg.lexique.glose.Sigma import Sigma
from pfmg.lexique.lexeme.Lexeme import Lexeme
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.realizable.ABCRealizable import ABCRealizable


@dataclass
class Paradigm(ABCRealizable, ABCReader):
    """Réalise les Lexeme en Forme."""

    gloses: Gloses
    blocks: BlockEntry

    def realize(self, lexeme: Lexeme) -> Generator[Forme, None, None]:
        """Méthode qui permet de réaliser un lexème donné.

        :param lexeme: Lexème à réaliser.
        :return: Liste des réalisations du lexème.
        """
        gloses = self.gloses(lexeme.source.pos)
        lexeme_pos = lexeme.source.pos
        for i_sigma in gloses:
            if Sigma(lexeme.source.sigma, lexeme.destination.sigma) <= i_sigma:
                desinence = self.blocks(lexeme_pos, i_sigma)
                yield Forme(
                    source=FormeEntry(
                        pos=lexeme_pos,
                        sigma=i_sigma.source,
                        morphemes=Morphemes(
                            radical=lexeme.source.to_radical(),
                            others=desinence.source,
                        ),
                    ),
                    destination=FormeEntry(
                        pos=lexeme_pos,
                        sigma=i_sigma.destination,
                        morphemes=Morphemes(
                            radical=lexeme.destination.to_radical(),
                            others=desinence.destination,
                        ),
                    ),
                )

    @classmethod
    def from_yaml(cls, path: Path) -> "Paradigm":
        """Charge un paradigme à partir d'un chemin donné.

        :param path: Chemin à partir duquel charger le paradigme.
        :return: Instance de Paradigm.
        """
        assert (path / "Gloses.yaml").exists()
        return cls(
            gloses=new_gloses(path=path / "Gloses.yaml"),
            blocks=BlockEntry.from_yaml(path=path / "Blocks.yaml"),
        )
