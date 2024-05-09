# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Gloses avec contraintes."""

from dataclasses import dataclass
from pathlib import Path

import yaml
from frozendict import frozendict

from pfmg.external.reader.ABCReader import ABCReader
from pfmg.lexique.glose.Gloses import Gloses
from pfmg.lexique.glose.Sigma import Sigma
from pfmg.lexique.glose.Sigmas import Sigmas
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class CGloses(ABCReader):
    """Gloses avec contraintes.

    Args:
    ----
        gloses: Les gloses standards d'un paradigme
        alignments: Contraintes appliquées sur le paradigme
                    entre source et destination

    Examples:
    --------
        Les contraintes permettent de valider l'exemple suivant.
        si le Nombre de source est 'sg' alors le Nombre de destination est 'sg'.
        De ce fait,
        si le Nombre de source est 'sg' et que le Nombre de destination est 'pl'
        alors cette configuration de Sigma ne sera pas retenue.

    """

    gloses: Gloses
    alignments: Gloses

    def __call__(self, pos: str) -> list:
        """Apply the normal Gloses and filter it with alignments.

        :param pos: Some POS value
        :return: the filtered list of sigmas
        """
        result = []
        for x in self.gloses(pos):
            if x in self.alignments(pos):
                result.append(x)
        return result

    @classmethod
    def from_yaml(cls, path: Path) -> "CGloses":
        """Construit un CGloses depuis un fichier YAML.

        :param path: Chemin vers le fichier YAML
        :return: Une CGloses valide prête à l'emploi
        """
        with open(path, encoding="utf8") as fh:
            data = yaml.safe_load(fh)
        gloses = Gloses.from_dict(data)
        alignments = Gloses(cls.__read_alignments(data))
        return cls(gloses=gloses, alignments=alignments)

    @staticmethod
    def __read_alignments(data: dict) -> dict:
        fr = FeatureReader()
        return {
            pos: Sigmas(
                [
                    Sigma(
                        source=frozendict(fr.parse(key)[0]),
                        destination=frozendict(fr.parse(value)[0]),
                    )
                    for key, values in sigmas["alignments"].items()
                    for value in values
                ]
            )
            for pos, sigmas in data.items()
        }
