# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass

from pfmg.parsing.features.Features import Features
from pfmg.parsing.percolation.Percolation import Percolation


@dataclass
class Production:
    """TODO : Write some doc."""

    lhs: str
    syntagmes: list[str]
    accords: Features
    percolation: Percolation

    def __post_init__(self):
        """TODO : Write some doc."""
        assert isinstance(self.lhs, str)
        assert isinstance(self.syntagmes, list)
        assert all(isinstance(x, str) for x in self.syntagmes)
        assert isinstance(self.accords, Features)
        assert isinstance(self.percolation, Percolation)

    def to_nltk(self) -> str:
        """TODO : Write some doc."""
        template = "{lhs}[{features}] -> {rhs}"
        features = self.percolation.to_nltk()
        rhs = [
            f"{nt}[{feats}]" if nt.isupper() else nt
            for nt, feats in zip(
                self.syntagmes, self.accords.to_nltk(), strict=True
            )
        ]
        return template.format(
            lhs=self.lhs, features=features, rhs=" ".join(rhs)
        )

    def add_translation(self, indices: list[int]):
        """TODO : Write some doc."""
        assert min(indices) >= 0
        assert max(indices) < len(self.syntagmes)

        self.accords.add_translation(self.syntagmes)
        trads = self.accords.get_translations()
        self.percolation.add_translation([trads[x] for x in indices])

    @classmethod
    def from_yaml(cls, data: dict):
        """TODO : Write some doc.

        TODO : Faire en sorte que les clés du fichier MorphoSyntax
         soit les noms des paramètres de la classe Production.

        :param data:
        :return:
        """
        assert len(data.keys()) == 1
        target = next(iter(data.keys()))
        assert target in ("Source", "Destination")
        data = data[target]

        production = cls(
            lhs=data["lhs"],
            syntagmes=data["Syntagmes"],
            accords=Features.from_string(
                Features.broadcast(data["Accords"], len(data["Syntagmes"])),
                target=target[0],
            ),
            percolation=Percolation.from_string(
                Features.broadcast(data["Percolation"], len(data["Syntagmes"])),
                target=target[0],
            ),
        )
        if "Traduction" in data:
            production.add_translation(data["Traduction"])
        return production
