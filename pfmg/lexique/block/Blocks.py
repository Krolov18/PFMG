# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""Blocks."""

from dataclasses import dataclass

from frozendict import frozendict

from pfmg.lexique.morpheme.Factory import create_morpheme
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.parsing.features.utils import FeatureReader


@dataclass
class Blocks:
    """Blocks."""

    data: list[list["Morpheme"]]  # noqa # type: ignore

    def __post_init__(self):
        """Vérifie les structures d'entrées.

        Pour garder les structures le plus propre possible,
        Tout entrée vide est refusée.
        """
        assert self.data
        assert all(x for x in self.data)

    def __call__(self, sigma: frozendict) -> list["Morpheme"]:  # noqa # type: ignore
        """Récupère la liste de morphèmes valides pour le sigma donné.

        :param sigma: le sigma d'une forme
        :return: une liste de morphème valide pour ce sigma
        """
        assert sigma

        output: list["Morpheme"] = []  # noqa # type: ignore
        for morphemes in self.data:
            winner: "Morpheme | None" = None  # noqa # type: ignore
            for morpheme in morphemes:
                if morpheme.get_sigma().items() <= sigma.items():
                    winner = morpheme
            if winner is not None:
                output.append(winner)
        return output

    @classmethod
    def from_list(cls, data: list[dict], phonology: "Phonology") -> "Blocks":  # type: ignore
        """Construit un Blocks à partir dd'une liste de blocs.

        :param data: listes de bloc pour un pos donné
        :param phonology: Instance de Phonology
        :return: un Blocks prêt à l'emploi
        """
        output: list[list["Morpheme"]] = []  # noqa # type: ignore

        fr = FeatureReader()
        for block in data:
            _tmp = []
            for key, value in block.items():
                _sigma = frozendict(fr.parse(key)[0])
                _tmp.append(
                    create_morpheme(
                        rule=value,
                        sigma=_sigma,
                        phonology=phonology,
                    ),
                )
            output.append(_tmp)

        assert output
        return cls(output)
