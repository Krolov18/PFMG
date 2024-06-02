# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Structure qui génère des Desinence."""

from dataclasses import dataclass
from pathlib import Path

import yaml

from pfmg.lexique.block.Blocks import Blocks
from pfmg.lexique.block.Desinence import Desinence
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.sigma.Sigma import Sigma


@dataclass
class BlockEntry:
    """Structure qui génère des Desinence."""

    source: dict[str, Blocks]
    destination: dict[str, Blocks]

    def __post_init__(self):
        """Vérifie les structures d'entrées.

        Pour garder les structures le plus propre possible,
        Toute entrée vide est refusée.
        """
        assert self.source
        assert self.destination

    def __call__(self, pos: str, sigma: Sigma) -> Desinence:
        """Construit un Desinence si le couple pos/sigma le permet.

        :param pos: un POS disponible dans source et destination
        :param sigma: un Sigma valide
        :return: Instance de Desinence
        """
        return Desinence(
            source=self.source[pos](sigma.source),
            destination=self.destination[pos](sigma.destination),
        )

    @classmethod
    def from_yaml(cls, path: Path) -> "BlockEntry":
        """Construit un BlockEntry depuis un fichier yaml.

        :param path: Chemin vers le fichier yaml
        :return: un BlockEntry prêt à l'emploi
        """
        assert path.name.endswith("Blocks.yaml")

        phonology = Phonology.from_yaml(
            path.parent / "Phonology.yaml",
        )

        with open(path, encoding="utf8") as file_handler:
            data: dict = yaml.safe_load(file_handler)

        sources = {}
        destinations = {}
        for pos, blocks in data.items():
            sources[pos] = Blocks.from_list(blocks["source"], phonology)
            destinations[pos] = Blocks.from_list(
                blocks["destination"], phonology
            )
        return cls(sources, destinations)
