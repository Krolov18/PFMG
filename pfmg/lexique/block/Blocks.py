# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Blocks."""

from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.lexique.block.BlockEntry import BlockEntry
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.external.reader.ABCReader import ABCReader


@dataclass
class Blocks(ABCReader):
    """Réprésente les blocs d'application de règles."""

    source: BlockEntry
    destination: BlockEntry

    def __post_init__(self):
        """Vérification après initialisation."""
        assert self.source
        assert self.destination

    @classmethod
    def from_yaml(cls, path: Path) -> "Blocks":
        """Construit un Blocks depuis un fichier JSON.

        :param path: Chemin vers le fichier JSON
        :return: une instance de Blocks
        """
        assert path.name.endswith("Blocks.yaml")

        with open(path, encoding="utf8") as file_handler:
            data: dict = yaml.load(file_handler, Loader=yaml.Loader)

        assert data

        phonology_from_disk = Phonology.from_yaml(
            path.parent / "Phonology.yaml",
        )

        source = BlockEntry.from_dict(
            data=data["source"],
            phonology=phonology_from_disk,
        )

        destination = BlockEntry.from_dict(
            data=data["destination"],
            phonology=phonology_from_disk,
        )

        return cls(source=source, destination=destination)

    def __call__(
        self,
        pos: str,
        sigma: frozendict,
    ) -> dict:
        """Construit un dictionnaire avec en clé les POS et les blocs en valeurs.

        :param pos:
        :param sigma:
        :return:
        """
        return {
            key: getattr(self, key)(pos, sigma[key])
            for key, value in sigma.items()
        }
