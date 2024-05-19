# Copyright (c) 2024, Korantin Lévêque <korantin.leveque@protonmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
"""TODO : Write some doc."""

from dataclasses import dataclass
from typing import Literal

from pfmg.parsing.features.Features import Features
from pfmg.parsing.features.Percolation import Percolation


@dataclass
class Production:
    """TODO : Write some doc."""

    lhs: str
    phrases: list[str]
    agreements: Features
    percolation: Percolation

    def __post_init__(self):
        """TODO : Write some doc."""
        assert isinstance(self.lhs, str)
        assert isinstance(self.phrases, list)
        assert all(isinstance(x, str) for x in self.phrases)
        assert isinstance(self.agreements, Features)
        assert isinstance(self.percolation, Percolation)

    def to_nltk(self) -> str:
        """TODO : Write some doc."""
        template = "{lhs}[{features}] -> {rhs}"
        features = self.percolation.to_nltk()
        rhs = [
            f"{nt}[{feats}]" if nt.isupper() else nt
            for nt, feats in zip(
                self.phrases, self.agreements.to_nltk(), strict=True
            )
        ]
        return template.format(
            lhs=self.lhs, features=features, rhs=" ".join(rhs)
        )

    def add_translation(self, indices: list[int]) -> None:
        """TODO : Write some doc."""
        assert min(indices) >= 0
        assert max(indices) < len(self.phrases)

        self.agreements.add_translation(self.phrases)
        trads = self.agreements.get_translations()
        self.percolation.add_translation([trads[x] for x in indices])

    def update(self, production: "Production", indices: list[int]) -> None:
        """Ajoute les infos morphosyntaxique destination à source.

        :param production: une production de destination
        :param indices:
        """
        # Ajoute les accords de destination
        for i_idx, value in enumerate(indices):
            self.agreements[value].update(production.agreements[i_idx])
        # Ajoute la percolation de destination
        self.percolation.update(production.percolation)

        # Ajoute la traduction
        self.add_translation(indices)

    @classmethod
    def from_yaml(cls, data: dict, target: Literal["S", "D"]):
        """TODO : Write some doc.

        TODO : Faire en sorte que les clés du fichier MorphoSyntax
         soit les noms des paramètres de la classe Production.

        :param data:
        :param target:
        :return:
        """
        return cls(
            lhs=data["lhs"],
            phrases=data["phrases"],
            agreements=Features.from_string(
                data=data["agreements"],
                target=target,
                phrase_len=len(data["phrases"]),
            ),
            percolation=Percolation.from_string(
                data=data["percolations"],
                target=target,
                phrase_len=len(data["phrases"]),
            ),
        )
